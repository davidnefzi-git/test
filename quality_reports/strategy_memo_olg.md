# Strategy Memo: Net Foreign Assets, Demographics, and the Structural Determinants of External Imbalances
## A Two-Country OLG Approach — Empirical Strategy Evaluation

**Prepared by:** Strategist Agent  
**Date:** 2026-05-19  
**Memo type:** Pre-estimation strategy audit and enrichment

---

## 1. Pre-Strategy Report: What Is Present, What Is Missing

### What Is Present

The paper provides an unusually tight theory-to-empirics pipeline. The structural cointegrating relation is derived from a two-country OLG model, not reverse-engineered from data, so the regressors are not ad hoc. The estimator hierarchy is explicitly ordered from least to most robust to cross-sectional dependence (CS dependence). The GE channel is handled conceptually via time fixed effects, and the plan to replace time FEs with an observable r* offers a genuine identification refinement rather than a cosmetic robustness check. Sign restrictions are structurally motivated and falsifiable.

### What Is Missing or Under-Specified

1. **Sample design is unspecified.** No country list, no time period. This is not a minor omission: the choice between advanced economies (AEs) only, AEs + emerging markets (EMs), or a broader panel fundamentally changes the plausibility of parameter homogeneity (the pooling assumption in DOLS/FMOLS) and the relevance of the OLG model itself (OLG savings mechanics work differently in countries with low financial depth or capital controls).

2. **Frequency is unspecified.** Annual vs. five-year averages matters enormously for panel cointegration: five-year averages reduce business-cycle noise but shrink T dramatically, weakening cointegration test power. Annual data preserve T but force you to control for cyclical dynamics in the ECM.

3. **Valuation effects are named but not operationalized.** The paper lists val_it as an extension but does not state how it will be measured (external wealth accounting à la Lane-Milesi-Ferretti, or a valuation residual from the current account identity). This is consequential: if NIIP changes mechanically via valuation, the cointegrating relation using stock NIIP/GDP will conflate savings-driven and valuation-driven positions.

4. **The ECM's α_i (speed of adjustment) identification** is stated but not discussed. How is it pinned separately from the long-run cointegrating vector? The mean-group or pooled mean-group specification is implied but not stated.

5. **TFP decomposition is invoked (non-global component of utilization-adjusted TFP) but the source and construction are not specified.** The standard series (Fernald, Penn World Tables) have different coverage and methodologies; the decomposition into global vs. country-specific components is non-trivial and itself requires a factor model.

6. **Projection horizon T for anticipated demographics is not specified.** The model needs a calibrated retirement horizon (15 years? 20 years? 30 years?) tied to the OLG structure, and the sensitivity to this choice is unaddressed.

7. **No discussion of capital controls.** NIIP positions are partially determined by whether capital can flow freely. Countries with binding capital controls violate the model's frictionless capital mobility assumption. No indicator or sample restriction is proposed.

---

## 2. Paper Type Classification: Theory + Empirics

This is a **theory-disciplined empirical paper** (Type III in the clo-author taxonomy): the structural model is used not merely for motivation but to derive an estimable equation with cross-equation restrictions on signs. The theory commits the empirics to:

- A **specific functional form** (linear cointegrating relation in logs/levels of the specified regressors).
- **Sign restrictions** that are over-identifying if tested: γ1>0 (richer countries are creditors), γ2<0 (current dependency depresses NIIP via lower saving), γ3>0 (anticipated aging raises precautionary saving today), γ4>0 (longer retirement increases saving), γ_D<0 (Ricardian-type crowding out of private NFA via public debt).
- A **two-country GE channel** through the world interest rate r*_t that is absorbed by time FEs in the benchmark but must be unpacked for the "total effects" decomposition.
- **Stationarity of the residual** ε_it as a testable implication (the cointegrating residual must be I(0)).

What the theory does **not** commit to: the speed of adjustment α_i, the short-run dynamics in the ECM, or the measurement of TFP (these are empirical design choices left to the researcher).

---

## 3. Evaluating the Proposed Estimator Hierarchy

### 3.1 Is the Hierarchy Ordered Correctly?

The proposed order — DOLS → FMOLS → CCE-MG → CupFM/CupBC — reflects a logical progression from simple to robust. Each step addresses an additional threat:

| Estimator | Primary threat addressed | Key assumption maintained |
|-----------|--------------------------|--------------------------|
| DOLS | Endogeneity via leads/lags | CS independence; pooled slope |
| FMOLS | Endogeneity + serial correlation | CS independence; pooled slope |
| CCE-MG | CS dependence via factor proxies | Factor structure on errors |
| CupFM/CupBC | CS dependence + slope heterogeneity + simultaneity in factor loading | Parametric factor structure |

The ordering is defensible. DOLS is a natural benchmark because it is the workhorse in panel cointegration (Stock & Watson 1993 applied to panels). The progression to CCE-MG is important because panel cointegration datasets from 1975–2020 almost certainly exhibit strong CS dependence (global business cycles, financial contagion, common demographic trends).

### 3.2 Key Threats to the Cointegrating Relation

**Threat 1: Cross-sectional dependence.** The regressors (especially demographics and TFP) contain a global factor. Time FEs absorb the first moment but not higher-order CS dependence. If the idiosyncratic errors ε_it are cross-sectionally correlated, DOLS and FMOLS are inconsistent (their residual variances are biased). CIPS-based pre-tests and CD tests (Pesaran 2004) should be run on residuals.

**Threat 2: Slope heterogeneity.** The OLG model predicts different γ coefficients for countries at different stages of demographic transition. Pooled estimators (DOLS, FMOLS) impose homogeneity. The Pesaran-Yamagata (2008) slope homogeneity test (Δ-test) should be a required pre-test, not an afterthought.

**Threat 3: Endogeneity of TFP.** Country-specific TFP ã_it affects both saving (via permanent income) and investment (via returns), creating ambiguous net effects and simultaneity bias. DOLS leads/lags handle this only if TFP is weakly exogenous to NIIP; this is doubtful over long horizons.

**Threat 4: Measurement error in anticipated demographics.** UN projections have systematic biases (underestimation of longevity in the early sample). These are classical measurement errors and attenuate γ3 and γ4 toward zero. This is a bias against finding the predicted positive signs — important to note for interpretation.

**Threat 5: Structural breaks.** The sample likely spans the Bretton-Woods → float transition, the global savings glut period, and post-GFC secular stagnation. These represent different r* regimes and potentially different γ coefficients. No structural break test is proposed.

### 3.3 CCE-MG and the GE Channel

The CCE-MG interpretation is subtle and the paper gets it right conceptually but should be explicit about what "absorbing rest-of-world fundamentals" means. When CS averages x̄_t are included as factor proxies:

- The coefficient on x_it is the effect of country i's deviation from the world average on its NIIP deviation from the world average.
- This is a **within-factor** effect: it holds fixed the global factor (proxied by x̄_t).
- This is NOT the same as the time-FE partial effect, because CCE uses a richer factor structure (one factor per regressor column in x̄_t, not one intercept per period).

The structural interpretation of CCE-MG: it identifies the partial equilibrium effect of country-idiosyncratic variation in demographics/TFP/debt on NIIP, holding fixed global trends (including the endogenous r*). This is precisely what the theory's γ parameters represent in the two-country model (deviations from symmetric equilibrium). **This makes CCE-MG not just a robustness check but arguably the estimator most aligned with the structural object of interest.**

The paper should state this explicitly in the identification section.

### 3.4 CupFM/CupBC as Primary Estimators

Bai, Kao & Ng (2009) CupFM and CupBC are appropriate when the common factors are correlated with the regressors (a likely scenario here, since global demographic trends, global TFP, and global fiscal cycles all enter x_it). The simultaneous estimation of the factor loadings and the cointegrating vector avoids generated-regressor bias. However:

- CupFM/CupBC require specifying the number of factors r. The paper should use Bai-Ng (2002) IC criteria on the first-differenced residuals to determine r, and check robustness to r ± 1.
- CupFM and CupBC are computationally intensive. For heterogeneous slopes (mean-group version), the estimation may be unstable with small N or T.
- These estimators are less familiar to applied macro referees than CCE-MG. The paper should not present them as "preferred" without a clear pedagogical explanation of why — it will invite pushback from referees who know CCE-MG better.

**Recommendation:** Elevate CCE-MG to co-primary estimator alongside CupFM/CupBC, with the structural interpretation argument from Section 3.3. CupFM/CupBC serves as the robustness check against misspecified factor structure.

### 3.5 Missing Estimators and Robustness Checks

The following are absent and should be added:

1. **Pooled Mean Group (PMG, Pesaran, Shin & Smith 1999).** PMG imposes long-run homogeneity but allows heterogeneous short-run dynamics. It is the natural companion to a structural cointegrating relation (the γ parameters are the pooled long-run coefficients). The Hausman test between PMG and MG tests the homogeneity restriction.

2. **AMG (Augmented Mean Group, Bond & Eberhardt 2009; Eberhardt & Bond 2009).** AMG estimates a "common dynamic process" from the cross-sectional average of first-differenced regressions, then subtracts it. It is more flexible than CCE-MG in factor structure and is standard in macro panel cointegration.

3. **CS-ARDL (Chudik & Pesaran 2015).** For shorter T panels, ARDL bounds testing with CS augmentation may outperform levels-based cointegrating estimators.

4. **Slope heterogeneity tests.** Pesaran-Yamagata (2008) Δ and Δ-adj tests must be reported before any pooled estimator is presented.

5. **CIPS and CD tests on residuals.** Post-estimation unit-root and cross-dependence tests on the cointegrating residuals are required to validate the cointegrating relation.

---

## 4. The r* Identification Strategy

### 4.1 Is the r* Decomposition Valid?

The proposed specification replaces time FEs λ_t with an observed global neutral rate r*_t and interactions r*_t × φ_it, r*_t × d^g_it. The theoretical motivation is sound: in the OLG model, r* is the market-clearing condition on the global bond market, so direct effects of x_it on NIIP and indirect effects via r* are separable in principle.

The decomposition is valid if:
1. r*_t is measured without error (or measurement error is classical and small).
2. The interaction terms capture the relevant heterogeneity in how each country's demographics/debt transmit to r*.
3. The residual time variation in λ_t not captured by r*_t is small.

Condition 1 is problematic. Observed estimates of r* (HLW Holston-Laubach-Williams, LJK Laubach-Williams, brand/Farrugia, or simple realized real rate) are themselves model-dependent and measured with large uncertainty bands. Substituting a noisy proxy for λ_t introduces attenuation bias in the coefficients on r*_t and its interactions.

**Recommended refinement:** Include both r*_t and time FEs λ_t simultaneously, using r*_t and its interactions as within-period controls while the residual λ_t absorbs unexplained global shocks. This does not give the clean decomposition the authors want, but it is more honest. Alternatively, instrument r*_t with lagged global factors (lagged global TFP, global demographic projections) to address measurement error.

### 4.2 Degrees-of-Freedom Constraint

With N countries and T years, replacing T-1 time dummies with r*_t + r*_t×φ_it + r*_t×d^g_it saves T-3 degrees of freedom. But the gain is only relevant if N is moderate (30–50 countries). If N is large, the DF savings are negligible and the tradeoff is worse (you exchange unbiased λ_t for noisy r*_t). The paper should report the test of joint significance of λ_t after conditioning on r*_t and its interactions.

### 4.3 Do the Interactions Cleanly Identify the GE Channel?

The GE effect of φ_it on NIIP through r* is:
```
(∂B*/∂r*) · (∂r*/∂φ_it)
```
The second term, ∂r*/∂φ_it, is the marginal effect of country i's demographics on the world rate — which depends on country i's weight in the global capital market. For small countries, ∂r*/∂φ_it ≈ 0 and the GE channel is negligible. For the US, Germany, Japan, and China, it is non-trivial.

The interaction r*_t × φ_it identifies the cross-sectional variation in GE sensitivity (countries with higher φ_it load more on r* changes) but does not recover ∂r*/∂φ_it itself. This is a **heterogeneous loading on a common factor** interpretation, not a structural decomposition of the GE channel. The paper should be precise about which it is claiming.

**Cleaner alternative:** Use the model's own calibrated ∂r*/∂φ_it (from the OLG equilibrium) as an external weight to construct a country-specific GE channel index, then test whether the residual direct effect (after subtracting the model-predicted GE component) matches the CCE-MG coefficient.

---

## 5. Anticipated Demographics Measurement

### 5.1 Endogeneity of UN Projections

UN population projections E_t[φ_{i,t+T}] are not model-endogenous (they are not determined by NIIP). However, they are:
- **Not purely exogenous.** Fertility decisions respond to economic conditions (Becker-Lewis quality-quantity tradeoff). High-income, high-NIIP countries have systematically lower projected fertility. This creates a spurious negative correlation between E_t[φ_{i,t+T}] and current NIIP growth via omitted economic fundamentals.
- **Pre-determined, not strictly exogenous.** Projections made at time t use information available at t. They are pre-determined relative to future NIIP realizations but may be correlated with current economic shocks that also affect NIIP.

**Practical consequence:** γ3 (anticipated dependency) is likely estimated with less endogeneity bias than γ2 (current dependency), because the projection horizon T means E_t[φ_{i,t+T}] is partially driven by cohort structure already locked in by past births. Use the 20-25 year horizon where the demographic structure is mostly determined by the existing age pyramid (born before period t), minimizing feedback from current economic conditions.

### 5.2 Choice of Horizon T

The OLG model implies T should correspond to the working-life-to-retirement transition, roughly 30-40 years at age-20 workforce entry, or 15-20 years at age-45 mid-career. In practice:
- 20-year projections are the most reliable UN series (mortality is more predictable than fertility at shorter horizons).
- 30-year projections introduce substantial fertility uncertainty, inflating measurement error in E_t[φ_{i,t+T}].
- **Recommendation:** Use 20-year horizon as baseline, 10-year and 30-year as sensitivity checks. Report a robustness table with γ3 across T ∈ {10, 15, 20, 25, 30} years. The structural model predicts an inverted-U relationship in |γ3| as T increases (too short: no time to save; too long: discounting attenuates present value of future liability).

### 5.3 Retirement Duration E_t[e_{65,i,t+T}]

Life expectancy at 65 projected T years forward is a double projection: survival tables projected forward in time. Measurement issues:
- **Compression vs. expansion uncertainty.** Whether morbidity compresses (healthy old age) or expands (longer sick-period) is unresolved. This is systematic uncertainty, not random noise.
- **Multicollinearity with φ_it.** Countries with longer life expectancy at 65 also have higher old-age dependency ratios. The OLG model separates these (φ captures relative cohort size, e_65 captures per-retiree duration), but empirically the correlation may be high enough to make separate identification difficult.
- **Recommendation:** Report the VIF (or pairwise correlation) between φ_it and E_t[e_{65,i,t+T}] in the descriptive statistics. If correlation exceeds 0.85, consider using a composite index (actuarial present value of retirement = e_65 / expected working years) as an alternative to including both separately.

---

## 6. TFP Measurement

### 6.1 Source and Construction

The "non-global component of utilization-adjusted TFP" requires two steps:
1. Start from utilization-adjusted TFP series (Fernald 2014 for the US; Penn World Tables 10.0 TFP for cross-country; or national accounts-based measures from EU KLEMS or AMECO).
2. Decompose into global (common factor) and idiosyncratic components via a dynamic factor model or simple cross-sectional demeaning with time FEs.

Step 2 interacts with the estimation strategy: if CCE-MG already includes the cross-sectional average of TFP in x̄_t, then the TFP regressor in the structural equation should be the total series, and CCE-MG handles the factor extraction internally. Using a pre-filtered ã_it and then running CCE-MG is double-filtering — it removes too much common variation and may attenuate γ_TFP. **Recommendation:** Use total utilization-adjusted TFP in the baseline (not pre-filtered), and rely on CCE-MG or CupFM to separate global from idiosyncratic effects. Report the pre-filtered version as robustness.

### 6.2 Endogeneity of ã_it

The theory predicts ambiguous γ_TFP because higher TFP raises both savings (permanent income effect → more saving) and investment returns (more domestic investment → lower NFA). The net sign depends on whether the substitution effect (investment attraction) or income effect (richer country saves more) dominates. This is a legitimate structural ambiguity, not an identification failure.

However, there is a simultaneity concern: NIIP levels affect productivity via imported capital goods, technology transfer through FDI, or learning-by-doing in traded sectors. Countries with large positive NIIP (creditors) import capital, which raises TFP in trading partners. This creates a reverse causality channel from b_it to ã_it.

**Does CCE-MG/CupFM adequately address this?** Partially. CCE-MG and CupFM address CS dependence (global TFP shock correlated with global NIIP shifts) but not country-level reverse causality. The leads/lags correction in DOLS addresses serial correlation and weak endogeneity but requires strict exogeneity of ã_it in the long run — a strong assumption.

**Recommended IV robustness check:** Instrument ã_it with the adoption rate of frontier technologies (e.g., IT capital share, patent citations from frontier countries) which affects TFP but is plausibly uncorrelated with a country's NIIP position after controlling for income level. This is a feasibility check, not a requirement, but reviewers at top journals will ask for it.

---

## 7. Missing Pieces and Critical Gaps

### 7.1 Speed of Adjustment α_i: Identification

The ECM specifies α_i as country-specific, which is the mean-group approach. Identification of α_i separately from the cointegrating coefficients requires the cointegrating vector to be estimated from the levels equation, then the residual b_it - b*_it to be used as the error-correction term in the first-difference equation. This two-step procedure (Engle-Granger style, applied to panels) has well-known size distortions in small T.

**Alternative:** Use the Pesaran-Shin-Smith (1999) PMG estimator, which jointly estimates α_i and γ in one step. This is more efficient under long-run homogeneity. Test PMG vs. MG via the Hausman statistic. Report the distribution of α̂_i across countries — economically, a slow adjustment (α̂_i close to 0) for some countries may indicate capital controls or structural rigidities worth discussing.

### 7.2 Valuation Effects

The paper proposes decomposing val_it separately. The practical measurement challenge is:
- **Lane-Milesi-Ferretti (2007, updated 2018, 2022)** provide external wealth accounts with valuation adjustments. The decomposition is ΔNIIP_it = CA_it + val_it + residual.
- Econometrically: if NIIP is the dependent variable and val_it is positively correlated with the regressors (e.g., demographic wealth-rich countries also hold more foreign equities that appreciate during global booms), then not including val_it biases the γ estimates upward.
- **Recommended treatment:** Run the baseline on NIIP/GDP. Then re-run with NIIP adjusted for valuation (cumulative current account) as the dependent variable. The difference in γ estimates reveals the valuation channel. This is cleaner than trying to control for val_it on the right-hand side (which is endogenous).

### 7.3 Sample Design: Countries and Time Period

This is the most underspecified element. The OLG model's predictions are most relevant for:
- **Countries with functional capital markets** (so NIIP positions reflect intertemporal optimization, not capital controls).
- **Countries with reliable demographic data** (UN projections are less accurate for countries with large emigrant/immigrant flows or poor vital statistics registration).
- **Countries with sufficient time series** (panel cointegration requires T ≥ 30 in practice for reliable cointegration test power with CCE-MG).

**Recommended sample specification:**
- Baseline: 30-40 OECD/advanced economies, 1980-2022 (annual, T≈43).
- Extension 1: Add 15-20 major EMs (China, Brazil, India, Korea, Mexico, Indonesia, etc.) with shorter T.
- Extension 2: Full 80+ country sample to test whether OLG predictions generalize.
- Report Chow-type parameter stability tests across subsamples.

### 7.4 Bilateral Gravity Extension: PPML and Zeros in CPIS Data

The bilateral gravity extension using CPIS (Coordinated Portfolio Investment Survey) data faces:
- **Zeros are structural, not random.** Many country-pairs have zero bilateral portfolio holdings (no investment relationship), not small positive holdings rounded down. Santos-Silva & Tenreyro (2006) PPML handles zeros and heteroskedasticity, which makes it appropriate here.
- **But PPML identifies off multiplicative variation in non-zero cells.** If 60%+ of the matrix is zero (common in CPIS pre-2005), PPML estimates are identified off a selected subsample, which may not represent the extensive margin of investment decisions.
- **Recommended addition:** Heckman selection model (first stage: probability of non-zero position; second stage: log bilateral holdings) as a robustness check. Or a corner-solution Tobit with origin-time and destination-time FEs. Report the share of zeros in the estimation sample by year as a data characteristic.
- **Origin-time + destination-time FEs** are correctly specified (they absorb all push and pull factors in each period). But they are computationally expensive with a large N×T matrix. Use the HDFE ("high-dimensional fixed effects") Stata command or the `fixest` R package.

---

## 8. Three Priority Recommendations

### Priority 1 (Critical): Specify the Sample and Address Slope Heterogeneity Before Estimation

The entire estimator hierarchy presupposes a maintained sample and a decision about slope homogeneity. The current setup has neither. Without knowing whether the slope coefficients γ are homogeneous across countries, the DOLS/FMOLS benchmarks may be severely biased (Pesaran & Smith 1995 show that pooled estimators under heterogeneity converge to a random weighted average of true parameters — not the structural γ the OLG model predicts).

**Concrete action:** 
1. Define the country sample with explicit inclusion/exclusion criteria tied to the model (capital account openness, data quality, minimum T).
2. Run Pesaran-Yamagata (2008) Δ-test and report before the estimation table.
3. If heterogeneity is rejected, proceed with DOLS/FMOLS as benchmark. If not, lead with CCE-MG or AMG.

This priority is upstream of all other estimation choices.

### Priority 2 (High): Elevate CCE-MG to Co-Primary Estimator and Provide the Structural GE Interpretation

The CCE-MG estimator is not just a robustness check — it is the estimator that most cleanly maps to the OLG model's partial equilibrium prediction for country-idiosyncratic variation. The paper should argue this explicitly:

- CCE-MG identifies γ from within-factor (cross-country relative) variation in demographics, TFP, and debt.
- The CS average x̄_t absorbs the global factor, including the endogenous r*_t.
- The structural γ parameters in the two-country OLG model are precisely defined relative to symmetric equilibrium — i.e., they measure the effect of country i deviating from the world average.

**Concrete action:** Add a subsection in the empirical strategy titled "Structural Interpretation of CCE-MG" that spells out this mapping. This is a genuine conceptual contribution that most applications of CCE-MG to external imbalances miss. Referees will recognize it.

### Priority 3 (High): Operationalize and Test the Valuation Effects Decomposition

The valuation effects extension is currently described as an afterthought. It should be front-loaded as a methodological contribution, because:

- If valuation effects are large and correlated with demographics (older, wealthier countries hold more foreign equity and bonds that appreciate), then the benchmark γ estimates conflate savings behavior with portfolio composition effects.
- The decomposition (NIIP = cumulative CA + cumulative val) is available from the Lane-Milesi-Ferretti dataset and can be implemented cleanly.
- Reporting results with and without valuation adjustment provides a natural table (Panel A: total NIIP; Panel B: savings-driven NIIP; Panel C: valuation component) that strengthens the paper's contribution to the external imbalances literature.

**Concrete action:** Build the valuation-adjusted NIIP series from LMF data as a baseline input (not just an extension). Report it in the data description table alongside the raw NIIP/GDP series.

---

## Appendix: Checklist of Required Pre-Tests and Diagnostics

| Test | Purpose | Timing |
|------|---------|--------|
| Pesaran (2004) CD test on regressors | Check for CS dependence in x_it | Before estimation |
| IPS, Fisher-ADF, CIPS on each series | Unit-root pre-test | Before estimation |
| Pesaran-Yamagata (2008) Δ-test | Slope homogeneity | Before pooled estimation |
| Pedroni (1999, 2004) cointegration | No-cointegration null | Before ECM |
| Westerlund (2007) cointegration with bootstrap | Robust to CS dependence | Before ECM |
| CD test on cointegrating residuals | Validate cointegration under CS dependence | After long-run estimation |
| CIPS on cointegrating residuals | Validate I(0) residual | After long-run estimation |
| Hausman PMG vs. MG | Long-run homogeneity | After long-run estimation |
| F-test: time FEs vs. r*_t specification | Validity of r* proxy | In GE decomposition |
| Bai-Ng (2002) IC for number of factors | CupFM factor selection | Before CupFM/CupBC |
| VIF / pairwise correlation: φ_it vs. e_{65} | Multicollinearity check | Data description |

---

## References Implied by This Memo

- Bai, J., Kao, C., Ng, S. (2009). Panel cointegration with global stochastic trends. *Journal of Econometrics*.
- Bond, S., Eberhardt, M. (2009). Cross-section dependence in nonstationary panel models. *A novel estimator.*
- Chudik, A., Pesaran, M.H. (2015). Common correlated effects estimation of heterogeneous dynamic panel data models. *Journal of Econometrics*.
- Eberhardt, M., Bond, S. (2009). Cross-section dependence in nonstationary panel models. *MPRA Working Paper*.
- Fernald, J. (2014). A quarterly, utilization-adjusted series on total factor productivity. *San Francisco Fed Working Paper*.
- Holston, K., Laubach, T., Williams, J.C. (2017). Measuring the natural rate of interest. *Journal of International Economics*.
- Im, K., Pesaran, M.H., Shin, Y. (2003). Testing for unit roots in heterogeneous panels. *Journal of Econometrics*.
- Lane, P.R., Milesi-Ferretti, G.M. (2007, 2018, 2022). The external wealth of nations. IMF datasets.
- Maddala, G.S., Wu, S. (1999). A comparative study of unit root tests with panel data. *Oxford Bulletin of Economics and Statistics*.
- Pedroni, P. (1999, 2004). Panel cointegration: asymptotic and finite sample properties. *Econometric Theory* / *Oxford Bulletin*.
- Pesaran, M.H. (2004). General diagnostic tests for cross section dependence in panels. *Cambridge Working Paper*.
- Pesaran, M.H. (2006). Estimation and inference in large heterogeneous panels with a multifactor error structure. *Econometrica*.
- Pesaran, M.H. (2007). A simple panel unit root test in the presence of cross section dependence. *Journal of Applied Econometrics*.
- Pesaran, M.H., Shin, Y., Smith, R.P. (1999). Pooled mean group estimation of dynamic heterogeneous panels. *JASA*.
- Pesaran, M.H., Smith, R. (1995). Estimating long-run relationships from dynamic heterogeneous panels. *Journal of Econometrics*.
- Pesaran, M.H., Yamagata, T. (2008). Testing slope homogeneity in large panels. *Journal of Econometrics*.
- Santos-Silva, J.M.C., Tenreyro, S. (2006). The log of gravity. *Review of Economics and Statistics*.
- Stock, J.H., Watson, M.W. (1993). A simple estimator of cointegrating vectors in higher order integrated systems. *Econometrica*.
- Westerlund, J. (2007). Testing for error correction in panel data. *Oxford Bulletin of Economics and Statistics*.
