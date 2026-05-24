## =============================================================================
## Title:   00_master.R
## Author:  Data Engineer
## Date:    2026-05-24
## Purpose: Master script for the FX swap microstructure paper. Sources scripts
##          01–07 in dependency order. Single entry point for full pipeline.
##
## Execution order and dependencies:
##   01_simulate_data.R          — synthetic panel data (no dependencies)
##   02_balance_tests.R          — balance tests (requires 01)
##   03_descriptives.R           — summary statistics and figures (requires 01)
##   04_iv_estimation.R          — demand + supply IV, simultaneous system (req 01)
##   05_demand_system.R          — demand system estimation (requires 01)
##   06_quality_checks.R         — data quality validation (requires 01)
##   07_bilateral_decomposition.R — bilateral flows, sector spreads (NEW v9, req 01)
##
## Inputs:  None (01_simulate_data.R generates all raw data)
## Outputs: All outputs from scripts 01–07 (see individual script headers)
## =============================================================================

library(here)

# Single set.seed() for the entire pipeline (INV-14).
# 01_simulate_data.R generates all stochastic data; downstream scripts are
# deterministic except for the plotting sample in 06_quality_checks.R.
set.seed(42)

# ---------------------------------------------------------------------------
# Execute pipeline in dependency order
# ---------------------------------------------------------------------------

message("=== 00_master.R: Starting FX swap analysis pipeline ===")
message(sprintf("  Working directory: %s", here::here()))
message(sprintf("  Timestamp: %s", Sys.time()))

message("\n--- Step 1: Simulate data ---")
source(here::here("scripts", "R", "01_simulate_data.R"))

message("\n--- Step 2: Balance tests ---")
source(here::here("scripts", "R", "02_balance_tests.R"))

message("\n--- Step 3: Descriptive statistics ---")
source(here::here("scripts", "R", "03_descriptives.R"))

message("\n--- Step 4: IV estimation ---")
source(here::here("scripts", "R", "04_iv_estimation.R"))

message("\n--- Step 5: Demand system ---")
source(here::here("scripts", "R", "05_demand_system.R"))

message("\n--- Step 6: Quality checks ---")
source(here::here("scripts", "R", "06_quality_checks.R"))

message("\n--- Step 7: Bilateral decomposition (v9) ---")
source(here::here("scripts", "R", "07_bilateral_decomposition.R"))

message("\n=== Pipeline complete ===")
message(sprintf("  Timestamp: %s", Sys.time()))
