## =============================================================================
## Title:   06_quality_checks.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: Data quality checks (Task 5).
##          1. Market clearing residual: Sigma_i SignedUSDFlow_{i,m,t} ≈ 0
##          2. TIB vs Bloomberg CCBS validation (correlation table)
##          3. Liquidity filter: report obs dropped by bid-ask spread > 2bp
## Inputs:  Output/fx_swap/panel_main.rds
## Outputs: paper/tables/quality_checks.tex
##          Output/fx_swap/quality_check_results.rds
## =============================================================================

library(here)
library(dplyr)
library(tidyr)
library(ggplot2)
library(scales)

# set.seed() is called once in 00_master.R; removed here to avoid duplicate.

# ---------------------------------------------------------------------------
# 0. Load data
# ---------------------------------------------------------------------------

out_dir   <- here::here("Output", "fx_swap")
table_dir <- here::here("paper", "tables")
fig_dir   <- here::here("paper", "figures")
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(fig_dir,   recursive = TRUE, showWarnings = FALSE)

panel <- readRDS(file.path(out_dir, "panel_main.rds"))

# ---------------------------------------------------------------------------
# 1. Market clearing residual
# ---------------------------------------------------------------------------
# Theoretical constraint: Sigma_s SignedUSDFlow_{s,m,t} = 0
# Residual = sum of all sector flows; should be small relative to U_t

panel <- panel %>%
  mutate(
    clearing_sum = SignedUSDFlow_FB + SignedUSDFlow_DLR +
                   SignedUSDFlow_HF + SignedUSDFlow_AM +
                   SignedUSDFlow_CORP + SignedUSDFlow_CB
  )

clearing_stats <- panel %>%
  group_by(currency_pair) %>%
  summarise(
    mean_abs_residual = mean(abs(clearing_sum), na.rm = TRUE),
    mean_U_t          = mean(U_t, na.rm = TRUE),
    rel_residual      = mean(abs(clearing_sum) / U_t, na.rm = TRUE),
    pct_within_5pct   = mean(abs(clearing_sum) / U_t < 0.05, na.rm = TRUE),
    .groups           = "drop"
  )

overall_clearing <- panel %>%
  summarise(
    mean_abs_residual = mean(abs(clearing_sum), na.rm = TRUE),
    mean_U_t          = mean(U_t, na.rm = TRUE),
    rel_residual      = mean(abs(clearing_sum) / U_t, na.rm = TRUE),
    pct_within_5pct   = mean(abs(clearing_sum) / U_t < 0.05, na.rm = TRUE)
  )

message(sprintf("  Mean absolute clearing residual: %.4f USD bn",
                overall_clearing$mean_abs_residual))
message(sprintf("  Relative residual (share of U_t): %.2f%%",
                100 * overall_clearing$rel_residual))
message(sprintf("  Fraction of obs within 5%% of market clearing: %.1f%%",
                100 * overall_clearing$pct_within_5pct))

# ---------------------------------------------------------------------------
# 2. TIB vs Bloomberg CCBS validation
# ---------------------------------------------------------------------------
# Correlation of TIB (transaction-implied basis) with Bloomberg CCBS proxy
# Split by currency pair and stress regime

corr_by_pair <- panel %>%
  group_by(currency_pair) %>%
  summarise(
    rho_tib_ccbs   = cor(TIB, CCBS_bloomberg, use = "complete.obs"),
    mean_TIB       = mean(TIB,            na.rm = TRUE),
    mean_CCBS      = mean(CCBS_bloomberg, na.rm = TRUE),
    mean_deviation = mean(TIB - CCBS_bloomberg, na.rm = TRUE),
    sd_deviation   = sd(TIB   - CCBS_bloomberg, na.rm = TRUE),
    n_obs          = sum(!is.na(TIB) & !is.na(CCBS_bloomberg)),
    .groups        = "drop"
  )

corr_by_regime <- panel %>%
  group_by(stress_regime) %>%
  summarise(
    rho_tib_ccbs   = cor(TIB, CCBS_bloomberg, use = "complete.obs"),
    mean_deviation = mean(TIB - CCBS_bloomberg, na.rm = TRUE),
    n_obs          = sum(!is.na(TIB) & !is.na(CCBS_bloomberg)),
    .groups        = "drop"
  )

# ---------------------------------------------------------------------------
# 3. Liquidity filter: bid-ask spread > 2bp threshold
# ---------------------------------------------------------------------------
# price_dispersion is the within-cell cross-counterparty spread proxy
# Cells with dispersion > 2bp are considered illiquid (filter applied)

liquidity_threshold <- 2.0  # bps

filter_stats <- panel %>%
  summarise(
    n_total        = n(),
    n_illiquid     = sum(price_dispersion > liquidity_threshold, na.rm = TRUE),
    n_liquid       = sum(price_dispersion <= liquidity_threshold, na.rm = TRUE),
    pct_dropped    = mean(price_dispersion > liquidity_threshold, na.rm = TRUE),
    pct_retained   = mean(price_dispersion <= liquidity_threshold, na.rm = TRUE)
  )

filter_by_pair <- panel %>%
  group_by(currency_pair) %>%
  summarise(
    pct_dropped  = mean(price_dispersion > liquidity_threshold, na.rm = TRUE),
    pct_retained = 1 - mean(price_dispersion > liquidity_threshold, na.rm = TRUE),
    n_dropped    = sum(price_dispersion > liquidity_threshold, na.rm = TRUE),
    .groups      = "drop"
  )

message(sprintf("  Liquidity filter (> %.0f bps): drops %.1f%% of observations",
                liquidity_threshold, 100 * filter_stats$pct_dropped))

# ---------------------------------------------------------------------------
# 4. LaTeX quality checks table
# ---------------------------------------------------------------------------

stars_fn <- function(p) {
  if (is.na(p))  return("")
  if (p < 0.01) return("^{***}")
  if (p < 0.05) return("^{**}")
  if (p < 0.10) return("^{*}")
  return("")
}

tex_lines <- c(
  "\\begin{tabular}{lcccc}",
  "  \\toprule",
  "  & \\textbf{Obs.} & \\textbf{Mean abs.} & \\textbf{Relative} & \\textbf{Within} \\\\",
  "  \\textit{Panel A: Market clearing residual} & & \\textbf{residual} & \\textbf{residual} & \\textbf{5\\%} \\\\",
  "  \\midrule"
)

# Pre-allocate to avoid growing vector (INV-17)
clearing_rows <- vapply(seq_len(nrow(clearing_stats)), function(i) {
  r <- clearing_stats[i, ]
  sprintf("  %s & --- & %.4f & %.2f\\%% & %.1f\\%% \\\\",
          r$currency_pair, r$mean_abs_residual,
          100 * r$rel_residual, 100 * r$pct_within_5pct)
}, character(1))
tex_lines <- c(tex_lines, clearing_rows)
tex_lines <- c(tex_lines,
  sprintf("  \\textit{Pooled} & --- & %.4f & %.2f\\%% & %.1f\\%% \\\\",
          overall_clearing$mean_abs_residual,
          100 * overall_clearing$rel_residual,
          100 * overall_clearing$pct_within_5pct),
  "  \\midrule",
  "  \\multicolumn{5}{l}{\\textit{Panel B: TIB vs.\\ Bloomberg CCBS correlation}} \\\\[3pt]"
)

# Pre-allocate to avoid growing vector (INV-17)
corr_rows <- vapply(seq_len(nrow(corr_by_pair)), function(i) {
  r <- corr_by_pair[i, ]
  sprintf("  %s & %s & $\\rho$=%.3f & Mean dev.=%.2f & SD dev.=%.2f \\\\",
          r$currency_pair,
          format(r$n_obs, big.mark = ","),
          r$rho_tib_ccbs, r$mean_deviation, r$sd_deviation)
}, character(1))
tex_lines <- c(tex_lines, corr_rows)

tex_lines <- c(tex_lines,
  "  \\midrule",
  "  \\multicolumn{5}{l}{\\textit{Panel C: Liquidity filter (bid-ask spread $>$ 2 bps)}} \\\\[3pt]"
)

# Pre-allocate to avoid growing vector (INV-17)
filter_rows <- vapply(seq_len(nrow(filter_by_pair)), function(i) {
  r <- filter_by_pair[i, ]
  sprintf("  %s & --- & Dropped: %s & (%.1f\\%%) & Retained: %.1f\\%% \\\\",
          r$currency_pair,
          format(r$n_dropped, big.mark = ","),
          100 * r$pct_dropped,
          100 * r$pct_retained)
}, character(1))
tex_lines <- c(tex_lines, filter_rows)
tex_lines <- c(tex_lines,
  sprintf("  \\textit{Pooled} & %s & Dropped: %s & (%.1f\\%%) & Retained: %.1f\\%% \\\\",
          format(filter_stats$n_total, big.mark = ","),
          format(filter_stats$n_illiquid, big.mark = ","),
          100 * filter_stats$pct_dropped,
          100 * filter_stats$pct_retained),
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines, file.path(table_dir, "quality_checks.tex"))

# ---------------------------------------------------------------------------
# 5. TIB vs CCBS scatter figure (supplementary)
# ---------------------------------------------------------------------------

custom_theme <- theme_bw(base_size = 14, base_family = "serif") +
  theme(
    panel.grid.minor  = element_blank(),
    panel.grid.major  = element_line(color = "grey90"),
    legend.position   = "bottom",
    legend.direction  = "horizontal",
    plot.background   = element_rect(fill = "white", color = NA),
    panel.background  = element_rect(fill = "white"),
    strip.background  = element_rect(fill = "grey95"),
    strip.text        = element_text(size = 12, face = "bold"),
    axis.title        = element_text(size = 13),
    axis.text         = element_text(size = 11)
  )

plot_sample <- panel %>%
  slice_sample(n = min(5000, nrow(panel)))

p_val <- ggplot(plot_sample, aes(x = TIB, y = CCBS_bloomberg,
                                 color = currency_pair)) +
  geom_point(alpha = 0.25, size = 0.8) +
  geom_abline(slope = 1, intercept = 0,
              linetype = "dashed", color = "black", linewidth = 0.8) +
  scale_color_viridis_d(option = "D", name = "Currency pair") +
  labs(
    x = "TIB (transaction-implied basis, bps)",
    y = "Bloomberg CCBS (bps)"
  ) +
  custom_theme

ggsave(file.path(fig_dir, "tib_ccbs_validation.pdf"),
       p_val, width = 8, height = 6)
ggsave(file.path(fig_dir, "tib_ccbs_validation.png"),
       p_val, width = 8, height = 6, dpi = 150)

# ---------------------------------------------------------------------------
# 6. Save results
# ---------------------------------------------------------------------------

qc_results <- list(
  clearing_stats    = clearing_stats,
  overall_clearing  = overall_clearing,
  corr_by_pair      = corr_by_pair,
  corr_by_regime    = corr_by_regime,
  filter_stats      = filter_stats,
  filter_by_pair    = filter_by_pair
)
saveRDS(qc_results, file.path(out_dir, "quality_check_results.rds"))

message("06_quality_checks.R complete.")
message(sprintf("  Market clearing relative residual: %.2f%%",
                100 * overall_clearing$rel_residual))
message(sprintf("  TIB-CCBS correlation (EUR/USD): %.3f",
                corr_by_pair$rho_tib_ccbs[corr_by_pair$currency_pair == "EURUSD"]))
