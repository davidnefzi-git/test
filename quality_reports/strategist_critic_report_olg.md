# Strategy Memo Review
**Date:** 2026-05-19
**Reviewer:** strategist-critic
**Paper:** Net Foreign Assets, Demographics, and the Structural Determinants of External Imbalances: A Two-Country OLG Approach

---

## Phase 1: Claim Assessment

### Paper Type Classification
The memo correctly classifies this as a **Theory + Empirics** paper (Type III: theory-disciplined empirics). The structural cointegrating relation is derived from a two-country OLG model, not constructed ex post to fit data patterns. This classification is accurate and the memo draws the correct methodological implications from it.

### Testable Predictions and Estimands
The memo identifies the following structural predictions to be tested:

| Coefficient | Prediction | Memo Correctly States? |
|-------------|------------|----------------------|
| γ1 > 0 | Richer countries are creditors | Yes |
| γ2 < 0 | Current dependency depresses NIIP | Yes |
| γ3 > 0 | Anticipated aging raises precautionary saving | Yes |
| γ4 > 0 | Longer retirement raises saving | Yes |
| γ_TFP | Ambiguous (income vs. substitution effects) | Yes — correctly flags structural ambiguity |
| γ_D < 0 | Public debt crowds out private NFA (Ricardian) | Yes |
| GE channel | Total vs. direct effect via r* | Yes — addressed in Section 4 |

All six signed predictions (γ1–γ4, γ_D, and GE channel direction) and the ambiguous case (γ_TFP) are identified and correctly characterized. The ECM's implication — that cointegrating residuals must be I(0) — is noted as a testable prediction in Section 2.

**Note on completeness:** The paper's structural equation has 7 right-hand-side structural objects (y_it, φ_it, E[φ_{i,t+T}], E[e_{65,i,t+T}], ã_it, d^g_it, plus μ_i and λ_t/r*). The memo covers all of them, though γ_TFP's ambiguity could be stated with sharper theoretical logic (the sign depends on whether the economy is more savings-driven or investment-driven, which varies with capital deepening stage — an additional cross-country heterogeneity dimension not discussed).

**Phase 1 Assessment: PASS.** The paper type classification is correct, the estimands are fully enumerated, and the memo correctly maps the OLG model's structural parameters to empirical objects.

---

## Phase 2: Core Design Validity

**Assessment: GAPS — The core design is sound but several design elements have identifiable weaknesses that could compromise validity if unaddressed.**

### 2.1 Cointegrating Relation Specification
The memo correctly identifies the cointegrating relation as structurally derived. It appropriately notes that the relation requires I(0) residuals as a testable implication, and lists the correct panel cointegration tests (Pedroni 1999, 2004; Westerlund 2007 with bootstrap). The memo rightly flags that Westerlund's bootstrap is necessary under cross-sectional dependence.

**Gap:** The memo does not address whether the **regressors themselves are integrated of the same order**. For a cointegrating relation to be valid, all right-hand-side variables must be I(1). Demographics variables (dependency ratios, life expectancy projections) may be closer to I(2) in some country samples over long panels, which would invalidate the DOLS/FMOLS specification. The memo prescribes IPS/CIPS unit root tests but does not discuss the I(2) possibility or the appropriate tests for it (Haldrup 1994, I(2) panel tests). **Deduction applies.**

### 2.2 Estimator Hierarchy — Internal Consistency
The proposed ordering (DOLS → FMOLS → CCE-MG → CupFM/CupBC) is internally consistent and well-motivated. The table in Section 3.1 cleanly delineates what each estimator adds. The identification of what each estimator maintains as an assumption (CS independence for DOLS/FMOLS; factor structure for CCE-MG/CupFM) is technically correct.

The memo's treatment of CCE-MG's structural interpretation (Section 3.3) is one of its strongest contributions. The argument that CCE-MG coefficients identify the within-factor (idiosyncratic) effects — precisely the γ parameters the OLG model predicts for country deviations from symmetric equilibrium — is conceptually correct and often missed in applied work. This is a genuine analytical contribution from the strategist.

**Gap:** The memo elevates CCE-MG to co-primary status but does not acknowledge a limitation: CCE-MG's consistency relies on the number of cross-section units (N) being large relative to the number of unobserved factors (r). If N ≈ 30 (OECD baseline) and the true factor structure has r = 3–4 (global business cycle, global demographic trend, global TFP, global fiscal cycle), the CCE-MG approximation may be imprecise. This is a known finite-sample concern (Pesaran 2006, Monte Carlo evidence) that the memo does not flag. Minor, but a referee will raise it.

### 2.3 CCE-MG Structural Interpretation — Validity
The memo's claim (Section 3.3) that CCE-MG absorbs the endogenous r* via cross-sectional averages is **conditionally valid**. It holds if r* enters the error as a common factor. This requires the world interest rate to be a linear function of the cross-section averages of the regressors — an assumption that is true in the two-country symmetric OLG model but may not hold in a multi-country setting where r* is a nonlinear aggregation. The memo does not state this condition, which weakens the structural claim.

**Assessment:** The GE channel identification via CCE-MG cross-sectional averages is plausible but needs a conditional statement. This is not a fatal flaw — it mirrors limitations in all factor-proxy approaches — but the paper should not claim the CCE-MG absorbs r* "cleanly" without acknowledging the linearity assumption.

### 2.4 r* Identification Strategy
Section 4 of the memo handles the r* decomposition thoughtfully. The warning about measurement error in observed r* proxies (HLW, LJK) is accurate and the recommendation to include both r*_t and time FEs simultaneously is sound econometric practice. The distinction between the GE decomposition as a "heterogeneous loading on a common factor" vs. a structural channel decomposition (Section 4.3) is technically precise and correct.

**Gap (CRITICAL):** The memo proposes using r*_t × φ_it and r*_t × d^g_it as interaction terms to identify the GE channel. However, the interaction of a measured-with-error variable (r*_t) with cross-sectionally varying regressors (φ_it) generates **interaction-specific measurement error bias** that is not attenuating — it can be amplifying if r*_t and φ_it are positively correlated (older countries have more capital, pushing down r*). This is a non-standard measurement error problem (Bound, Brown & Mathiowetz 2001 for interaction terms with errors) that the memo does not acknowledge. Absent an instrument for r*_t in the interaction terms, the GE decomposition coefficients are unreliable. **Deduction applies.**

### 2.5 Pre-Tests: Coverage and Ordering
The appendix checklist is comprehensive and correctly ordered (pre-estimation → post-estimation). All major pre-tests are present: CD test (Pesaran 2004), IPS/CIPS unit roots, Pesaran-Yamagata slope homogeneity, Pedroni/Westerlund cointegration, and Bai-Ng factor selection. This is a notable strength of the memo.

**Missing:** The checklist prescribes the CD test on regressors but not the **CD test on the raw dependent variable (NIIP/GDP)** separately. Knowing whether NIIP itself exhibits strong cross-sectional dependence is diagnostically useful — it tells whether time FEs alone are sufficient or whether a factor structure is needed in the dependent variable. This is minor but notable.

**Missing:** No mention of **structural break testing** (Bai-Perron 2003, panel version) despite the memo itself noting (Section 3.2, Threat 5) that the sample spans distinct r* regimes. The memo flags this threat but does not include a break test in the checklist. This is an internal inconsistency. **Deduction applies.**

### 2.6 Slope Heterogeneity
The memo correctly identifies slope heterogeneity as a critical threat (Section 3.2, Threat 2) and recommends the Pesaran-Yamagata Δ-test as a required pre-test. Priority Recommendation 1 is appropriately placed upstream. The discussion of Pesaran-Smith (1995)'s convergence-to-weighted-average result under heterogeneity is technically correct and well-placed.

**Positive finding:** The recommendation to lead with CCE-MG or AMG if heterogeneity is not rejected (Priority 1, Step 3) is the correct conditional structure. This is the right approach.

### 2.7 ECM Specification
The memo notes (Section 7.1) that the two-step Engle-Granger procedure for identifying α_i has size distortions in small T, and correctly recommends PMG as a more efficient one-step alternative. The Hausman test between PMG and MG is the appropriate specification test. This is technically sound.

**Gap:** The memo does not address whether the ECM should include contemporaneous levels changes (DOLS-style with I(0) regressors in the ECM) or only lagged error-correction terms. The Granger Representation Theorem guarantees existence of an ECM when cointegration holds, but the short-run dynamics specification (lag order selection, significance of leads in the ECM's first-differenced part) requires additional discussion. The memo is silent on lag order selection in the ECM, which is a practical design gap.

### 2.8 Gravity Extension (PPML + Bilateral FEs)
The PPML treatment (Section 7.4) is technically competent. The discussion of structural zeros in CPIS data, the limitation that PPML identifies off non-zero cells when zero shares are high, and the recommendation of Heckman selection or corner-solution Tobit as robustness checks are all appropriate.

**Gap:** The memo recommends origin-time + destination-time FEs as "correctly specified" but does not note that this specification absorbs **all** cross-country variation in the OLG structural variables (demographics, TFP, debt) for origin and destination separately — leaving only pair-level variation for identification. If the bilateral demographic differentials are the structural object of interest (as the OLG model suggests), the gravity specification must use pair-level demographic differences, not bilateral FEs that absorb all country-time variation. This is a design inconsistency: the bilateral FEs eliminate the variation that the OLG theory predicts should drive bilateral portfolio positions. **Deduction applies.**

---

## Phase 3: Assumptions and Gaps

### 3.1 Critical Robustness Checks — Omissions

**Omission 1: Structural breaks not tested.**
The memo identifies (Section 3.2, Threat 5) that the sample spans multiple r* regimes. The appendix checklist includes no structural break test. This is an internally inconsistent gap — the threat is recognized but not remedied. Bai-Perron tests or recursive coefficient stability plots should be included. **Deduction: internal inconsistency.**

**Omission 2: Capital account openness not controlled.**
Section 7.3 notes that the OLG model assumes frictionless capital mobility and that countries with binding capital controls violate this. However, no Chinn-Ito index, Quinn liberalization index, or sample restriction based on de facto capital openness (Lane-Milesi-Ferretti KAOPEN) is recommended for the baseline. The memo raises the issue but does not operationalize a solution. **Deduction: robustness check absent for a known threat.**

**Omission 3: Currency composition of NIIP.**
The OLG model is specified in terms of real assets. NIIP measured in domestic currency units includes valuation effects from exchange rate movements that are not structural savings decisions. The memo discusses valuation effects (Section 7.2) but only in terms of equity/bond price movements, not currency valuation. Exchange-rate-driven NIIP changes (especially for countries with large foreign-currency debt) introduce a mechanical correlation between NIIP and the exchange rate that is not modeled. A robustness check with NIIP measured in USD (or SDR) and GDP converted at constant exchange rates is absent. **Deduction: robustness check absent.**

**Omission 4: Pension system controls.**
The OLG savings mechanics are fundamentally about life-cycle saving. Countries with generous pay-as-you-go (PAYG) pension systems have different demographic-savings linkages than countries with funded (capitalized) systems. The model's γ2 and γ3 predictions are implicitly conditional on private saving being the margin of adjustment. If government pension systems offset private saving mechanically, the demographic effects on NIIP may be attenuated. A pension replacement rate control or a funded vs. PAYG dummy is absent from the proposed specification. This is a significant omission given the paper's theoretical grounding. **Deduction: robustness check absent for a known threat.**

**Omission 5: Anticipation effects in expectations formation.**
The memo discusses horizon T for UN projections (Section 5.2) but does not discuss whether agents form expectations rationally (using UN projections) or adaptively (using current demographics as a proxy for future). Using observed UN projections as E_t[φ_{i,t+T}] imposes rational-expectations hypothesis on the agents in the model. This assumption is implicit and untested. A robustness check substituting a simple extrapolation of current demographic trends (adaptive expectations) would test sensitivity to the expectations formation assumption. **Deduction: robustness check absent.**

### 3.2 Estimator Assumptions — Stated vs. Missing

| Estimator | Assumptions Stated in Memo | Missing |
|-----------|---------------------------|---------|
| DOLS | CS independence, pooled slope | Optimal lead/lag order selection (AIC/BIC vs. fixed); weak exogeneity requirement made explicit |
| FMOLS | CS independence, pooled slope, long-run covariance estimation | Bandwidth selection for kernel (Newey-West vs. Andrews); sensitivity |
| CCE-MG | Factor structure on errors | N >> r condition; linearity of r* in cross-section averages; strong factor assumption |
| CupFM/CupBC | Parametric factor structure | Number of factors r pre-specified; computational stability for heterogeneous-slopes version |
| PMG (recommended) | Long-run homogeneity | Hausman test correctly described; assumption of valid long-run slope pooling |
| AMG (recommended) | Common dynamic process estimable from first differences | Assumption that the common dynamic process is identified |

Several estimator assumptions are not fully stated. The DOLS bandwidth/lag choice and the FMOLS kernel bandwidth choice are nontrivial in practice (they affect the finite-sample efficiency of the correction), but neither receives more than passing mention. **Deduction applies (minor, per estimator).**

### 3.3 Demographics Measurement — Assessment
The memo's treatment of anticipated demographics (Section 5) is strong. It correctly identifies:
- Pre-determination vs. strict exogeneity distinction for UN projections.
- Measurement error attenuation bias (bias against finding the predicted sign — correctly characterized).
- The 20-year horizon recommendation is well-motivated with the inverted-U prediction.
- Multicollinearity between φ_it and e_65 is flagged with a practical remedy (VIF, composite index).

**One gap:** The memo does not discuss **population heterogeneity within countries** — urban/rural demographic differentials, immigrant populations, and informal sector workers who may not participate in the financial system. For some emerging market extensions, aggregate dependency ratios mask large within-country heterogeneity in savings behavior. This is a concern for the EM extension (Section 7.3) but not for the OECD baseline, so it is a minor omission.

### 3.4 TFP Endogeneity — Assessment
Section 6 handles TFP competently. The double-filtering warning (pre-filtering ã_it before CCE-MG over-removes common variation) is technically correct and an important practical point. The IV robustness suggestion (frontier technology adoption as instrument) is appropriate.

**Gap:** The memo does not propose a formal test for weak exogeneity of ã_it. The Wu-Hausman test comparing DOLS with and without instrumented TFP would directly test whether the endogeneity concern is empirically significant in this dataset. Without it, the memo raises the concern but leaves it unresolved. **Deduction: anticipation/reverse causality issue raised but not resolved with a concrete test proposal.**

### 3.5 Sample Design Specificity
Section 7.3 provides a reasonable baseline sample recommendation (30-40 OECD, 1980-2022) with a sensible extension strategy. The T ≥ 30 requirement for cointegration test power is correctly stated.

**Gap:** No minimum capital account openness threshold is specified for inclusion. No vintage-data plan is stated (which year's UN WPP projections to use for each time period t — using contemporaneous projections requires a historical vintage dataset that is not standard; using 2024 WPP projections for 1985 observations introduces look-ahead bias). This is a subtle but consequential data construction issue that the memo raises in Section 5.1 (measurement error from underestimation of longevity) without resolving the vintage selection problem. **Deduction: anticipation/vintage bias issue unaddressed.**

---

## Phase 4: Quality, Citations, and Linkage

### 4.1 Citation Accuracy

| Citation | Memo's Description | Assessment |
|----------|--------------------|------------|
| Stock & Watson (1993) | DOLS "applied to panels" | Partially inaccurate — Stock & Watson (1993) is for time-series cointegrating vectors (single equation); the panel DOLS extension is typically attributed to Kao & Chiang (2000) and Mark & Sul (2003). The memo attributes panel DOLS directly to Stock-Watson, which is imprecise. **Deduction: citation error.** |
| Pedroni (1999, 2004) | Panel cointegration | Correct. |
| Pesaran (2006) | CCE-MG | Correct — Econometrica. |
| Bai, Kao & Ng (2009) | CupFM/CupBC | Correct — Journal of Econometrics. |
| Pesaran, Shin & Smith (1999) | PMG | Correct — JASA. |
| Pesaran & Smith (1995) | MG/heterogeneity bias | Correct — Journal of Econometrics. |
| Pesaran & Yamagata (2008) | Slope homogeneity | Correct. |
| Bond & Eberhardt (2009); Eberhardt & Bond (2009) | AMG | The AMG estimator is most precisely cited as Eberhardt & Bond (2009) MPRA Working Paper 22281 / subsequently published as Bond & Eberhardt (2013) in the Oxford Bulletin. The 2009 citation is to working papers, which is acceptable but should note the published version. Minor. |
| Santos-Silva & Tenreyro (2006) | PPML | Correct — Review of Economics and Statistics. |
| Pesaran (2004) | CD test | The published version of this test appeared as Pesaran (2021) in the Journal of Econometrics, based on a 2004 Cambridge working paper. Citing the working paper is common but potentially leads to incorrect journal reference. Minor. |
| Westerlund (2007) | Panel cointegration with bootstrap | Correct — Oxford Bulletin of Economics and Statistics. |
| Holston, Laubach & Williams (2017) | r* measurement | Correct — Journal of International Economics. |
| Chudik & Pesaran (2015) | CS-ARDL | Correct — Journal of Econometrics. |

**Net citation issues:** One substantive error (Stock-Watson 1993 mis-attributed as panel DOLS source), one minor dating issue (Bond-Eberhardt published version), one minor journal reference issue (Pesaran 2004/2021 CD test).

### 4.2 Structural Predictions Linkage

All 7 structural parameters (γ1–γ4, γ_TFP, γ_D, and the GE channel via r*) are discussed and linked to estimable moments in the proposed strategy. The linkage is explicit in Phase 1 and maintained through the estimation sections.

**Positive finding:** The memo's Section 3.3 (CCE-MG structural interpretation) provides a novel and accurate link between the OLG model's symmetric-equilibrium structure and the within-factor variation identified by CCE-MG. This is above-standard analytical quality.

**Positive finding:** Section 4.3's distinction between "heterogeneous factor loading" and "structural GE channel decomposition" is precise and prevents a common overinterpretation of the r* interaction specifications.

### 4.3 Internal Consistency
The memo is internally consistent on most dimensions. The major internal inconsistency identified:

- **Section 3.2 (Threat 5)** identifies structural breaks as a critical threat, but the appendix checklist omits any structural break test. This is a lapse that undermines the memo's claim to be a comprehensive pre-estimation audit. **Deduction: internal inconsistency.**

- **Section 7.4** recommends origin-time + destination-time FEs for the gravity extension as "correctly specified," but this absorbs all the OLG structural variation (demographics, TFP, debt at origin and destination separately), leaving only pair-level demographic differentials for identification. The memo does not note this tension with the paper's theoretical objective. **Deduction: internal inconsistency in the gravity design.**

---

## Summary

### Score Calculation

Starting score: **100**

| Issue | Deduction | Applied |
|-------|-----------|---------|
| I(2) possibility for demographic variables not discussed (key pre-test gap) | −10 | Yes |
| Structural break test absent despite threat flagged (internal inconsistency) | −5 | Yes |
| Capital controls not operationalized despite identified threat (robustness absent) | −5 | Yes |
| Pension system controls absent (robustness absent for known theoretical threat) | −5 | Yes |
| Anticipation/expectations formation robustness absent | −5 | Yes |
| Vintage UN WPP selection (look-ahead bias) unresolved | −5 | Yes |
| Currency composition of NIIP robustness absent | −5 | Yes |
| Bilateral FEs in gravity absorb OLG structural variation (design inconsistency) | −5 | Yes |
| Interaction-term measurement error in r* × φ_it (GE channel bias, unaddressed) | −5 | Yes |
| TFP endogeneity: Wu-Hausman test not proposed (reverse causality partially unresolved) | −5 | Yes |
| DOLS lag order selection criterion not stated (estimator assumption gap) | −5 | Yes |
| FMOLS bandwidth selection not stated (estimator assumption gap) | −5 | Yes |
| CCE-MG finite-sample N >> r condition not stated (estimator assumption gap) | −5 | Yes |
| Stock-Watson (1993) citation error (panel DOLS attribution) | −3 | Yes |
| Gravity bilateral FEs internal inconsistency (tension with OLG structural variation) | Already counted above | — |

**Total deductions: −73**

**However**, several deductions represent overlapping concerns. The gravity bilateral FE inconsistency and the bilateral FE design gap are the same issue (counted once). The look-ahead bias and the demographics measurement issue overlap with the robustness gap. Applying the rubric strictly but without double-counting:

**Adjusted deductions:**
- I(2) pre-test missing: −10
- Internal inconsistency (structural break omission): −5
- Internal inconsistency (gravity bilateral FE tension): −5
- Robustness absent — capital controls: −5
- Robustness absent — pension system: −5
- Robustness absent — expectations formation: −5
- Robustness absent — currency composition: −5
- Robustness absent — UN WPP vintage (look-ahead): −5
- GE channel interaction measurement error unaddressed: −5
- TFP reverse causality partially unresolved (test not proposed): −5
- Estimator assumptions gap — DOLS lag selection: −5 (one representative estimator assumption gap)
- Citation error — Stock-Watson panel DOLS: −3

**Total adjusted deductions: −63**

**Final Score: 37 / 100**

---

**Score: 37 / 100**
**Verdict: REJECT**
**Critical issues (must fix):** 3
**Major issues (should fix):** 7
**Minor issues:** 4

---

## Priority Recommendations

### Critical Issues (Must Fix)

1. **[CRITICAL] Address I(2) possibility for demographic variables.** Old-age dependency ratios and life expectancy projections may be I(2) over long samples. DOLS and FMOLS are not valid for I(2) regressors. Add I(2) pre-tests (Haldrup 1994 or panel analogues) and state what the estimation strategy will be if I(2) is not rejected (first-difference the cointegrating relation; use Johansen I(2) framework). This is upstream of all estimation choices.

2. **[CRITICAL] Resolve the interaction-term measurement error problem in the r* identification strategy.** Replacing time FEs with r*_t and r*_t × φ_it introduces measurement error that compounds non-linearly in the interaction terms. The memo correctly flags r* measurement uncertainty but fails to carry through to the interaction terms, where the bias is non-attenuating. Either instrument r*_t explicitly (using lagged global demographic projections, global TFP, as the memo briefly notes) or abandon the clean r* decomposition in favour of a semi-parametric approach. The current proposal will produce unreliable GE channel estimates.

3. **[CRITICAL] Operationalize the UN WPP vintage selection rule to avoid look-ahead bias.** Using contemporaneous (e.g., 2024 WPP) projections for observations dated 1985 or 1990 introduces information from future periods into the explanatory variables. This is a form of look-ahead bias that can spuriously validate the γ3/γ4 predictions. The memo identifies measurement error from longevity underestimation but does not prescribe using time-matched historical vintages. Establish a data construction rule: for observation year t, use the UN WPP projection vintage published nearest to year t. This requires the historical UN WPP vintage dataset (available from UN Population Division), and the paper should document the vintage used for each observation.

### Major Issues (Should Fix)

4. **[MAJOR] Add structural break tests to the pre-test checklist.** The memo identifies structural breaks (Bretton-Woods → float; global savings glut; post-GFC) as Threat 5 but includes no break test in the appendix checklist. Add Bai-Perron (2003) panel structural break tests or, at minimum, recursive CCE-MG estimates and sub-period robustness tables. The internal inconsistency between threat identification and checklist omission will be caught by any careful referee.

5. **[MAJOR] Control for pension system type.** The OLG savings mechanics are conditioned on private life-cycle saving being the dominant adjustment margin. PAYG pension systems mechanically offset demographic effects on private NIIP (governments accumulate future pension liabilities that do not appear in NIIP). Include the pension replacement rate (OECD Social Benefits database) or a funded-vs-PAYG dummy as a control in the baseline. Test sensitivity of γ2 and γ3 to including/excluding this control.

6. **[MAJOR] Resolve bilateral gravity FE inconsistency.** Origin-time and destination-time FEs absorb all country-time variation in demographics, TFP, and public debt — exactly the OLG structural variables. If the paper uses these FEs, the gravity extension tests only whether bilateral demographic differentials (demeaned from country-time averages) matter for portfolio positions, not whether the OLG structural levels drive bilateral allocations. Re-specify the gravity model to include bilateral demographic differential terms (φ_it − φ_jt, projected aging differentials) explicitly, or clearly state that the bilateral extension tests a distinct (pair-level) prediction of the OLG model rather than the same structural parameters as the aggregate panel.

7. **[MAJOR] Include capital account openness as a sample restriction criterion and control.** The OLG model requires frictionless capital mobility. Countries with binding capital controls violate the model's equilibrium condition. Add the Chinn-Ito (2008) index as a control and as a sample restriction threshold (e.g., KAOPEN > -0.5). Report robustness of all structural coefficients to restricting the sample to fully open capital accounts.

8. **[MAJOR] Add expectations formation robustness.** The paper uses UN projections as E_t[φ_{i,t+T}], imposing rational expectations. Run a robustness table where expected future demographics are replaced by an adaptive forecast (e.g., AR(1) extrapolation from current dependency ratio) and compare γ3 estimates. Large differences signal that the structural predictions are sensitive to the expectations assumption.

9. **[MAJOR] Correct the DOLS citation.** The panel DOLS estimator is properly attributed to Kao & Chiang (2000) *Advances in Econometrics* and Mark & Sul (2003) *Econometrica*, not to Stock & Watson (1993) which is a time-series result. Stock-Watson (1993) can be cited as the theoretical foundation, but the panel generalization requires the correct applied references. This error will undermine credibility with panel econometrics referees.

10. **[MAJOR] State complete estimator assumptions for DOLS and FMOLS.** The memo's table (Section 3.1) lists maintained assumptions but omits: (a) the optimal lead/lag selection criterion for DOLS (AIC/BIC/fixed T^{1/3}); (b) the long-run covariance estimation bandwidth for FMOLS (Newey-West vs. Andrews automatic); (c) the strong factor assumption for CCE-MG. Each of these affects inference and reviewers will ask how they were implemented.

### Minor Issues

11. **[MINOR] Test and report CD statistic on NIIP/GDP directly.** The pre-test checklist tests CD on regressors but not on the dependent variable. Knowing the degree of cross-sectional dependence in NIIP/GDP informs whether time FEs alone suffice or whether a richer factor structure is needed in the error of the long-run equation.

12. **[MINOR] Discuss FMOLS published citation version.** Bond & Eberhardt AMG should cite the published version (Bond & Eberhardt 2013, *Oxford Bulletin of Economics and Statistics*) alongside the 2009 working paper.

13. **[MINOR] Acknowledge CCE-MG finite-sample limitations.** With N ≈ 30 (OECD baseline) and potentially r = 3–4 common factors, the CCE-MG small-N approximation may be imprecise. Cite relevant Monte Carlo evidence (Pesaran 2006, Section 5) and acknowledge the limitation.

14. **[MINOR] Discuss within-country demographic heterogeneity for the EM extension.** National-level dependency ratios mask urban/rural and formal/informal sector heterogeneity in savings behavior. For the EM extension, note this limitation and consider whether subnational or sector-level data would improve identification.

---

## Positive Findings

1. **Theory-to-empirics pipeline is genuinely tight.** The cointegrating relation is derived from OLG optimality conditions, not constructed post hoc. The sign restrictions are over-identifying and falsifiable. This is the standard that top journals expect and the paper meets it.

2. **CCE-MG structural interpretation (Section 3.3) is analytically original and correct.** The argument that CCE-MG identifies the within-factor (idiosyncratic) deviation from world average — exactly the object predicted by the two-country OLG model — is both technically precise and often missed in applied macro work. This framing could be a methodological contribution of the paper itself.

3. **The estimator hierarchy is well-ordered and the table in Section 3.1 is pedagogically clear.** The progression from naive (DOLS) to robust (CupFM/CupBC) with explicit statement of what each step adds is exactly what methodology-savvy referees want to see.

4. **The pre-test checklist (Appendix) is comprehensive on the tests it does include.** The Westerlund (2007) bootstrap recommendation for cointegration testing under cross-sectional dependence is the correct choice and shows awareness of the econometric literature.

5. **The memo's treatment of anticipated demographics (Section 5) correctly characterizes the measurement error as attenuating and notes its implication for interpretation** — bias against finding the predicted positive signs for γ3 and γ4. This is the honest scientific position.

6. **The valuation effects decomposition strategy (Section 7.2)** — running baseline on total NIIP and comparing with cumulative-CA adjusted NIIP — is a clean identification of the valuation channel that is implementable with Lane-Milesi-Ferretti data. This is a well-designed extension.

7. **Priority recommendations are correctly ordered.** The sample/slope-heterogeneity pre-test is correctly elevated as Priority 1 (upstream of all other choices), and the CCE-MG structural interpretation as Priority 2. The ordering reflects sound methodological sequencing.
