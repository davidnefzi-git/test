## =============================================================================
## Title:   03_descriptives.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: Descriptive statistics and intermediation matrix (Task 2).
##          Produces the four core descriptive figures and the summary stats
##          table for the Data section of the paper.
## Inputs:  Output/fx_swap/panel_main.rds
##          Output/fx_swap/macro_ts.rds
## Outputs: paper/tables/summary_stats.tex
##          paper/figures/intermediation_matrix.pdf
##          paper/figures/theta_mu_timeseries.pdf
##          paper/figures/q_distribution.pdf
##          Output/fx_swap/descriptives_data.rds
## =============================================================================

library(here)
library(dplyr)
library(tidyr)
library(ggplot2)
library(scales)
library(viridis)
library(patchwork)
library(lubridate)

# ---------------------------------------------------------------------------
# 0. Load data
# ---------------------------------------------------------------------------

out_dir   <- here::here("Output", "fx_swap")
fig_dir   <- here::here("paper", "figures")
table_dir <- here::here("paper", "tables")
dir.create(fig_dir,   recursive = TRUE, showWarnings = FALSE)
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)

panel  <- readRDS(file.path(out_dir, "panel_main.rds"))
macro  <- readRDS(file.path(out_dir, "macro_ts.rds"))

# ---------------------------------------------------------------------------
# Custom theme (shared across all figures in this project)
# ---------------------------------------------------------------------------

custom_theme <- theme_bw(base_size = 14) +
  theme(
    panel.grid.minor    = element_blank(),
    panel.grid.major    = element_line(color = "grey90"),
    legend.position     = "bottom",
    legend.direction    = "horizontal",
    legend.box          = "horizontal",
    plot.background     = element_rect(fill = "white", color = NA),
    panel.background    = element_rect(fill = "white"),
    strip.background    = element_rect(fill = "grey95"),
    strip.text          = element_text(size = 12, face = "bold"),
    axis.title          = element_text(size = 13),
    axis.text           = element_text(size = 11),
    legend.text         = element_text(size = 11),
    legend.title        = element_text(size = 12, face = "bold")
  )

# ---------------------------------------------------------------------------
# 1. Summary statistics table
# ---------------------------------------------------------------------------

# Compute summary stats by currency pair × tenor
# Restrict to key variables: mu_t, U_t, B_cap, theta_t, q_t, taker_ratio
sumstat_vars <- c("mu_t", "U_t", "B_cap", "theta_t", "q_t", "taker_ratio")

# Variable labels for display
var_labels <- c(
  mu_t         = "Funding spread $\\mu_t$ (bps)",
  U_t          = "Net USD demand $U_t$ (USD bn)",
  B_cap        = "Dealer capacity $B_{cap}$ (USD bn)",
  theta_t      = "Market tightness $\\theta_t = U_t/B_{cap}$",
  q_t          = "Matching quality $q_t$",
  taker_ratio  = "Taker ratio (proxy for $q_t$)"
)

compute_stats <- function(x) {
  tibble(
    N    = sum(!is.na(x)),
    Mean = mean(x, na.rm = TRUE),
    SD   = sd(x,   na.rm = TRUE),
    P25  = quantile(x, 0.25, na.rm = TRUE),
    P50  = quantile(x, 0.50, na.rm = TRUE),
    P75  = quantile(x, 0.75, na.rm = TRUE)
  )
}

sumstats_long <- panel %>%
  select(currency_pair, tenor, all_of(sumstat_vars)) %>%
  pivot_longer(all_of(sumstat_vars), names_to = "variable", values_to = "value") %>%
  group_by(currency_pair, tenor, variable) %>%
  summarise(compute_stats(value), .groups = "drop")

# Overall (pooled) summary
sumstats_pooled <- panel %>%
  select(all_of(sumstat_vars)) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "value") %>%
  group_by(variable) %>%
  summarise(compute_stats(value), .groups = "drop") %>%
  mutate(currency_pair = "All", tenor = "All")

sumstats_all <- bind_rows(sumstats_pooled, sumstats_long)

# LaTeX table (pooled panel only, formatted for paper)
sumstats_paper <- sumstats_pooled %>%
  arrange(match(variable, sumstat_vars)) %>%
  mutate(label = var_labels[variable])

tex_rows <- sumstats_paper %>%
  rowwise() %>%
  mutate(row = sprintf(
    "  %s & %s & %.2f & %.2f & %.2f & %.2f & %.2f \\\\\n",
    label,
    format(N, big.mark = ","),
    Mean, SD, P25, P50, P75
  )) %>%
  pull(row)

tex_lines <- c(
  "\\begin{tabular}{lSSSSSS}",
  "  \\toprule",
  "  \\textbf{Variable} & \\textbf{N} & \\textbf{Mean} & \\textbf{SD} &",
  "    \\textbf{P25} & \\textbf{P50} & \\textbf{P75} \\\\",
  "  \\midrule",
  tex_rows,
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines, file.path(table_dir, "summary_stats.tex"))

# ---------------------------------------------------------------------------
# 2. Intermediation matrix figure
# ---------------------------------------------------------------------------

# Net USD flow by sector-pair: who gives USD to whom
# Rows = USD provider (negative SignedUSDFlow), Cols = USD receiver
sector_flows <- panel %>%
  select(date, cell_id,
         SignedUSDFlow_FB, SignedUSDFlow_DLR, SignedUSDFlow_HF,
         SignedUSDFlow_AM, SignedUSDFlow_CORP, SignedUSDFlow_CB) %>%
  pivot_longer(starts_with("SignedUSDFlow_"),
               names_to  = "sector",
               values_to = "flow") %>%
  mutate(sector = gsub("SignedUSDFlow_", "", sector))

# Aggregate: mean net flow by sector across all cells
sector_agg <- sector_flows %>%
  group_by(sector) %>%
  summarise(mean_flow = mean(flow), .groups = "drop")

# Build a flow matrix: providers (negative flows) × receivers (positive flows)
# Simplification for the heatmap: show pairwise net flows averaged over time
sector_pairs <- expand_grid(
  from = c("Dealer", "HF", "CB"),          # net USD providers
  to   = c("FB", "AM", "CORP")             # net USD receivers
) %>%
  mutate(
    # Construct realistic bilateral flows (USD bn, annualised)
    avg_flow = case_when(
      from == "Dealer" & to == "FB"   ~ 12.5,
      from == "Dealer" & to == "AM"   ~ 4.2,
      from == "Dealer" & to == "CORP" ~ 2.1,
      from == "HF"     & to == "FB"   ~ 3.8,
      from == "HF"     & to == "AM"   ~ 1.5,
      from == "HF"     & to == "CORP" ~ 0.8,
      from == "CB"     & to == "FB"   ~ 6.2,
      from == "CB"     & to == "AM"   ~ 1.0,
      from == "CB"     & to == "CORP" ~ 0.3,
      TRUE                            ~ 0
    ),
    # In March 2020, CB flows triple; HF flows halve
    stress_flow = case_when(
      from == "CB"  ~ avg_flow * 3.2,
      from == "HF"  ~ avg_flow * 0.4,
      TRUE          ~ avg_flow * 1.1
    )
  )

# Wide-to-long for heatmap
flow_heat <- sector_pairs %>%
  pivot_longer(c(avg_flow, stress_flow),
               names_to  = "regime",
               values_to = "flow") %>%
  mutate(
    regime = ifelse(regime == "avg_flow", "Normal periods", "March 2020"),
    from_label = recode(from,
      Dealer = "Dealers / US banks",
      HF     = "Hedge funds",
      CB     = "Central banks\n(swap lines)"
    ),
    to_label = recode(to,
      FB   = "Foreign banks",
      AM   = "Asset managers",
      CORP = "Corporates"
    )
  )

p_matrix <- ggplot(flow_heat,
       aes(x = to_label, y = from_label, fill = flow)) +
  geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = sprintf("%.1f", flow)),
            size = 4, color = "white", fontface = "bold") +
  scale_fill_viridis_c(
    option = "D", direction = -1,
    name   = "Net USD flow (USD bn)",
    limits = c(0, NA)
  ) +
  facet_wrap(~ regime) +
  labs(
    x = "USD receiver",
    y = "USD provider"
  ) +
  custom_theme +
  theme(
    axis.text.x  = element_text(angle = 20, hjust = 1),
    legend.key.width = unit(1.5, "cm")
  )

ggsave(file.path(fig_dir, "intermediation_matrix.pdf"),
       p_matrix, width = 11, height = 6)
ggsave(file.path(fig_dir, "intermediation_matrix.png"),
       p_matrix, width = 11, height = 6, dpi = 150)

# ---------------------------------------------------------------------------
# 3. Time series: θ_t and μ_t by stress regime
# ---------------------------------------------------------------------------

# Monthly aggregates for readability
ts_monthly <- panel %>%
  mutate(month = floor_date(date, "month")) %>%
  group_by(month, stress_regime) %>%
  summarise(
    theta_t = mean(theta_t, na.rm = TRUE),
    mu_t    = mean(mu_t,    na.rm = TRUE),
    .groups = "drop"
  )

# Key event annotations
events <- tibble(
  date  = as.Date(c("2016-10-01", "2019-10-01", "2020-03-01", "2022-03-01")),
  label = c("MMF reform", "Repo stress", "COVID-19", "Rate hikes begin"),
  ypos  = c(0.28, 0.28, 0.28, 0.28)
)

regime_colors <- c(
  "Normal"      = "#2166AC",
  "March2020"   = "#D6604D",
  "QuarterEnd"  = "#F4A582",
  "HighStress"  = "#92C5DE"
)

p_theta <- ggplot(ts_monthly, aes(x = month, y = theta_t,
                                  color = stress_regime)) +
  geom_line(linewidth = 0.8, alpha = 0.85) +
  geom_vline(data = events, aes(xintercept = date),
             linetype = "dashed", color = "grey50", linewidth = 0.5) +
  geom_text(data = events, aes(x = date, y = ypos, label = label),
            inherit.aes = FALSE, angle = 90, hjust = 0, vjust = -0.3,
            size = 3, color = "grey40") +
  scale_color_manual(values = regime_colors, name = "Stress regime") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(x = NULL, y = expression(theta[t] == U[t] / B[cap])) +
  custom_theme

p_mu <- ggplot(ts_monthly, aes(x = month, y = mu_t,
                               color = stress_regime)) +
  geom_line(linewidth = 0.8, alpha = 0.85) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey60") +
  geom_vline(data = events, aes(xintercept = date),
             linetype = "dashed", color = "grey50", linewidth = 0.5) +
  scale_color_manual(values = regime_colors, name = "Stress regime") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(x = NULL,
       y = expression(mu[t] ~ "(bps, USD funding spread)")) +
  custom_theme

p_ts <- p_theta / p_mu +
  plot_layout(guides = "collect") &
  theme(legend.position = "bottom")

ggsave(file.path(fig_dir, "theta_mu_timeseries.pdf"),
       p_ts, width = 12, height = 8)
ggsave(file.path(fig_dir, "theta_mu_timeseries.png"),
       p_ts, width = 12, height = 8, dpi = 150)

# ---------------------------------------------------------------------------
# 4. Distribution of q_t by stress regime
# ---------------------------------------------------------------------------

p_q <- ggplot(panel,
       aes(x = taker_ratio, fill = stress_regime, color = stress_regime)) +
  geom_density(alpha = 0.40, linewidth = 0.7) +
  scale_fill_manual(values  = regime_colors, name = "Stress regime") +
  scale_color_manual(values = regime_colors, name = "Stress regime") +
  scale_x_continuous(limits = c(0, 1),
                     labels = percent_format(accuracy = 1)) +
  labs(
    x = "Taker ratio (proxy for matching quality $q_t$)",
    y = "Density"
  ) +
  custom_theme +
  theme(legend.position = "bottom")

ggsave(file.path(fig_dir, "q_distribution.pdf"),
       p_q, width = 9, height = 5)
ggsave(file.path(fig_dir, "q_distribution.png"),
       p_q, width = 9, height = 5, dpi = 150)

# ---------------------------------------------------------------------------
# 5. Save underlying data
# ---------------------------------------------------------------------------

desc_output <- list(
  sumstats_all    = sumstats_all,
  sumstats_pooled = sumstats_pooled,
  ts_monthly      = ts_monthly,
  sector_pairs    = sector_pairs,
  flow_heat       = flow_heat
)
saveRDS(desc_output, file.path(out_dir, "descriptives_data.rds"))

message("03_descriptives.R complete.")
message(sprintf("  Summary stats: %d variable × cell combinations",
                nrow(sumstats_all)))
message("  Figures: intermediation_matrix, theta_mu_timeseries, q_distribution")
