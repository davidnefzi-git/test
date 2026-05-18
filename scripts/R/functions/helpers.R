## =============================================================================
## Title:   helpers.R
## Author:  Data Engineer
## Date:    2026-05-18
## Purpose: Shared helper functions for the FX swap paper analysis pipeline.
##          Sourced by 04_iv_estimation.R and 05_demand_system.R to avoid
##          copy-paste duplication (INV-15 compliance: all shared utilities
##          live in one place).
## Inputs:  (none — pure function definitions)
## Outputs: (none — sourced by other scripts)
## =============================================================================

# ---------------------------------------------------------------------------
# Significance stars (working paper convention)
# p < 0.01 → ***; p < 0.05 → **; p < 0.10 → *
# ---------------------------------------------------------------------------
stars <- function(p) {
  stopifnot(is.numeric(p) || is.na(p))
  if (is.na(p))  return("")
  if (p < 0.01) return("^{***}")
  if (p < 0.05) return("^{**}")
  if (p < 0.10) return("^{*}")
  return("")
}

# ---------------------------------------------------------------------------
# Format a coefficient and its SE for a LaTeX tabular row.
# Returns a list with $main (coef + stars) and $se (parenthesised SE).
# ---------------------------------------------------------------------------
fmt_coef_se <- function(mod, var) {
  stopifnot(inherits(mod, "fixest"), is.character(var), nchar(var) > 0)
  co   <- coef(mod)
  se_v <- se(mod)
  pv   <- pvalue(mod)
  nm   <- names(co)[grepl(var, names(co), fixed = TRUE)][1]
  if (is.na(nm)) return(list(main = "---", se = ""))
  list(
    main = sprintf("%.4f%s", co[[nm]], stars(pv[[nm]])),
    se   = sprintf("(%.4f)", se_v[[nm]])
  )
}

# ---------------------------------------------------------------------------
# Extract one coefficient row (estimates + stars) and one SE row for a list
# of fixest models, matched by regex pattern on coefficient names.
# Returns a character vector of two LaTeX row strings.
# ---------------------------------------------------------------------------
coef_se_rows <- function(models, var_pattern, row_label) {
  stopifnot(is.list(models), length(models) > 0,
            is.character(var_pattern), nchar(var_pattern) > 0)

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
# Extract the IV beta from a fixest demand-system model.
# var_pattern: regex pattern for the instrumented coefficient (default "fit_mu_t").
# Used in 05_demand_system.R to compute B_agg = Sigma(beta_s).
# ---------------------------------------------------------------------------
get_iv_beta <- function(mod, var_pattern = "fit_mu_t") {
  stopifnot(inherits(mod, "fixest"),
            is.character(var_pattern), nchar(var_pattern) > 0)
  nm <- names(coef(mod))[grepl(var_pattern, names(coef(mod)))][1]
  if (is.na(nm)) return(NA_real_)
  coef(mod)[[nm]]
}

# ---------------------------------------------------------------------------
# Summary statistics for a single numeric vector.
# Returns a one-row tibble with N, Mean, SD, P25, P50, P75.
# ---------------------------------------------------------------------------
compute_stats <- function(x) {
  stopifnot(is.numeric(x))
  tibble::tibble(
    N    = sum(!is.na(x)),
    Mean = mean(x, na.rm = TRUE),
    SD   = sd(x,   na.rm = TRUE),
    P25  = quantile(x, 0.25, na.rm = TRUE),
    P50  = quantile(x, 0.50, na.rm = TRUE),
    P75  = quantile(x, 0.75, na.rm = TRUE)
  )
}

# ---------------------------------------------------------------------------
# Format mean and SD for balance table cells: "12.34 (5.67)"
# ---------------------------------------------------------------------------
fmt_mean_sd <- function(m, s) {
  sprintf("%.2f (%.2f)", m, s)
}
