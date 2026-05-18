## =============================================================================
## Title:   02_balance_tests.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: Balance tests for shift-share IV validity (Task 1).
##          Tests whether dominant-share / MMF-exposed banks are systematically
##          different from other banks on pre-period characteristics.
##          Per strategy memo (Objection 1 response): this is a prerequisite
##          for IV validity, not optional robustness.
## Inputs:  Output/fx_swap/bank_cell_base.rds
##          Output/fx_swap/panel_bank.rds
## Outputs: paper/tables/balance_tests.tex
##          paper/figures/balance_tests_share_distribution.pdf
##          Output/fx_swap/balance_test_results.rds
## =============================================================================

library(here)
library(dplyr)
library(tidyr)
library(ggplot2)
library(scales)
library(viridis)

# ---------------------------------------------------------------------------
# 0. Load data
# ---------------------------------------------------------------------------

out_dir    <- here::here("Output", "fx_swap")
fig_dir    <- here::here("paper", "figures")
table_dir  <- here::here("paper", "tables")
dir.create(fig_dir,   recursive = TRUE, showWarnings = FALSE)
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)

bank_cell  <- readRDS(file.path(out_dir, "bank_cell_base.rds"))
panel_bank <- readRDS(file.path(out_dir, "panel_bank.rds"))

# ---------------------------------------------------------------------------
# 1. Market share distribution (HHI, top-3 share) by cell
# ---------------------------------------------------------------------------

cell_concentration <- bank_cell %>%
  group_by(cell_id) %>%
  summarise(
    HHI        = sum(market_share_pre^2),
    top3_share = sum(sort(market_share_pre, decreasing = TRUE)[1:3]),
    n_banks    = n(),
    .groups    = "drop"
  ) %>%
  separate(cell_id, into = c("currency_pair", "tenor"), sep = "_",
           extra = "merge")

# ---------------------------------------------------------------------------
# 2. MMF-exposed bank weight by cell
# ---------------------------------------------------------------------------

mmf_weight_by_cell <- bank_cell %>%
  group_by(cell_id) %>%
  summarise(
    mmf_exposed_share = sum(market_share_pre[is_mmf_exposed]),
    n_mmf_exposed     = sum(is_mmf_exposed),
    .groups           = "drop"
  ) %>%
  separate(cell_id, into = c("currency_pair", "tenor"), sep = "_",
           extra = "merge")

# Fraction of cells where MMF-exposed banks hold > 20% share
frac_above20 <- mean(mmf_weight_by_cell$mmf_exposed_share > 0.20)
message(sprintf("  Fraction of cells with MMF-exposed share > 20%%: %.1f%%",
                100 * frac_above20))

# ---------------------------------------------------------------------------
# 3. Balance test: high vs low MMF exposure groups
# ---------------------------------------------------------------------------

# Use pre-period bank-level averages (first 52 weeks as "pre-period")
bank_pre <- panel_bank %>%
  filter(date <= min(date) + 365) %>%
  group_by(bank_id, sector, is_mmf_exposed) %>%
  summarise(
    avg_CDS      = mean(CDS_pre,   na.rm = TRUE),
    avg_vol      = mean(vol_pre,   na.rm = TRUE),
    avg_mshare   = mean(market_share_pre, na.rm = TRUE),
    .groups      = "drop"
  ) %>%
  distinct()

# Only foreign banks meaningful for balance test
bank_pre_fb <- bank_pre %>%
  filter(sector == "ForeignBank")

balance_table <- bank_pre_fb %>%
  group_by(Group = ifelse(is_mmf_exposed, "High MMF Exposure", "Low MMF Exposure")) %>%
  summarise(
    N            = n(),
    mean_CDS     = mean(avg_CDS),
    sd_CDS       = sd(avg_CDS),
    mean_vol     = mean(avg_vol),
    sd_vol       = sd(avg_vol),
    mean_mshare  = mean(avg_mshare),
    sd_mshare    = sd(avg_mshare),
    .groups      = "drop"
  )

# Two-sample t-tests for the balance check
t_CDS   <- t.test(avg_CDS   ~ is_mmf_exposed, data = bank_pre_fb)
t_vol   <- t.test(avg_vol   ~ is_mmf_exposed, data = bank_pre_fb)
t_share <- t.test(avg_mshare ~ is_mmf_exposed, data = bank_pre_fb)

balance_results <- tibble(
  Variable     = c("Pre-period CDS spread (bps)", "Pre-period FX swap volume",
                   "Pre-period market share"),
  High_mean    = c(balance_table$mean_CDS[balance_table$Group == "High MMF Exposure"],
                   balance_table$mean_vol[balance_table$Group == "High MMF Exposure"],
                   balance_table$mean_mshare[balance_table$Group == "High MMF Exposure"]),
  High_sd      = c(balance_table$sd_CDS[balance_table$Group == "High MMF Exposure"],
                   balance_table$sd_vol[balance_table$Group == "High MMF Exposure"],
                   balance_table$sd_mshare[balance_table$Group == "High MMF Exposure"]),
  Low_mean     = c(balance_table$mean_CDS[balance_table$Group == "Low MMF Exposure"],
                   balance_table$mean_vol[balance_table$Group == "Low MMF Exposure"],
                   balance_table$mean_mshare[balance_table$Group == "Low MMF Exposure"]),
  Low_sd       = c(balance_table$sd_CDS[balance_table$Group == "Low MMF Exposure"],
                   balance_table$sd_vol[balance_table$Group == "Low MMF Exposure"],
                   balance_table$sd_mshare[balance_table$Group == "Low MMF Exposure"]),
  Diff         = High_mean - Low_mean,
  p_value      = c(t_CDS$p.value, t_vol$p.value, t_share$p.value)
)

# ---------------------------------------------------------------------------
# 4. Publication-quality figure: market share distribution
# ---------------------------------------------------------------------------

custom_theme <- theme_bw(base_size = 14) +
  theme(
    panel.grid.minor    = element_blank(),
    panel.grid.major    = element_line(color = "grey90"),
    legend.position     = "bottom",
    legend.direction    = "horizontal",
    plot.background     = element_rect(fill = "white", color = NA),
    panel.background    = element_rect(fill = "white"),
    strip.background    = element_rect(fill = "grey95"),
    strip.text          = element_text(size = 12, face = "bold"),
    axis.title          = element_text(size = 13),
    axis.text           = element_text(size = 11),
    legend.text         = element_text(size = 11),
    legend.title        = element_text(size = 12, face = "bold")
  )

# Individual bank share distribution by currency pair
share_dist_data <- bank_cell %>%
  separate(cell_id, into = c("currency_pair", "tenor"), sep = "_",
           extra = "merge") %>%
  filter(tenor == "1M")   # show 1M tenor for clarity

p_share_dist <- ggplot(share_dist_data,
       aes(x = market_share_pre, fill = sector)) +
  geom_histogram(bins = 25, position = "stack", alpha = 0.85) +
  scale_fill_viridis_d(option = "D", name = "Sector") +
  scale_x_continuous(labels = percent_format(accuracy = 1)) +
  facet_wrap(~ currency_pair, ncol = 3, scales = "free_y") +
  labs(
    x = "Pre-period market share (1-month tenor)",
    y = "Number of bank-cell observations"
  ) +
  custom_theme

ggsave(file.path(fig_dir, "balance_tests_share_distribution.pdf"),
       p_share_dist, width = 10, height = 6)
ggsave(file.path(fig_dir, "balance_tests_share_distribution.png"),
       p_share_dist, width = 10, height = 6, dpi = 150)

# ---------------------------------------------------------------------------
# 5. LaTeX balance table (bare tabular — no \begin{table})
# ---------------------------------------------------------------------------

fmt_mean_sd <- function(m, s) {
  sprintf("%.2f (%.2f)", m, s)
}
fmt_p <- function(p) {
  if (p < 0.01) "< 0.01" else sprintf("%.3f", p)
}

tex_rows <- balance_results %>%
  rowwise() %>%
  mutate(
    row = sprintf(
      "  %s & %s & %s & %.3f & %s \\\\\n",
      Variable,
      fmt_mean_sd(High_mean, High_sd),
      fmt_mean_sd(Low_mean,  Low_sd),
      Diff,
      fmt_p(p_value)
    )
  ) %>%
  pull(row)

# Concentration statistics row block
conc_stats <- mmf_weight_by_cell %>%
  summarise(
    med_mmf  = median(mmf_exposed_share),
    p25_mmf  = quantile(mmf_exposed_share, 0.25),
    p75_mmf  = quantile(mmf_exposed_share, 0.75)
  )

tex_lines <- c(
  "\\begin{tabular}{lcccc}",
  "  \\toprule",
  "  \\textbf{Variable} & \\textbf{High MMF} & \\textbf{Low MMF} &",
  "    \\textbf{Difference} & \\textbf{$p$-value} \\\\",
  "  & \\textit{Mean (SD)} & \\textit{Mean (SD)} & & \\\\",
  "  \\midrule",
  "  \\multicolumn{5}{l}{\\textit{Panel A: Bank pre-period characteristics",
  "    (foreign banks only)}} \\\\[3pt]",
  tex_rows,
  "  \\midrule",
  "  \\multicolumn{5}{l}{\\textit{Panel B: MMF-exposed bank market weight by cell}} \\\\[3pt]",
  sprintf("  Median cell MMF-exposed share & \\multicolumn{4}{l}{%.1f\\%%} \\\\",
          100 * conc_stats$med_mmf),
  sprintf("  Interquartile range & \\multicolumn{4}{l}{[%.1f\\%%, %.1f\\%%]} \\\\",
          100 * conc_stats$p25_mmf, 100 * conc_stats$p75_mmf),
  sprintf("  Fraction of cells with MMF share $>$ 20\\%% & \\multicolumn{4}{l}{%.1f\\%%} \\\\",
          100 * frac_above20),
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines, file.path(table_dir, "balance_tests.tex"))

# ---------------------------------------------------------------------------
# 6. Save results object
# ---------------------------------------------------------------------------

balance_output <- list(
  cell_concentration = cell_concentration,
  mmf_weight         = mmf_weight_by_cell,
  balance_results    = balance_results,
  t_tests            = list(CDS = t_CDS, vol = t_vol, share = t_share)
)
saveRDS(balance_output, file.path(out_dir, "balance_test_results.rds"))

message("02_balance_tests.R complete.")
message(sprintf("  N cells: %d", nrow(cell_concentration)))
message(sprintf("  N foreign banks in balance test: %d", nrow(bank_pre_fb)))
message(sprintf("  Figures written to: %s", fig_dir))
message(sprintf("  Table written to:   %s", table_dir))
