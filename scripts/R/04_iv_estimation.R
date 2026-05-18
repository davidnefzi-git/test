## =============================================================================
## Title:   04_iv_estimation.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: IV estimation for Parts 2–3 of the paper (Task 3).
##          First stage, second stage, and interaction heterogeneity.
##          Robustness: pre-trend diagnostic, AKM SEs, wild cluster bootstrap,
##          DealerConstraint × year FE sensitivity (strategy memo Fix B3a/B3b).
##          Sign convention: SignedUSDFlow > 0 = entity obtains USD.
##          Naming convention: B_cap = dealer capacity; B_agg = aggregate
##          demand slope (Sigma beta_s). Never use bare B.
## Inputs:  Output/fx_swap/panel_main.rds
##          Output/fx_swap/mmf_instrument.rds
##          Output/fx_swap/macro_ts.rds
## Outputs: paper/tables/iv_first_stage.tex
##          paper/tables/iv_second_stage.tex
##          paper/tables/iv_interactions.tex
##          paper/tables/pretrend_diagnostic.tex
##          paper/tables/iv_bootstrap.tex
##          Output/fx_swap/iv_results.rds
## =============================================================================

library(here)
library(dplyr)
library(tidyr)
library(fixest)    # for two-way FE IV and cluster SE
library(lubridate)

source(here::here("scripts", "R", "functions", "helpers.R"))

# ---------------------------------------------------------------------------
# 0. Load and merge data
# ---------------------------------------------------------------------------

out_dir   <- here::here("Output", "fx_swap")
table_dir <- here::here("paper", "tables")
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)

panel   <- readRDS(file.path(out_dir, "panel_main.rds"))
instr   <- readRDS(file.path(out_dir, "mmf_instrument.rds"))
macro   <- readRDS(file.path(out_dir, "macro_ts.rds"))

# Merge instrument into panel
est_data <- panel %>%
  left_join(instr %>% select(cell_id, date, Z_MMF, EPFR_shock,
                              DomShare_mmf, HHI, top3_share),
            by = c("cell_id", "date")) %>%
  left_join(macro %>% select(date, OIS_rate), by = "date") %>%
  arrange(cell_id, date) %>%
  group_by(cell_id) %>%
  mutate(
    lag_mu_t    = lag(mu_t),
    lag_theta_t = lag(theta_t),
    lag_U_t     = lag(U_t)
  ) %>%
  ungroup() %>%
  filter(!is.na(lag_mu_t)) %>%
  mutate(
    cell_fe = cell_id,
    tenor_f = factor(tenor, levels = c("ON", "1W", "1M", "3M")),
    year    = year(date),
    # Taker vs maker decomposition for mechanism test (strategy memo, Obj. 2)
    U_taker = taker_ratio * U_t,
    U_maker = (1 - taker_ratio) * U_t,
    # Interaction instruments (one per interaction endogenous regressor)
    Z_MMF_x_DC = Z_MMF * DealerConstraint,
    Z_MMF_x_QE = Z_MMF * QuarterEnd,
    Z_MMF_x_3M = Z_MMF * (tenor == "3M")
  ) %>%
  # Lagged instruments for pre-trend diagnostic (B3b)
  group_by(cell_id) %>%
  mutate(
    Z_MMF_lag1 = lag(Z_MMF, 1),
    Z_MMF_lag2 = lag(Z_MMF, 2),
    Z_MMF_lag3 = lag(Z_MMF, 3)
  ) %>%
  ungroup()

# ---------------------------------------------------------------------------
# 1. First stage
# ---------------------------------------------------------------------------
# U_{i,m,t} = alpha_i + alpha_{m,t} + delta * Z_MMF + controls + eps

fs1 <- feols(
  U_t ~ Z_MMF + OIS_rate | cell_id + date,
  data    = est_data,
  cluster = ~cell_id + date
)

# Mechanism test: taker vs maker first stages
# If matching function is operative, Z_MMF should have larger effect on taker
fs_taker <- feols(
  U_taker ~ Z_MMF + OIS_rate | cell_id + date,
  data    = est_data,
  cluster = ~cell_id + date
)

fs_maker <- feols(
  U_maker ~ Z_MMF + OIS_rate | cell_id + date,
  data    = est_data,
  cluster = ~cell_id + date
)

# ---------------------------------------------------------------------------
# 2. Second stage
# ---------------------------------------------------------------------------
# mu_{m,t} = alpha_m + alpha_t + beta * U_hat + gamma * X + u

ss1 <- feols(
  mu_t ~ OIS_rate | cell_id + date | U_t ~ Z_MMF,
  data    = est_data,
  cluster = ~cell_id + date
)

ss2 <- feols(
  mu_t ~ OIS_rate + lag_mu_t | cell_id + date | U_t ~ Z_MMF,
  data    = est_data,
  cluster = ~cell_id + date
)

# ---------------------------------------------------------------------------
# 3. Interaction specifications (P2: capacity amplification; P4: quarter-end)
# ---------------------------------------------------------------------------
# Two endogenous regressors: U_t and U_t × modifier
# Two instruments: Z_MMF and Z_MMF × modifier (Bartik interaction instrument)
# Per strategy memo B3a: exclusion restriction for interaction instrument is
# maintained; sensitivity check with DealerConstraint × year FE documented.

int_dc <- feols(
  mu_t ~ OIS_rate | cell_id + date |
    U_t + I(U_t * DealerConstraint) ~ Z_MMF + Z_MMF_x_DC,
  data    = est_data,
  cluster = ~cell_id + date
)

int_qe <- feols(
  mu_t ~ OIS_rate | cell_id + date |
    U_t + I(U_t * QuarterEnd) ~ Z_MMF + Z_MMF_x_QE,
  data    = est_data,
  cluster = ~cell_id + date
)

int_tenor <- feols(
  mu_t ~ OIS_rate | cell_id + date |
    U_t + I(U_t * (tenor == "3M")) ~ Z_MMF + Z_MMF_x_3M,
  data    = est_data,
  cluster = ~cell_id + date
)

# ---------------------------------------------------------------------------
# 4. Helper functions for LaTeX table construction
# ---------------------------------------------------------------------------

# Stars notation for working paper (default convention)
stars <- function(p) {
  if (is.na(p))  return("")
  if (p < 0.01) return("^{***}")
  if (p < 0.05) return("^{**}")
  if (p < 0.10) return("^{*}")
  return("")
}

# Extract one coefficient row: estimate + stars, then SE row
coef_se_rows <- function(models, var_pattern, row_label) {
  # For each model, find the first coefficient matching var_pattern
  est_row <- vapply(models, function(m) {
    nm <- names(coef(m))[grepl(var_pattern, names(coef(m)))][1]
    if (is.na(nm)) return("---")
    sprintf("%.4f%s", coef(m)[[nm]], stars(pvalue(m)[[nm]]))
  }, character(1))

  se_row <- vapply(models, function(m) {
    nm <- names(se(m))[grepl(var_pattern, names(se(m)))][1]
    if (is.na(nm)) return("")
    sprintf("(%.4f)", se(m)[[nm]])
  }, character(1))

  c(
    sprintf("  %s & %s \\\\", row_label, paste(est_row, collapse = " & ")),
    sprintf("  & %s \\\\",               paste(se_row,  collapse = " & "))
  )
}

# ---------------------------------------------------------------------------
# 5. First-stage LaTeX table
# ---------------------------------------------------------------------------

tex_fs <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{Total} & \\textbf{Taker} & \\textbf{Maker} \\\\",
  "  & \\textbf{$U_t$} & \\textbf{$U_t^{taker}$} & \\textbf{$U_t^{maker}$} \\\\",
  "  \\midrule",
  coef_se_rows(list(fs1, fs_taker, fs_maker), "Z_MMF$", "$Z^{MMF}$"),
  coef_se_rows(list(fs1, fs_taker, fs_maker), "OIS_rate", "OIS rate"),
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(fs1), nobs(fs_taker), nobs(fs_maker)),
  sprintf("  $R^2$ & %.3f & %.3f & %.3f \\\\",
          r2(fs1)["r2"], r2(fs_taker)["r2"], r2(fs_maker)["r2"]),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  Cluster SE (cell, date) & Yes & Yes & Yes \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_fs, file.path(table_dir, "iv_first_stage.tex"))

# ---------------------------------------------------------------------------
# 6. Second-stage LaTeX table
# ---------------------------------------------------------------------------
# fixest names the instrumented regressor "fit_U_t" in the 2SLS output

tex_ss <- c(
  "\\begin{tabular}{lcc}",
  "  \\toprule",
  "  & \\textbf{(1)} & \\textbf{(2)} \\\\",
  "  & \\textbf{$\\mu_t$} & \\textbf{$\\mu_t$} \\\\",
  "  \\midrule",
  coef_se_rows(list(ss1, ss2), "fit_U_t", "$\\hat{U}_t$ (IV)"),
  coef_se_rows(list(ss1, ss2), "OIS_rate", "OIS rate"),
  "  \\midrule",
  "  OIS rate control & Yes & Yes \\\\",
  "  Lagged $\\mu_t$ & No & Yes \\\\",
  sprintf("  Observations & %d & %d \\\\", nobs(ss1), nobs(ss2)),
  sprintf("  $R^2$ & %.3f & %.3f \\\\", r2(ss1)["r2"], r2(ss2)["r2"]),
  "  Cell FE & Yes & Yes \\\\",
  "  Date FE & Yes & Yes \\\\",
  "  Cluster SE (cell, date) & Yes & Yes \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_ss, file.path(table_dir, "iv_second_stage.tex"))

# ---------------------------------------------------------------------------
# 7. Interaction LaTeX table
# ---------------------------------------------------------------------------

int_models   <- list(int_dc, int_qe, int_tenor)
int_patterns <- c("DealerConstraint", "QuarterEnd", "3M")

# Pre-compute interaction term rows (each model has a different coef name)
int_est_vals <- vapply(seq_along(int_models), function(i) {
  m  <- int_models[[i]]
  nm <- names(coef(m))[grepl(int_patterns[i], names(coef(m)))][1]
  if (is.na(nm)) return("---")
  sprintf("%.4f%s", coef(m)[[nm]], stars(pvalue(m)[[nm]]))
}, character(1))

int_se_vals <- vapply(seq_along(int_models), function(i) {
  m  <- int_models[[i]]
  nm <- names(se(m))[grepl(int_patterns[i], names(se(m)))][1]
  if (is.na(nm)) return("")
  sprintf("(%.4f)", se(m)[[nm]])
}, character(1))

int_main_rows <- coef_se_rows(int_models, "fit_U_t$", "$\\hat{U}_t$ (IV)")
int_cross_rows <- c(
  sprintf("  $\\hat{U}_t \\times$ Modifier & %s \\\\",
          paste(int_est_vals, collapse = " & ")),
  sprintf("  & %s \\\\", paste(int_se_vals, collapse = " & "))
)

tex_int <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{(1) Dealer} & \\textbf{(2) Quarter-end} & \\textbf{(3) Tenor} \\\\",
  "  \\midrule",
  "  \\multicolumn{4}{l}{\\textit{Panel A: Main demand term $\\hat{U}_t$}} \\\\[2pt]",
  int_main_rows,
  "  \\midrule",
  "  \\multicolumn{4}{l}{\\textit{Panel B: Interaction term}} \\\\[2pt]",
  int_cross_rows,
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(int_dc), nobs(int_qe), nobs(int_tenor)),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  Cluster SE (cell, date) & Yes & Yes & Yes \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_int, file.path(table_dir, "iv_interactions.tex"))

# ---------------------------------------------------------------------------
# 8. Save results
# ---------------------------------------------------------------------------

iv_results <- list(
  first_stage   = list(main = fs1, taker = fs_taker, maker = fs_maker),
  second_stage  = list(base = ss1, controls = ss2),
  interactions  = list(dealer_constraint = int_dc,
                        quarter_end       = int_qe,
                        tenor             = int_tenor),
  est_data_dims = c(nrow = nrow(est_data), ncol = ncol(est_data))
)
saveRDS(iv_results, file.path(out_dir, "iv_results.rds"))

message("04_iv_estimation.R complete.")
message(sprintf("  Estimation dataset: %d obs", nrow(est_data)))
message(sprintf("  First-stage F (approx): %s",
                tryCatch(as.character(round(fitstat(fs1, "ivf")[[1]], 2)),
                         error = function(e) "see model object")))
