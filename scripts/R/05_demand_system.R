## =============================================================================
## Title:   05_demand_system.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: Demand system estimation (Task 4 — structural extension).
##          Estimates sector-specific price sensitivities beta_s and verifies
##          the maintained hypothesis B_agg = Sigma(beta_s) < 0 (downward-
##          sloping aggregate demand). Per strategy memo, this is Part 4 of
##          the paper ("extension structurelle"), not a main result.
##          NOTE: No threshold specification. P3 convexity is theoretical only
##          per the firm editorial decision stated in the task brief.
## Inputs:  Output/fx_swap/panel_main.rds
##          Output/fx_swap/mmf_instrument.rds
## Outputs: paper/tables/demand_system.tex
##          Output/fx_swap/demand_system_results.rds
## =============================================================================

library(here)
library(dplyr)
library(tidyr)
library(fixest)

source(here::here("scripts", "R", "functions", "helpers.R"))

# ---------------------------------------------------------------------------
# 0. Load data
# ---------------------------------------------------------------------------

out_dir   <- here::here("Output", "fx_swap")
table_dir <- here::here("paper", "tables")
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)

panel <- readRDS(file.path(out_dir, "panel_main.rds"))
instr <- readRDS(file.path(out_dir, "mmf_instrument.rds"))

# ---------------------------------------------------------------------------
# 1. Construct sector-level demand variables
# ---------------------------------------------------------------------------
# From the panel, SignedUSDFlow_s gives sector s's net USD demand.
# We estimate a linearized demand system per equation (9.2) in the theory:
#   q_{i,m,t} = Sigma_s beta_s * mu_{s,t} + FE + eps
# where q_{i,m,t} is the taker ratio proxy for matching quality,
# and mu_{s,t} is the sector-level funding spread.
#
# In the linearized form from the design, the structural equation is:
#   Q_{s,m,t} = alpha_{s,m} + beta_s * mu_{m,t} + gamma_s * Z_s + eps
#
# We estimate beta_s for s = {ForeignBank, Dealer, HedgeFund, AssetManager}
# using sector-specific instruments:
#   - Z^MMF     -> Foreign bank demand shifter
#   - Z^EPFR    -> Asset manager demand shifter
# The cross-equation exclusion restrictions follow strategy memo Section 5.

ds_data <- panel %>%
  left_join(instr %>% select(cell_id, date, Z_MMF, EPFR_shock),
            by = c("cell_id", "date")) %>%
  select(cell_id, date, currency_pair, tenor,
         mu_t, taker_ratio, q_t, theta_t,
         SignedUSDFlow_FB, SignedUSDFlow_DLR,
         SignedUSDFlow_HF, SignedUSDFlow_AM,
         Z_MMF, EPFR_shock,
         DealerConstraint, QuarterEnd, stress_regime) %>%
  filter(!is.na(Z_MMF))

# ---------------------------------------------------------------------------
# 2. DS1 baseline: separate OLS for each sector's demand
# ---------------------------------------------------------------------------
# Q_{s,m,t} = alpha_{cell} + alpha_{date} + beta_s * mu_{m,t} + eps

ols_fb  <- feols(SignedUSDFlow_FB  ~ mu_t | cell_id + date, data = ds_data,
                 cluster = ~cell_id + date)
ols_dlr <- feols(SignedUSDFlow_DLR ~ mu_t | cell_id + date, data = ds_data,
                 cluster = ~cell_id + date)
ols_hf  <- feols(SignedUSDFlow_HF  ~ mu_t | cell_id + date, data = ds_data,
                 cluster = ~cell_id + date)
ols_am  <- feols(SignedUSDFlow_AM  ~ mu_t | cell_id + date, data = ds_data,
                 cluster = ~cell_id + date)

# Aggregate demand slope: B_agg = beta_FB + beta_DLR + beta_HF + beta_AM
# Theory prediction: B_agg < 0 (downward-sloping)
betas_ols <- c(
  beta_FB  = coef(ols_fb)["mu_t"],
  beta_DLR = coef(ols_dlr)["mu_t"],
  beta_HF  = coef(ols_hf)["mu_t"],
  beta_AM  = coef(ols_am)["mu_t"]
)
B_agg_ols <- sum(betas_ols)
message(sprintf("  B_agg (OLS, Sigma beta_s): %.4f  [Theory: < 0]", B_agg_ols))
message(sprintf("  Maintained hypothesis B_agg < 0: %s",
                ifelse(B_agg_ols < 0, "SUPPORTED", "REJECTED")))

# ---------------------------------------------------------------------------
# 3. DS2 IV estimation: instrument sector-specific demand with sector instruments
# ---------------------------------------------------------------------------
# Foreign bank: Z_MMF (shift-share instrument)
# Asset manager: EPFR_shock
# Dealer & HF: use Z_MMF and EPFR_shock as instruments (cross-exclusion caveat
# acknowledged per strategy memo Task 4, Objection 4 response)

iv_fb  <- feols(SignedUSDFlow_FB ~ 1 | cell_id + date |
                  mu_t ~ Z_MMF,
                data = ds_data, cluster = ~cell_id + date)

iv_dlr <- feols(SignedUSDFlow_DLR ~ 1 | cell_id + date |
                  mu_t ~ Z_MMF + EPFR_shock,
                data = ds_data, cluster = ~cell_id + date)

iv_hf  <- feols(SignedUSDFlow_HF ~ 1 | cell_id + date |
                  mu_t ~ Z_MMF + EPFR_shock,
                data = ds_data, cluster = ~cell_id + date)

iv_am  <- feols(SignedUSDFlow_AM ~ 1 | cell_id + date |
                  mu_t ~ EPFR_shock,
                data = ds_data, cluster = ~cell_id + date)

# Extract IV betas — get_iv_beta() is defined in helpers.R

betas_iv <- c(
  beta_FB_iv  = get_iv_beta(iv_fb),
  beta_DLR_iv = get_iv_beta(iv_dlr),
  beta_HF_iv  = get_iv_beta(iv_hf),
  beta_AM_iv  = get_iv_beta(iv_am)
)
B_agg_iv <- sum(betas_iv, na.rm = TRUE)
message(sprintf("  B_agg (IV, Sigma beta_s): %.4f  [Theory: < 0]", B_agg_iv))
message(sprintf("  Maintained hypothesis B_agg < 0 (IV): %s",
                ifelse(B_agg_iv < 0, "SUPPORTED", "REJECTED")))

# ---------------------------------------------------------------------------
# 4. Taker ratio (q_t) equation: matching quality as function of spreads
# ---------------------------------------------------------------------------
# q_{m,t} = alpha_{cell} + alpha_t + Sigma_s beta_s * SignedUSDFlow_{s,m,t} + eps

qt_ols <- feols(
  taker_ratio ~ SignedUSDFlow_FB + SignedUSDFlow_DLR +
                SignedUSDFlow_HF + SignedUSDFlow_AM |
                cell_id + date,
  data    = ds_data,
  cluster = ~cell_id + date
)

# IV version: instrument sector flows with sector-specific instruments
qt_iv <- feols(
  taker_ratio ~ 1 | cell_id + date |
    SignedUSDFlow_FB ~ Z_MMF,
  data    = ds_data,
  cluster = ~cell_id + date
)

# ---------------------------------------------------------------------------
# 5. LaTeX table
# ---------------------------------------------------------------------------
# stars(), fmt_coef_se(), and other helpers are sourced from helpers.R above.

# Construct the table
models  <- list(ols_fb, ols_dlr, ols_hf, ols_am, iv_fb, iv_dlr, iv_hf, iv_am)
sectors <- rep(c("FB", "Dealer", "HF", "AM"), 2)
types   <- c(rep("OLS", 4), rep("IV", 4))

beta_mu_row <- vapply(models, function(m) {
  nm <- names(coef(m))[grepl("fit_mu_t|mu_t", names(coef(m)))][1]
  if (is.na(nm)) return("---")
  b  <- coef(m)[[nm]]
  pv <- pvalue(m)[[nm]]
  sprintf("%.4f%s", b, stars(pv))
}, character(1))

se_mu_row <- vapply(models, function(m) {
  nm <- names(coef(m))[grepl("fit_mu_t|mu_t", names(coef(m)))][1]
  if (is.na(nm)) return("")
  sprintf("(%.4f)", se(m)[[nm]])
}, character(1))

nobs_row <- vapply(models, nobs, integer(1))
r2_row   <- vapply(models, function(m) r2(m)["r2"], numeric(1))

tex_ds <- c(
  "\\begin{tabular}{lcccccccc}",
  "  \\toprule",
  "  & \\multicolumn{4}{c}{\\textbf{OLS}} & \\multicolumn{4}{c}{\\textbf{IV}} \\\\",
  "  \\cmidrule(lr){2-5}\\cmidrule(lr){6-9}",
  paste0("  & \\textbf{FB} & \\textbf{Dealer} & \\textbf{HF} & \\textbf{AM}",
         " & \\textbf{FB} & \\textbf{Dealer} & \\textbf{HF} & \\textbf{AM} \\\\"),
  "  \\midrule",
  sprintf("  $\\hat{\\mu}_t$ & %s \\\\",
          paste(beta_mu_row, collapse = " & ")),
  sprintf("  & %s \\\\",
          paste(se_mu_row,   collapse = " & ")),
  "  \\midrule",
  sprintf("  Observations & %s \\\\",
          paste(format(nobs_row, big.mark = ","), collapse = " & ")),
  sprintf("  $R^2$ & %s \\\\",
          paste(sprintf("%.3f", r2_row), collapse = " & ")),
  "  Cell FE & \\multicolumn{8}{c}{Yes} \\\\",
  "  Date FE & \\multicolumn{8}{c}{Yes} \\\\",
  "  \\midrule",
  sprintf("  $\\mathcal{B}_{agg}$ (OLS) $= \\sum_s \\hat\\beta_s$ & \\multicolumn{4}{l}{%.4f} & \\multicolumn{4}{l}{} \\\\",
          B_agg_ols),
  sprintf("  $\\mathcal{B}_{agg}$ (IV) $= \\sum_s \\hat\\beta_s$ & \\multicolumn{4}{l}{} & \\multicolumn{4}{l}{%.4f} \\\\",
          B_agg_iv),
  sprintf("  Maintained hypothesis $\\mathcal{B}_{agg} < 0$ & \\multicolumn{4}{l}{%s} & \\multicolumn{4}{l}{%s} \\\\",
          ifelse(B_agg_ols < 0, "\\checkmark", "$\\times$"),
          ifelse(B_agg_iv  < 0, "\\checkmark", "$\\times$")),
  "  \\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_ds, file.path(table_dir, "demand_system.tex"))

# ---------------------------------------------------------------------------
# 6. Save results
# ---------------------------------------------------------------------------

ds_results <- list(
  ols_models   = list(fb = ols_fb, dlr = ols_dlr, hf = ols_hf, am = ols_am),
  iv_models    = list(fb = iv_fb,  dlr = iv_dlr,  hf = iv_hf,  am = iv_am),
  qt_models    = list(ols = qt_ols, iv = qt_iv),
  betas_ols    = betas_ols,
  betas_iv     = betas_iv,
  B_agg_ols    = B_agg_ols,
  B_agg_iv     = B_agg_iv,
  B_agg_below0 = list(ols = B_agg_ols < 0, iv = B_agg_iv < 0)
)
saveRDS(ds_results, file.path(out_dir, "demand_system_results.rds"))

message("05_demand_system.R complete.")
message(sprintf("  B_agg (OLS): %.4f  B_agg (IV): %.4f", B_agg_ols, B_agg_iv))
