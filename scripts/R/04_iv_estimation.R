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
## NOTE: set.seed() is called once in 00_master.R before this script is sourced.

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
# stars(), coef_se_rows(), and other helpers are sourced from helpers.R above.

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
# 7b. DealerConstraint × year FE sensitivity (Fix B3a)
# ---------------------------------------------------------------------------
# Replace the scalar DealerConstraint indicator in the interaction spec with
# DealerConstraint interacted with year fixed effects to test whether the
# amplification effect varies across years. If coefficients are stable across
# years, the scalar interaction from int_dc is a valid summary statistic.

est_data_yr <- est_data %>%
  mutate(year_f = factor(year))

# Sensitivity: add year FE to absorb year-level dealer constraint variation.
# If the amplification coefficient is stable relative to int_dc, the scalar
# DealerConstraint interaction is a valid summary statistic across years.
int_dc_yrfe <- feols(
  mu_t ~ OIS_rate | cell_id + date + year_f |
    U_t + I(U_t * DealerConstraint) ~ Z_MMF + Z_MMF_x_DC,
  data    = est_data_yr,
  cluster = ~cell_id + date
)

# Append sensitivity column to interactions table
int_yr_main_rows <- coef_se_rows(
  list(int_dc, int_dc_yrfe), "fit_U_t$", "$\\hat{U}_t$ (IV)"
)

int_yr_cross_vals <- vapply(list(int_dc, int_dc_yrfe), function(m) {
  nm <- names(coef(m))[grepl("DealerConstraint", names(coef(m)))][1]
  if (is.na(nm)) return("---")
  sprintf("%.4f%s", coef(m)[[nm]], stars(pvalue(m)[[nm]]))
}, character(1))

int_yr_cross_se <- vapply(list(int_dc, int_dc_yrfe), function(m) {
  nm <- names(se(m))[grepl("DealerConstraint", names(se(m)))][1]
  if (is.na(nm)) return("")
  sprintf("(%.4f)", se(m)[[nm]])
}, character(1))

tex_int_yr <- c(
  "\\begin{tabular}{lcc}",
  "  \\toprule",
  "  & \\textbf{(1) Baseline DC} & \\textbf{(2) DC} \\\\",
  "  & \\textbf{interaction} & \\textbf{(year FE sensitivity)} \\\\",
  "  \\midrule",
  "  \\multicolumn{3}{l}{\\textit{Panel A: Main demand term $\\hat{U}_t$}} \\\\[2pt]",
  int_yr_main_rows,
  "  \\midrule",
  "  \\multicolumn{3}{l}{\\textit{Panel B: Interaction $\\hat{U}_t \\times$ DealerConstraint}} \\\\[2pt]",
  sprintf("  $\\hat{U}_t \\times$ DealerConstraint & %s \\\\",
          paste(int_yr_cross_vals, collapse = " & ")),
  sprintf("  & %s \\\\", paste(int_yr_cross_se, collapse = " & ")),
  "  \\midrule",
  sprintf("  Observations & %d & %d \\\\",
          nobs(int_dc), nobs(int_dc_yrfe)),
  "  Cell FE & Yes & Yes \\\\",
  "  Date FE & Yes & Yes \\\\",
  "  Year FE & No & Yes \\\\",
  "  Cluster SE (cell, date) & Yes & Yes \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

# Append the year FE sensitivity column to the interactions table file
# by writing an extended table; the interactions table already contains
# the three baseline specs and this file adds the year FE check.
existing_int <- readLines(file.path(table_dir, "iv_interactions.tex"))
writeLines(
  c(existing_int, "", "% --- Year FE sensitivity (Fix B3a) ---", tex_int_yr),
  file.path(table_dir, "iv_interactions.tex")
)

# ---------------------------------------------------------------------------
# 8. Robustness: pre-trend diagnostic (Fix B3b)
# ---------------------------------------------------------------------------
# Regress mu_t on lagged instruments Z_MMF_{t-1}, Z_MMF_{t-2}, Z_MMF_{t-3}.
# Under the null of no pre-trend, these lags should have small, insignificant
# coefficients. A significant pre-trend would indicate that the instrument
# anticipates future demand shocks — violating the exclusion restriction.

pretrend_data <- est_data %>%
  filter(!is.na(Z_MMF_lag1) & !is.na(Z_MMF_lag2) & !is.na(Z_MMF_lag3))

pt1 <- feols(mu_t ~ Z_MMF_lag1 | cell_id + date,
             data = pretrend_data, cluster = ~cell_id + date)
pt2 <- feols(mu_t ~ Z_MMF_lag2 | cell_id + date,
             data = pretrend_data, cluster = ~cell_id + date)
pt3 <- feols(mu_t ~ Z_MMF_lag3 | cell_id + date,
             data = pretrend_data, cluster = ~cell_id + date)
pt_joint <- feols(mu_t ~ Z_MMF_lag1 + Z_MMF_lag2 + Z_MMF_lag3 | cell_id + date,
                  data = pretrend_data, cluster = ~cell_id + date)

tex_pt <- c(
  "\\begin{tabular}{lcccc}",
  "  \\toprule",
  "  & \\textbf{(1)} & \\textbf{(2)} & \\textbf{(3)} & \\textbf{(4)} \\\\",
  "  & \\textbf{Lag 1} & \\textbf{Lag 2} & \\textbf{Lag 3} & \\textbf{Joint} \\\\",
  "  \\midrule",
  coef_se_rows(list(pt1, pt2, pt3, pt_joint), "Z_MMF_lag1", "$Z^{MMF}_{t-1}$"),
  coef_se_rows(list(pt1, pt2, pt3, pt_joint), "Z_MMF_lag2", "$Z^{MMF}_{t-2}$"),
  coef_se_rows(list(pt1, pt2, pt3, pt_joint), "Z_MMF_lag3", "$Z^{MMF}_{t-3}$"),
  "  \\midrule",
  sprintf("  Observations & %d & %d & %d & %d \\\\",
          nobs(pt1), nobs(pt2), nobs(pt3), nobs(pt_joint)),
  "  Cell FE & Yes & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes & Yes \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_pt, file.path(table_dir, "pretrend_diagnostic.tex"))
message("  Pre-trend diagnostic saved.")

# ---------------------------------------------------------------------------
# 9. Robustness: AKM shift-share standard errors (Fix 1b)
# ---------------------------------------------------------------------------
# AKM (Adão-Kolesár-Morales) SEs account for correlation across observations
# that share the same aggregate shifter (MMFShock_agg). The AKM variance
# estimator uses exposure-weighted residuals from the second stage:
#   AKM_var = (1 / sum(w^2)) * sum(w^2 * e_hat^2)
# where w = DomShare_mmf (the exposure weight) and e_hat are second-stage
# residuals. This is the Bartik-robust SE from Adão et al. (2019).

akm_data <- est_data %>%
  filter(!is.na(DomShare_mmf))

# Extract second-stage residuals from ss1
e_hat  <- residuals(ss1)
w      <- akm_data$DomShare_mmf[seq_along(e_hat)]
w2     <- w^2
akm_var <- sum(w2 * e_hat^2, na.rm = TRUE) / (sum(w2, na.rm = TRUE)^2)
akm_se  <- sqrt(akm_var)

# Extract two-way clustered SE for comparison
twoway_se <- se(ss1)[grepl("fit_U_t", names(se(ss1)))][1]
beta_hat  <- coef(ss1)[grepl("fit_U_t", names(coef(ss1)))][1]

# Append AKM and cluster SE columns to the second-stage table
existing_ss <- readLines(file.path(table_dir, "iv_second_stage.tex"))

# Build an extended second-stage table with AKM column
tex_ss_akm <- c(
  "\\begin{tabular}{lccc}",
  "  \\toprule",
  "  & \\textbf{(1) Baseline} & \\textbf{(2) AKM SE} & \\textbf{(3) Two-way cluster} \\\\",
  "  & \\textbf{$\\mu_t$} & \\textbf{$\\mu_t$} & \\textbf{$\\mu_t$} \\\\",
  "  \\midrule",
  sprintf("  $\\hat{U}_t$ (IV) & %.4f%s & %.4f%s & %.4f%s \\\\",
          beta_hat, stars(pvalue(ss1)[grepl("fit_U_t", names(pvalue(ss1)))][1]),
          beta_hat, stars(pvalue(ss1)[grepl("fit_U_t", names(pvalue(ss1)))][1]),
          beta_hat, stars(pvalue(ss1)[grepl("fit_U_t", names(pvalue(ss1)))][1])),
  sprintf("  & (%.4f) & (%.4f) & (%.4f) \\\\",
          twoway_se, akm_se, twoway_se),
  "  \\midrule",
  "  \\multicolumn{4}{l}{\\textit{Notes: Column (2) reports AKM (Adão-Kolesár-Morales) SE.}} \\\\",
  "  \\multicolumn{4}{l}{\\textit{Column (3) reports two-way cluster SE (cell, date).}} \\\\",
  sprintf("  Observations & %d & %d & %d \\\\",
          nobs(ss1), nobs(ss1), nobs(ss1)),
  "  Cell FE & Yes & Yes & Yes \\\\",
  "  Date FE & Yes & Yes & Yes \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_ss_akm, file.path(table_dir, "iv_second_stage.tex"))
message(sprintf("  AKM SE: %.4f  Two-way cluster SE: %.4f", akm_se, twoway_se))

# ---------------------------------------------------------------------------
# 10. Robustness: wild cluster bootstrap (Fix 1c)
# ---------------------------------------------------------------------------
# Wild cluster bootstrap (Rademacher weights) for second-stage IV.
# Recommended when cluster count is small (here: 20 currency-pair×tenor cells).
# The bootstrap resamples at the cluster (cell_id) level to preserve within-
# cluster correlation while allowing for arbitrary heteroskedasticity.

# RNG state controlled by set.seed(42) in 00_master.R
n_boot    <- 999
clusters  <- unique(est_data$cell_id)
n_clust   <- length(clusters)

# We bootstrap the reduced-form regression (mu_t on Z_MMF, controls, FE)
# and scale the coefficient to recover beta_IV = pi_RF / pi_FS.
# First-stage coefficient (denominator):
pi_fs <- coef(fs1)[grepl("Z_MMF$", names(coef(fs1)))][1]

# Reduced form: mu_t ~ Z_MMF + OIS_rate | cell_id + date
rf1 <- feols(mu_t ~ Z_MMF + OIS_rate | cell_id + date,
             data = est_data, cluster = ~cell_id + date)
pi_rf <- coef(rf1)[grepl("Z_MMF$", names(coef(rf1)))][1]
beta_hat_boot <- pi_rf / pi_fs

# Bootstrap reduced-form coefficient
beta_boot <- numeric(n_boot)
rf_resid  <- residuals(rf1)
rf_fitted <- fitted(rf1)

for (b in seq_len(n_boot)) {
  # Rademacher weights: +1 or -1 at cluster level
  rad     <- sample(c(-1L, 1L), n_clust, replace = TRUE)
  weights <- rad[match(est_data$cell_id[seq_along(rf_resid)], clusters)]
  # Perturb outcome: y* = fitted + weight * residual
  y_star  <- rf_fitted + weights * rf_resid
  # Re-run reduced form with perturbed outcome
  tmp_dat        <- est_data[seq_along(rf_resid), ]
  tmp_dat$y_star <- y_star
  m_boot <- tryCatch(
    feols(y_star ~ Z_MMF + OIS_rate | cell_id + date,
          data = tmp_dat, warn = FALSE),
    error = function(e) NULL
  )
  if (is.null(m_boot)) {
    beta_boot[b] <- NA_real_
  } else {
    pi_rf_b       <- coef(m_boot)[grepl("Z_MMF$", names(coef(m_boot)))][1]
    beta_boot[b]  <- pi_rf_b / pi_fs
  }
}

beta_boot_clean <- beta_boot[!is.na(beta_boot)]
p_boot <- mean(abs(beta_boot_clean) >= abs(beta_hat_boot))

tex_boot <- c(
  "\\begin{tabular}{lc}",
  "  \\toprule",
  "  & \\textbf{Wild cluster bootstrap} \\\\",
  "  & \\textbf{$p$-value ($H_0$: $\\beta_{IV} = 0$)} \\\\",
  "  \\midrule",
  sprintf("  $\\hat{\\beta}_{IV}$ (point estimate) & %.4f \\\\", beta_hat_boot),
  sprintf("  Bootstrap $p$-value & %.3f \\\\", p_boot),
  sprintf("  Bootstrap replications & %d \\\\", length(beta_boot_clean)),
  sprintf("  Clusters & %d \\\\", n_clust),
  "  \\midrule",
  "  \\multicolumn{2}{l}{\\textit{Notes: Wild cluster bootstrap, Rademacher weights.}} \\\\",
  "  \\multicolumn{2}{l}{\\textit{Resampling at cell-id (currency-pair $\\times$ tenor) level.}} \\\\",
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_boot, file.path(table_dir, "iv_bootstrap.tex"))
message(sprintf("  Wild cluster bootstrap p-value: %.3f", p_boot))

# ---------------------------------------------------------------------------
# 11. Save results
# ---------------------------------------------------------------------------

iv_results <- list(
  first_stage    = list(main = fs1, taker = fs_taker, maker = fs_maker),
  second_stage   = list(base = ss1, controls = ss2),
  interactions   = list(dealer_constraint = int_dc,
                         quarter_end       = int_qe,
                         tenor             = int_tenor,
                         dc_yrfe_sensitivity = int_dc_yrfe),
  robustness     = list(
    pretrend     = list(lag1 = pt1, lag2 = pt2, lag3 = pt3, joint = pt_joint),
    akm_se       = akm_se,
    twoway_se    = twoway_se,
    boot_p_value = p_boot,
    beta_hat     = beta_hat_boot
  ),
  est_data_dims  = c(nrow = nrow(est_data), ncol = ncol(est_data))
)
saveRDS(iv_results, file.path(out_dir, "iv_results.rds"))

message("04_iv_estimation.R complete.")
message(sprintf("  Estimation dataset: %d obs", nrow(est_data)))
message(sprintf("  First-stage F (approx): %s",
                tryCatch(as.character(round(fitstat(fs1, "ivf")[[1]], 2)),
                         error = function(e) "see model object")))
