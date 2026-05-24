## =============================================================================
## Title:   07_bilateral_decomposition.R
## Author:  Data Engineer
## Date:    2026-05-24
## Purpose: Bilateral flow decomposition (NEW — empirical-roadmap-v9.md Section 8).
##          1. Sectoral price spreads relative to interdealer benchmark.
##          2. Bilateral flow matrix: Flow_{s→r,m,t} and absorption shares.
##          3. Taker/maker decomposition by sector.
##          4. Dealer heterogeneity: UnmatchedLoad, NettingEfficiency.
##          All regressions follow:
##            Y_{s,m,t} = α_{s,m} + δ_t + β_s Ẑ^D + γ_s Ẑ^S + ε
##          Sign convention: SignedUSDFlow > 0 = entity obtains USD.
## Inputs:  Output/fx_swap/panel_main.rds
##          Output/fx_swap/bilateral_flows.rds
##          Output/fx_swap/dealer_positions.rds
##          Output/fx_swap/mmf_instrument.rds
##          Output/fx_swap/supply_instrument.rds
##          Output/fx_swap/macro_ts.rds
## Outputs: paper/tables/bilateral_sector_spreads.tex
##          paper/tables/bilateral_flow_matrix.tex
##          paper/tables/bilateral_taker_maker.tex
##          paper/tables/bilateral_dealer_heterogeneity.tex
##          paper/figures/intermediation_matrix_heatmap.pdf
##          paper/figures/sector_spread_dynamics.pdf
##          paper/figures/cross_qe_variation.pdf
##          Output/fx_swap/bilateral_results.rds
## =============================================================================
## NOTE: set.seed() is called once in 00_master.R before this script is sourced.

library(here)
library(dplyr)
library(tidyr)
library(fixest)
library(lubridate)
library(ggplot2)

source(here::here("scripts", "R", "functions", "helpers.R"))

out_dir   <- here::here("Output", "fx_swap")
table_dir <- here::here("paper", "tables")
fig_dir   <- here::here("paper", "figures")
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(fig_dir,   recursive = TRUE, showWarnings = FALSE)

# ---------------------------------------------------------------------------
# 0. Load data
# ---------------------------------------------------------------------------

panel    <- readRDS(file.path(out_dir, "panel_main.rds"))
bilateral <- readRDS(file.path(out_dir, "bilateral_flows.rds"))
positions <- readRDS(file.path(out_dir, "dealer_positions.rds"))
instr    <- readRDS(file.path(out_dir, "mmf_instrument.rds"))
sinstr   <- readRDS(file.path(out_dir, "supply_instrument.rds"))
macro    <- readRDS(file.path(out_dir, "macro_ts.rds"))

# Merge all instruments into panel
panel_full <- panel %>%
  left_join(instr  %>% select(cell_id, date, Z_MMF, DomShare_mmf),
            by = c("cell_id", "date")) %>%
  left_join(sinstr %>% select(cell_id, date, Z_S_QE),
            by = c("cell_id", "date")) %>%
  left_join(macro  %>% select(date, OIS_rate), by = "date") %>%
  mutate(
    Z_S_QE_na0 = replace(Z_S_QE, is.na(Z_S_QE), 0),
    Scarcity   = -DealerSupply,
    cell_fe    = cell_id,
    year       = year(date)
  ) %>%
  filter(!is.na(Z_MMF))

# ---------------------------------------------------------------------------
# 1. Sectoral price spreads (Section 8.1, empirical-roadmap-v9.md)
# ---------------------------------------------------------------------------
# Spread_{s,m,t} = P_{s,m,t} - P_{ID,m,t}
# Spec: Spread_{s,m,t} = α_{s,m} + δ_t + β_s Q̂^FB + γ_s Scarcityhat + ε

# Reshape to long format: one row per sector-cell-date
sector_spreads_long <- panel_full %>%
  select(cell_id, date, Z_MMF, Z_S_QE_na0, OIS_rate,
         spread_FB, spread_HF, spread_AM, DealerConstraint, QuarterEnd) %>%
  pivot_longer(
    cols = c(spread_FB, spread_HF, spread_AM),
    names_to  = "sector",
    values_to = "spread"
  ) %>%
  mutate(
    sector   = sub("spread_", "", sector),
    group_id = paste(cell_id, sector, sep = "_")
  )

# Sector-specific regressions: spread ~ Z^D + Z^S + FE
ss_spread_FB <- feols(
  spread ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = panel_full,
  cluster = ~cell_id + date
)

# Reduced-form spread for foreign banks (how does demand shock affect FB spread?)
ss_spread_HF <- feols(
  spread_HF ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = panel_full,
  cluster = ~cell_id + date
)

ss_spread_AM <- feols(
  spread_AM ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = panel_full,
  cluster = ~cell_id + date
)

tex_spreads <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{(1) Foreign Bank} & \\textbf{(2) Hedge Fund} & \\textbf{(3) Asset Manager} \\\\",
  "  & \\textbf{Spread vs. ID} & \\textbf{Spread vs. ID} & \\textbf{Spread vs. ID} \\\\",
  "  \\midrule",
  coef_se_rows(list(ss_spread_FB, ss_spread_HF, ss_spread_AM),
               "Z_MMF$", "$Z^D$ (demand shock)"),
  coef_se_rows(list(ss_spread_FB, ss_spread_HF, ss_spread_AM),
               "Z_S_QE_na0", "$Z^S$ (supply shock)"),
  coef_se_rows(list(ss_spread_FB, ss_spread_HF, ss_spread_AM),
               "OIS_rate", "OIS rate"),
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(ss_spread_FB), nobs(ss_spread_HF), nobs(ss_spread_AM)),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  \\multicolumn{4}{l}{\\textit{Notes: Spread = sectoral price minus interdealer benchmark (bps).}} \\\\",
  "  \\multicolumn{4}{l}{\\textit{Positive coefficient on $Z^D$: sector pays more when FB demand rises.}} \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)
writeLines(tex_spreads, file.path(table_dir, "bilateral_sector_spreads.tex"))
message("  Bilateral sector spreads table saved.")

# ---------------------------------------------------------------------------
# 2. Bilateral flow matrix (Section 8.2, empirical-roadmap-v9.md)
# ---------------------------------------------------------------------------
# Share_{s→r,m,t} = Flow_{s→r} / total_flow_{m,t}
# Spec: Share ~ α_{s,r,m} + δ_t + β_{s,r} Z^D + γ_{s,r} Z^S

bilateral_full <- bilateral %>%
  left_join(instr  %>% select(cell_id, date, Z_MMF),
            by = c("cell_id", "date")) %>%
  left_join(sinstr %>% select(cell_id, date, Z_S_QE),
            by = c("cell_id", "date")) %>%
  left_join(macro  %>% select(date, OIS_rate), by = "date") %>%
  mutate(
    Z_S_QE_na0 = replace(Z_S_QE, is.na(Z_S_QE), 0),
    pair_key   = paste(sector_provider, sector_demander, sep = "->"),
    group_id   = paste(cell_id, pair_key, sep = "_")
  ) %>%
  filter(!is.na(Z_MMF))

# Average flow matrix (descriptive)
avg_matrix <- bilateral_full %>%
  group_by(sector_provider, sector_demander) %>%
  summarise(
    avg_flow_M  = mean(flow_M, na.rm = TRUE),
    avg_share   = mean(share_adj, na.rm = TRUE),
    .groups = "drop"
  )

# Regression: dealer→FB share ~ instruments (key result: dealers retreat at QE)
flow_dealer_fb <- bilateral_full %>%
  filter(sector_provider == "Dealer" & sector_demander == "ForeignBank")

m_dealer_fb <- feols(
  share_adj ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = flow_dealer_fb,
  cluster = ~cell_id + date
)

# HF→FB share ~ instruments (do HFs step in when dealers retreat?)
flow_hf_fb <- bilateral_full %>%
  filter(sector_provider == "HedgeFund" & sector_demander == "ForeignBank")

m_hf_fb <- feols(
  share_adj ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = flow_hf_fb,
  cluster = ~cell_id + date
)

# CB→FB share ~ instruments (CB swap lines as supply)
flow_cb_fb <- bilateral_full %>%
  filter(sector_provider == "CentralBank" & sector_demander == "ForeignBank")

m_cb_fb <- feols(
  share_adj ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = flow_cb_fb,
  cluster = ~cell_id + date
)

tex_flow_matrix <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{(1) Dealer$\\to$FB} & \\textbf{(2) HF$\\to$FB} & \\textbf{(3) CB$\\to$FB} \\\\",
  "  & \\textbf{Market share} & \\textbf{Market share} & \\textbf{Market share} \\\\",
  "  \\midrule",
  coef_se_rows(list(m_dealer_fb, m_hf_fb, m_cb_fb),
               "Z_MMF$", "$Z^D$ (demand shock)"),
  coef_se_rows(list(m_dealer_fb, m_hf_fb, m_cb_fb),
               "Z_S_QE_na0", "$Z^S$ (supply shock)"),
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(m_dealer_fb), nobs(m_hf_fb), nobs(m_cb_fb)),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  \\multicolumn{4}{l}{\\textit{Notes: Dependent variable = provider sector share of total flow to ForeignBank.}} \\\\",
  "  \\multicolumn{4}{l}{\\textit{$Z^S < 0$ in col (1): dealers supply less when regulatory pressure rises.}} \\\\",
  "  \\multicolumn{4}{l}{\\textit{$Z^S > 0$ in col (2): hedge funds partially absorb dealer retreat.}} \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)
writeLines(tex_flow_matrix, file.path(table_dir, "bilateral_flow_matrix.tex"))
message("  Bilateral flow matrix table saved.")

# ---------------------------------------------------------------------------
# 3. Taker/maker by sector (Section 8.3)
# ---------------------------------------------------------------------------
# Q^{Taker}_{FB} = taker_ratio × flow_M for demander = ForeignBank
# Test: π^taker >> π^maker for FB (urgent demand vs. routine)

panel_taker <- panel_full %>%
  mutate(
    U_taker = taker_ratio * U_t,
    U_maker = (1 - taker_ratio) * U_t
  )

fs_taker_demand <- feols(
  U_taker ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = panel_taker,
  cluster = ~cell_id + date
)

fs_maker_demand <- feols(
  U_maker ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = panel_taker,
  cluster = ~cell_id + date
)

# Taker ratio as outcome: does urgency rise with Z^D?
fs_taker_ratio <- feols(
  taker_ratio ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = panel_full,
  cluster = ~cell_id + date
)

tex_taker <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{(1) Taker demand} & \\textbf{(2) Maker demand} & \\textbf{(3) Taker ratio} \\\\",
  "  \\midrule",
  coef_se_rows(list(fs_taker_demand, fs_maker_demand, fs_taker_ratio),
               "Z_MMF$", "$Z^D$ (demand shock)"),
  coef_se_rows(list(fs_taker_demand, fs_maker_demand, fs_taker_ratio),
               "Z_S_QE_na0", "$Z^S$ (supply shock)"),
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(fs_taker_demand), nobs(fs_maker_demand), nobs(fs_taker_ratio)),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  \\multicolumn{4}{l}{\\textit{Notes: Matching-function prediction: $\\pi^{taker}_{Z^D} >> \\pi^{maker}_{Z^D}$.}} \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)
writeLines(tex_taker, file.path(table_dir, "bilateral_taker_maker.tex"))
message("  Taker/maker table saved.")

# ---------------------------------------------------------------------------
# 4. Dealer heterogeneity: UnmatchedLoad and NettingEfficiency (Section 8.4)
# ---------------------------------------------------------------------------
# Test: supply instrument Z^S is stronger for dealers with high UnmatchedLoad
# and low NettingEfficiency (dealers already loaded are more constrained at QE)

pos_full <- positions %>%
  left_join(instr  %>% select(cell_id, date, Z_MMF),
            by = c("cell_id", "date")) %>%
  left_join(sinstr %>% select(cell_id, date, Z_S_QE),
            by = c("cell_id", "date")) %>%
  left_join(macro  %>% select(date, OIS_rate), by = "date") %>%
  mutate(Z_S_QE_na0 = replace(Z_S_QE, is.na(Z_S_QE), 0)) %>%
  filter(!is.na(Z_MMF))

m_unmatched <- feols(
  unmatched_load_M ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = pos_full,
  cluster = ~cell_id + date
)

m_netting <- feols(
  netting_eff ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = pos_full,
  cluster = ~cell_id + date
)

m_matched <- feols(
  matched_M ~ Z_MMF + Z_S_QE_na0 + OIS_rate | cell_id + date,
  data    = pos_full,
  cluster = ~cell_id + date
)

tex_dealer_het <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{(1) UnmatchedLoad} & \\textbf{(2) NettingEffic.} & \\textbf{(3) MatchedInterm.} \\\\",
  "  \\midrule",
  coef_se_rows(list(m_unmatched, m_netting, m_matched),
               "Z_MMF$", "$Z^D$ (demand shock)"),
  coef_se_rows(list(m_unmatched, m_netting, m_matched),
               "Z_S_QE_na0", "$Z^S$ (supply shock)"),
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(m_unmatched), nobs(m_netting), nobs(m_matched)),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  \\multicolumn{4}{l}{\\textit{Notes: UnmatchedLoad = |USD supplied - USD obtained| (dealer balance sheet load).}} \\\\",
  "  \\multicolumn{4}{l}{\\textit{NettingEfficiency = 1 - UnmatchedLoad/GrossLoad. Prediction: $Z^S$ raises unmatched load.}} \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)
writeLines(tex_dealer_het, file.path(table_dir, "bilateral_dealer_heterogeneity.tex"))
message("  Dealer heterogeneity table saved.")

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------

# Figure 1: Average intermediation matrix heatmap
avg_matrix_plot <- avg_matrix %>%
  mutate(
    sector_provider = factor(sector_provider,
                             levels = c("Dealer", "HedgeFund", "CentralBank")),
    sector_demander = factor(sector_demander,
                             levels = c("ForeignBank", "AssetManager", "Corporate"))
  )

p_matrix <- ggplot(avg_matrix_plot,
                   aes(x = sector_demander, y = sector_provider, fill = avg_share)) +
  geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = sprintf("%.0f%%", avg_share * 100)),
            family = "serif", size = 3.5) +
  scale_fill_gradient(low = "white", high = "#003366",
                      name = "Average\nmarket share",
                      labels = scales::percent) +
  labs(x = "Sector receiving USD (demander)",
       y = "Sector providing USD (provider)") +
  theme_minimal(base_family = "serif") +
  theme(
    panel.grid    = element_blank(),
    axis.text     = element_text(size = 9),
    legend.position = "right"
  )

ggsave(file.path(fig_dir, "intermediation_matrix_heatmap.pdf"),
       p_matrix, width = 6, height = 4)
message("  Intermediation matrix heatmap saved.")

# Figure 2: Sector spread dynamics over time
spread_ts <- panel_full %>%
  group_by(date) %>%
  summarise(
    spread_FB = mean(spread_FB, na.rm = TRUE),
    spread_HF = mean(spread_HF, na.rm = TRUE),
    spread_AM = mean(spread_AM, na.rm = TRUE),
    QuarterEnd = max(QuarterEnd),
    DealerConstraint = max(DealerConstraint),
    .groups = "drop"
  ) %>%
  pivot_longer(cols = c(spread_FB, spread_HF, spread_AM),
               names_to = "sector", values_to = "spread") %>%
  mutate(sector = recode(sector,
    spread_FB = "Foreign Bank", spread_HF = "Hedge Fund", spread_AM = "Asset Manager"
  ))

p_spreads <- ggplot(spread_ts, aes(x = date, y = spread,
                                    color = sector, linetype = sector)) +
  geom_line(linewidth = 0.6) +
  scale_color_brewer(palette = "Set2", name = NULL) +
  scale_linetype_manual(values = c("solid", "dashed", "dotdash"), name = NULL) +
  labs(x = NULL, y = "Spread vs. interdealer benchmark (bps)") +
  theme_minimal(base_family = "serif") +
  theme(legend.position = "bottom",
        panel.grid.minor = element_blank())

ggsave(file.path(fig_dir, "sector_spread_dynamics.pdf"),
       p_spreads, width = 7, height = 4)
message("  Sector spread dynamics figure saved.")

# Figure 3: CrossQE variation by tenor and date
cross_qe_ts <- panel_full %>%
  filter(!is.na(cross_qe)) %>%
  group_by(date, tenor) %>%
  summarise(cross_qe_frac = mean(as.integer(cross_qe)), .groups = "drop")

p_crossqe <- ggplot(cross_qe_ts,
                    aes(x = date, y = cross_qe_frac,
                        color = tenor, linetype = tenor)) +
  geom_line(linewidth = 0.6) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  scale_color_brewer(palette = "Set2", name = "Tenor") +
  scale_linetype_manual(values = c("solid", "dashed", "dotdash", "twodash"),
                        name = "Tenor") +
  labs(x = NULL,
       y = "Fraction of contracts crossing a quarter-end") +
  theme_minimal(base_family = "serif") +
  theme(legend.position = "bottom",
        panel.grid.minor = element_blank())

ggsave(file.path(fig_dir, "cross_qe_variation.pdf"),
       p_crossqe, width = 7, height = 4)
message("  CrossQE variation figure saved.")

# ---------------------------------------------------------------------------
# 6. Save results
# ---------------------------------------------------------------------------

bilateral_results <- list(
  sector_spreads = list(fb = ss_spread_FB, hf = ss_spread_HF, am = ss_spread_AM),
  flow_matrix    = list(dealer_fb = m_dealer_fb, hf_fb = m_hf_fb, cb_fb = m_cb_fb),
  taker_maker    = list(taker = fs_taker_demand, maker = fs_maker_demand,
                         ratio = fs_taker_ratio),
  dealer_het     = list(unmatched = m_unmatched, netting = m_netting,
                         matched = m_matched),
  avg_matrix     = avg_matrix
)
saveRDS(bilateral_results, file.path(out_dir, "bilateral_results.rds"))

message("07_bilateral_decomposition.R complete.")
