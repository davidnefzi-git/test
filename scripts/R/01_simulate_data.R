## =============================================================================
## Title:   01_simulate_data.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: Generate synthetic panel data that replicates the distributional
##          properties of bilateral FX swap regulatory microdata. This script
##          is the single point of entry for swapping in real data: replace
##          the simulation block with a real read and the downstream scripts
##          run unchanged.
## Inputs:  None (simulation only)
## Outputs: Output/fx_swap/panel_main.rds   — main panel (cell level)
##          Output/fx_swap/panel_bank.rds   — bank × cell level (for balance tests)
##          Output/fx_swap/mmf_instrument.rds — MMF outflow instrument series
## =============================================================================

library(here)
library(dplyr)
library(tidyr)
library(lubridate)

# set.seed() is called once in 00_master.R; removed here per INV-14.
# Standalone use: call set.seed(42) before sourcing this script.

# ---------------------------------------------------------------------------
# 0. Dimension definitions
# ---------------------------------------------------------------------------

currency_pairs <- c("EURUSD", "JPYUSD", "GBPUSD", "CADUSD", "CHFUSD")
tenors         <- c("ON", "1W", "1M", "3M")
sectors        <- c("ForeignBank", "Dealer", "HedgeFund", "AssetManager",
                    "Corporate", "CentralBank")
n_banks        <- 30   # synthetic bank IDs (10 dealers, 20 foreign banks)
start_date     <- as.Date("2016-01-01")
end_date       <- as.Date("2022-12-31")
dates          <- seq(start_date, end_date, by = "week")
n_dates        <- length(dates)

# Bank registry: each bank belongs to one sector and has a home currency
bank_df <- tibble(
  bank_id   = paste0("BNK", sprintf("%02d", seq_len(n_banks))),
  sector    = c(rep("Dealer", 10), rep("ForeignBank", 12),
                rep("HedgeFund", 4), rep("AssetManager", 4)),
  home_ccy  = c(rep("USD", 10),
                sample(currency_pairs, 12, replace = TRUE),
                rep("USD", 4),
                rep("USD", 4)),
  # Pre-determined MMF exposure share: proportion of funding from prime MMFs
  # Higher for FBOs / foreign banks; effectively zero for dealers and HFs
  mmf_share_pre = c(runif(10, 0.02, 0.08),   # dealers: low MMF exposure
                    runif(12, 0.15, 0.55),    # foreign banks: high
                    runif(4,  0.01, 0.05),    # HFs: minimal
                    runif(4,  0.05, 0.15))    # AMs: moderate
)

# ---------------------------------------------------------------------------
# 1. Macro / aggregate time-series variables
# ---------------------------------------------------------------------------

# Stress regimes: Normal | March2020 | QuarterEnd | PostVolcker
quarter_end_dates <- dates[month(dates) %in% c(3, 6, 9, 12) &
                              day(dates) >= 20]
march2020_dates   <- dates[year(dates) == 2020 & month(dates) == 3]

macro_ts <- tibble(date = dates) %>%
  mutate(
    # VIX proxy: elevated in 2020 and episodically
    VIX = 15 + 5 * sin(as.numeric(date - start_date) / 365 * pi) +
      rnorm(n_dates, 0, 3) +
      ifelse(date %in% march2020_dates, 40, 0) +
      ifelse(year(date) >= 2022, 8, 0),

    # MOVE (bond vol)
    MOVE = 60 + 15 * sin(as.numeric(date - start_date) / 300) +
      rnorm(n_dates, 0, 8) +
      ifelse(date %in% march2020_dates, 80, 0),

    # MMF aggregate net outflow shock (instrument source):
    # ~N(0,1) in normal times; large negative in March 2020
    MMFShock_agg = rnorm(n_dates, 0, 1) +
      ifelse(date %in% march2020_dates, -4.5, 0) +
      ifelse(year(date) >= 2016 & year(date) <= 2016 &
               month(date) >= 10, -2.5, 0),  # 2016 MMF reform

    # Fed funds effective / OIS rate
    OIS_rate = 0.5 + cumsum(rnorm(n_dates, 0, 0.002)) %>%
      pmax(0) %>% pmin(3),

    # Dealer constraint indicator: 1 when VIX > 28 or MOVE > 110
    DealerConstraint = as.integer(VIX > 28 | MOVE > 110),

    # Quarter-end indicator
    QuarterEnd = as.integer(date %in% quarter_end_dates),

    # Stress regime label
    stress_regime = case_when(
      date %in% march2020_dates              ~ "March2020",
      date %in% quarter_end_dates            ~ "QuarterEnd",
      DealerConstraint == 1                  ~ "HighStress",
      TRUE                                   ~ "Normal"
    )
  )

# ---------------------------------------------------------------------------
# 2. Cell-level panel (currency_pair × tenor × date)
# ---------------------------------------------------------------------------

cells <- expand_grid(currency_pair = currency_pairs, tenor = tenors)
n_cells <- nrow(cells)

# Assign cells tenor-specific base spreads (in basis points)
tenor_spread_adj <- c("ON" = -2, "1W" = 0, "1M" = 3, "3M" = 7)
pair_spread_adj  <- c("EURUSD" = 5, "JPYUSD" = 8, "GBPUSD" = 3,
                      "CADUSD" = 2, "CHFUSD" = 6)

# Construct cell FE (random intercepts centred at 0)
cell_fe <- cells %>%
  mutate(
    cell_fe_mu  = pair_spread_adj[currency_pair] +
                    tenor_spread_adj[tenor] + rnorm(n_cells, 0, 1),
    cell_id     = paste(currency_pair, tenor, sep = "_")
  )

# Expand to full panel
panel_cell <- expand_grid(
  cell_id     = cell_fe$cell_id,
  date        = dates
) %>%
  left_join(cell_fe, by = "cell_id") %>%
  left_join(macro_ts, by = "date")

# --- Construct U_t (net foreign bank USD demand) ---
# U_t is aggregate net demand for synthetic USD from foreign banks in each cell
# Scale varies by currency pair (JPY largest, CAD smallest)
pair_scale <- c("EURUSD" = 1.2, "JPYUSD" = 1.8, "GBPUSD" = 0.9,
                "CADUSD" = 0.6, "CHFUSD" = 0.7)
tenor_scale <- c("ON" = 1.0, "1W" = 0.8, "1M" = 0.6, "3M" = 0.4)

panel_cell <- panel_cell %>%
  mutate(
    pair_sc  = pair_scale[currency_pair],
    tenor_sc = tenor_scale[tenor],

    # U_t: positive = foreign bank demands USD; units = USD bn (synthetic)
    U_t = pair_sc * tenor_sc * (
      5 +
      1.5 * abs(rnorm(n(), 0, 1)) +
      0.6 * VIX / 15 +
      ifelse(stress_regime == "March2020", 8, 0) +
      ifelse(stress_regime == "QuarterEnd", 2, 0)
    ),

    # B_cap: dealer/FBO balance-sheet capacity, > 0
    # Decreases with VIX, drops sharply at quarter-end and in crisis
    B_cap = pair_sc * tenor_sc * (
      20 - 0.25 * VIX +
      rnorm(n(), 0, 2) -
      5 * DealerConstraint -
      3 * QuarterEnd
    ) %>% pmax(2),   # floor at 2 to avoid non-positive capacity

    # theta_t = U_t / B_cap (market tightness)
    theta_t = U_t / B_cap,

    # mu_t: USD funding spread (outcome variable), bps
    # Constructed from structural equation + noise; > 0 = USD expensive
    mu_t = cell_fe_mu +
      2.5 * theta_t +                     # P1: demand pressure channel
      -0.3 * B_cap +                      # P2: capacity relief channel
      1.5 * DealerConstraint * theta_t +  # P2 interaction: amplification
      2.0 * QuarterEnd +                  # P4: quarter-end effect
      rnorm(n(), 0, 2) +
      ifelse(stress_regime == "March2020", 15, 0),

    # q_t: matching quality proxy in [0,1]
    # Taker ratio / inverse price dispersion proxy
    # Falls when market is tight (theta_t high)
    q_t = plogis(
      2 - 1.2 * theta_t +
      -0.8 * DealerConstraint +
      rnorm(n(), 0, 0.4)
    ),

    # Market clearing residual: sum of signed flows should ≈ 0
    # Construct as small noise around 0
    clearing_residual = rnorm(n(), 0, 0.05) * U_t,

    # SignedUSDFlow (aggregate across sectors): > 0 means net USD obtained
    # By construction, the foreign bank sector aggregate = U_t
    SignedUSDFlow_FB   =  U_t + rnorm(n(), 0, 0.5),
    SignedUSDFlow_DLR  = -U_t * 0.65 + rnorm(n(), 0, 0.5),
    SignedUSDFlow_HF   = -U_t * 0.20 + rnorm(n(), 0, 0.3),
    SignedUSDFlow_AM   =  U_t * 0.12 + rnorm(n(), 0, 0.2),
    SignedUSDFlow_CORP =  U_t * 0.08 + rnorm(n(), 0, 0.1),
    SignedUSDFlow_CB   = -U_t * 0.15 *
                           ifelse(stress_regime == "March2020", 3, 1) +
                         rnorm(n(), 0, 0.1),

    # TIB (Transaction-Implied Basis): TIB = -mu_t
    TIB = -mu_t,

    # Bloomberg CCBS (proxy for basis from swap data): TIB + noise + small bias
    CCBS_bloomberg = TIB + rnorm(n(), 0, 0.5) - 0.3,

    # Taker ratio (proxy for q_t): clamp the full composite expression to [0,1].
    # The pipe would bind only to rnorm() without the outer pmin/pmax wrapping.
    taker_ratio = pmin(1, pmax(0, q_t * 0.8 + 0.1 + rnorm(n(), 0, 0.05))),

    # Price dispersion across counterparties within cell (bps)
    price_dispersion = abs(2 + 0.8 * theta_t + rnorm(n(), 0, 0.5)) *
      (1 + DealerConstraint)
  ) %>%
  select(-pair_sc, -tenor_sc)

# ---------------------------------------------------------------------------
# 3. Bank × cell panel (for balance tests and IV construction)
# ---------------------------------------------------------------------------

# Each bank × cell combination: bank's share of total FX swap volume in cell
bank_cell_base <- expand_grid(
  bank_id     = bank_df$bank_id,
  cell_id     = cell_fe$cell_id
) %>%
  left_join(bank_df, by = "bank_id") %>%
  left_join(cell_fe %>% select(cell_id, currency_pair, tenor), by = "cell_id")

# Pre-period market share (determined before 2018; used as IV weight)
# Foreign banks have high shares in their home-currency pair cells
# Dealers have moderate shares in all cells
bank_cell_base <- bank_cell_base %>%
  mutate(
    # Raw share draw (will be normalized to sum to 1 within cell)
    share_raw = case_when(
      sector == "Dealer"      ~ runif(n(), 0.02, 0.15),
      sector == "ForeignBank" &
        substr(home_ccy, 1, 3) == substr(cell_id, 1, 3) ~
                                runif(n(), 0.10, 0.40),   # dominant share
      sector == "ForeignBank" ~ runif(n(), 0.01, 0.08),
      sector == "HedgeFund"   ~ runif(n(), 0.01, 0.06),
      sector == "AssetManager"~ runif(n(), 0.01, 0.05),
      TRUE                    ~ runif(n(), 0.001, 0.02)
    )
  ) %>%
  group_by(cell_id) %>%
  mutate(market_share_pre = share_raw / sum(share_raw)) %>%
  ungroup() %>%
  select(-share_raw)

# Dominant-share indicator: bank with highest market share in each cell
dominant_banks <- bank_cell_base %>%
  group_by(cell_id) %>%
  slice_max(market_share_pre, n = 1, with_ties = FALSE) %>%
  mutate(is_dominant = TRUE) %>%
  select(bank_id, cell_id, is_dominant)

bank_cell_base <- bank_cell_base %>%
  left_join(dominant_banks, by = c("bank_id", "cell_id")) %>%
  mutate(is_dominant = replace_na(is_dominant, FALSE))

# MMF-exposed bank indicator: foreign banks with high pre-period MMF share
mmf_exposed_banks <- bank_df %>%
  filter(mmf_share_pre > 0.25) %>%
  pull(bank_id)

bank_cell_base <- bank_cell_base %>%
  mutate(is_mmf_exposed = bank_id %in% mmf_exposed_banks)

# Expand to time dimension: bank × cell × date (sample to avoid memory issues)
# For estimation, we use a representative weekly subset
panel_bank <- expand_grid(
  bank_id = bank_df$bank_id,
  cell_id = cell_fe$cell_id,
  date    = dates
) %>%
  left_join(bank_cell_base, by = c("bank_id", "cell_id")) %>%
  left_join(panel_cell %>%
              select(cell_id, date, U_t, B_cap, mu_t, theta_t, q_t,
                     DealerConstraint, QuarterEnd, stress_regime,
                     VIX, OIS_rate),
            by = c("cell_id", "date")) %>%
  # Bank-level signed USD flow = cell aggregate × individual share + noise
  mutate(
    SignedUSDFlow = U_t * market_share_pre *
      ifelse(sector == "ForeignBank", 1, -1) +
      rnorm(n(), 0, 0.3),

    # First-stage variable: U_i_m_t (individual bank demand shock)
    U_imt = abs(SignedUSDFlow) * ifelse(sector == "ForeignBank", 1, 0),

    # Pre-period CDS spread (for balance test)
    CDS_pre = case_when(
      sector == "ForeignBank" ~ 50 + 20 * mmf_share_pre + rnorm(n(), 0, 5),
      sector == "Dealer"      ~ 30 + rnorm(n(), 0, 5),
      TRUE                    ~ 40 + rnorm(n(), 0, 5)
    ),

    # Pre-period average FX swap volume (for balance test)
    vol_pre = U_t * market_share_pre * (0.9 + rnorm(n(), 0, 0.05))
  )

# ---------------------------------------------------------------------------
# 4. MMF instrument series
# ---------------------------------------------------------------------------
# Z^MMF_{m,t} = Exposure^MMF_{m, pre} × FundingShock_t
# Exposure^MMF_{m, pre}: weighted average MMF share of dominant banks in cell m

cell_mmf_exposure <- bank_cell_base %>%
  group_by(cell_id) %>%
  summarise(
    # Shift-share weight: dominant-share bank MMF exposure
    DomShare_mmf = sum(market_share_pre * mmf_share_pre[match(bank_id,
                                                               bank_df$bank_id)]),
    top3_share   = sum(sort(market_share_pre, decreasing = TRUE)[1:3]),
    HHI          = sum(market_share_pre^2),
    .groups      = "drop"
  )

mmf_instrument <- expand_grid(
  cell_id = cell_fe$cell_id,
  date    = dates
) %>%
  left_join(cell_mmf_exposure, by = "cell_id") %>%
  left_join(macro_ts %>% select(date, MMFShock_agg), by = "date") %>%
  mutate(
    # Shift-share IV: DomShare × aggregate shock
    Z_MMF = DomShare_mmf * MMFShock_agg,
    # EPFR instrument (asset manager flows shifter)
    EPFR_shock = rnorm(n(), 0, 1) +
      ifelse(year(date) == 2020 & month(date) == 3, -2, 0)
  )

# ---------------------------------------------------------------------------
# 5. Save outputs
# ---------------------------------------------------------------------------

out_dir <- here::here("Output", "fx_swap")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

saveRDS(panel_cell,      file.path(out_dir, "panel_main.rds"))
saveRDS(panel_bank,      file.path(out_dir, "panel_bank.rds"))
saveRDS(mmf_instrument,  file.path(out_dir, "mmf_instrument.rds"))
saveRDS(bank_df,         file.path(out_dir, "bank_registry.rds"))
saveRDS(bank_cell_base,  file.path(out_dir, "bank_cell_base.rds"))
saveRDS(macro_ts,        file.path(out_dir, "macro_ts.rds"))

message("01_simulate_data.R complete.")
message(sprintf("  panel_main:  %d rows × %d cols",
                nrow(panel_cell), ncol(panel_cell)))
message(sprintf("  panel_bank:  %d rows × %d cols",
                nrow(panel_bank), ncol(panel_bank)))
message(sprintf("  mmf_instrument: %d rows", nrow(mmf_instrument)))
