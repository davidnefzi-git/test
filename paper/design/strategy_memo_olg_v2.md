# Strategy Memo (v2): Net Foreign Assets, Demographics, and the Structural Determinants of External Imbalances
## A Two-Country OLG Approach — Revised Empirical Strategy

**Prepared by:** Strategist Agent (Round 2)
**Date:** 2026-05-19
**Memo type:** Pre-estimation strategy audit and enrichment — revised in response to strategist-critic Round 1 report (score 37/100)
**Supersedes:** `quality_reports/strategy_memo_olg.md`

---

## 1. Pre-Strategy Report

### 1.1 What Was Read for This Revision

1. `quality_reports/strategy_memo_olg.md` — Round 1 memo
2. `quality_reports/strategist_critic_report_olg.md` — critic's deductions (37/100, Reject)
3. `quality_reports/explorer_data_report_olg.md` — data availability and feasibility constraints
4. `.claude/rules/content-invariants.md` — design invariants binding on all agents

### 1.2 User Clarifications (Binding)

Two user clarifications received between Round 1 and Round 2 reshape this revision:

- **CL-1 (vintage UN WPP):** The vintage construction rule **is** in force. For each observation year $t$, the projection $\mathbb{E}_t[\phi_{i,t+H}]$ is drawn from the WPP edition published in year $t$ (or the most recent vintage available no later than $t$). Section 8 formalizes this rule. The critic's Critical Issue #3 (look-ahead bias) is therefore RESOLVED by construction; this memo documents the rule rather than re-litigating it.
- **CL-2 (drop bilateral gravity extension):** The CPIS bilateral portfolio extension is dropped from the present paper. The critic correctly identified that origin-time × destination-time fixed effects absorb all the OLG structural variation (demographics, TFP, debt) at the origin and destination separately, leaving no within-cell identification for the structural γ parameters. Section 11 records this as future work and explains the FE incompatibility.

### 1.3 Scope of the Revision

This v2 memo (i) addresses every deduction in the Round 1 critic report, (ii) preserves the conceptual contributions the critic flagged as strengths (the CCE-MG structural interpretation, the comprehensive pre-test checklist, the valuation-effects design, the estimator hierarchy), and (iii) folds in the additional improvements proposed during Round 1 (PMG/AMG/CS-ARDL, slope-homogeneity pre-test, front-loaded LMF valuation decomposition).

---

## 2. Paper Classification

This is a **Theory + Empirics** paper (Type III, theory-disciplined empirics). The cointegrating relation is derived from a two-country OLG model, not reverse-engineered from data. The structural commitments are:

- A linear cointegrating relation in the levels (or logs of levels) of NIIP/GDP and the OLG state variables.
- Sign restrictions over-identifying the model: $\gamma_1 > 0$ (income/creditor), $\gamma_2 < 0$ (current dependency depresses NIIP), $\gamma_3 > 0$ (anticipated aging raises precautionary saving), $\gamma_4 > 0$ (longer retirement raises saving), $\gamma_D < 0$ (Ricardian-type crowding out via public debt), and $\gamma_{TFP}$ ambiguous (income vs. substitution).
- A GE channel via the world real rate $r^\ast_t$, which is absorbed by time FEs in the benchmark and unpacked in the GE decomposition.
- An I(0) cointegrating residual $\varepsilon_{it}$ as a testable implication.

What the theory does **not** commit to: the speed of adjustment $\alpha_i$, the short-run ECM dynamics, the measurement of TFP, or the projection horizon $H$. These are empirical design choices made below.

---

## 3. Sample Design (NEW SECTION — addressing critic deduction on sample specificity)

### 3.1 Country Set

Building on the explorer's recommendation, the **baseline panel** is N ≈ 45 countries:

- **OECD/advanced economies (24):** US, Canada, UK, Japan, Australia, New Zealand, plus Germany, France, Italy, Spain, Netherlands, Belgium, Austria, Sweden, Denmark, Norway, Finland, Switzerland, Ireland, Portugal, Greece, Korea, Israel, Iceland.
- **Emerging Europe (5):** Czechia, Hungary, Poland, Slovenia, Slovakia.
- **Latin America (5):** Mexico, Brazil, Chile, Colombia, Peru.
- **Emerging Asia (6):** China, India, Indonesia, Malaysia, Thailand, Philippines.
- **Other EMs (5):** South Africa, Turkey, Saudi Arabia, Russia, Argentina.

**Exclusions:** Offshore financial centers (Luxembourg, Singapore, Hong Kong, Cayman Islands, Ireland-as-OFC checks), micro-states (population < 1 million), and countries with fewer than 20 annual NIIP observations.

### 3.2 Time Period

- **Baseline:** 1994–2023 (T = 30, annual). Begins after Bretton Woods II consolidation, captures Maastricht/EMU and 2008 GFC, post-COVID restoration.
- **Robustness extension:** 1985–2023 (T = 39). Drops sample down to ~30 countries with NIIP coverage; documents pre-1994 splicing in LMF.

### 3.3 Frequency

**Annual.** Five-year averages are rejected: they shrink T to 6, well below the T ≥ 30 rule of thumb for CCE-MG with r ≥ 3 latent factors. Annual frequency preserves cointegration test power; cyclical noise is absorbed in the ECM short-run dynamics (Section 7).

### 3.4 Source Priorities (from explorer report)

- NIIP/GDP: Lane–Milesi-Ferretti EWN (2022 update) as primary; IMF IIP as cross-check.
- Demographics: UN WPP, **vintage-matched** per Section 8.
- TFP: PWT 10.x `ctfp` as primary; EU-KLEMS 2023 for OECD sub-sample robustness.
- Public debt: IMF WEO `GGXWDG_NGDP`; HPDD/GDD as backup.
- $r^\ast$: Rachel & Summers (2019) extended with HLW for AE aggregate post-2019.
- Capital account openness: Chinn–Ito KAOPEN.
- Pension type: OECD Pensions at a Glance classification (PAYG vs. funded).

### 3.5 Sample Restrictions Tied to the Model

The OLG model presumes:

- **Frictionless capital mobility.** Operationalize with Chinn–Ito KAOPEN: include sample-restriction robustness dropping country-years with KAOPEN below its 25th percentile (low openness). See Section 9.2.
- **Private life-cycle saving as adjustment margin.** Operationalize with OECD pension classification: see Section 9.1.

---

## 4. Pre-Tests (EXPANDED — addressing I(2), CD on dependent variable, and structural breaks)

### 4.1 Unit-Root Tests at First Difference (I(1) maintained hypothesis)

For each variable in the cointegrating relation ($b_{it}$, $y_{it}$, $\phi_{it}$, $\mathbb{E}_t[\phi_{i,t+H}]$, $\mathbb{E}_t[e_{65,i,t+H}]$, $\tilde{a}_{it}$, $d^g_{it}$):

| Test | Citation | Handles CSD? | Reported |
|------|----------|-------------|----------|
| IPS | Im, Pesaran & Shin (2003) | No | Yes |
| Fisher-ADF | Maddala & Wu (1999) | No | Yes |
| CIPS | Pesaran (2007) | Yes | Yes (primary) |

### 4.2 I(2) Pre-Tests (NEW — addressing Critic CRITICAL Issue #1)

Old-age dependency ratios and life expectancy projections may evolve as I(2) processes over a 30–40 year sample (demographic transitions are slow-moving). DOLS and FMOLS are invalid for I(2) regressors. We therefore apply:

| Test | Citation | What It Tests |
|------|----------|---------------|
| IPS on first differences | Pesaran & Shin (1995) (test) / Im–Pesaran–Shin (2003) (panel) | If $\Delta x_{it}$ has a unit root, then $x_{it}$ is I(2) |
| Hadri stationarity | Hadri (2000) | Stationarity null; rejection at first differences implies I(2) |
| Lyhagen (2000) panel I(2) | Lyhagen (2000) | Panel I(2) factor structure |

**Decision rule:** If, for any structural regressor, both the level and first difference fail unit-root rejection (i.e., I(2) cannot be rejected), we adopt one of two responses:
1. **Pre-differencing.** Re-specify the cointegrating relation in first differences for the affected variable, with the implication that the level of NIIP is cointegrated with the differenced demographic variable.
2. **Johansen I(2) framework / Lyhagen (2000) extension.** Apply the I(2) cointegration framework with multicointegrating ranks.

The chosen response is documented and reported in the diagnostics table. This is upstream of DOLS/FMOLS.

### 4.3 Cross-Sectional Dependence

- Pesaran (2004/2021) CD test applied to: each regressor, the dependent variable $b_{it}$ (NEW — addressing critic Minor Issue #11), and the cointegrating residuals.
- Bias-corrected CD-LM and CD tests.

### 4.4 Slope Homogeneity

- Pesaran & Yamagata (2008) $\tilde\Delta$ and $\tilde\Delta_{adj}$ tests.
- Reported **before** any pooled estimator is presented. The conditional structure (lead with CCE-MG / AMG if heterogeneity is rejected; otherwise DOLS/FMOLS is the appropriate benchmark) is maintained from Round 1.

### 4.5 Cointegration

- Pedroni (1999, 2004) seven-statistic battery.
- Westerlund (2007) ECM-based tests with bootstrap (handles CSD).
- Gengenbach, Urbain & Westerlund (2016) for cointegration with factor structure.

### 4.6 Structural Break Tests (NEW — addressing critic Major Issue and internal inconsistency on Threat 5)

The sample spans multiple regimes (pre-/post-EMU 1999, pre-/post-GFC 2008, the commodity shock 2014, COVID 2020). The Round 1 memo flagged this but omitted any break test. We now include:

| Test | Citation | Scope |
|------|----------|-------|
| Bai–Perron multiple breaks | Bai & Perron (1998, 2003) | Time series of cointegrating residual averages; candidate breaks 1999, 2008, 2014, 2020 |
| Hansen cointegration breakdown | Hansen (2001) | Stability of cointegrating relation |
| Recursive CCE-MG | own implementation | Coefficient stability plots |
| Sub-period robustness | own implementation | 1994–2007, 2008–2023 splits |

Candidate break dates are pre-specified; the test results are reported regardless of outcome to forestall selective reporting.

### 4.7 Number of Common Factors

Bai & Ng (2002) information criteria ($IC_{p1}, IC_{p2}, IC_{p3}$) applied to the panel residuals to select the number of factors $r$ for CupFM/CupBC. We report robustness to $r \pm 1$.

---

## 5. Estimator Hierarchy (REVISED — corrected citations, CCE-MG as co-primary, full assumption statements)

### 5.1 Hierarchy

The estimator hierarchy is ordered from least to most robust to cross-sectional dependence and slope heterogeneity. Each estimator addresses an additional threat; the choice of primary estimator depends on which threats the pre-tests confirm.

| Estimator | Citation | Primary threat addressed | Key assumption |
|-----------|----------|--------------------------|----------------|
| Panel DOLS | Kao & Chiang (2000), Mark & Sul (2003) — extending Stock & Watson (1993) for time series | Endogeneity via leads/lags | CS independence; pooled slope |
| Panel FMOLS | Phillips & Moon (1999); Pedroni (2000) | Endogeneity + serial correlation | CS independence; pooled slope |
| **CCE-MG (co-primary)** | Pesaran (2006); Kapetanios, Pesaran & Yamagata (2011) | CS dependence via factor proxies | Factor structure; N ≫ r |
| CupFM / CupBC | Bai, Kao & Ng (2009) | CS dependence + factor-regressor correlation | Parametric factor structure; pre-specified $r$ |
| AMG | Eberhardt & Bond (2009 MPRA); Bond & Eberhardt (2013 OBES) | CS dependence; common dynamic process | Common dynamic process identifiable from first differences |
| PMG | Pesaran, Shin & Smith (1999) | Long-run homogeneity with short-run heterogeneity | Long-run pooling valid (Hausman test) |
| CS-ARDL | Chudik & Pesaran (2015) | Shorter T panels with CSD | Truncation lag $\lfloor T^{1/3} \rfloor$ on CS averages |

**Citation correction (addressing critic Major Issue #9).** Round 1 attributed panel DOLS directly to Stock & Watson (1993). Stock–Watson (1993) is the time-series DOLS estimator. The panel extension is properly attributed to **Kao & Chiang (2000)** (*Advances in Econometrics* 15) and **Mark & Sul (2003)** (*Oxford Bulletin* 65). Stock–Watson (1993) is cited as the theoretical foundation but not as the panel reference.

**AMG citation update.** Round 1 cited "Bond & Eberhardt (2009)". The MPRA working paper is Eberhardt & Bond (2009) MPRA 22281; the published version is Bond & Eberhardt (2013) *Oxford Bulletin* 75(2). Both are cited.

**CD test citation.** Pesaran (2004) Cambridge WP; published as Pesaran (2021) *Journal of Econometrics*. Both cited.

### 5.2 Stated Estimator Assumptions (NEW — addressing critic Major Issue #10)

For each estimator we state explicitly how implementation parameters are chosen:

| Estimator | Lag / bandwidth / factor rule | Source |
|-----------|------------------------------|--------|
| DOLS | Leads and lags selected by **BIC** within range $\{1, \ldots, \lfloor T^{1/3} \rfloor\}$; report sensitivity to AIC | Choi & Kurozumi (2012) |
| FMOLS | Long-run covariance kernel: Bartlett; bandwidth selected by **Andrews (1991)** automatic data-dependent procedure; sensitivity to Newey & West (1994) reported | Andrews (1991), Newey & West (1994) |
| CCE-MG | Cross-sectional averages of all regressors used as factor proxies; requires **N ≫ r**, rule of thumb N, T ≥ 30 (Chudik & Pesaran 2015 Monte Carlo) | Pesaran (2006) §5; Chudik & Pesaran (2015) |
| CupFM / CupBC | Number of factors $r$ chosen by **Bai & Ng (2002) IC_{p2}**; robustness to $r \pm 1$ | Bai, Kao & Ng (2009) |
| PMG | Long-run homogeneity tested by **Hausman PMG vs. MG**; ARDL(p,q) lag orders selected jointly by BIC | Pesaran, Shin & Smith (1999) |
| AMG | Common dynamic process estimated from first differences augmented with CS averages of dependent and independent variables | Eberhardt & Bond (2009) |
| CS-ARDL | Truncation lag for CS averages: $\lfloor T^{1/3} \rfloor$ | Chudik & Pesaran (2015) |

**Finite-sample acknowledgement (addressing critic Minor Issue #13).** With N ≈ 45 (baseline) and likely r = 3–4 latent factors (global business cycle, global demographic trend, global TFP, global fiscal cycle), the CCE-MG small-sample approximation may be imprecise. We cite Pesaran (2006) §5 Monte Carlo evidence and report CCE-MG bootstrap confidence intervals as a robustness check.

### 5.3 CCE-MG Structural Interpretation (PRESERVED from Round 1, with conditional statement added)

CCE-MG is co-primary because it cleanly maps to the OLG model's symmetric-equilibrium structure:

- CCE-MG identifies $\gamma$ from within-factor (cross-country relative) variation in demographics, TFP, and debt.
- The cross-sectional average $\bar x_t$ absorbs the global factor, including the endogenous $r^\ast_t$.
- The structural $\gamma$ parameters in the two-country OLG model measure precisely the effect of country $i$ deviating from the world average.

**Conditional statement (NEW — addressing critic Gap 2.3).** This interpretation holds *conditional on $r^\ast_t$ entering the error term as a linear function of the cross-sectional averages of the regressors*. The two-country symmetric OLG model satisfies this by construction; multi-country aggregation may not, since $r^\ast_t$ could be a nonlinear function of the cross-sectional distribution. We acknowledge the linearity assumption and report robustness with the AMG estimator, which uses a different functional form for the common dynamic process.

---

## 6. GE Channel Identification (REFINED — addressing critic Critical Issue #2 on interaction-term measurement error)

### 6.1 Specifications

We consider three specifications for the long-run cointegrating relation. The primary specification absorbs the GE channel via time FEs; the alternatives are diagnostic.

**Specification A (PRIMARY — absorbs GE channel):**

$$b_{it} = \mu_i + \lambda_t + \gamma_1 y_{it} + \gamma_2 \phi_{it} + \gamma_3 \mathbb{E}_t[\phi_{i,t+H}] + \gamma_4 \mathbb{E}_t[e_{65,i,t+H}] + \gamma_{TFP} \tilde a_{it} + \gamma_D d^g_{it} + \varepsilon_{it}$$

Time FEs $\lambda_t$ absorb $r^\ast_t$ and any other global factor. The $\gamma$ coefficients are partial equilibrium effects of country-idiosyncratic variation.

**Specification B (CO-PRIMARY — CCE-MG):**

Same structural variables, with time FEs replaced by cross-sectional averages $\bar b_t$, $\bar y_t$, $\bar \phi_t$, $\bar{\mathbb{E}_t[\phi_{t+H}]}$, $\bar{\mathbb{E}_t[e_{65,t+H}]}$, $\bar{\tilde a_t}$, $\bar{d^g_t}$. Heterogeneous slopes, mean-grouped.

**Specification C (DIAGNOSTIC ONLY — total effect via $r^\ast$):**

$$b_{it} = \mu_i + \gamma_1 y_{it} + \gamma_2 \phi_{it} + \gamma_3 \mathbb{E}_t[\phi_{i,t+H}] + \gamma_4 \mathbb{E}_t[e_{65,i,t+H}] + \gamma_{TFP} \tilde a_{it} + \gamma_D d^g_{it} + \beta_r r^\ast_t + \beta_{r\phi} (r^\ast_t \cdot \phi_{it}) + \beta_{rD} (r^\ast_t \cdot d^g_{it}) + \nu_{it}$$

### 6.2 Why Specification C Is Demoted to Diagnostic (NEW — addressing critic Critical Issue #2)

The critic correctly identified that **measurement error in $r^\ast_t$ amplifies non-linearly when entered as an interaction**. Specifically, if observed $r^\ast_t = r^{\ast,\text{true}}_t + \eta_t$ with $\mathbb{E}[\eta_t] = 0$ and $\text{Var}(\eta_t) > 0$, and if $\eta_t$ is correlated with $\phi_{it}$ (which it is, since older countries lower world rates), then the interaction term $r^\ast_t \cdot \phi_{it}$ carries bias of the form

$$\text{plim}\,\hat\beta_{r\phi} = \beta_{r\phi}^{\text{true}} \cdot \frac{\text{Var}(r^{\ast,\text{true}}_t)}{\text{Var}(r^{\ast,\text{true}}_t) + \text{Var}(\eta_t)} + \frac{\text{Cov}(\eta_t, \phi_{it} \cdot \eta_t)}{\text{Var}(r^\ast_t \cdot \phi_{it})}$$

The second term is non-attenuating and can be of either sign — see Bound, Brown & Mathiowetz (2001) on interaction-term measurement error. Standard errors-in-variables corrections that attenuate the levels coefficient do not correct the interaction coefficient.

**Two mitigations (NEW), applied to Specification C only:**

1. **IV approach.** Instrument $r^\ast_t$ with global demographic averages from UN WPP, **lagged**, and global TFP from PWT, lagged. These instruments shift $r^\ast_t$ through structural channels and are predetermined relative to current measurement noise $\eta_t$. The instruments are then interacted with $\phi_{it}$ and $d^g_{it}$ to form the IV moment conditions for the interaction terms.
2. **Report Specification C as DIAGNOSTIC only.** Specification C is reported as a check on whether the GE channel sign is consistent with theory, not as a primary estimate. The primary structural interpretation rests on Specifications A (time FEs) and B (CCE-MG), which avoid the interaction-error problem by absorbing the GE channel.

### 6.3 What Specification C Identifies When Validly Estimated

Per Round 1, the interaction $r^\ast_t \cdot \phi_{it}$ identifies the **heterogeneous loading on a common factor** — i.e., whether countries with higher current dependency are more or less sensitive to global rate movements — not the structural derivative $\partial r^\ast / \partial \phi_{it}$ itself. This precise interpretation is preserved.

### 6.4 Validity Check: F-Test for r* vs. Time FEs

Following Round 1, we test the joint significance of time FEs $\lambda_t$ after conditioning on $r^\ast_t$ and its interactions. Failure to reject suggests $r^\ast_t$ adequately proxies the global factor; rejection suggests residual global shocks remain unexplained and Specification A (time FEs) should be preferred.

---

## 7. ECM and Speed of Adjustment

### 7.1 ECM Form

For each country $i$, with $\tilde b_{it}$ the cointegrating residual from the long-run estimation:

$$\Delta b_{it} = \alpha_i \tilde b_{i,t-1} + \sum_{j=1}^{p} \delta_{ij}^b \Delta b_{i,t-j} + \sum_{k} \sum_{j=0}^{q_k} \theta_{ij}^{x_k} \Delta x_{k,i,t-j} + u_{it}$$

Lag orders $p, q_k$ selected by **BIC** with maximum lag $\lfloor T^{1/3} \rfloor$. The Granger Representation Theorem guarantees existence of this ECM when cointegration holds; lag selection is a finite-sample optimization (addressing critic Gap 2.7).

### 7.2 Identification of $\alpha_i$

We use **PMG (Pesaran, Shin & Smith 1999)** as the primary one-step estimator, which jointly estimates $\alpha_i$ and the long-run $\gamma$ vector. **Hausman test PMG vs. MG** evaluates the long-run homogeneity restriction. If Hausman rejects, fall back to two-step Engle–Granger ECM with bias correction.

The distribution of $\hat\alpha_i$ across countries is reported; slow adjustment (small $|\hat\alpha_i|$) is interpreted as evidence of capital controls or structural rigidities. Cross-checked against KAOPEN (Section 9.2).

---

## 8. Vintage WPP Construction Rule (NEW SECTION — formalizes the user clarification CL-1)

### 8.1 The Rule

For each observation year $t$ and each country $i$:

$$\mathbb{E}_t[\phi_{i,t+H}] := \text{WPP projection of } \phi_{i,t+H} \text{ taken from the WPP edition published in year } t,$$

or, if no WPP edition was published in year $t$, the most recent edition published in year $t' \leq t$.

Analogously for $\mathbb{E}_t[e_{65,i,t+H}]$.

### 8.2 Why This Resolves Look-Ahead Bias

Under this rule, the explanatory variable at date $t$ uses information available at $t$ and no information from $t+1, t+2, \ldots$. Therefore, the expectation operator $\mathbb{E}_t[\cdot]$ reflects the information set $\mathcal{F}_t$ of an econometrician living in year $t$, not the modern researcher's hindsight. This eliminates look-ahead bias (critic Critical Issue #3 — RESOLVED).

### 8.3 Operational Vintage Map

Per the explorer's report, WPP vintages are published every 2 years from 1980 (with gaps). The following mapping is applied:

| Observation year $t$ | WPP vintage used |
|-----------|---------------------------|
| 1994–1995 | WPP 1994 |
| 1996–1997 | WPP 1996 |
| 1998–1999 | WPP 1998 |
| 2000–2001 | WPP 2000 |
| 2002–2003 | WPP 2002 |
| 2004–2005 | WPP 2004 |
| 2006–2007 | WPP 2006 |
| 2008–2009 | WPP 2008 |
| 2010–2011 | WPP 2010 |
| 2012–2013 | WPP 2012 |
| 2014–2016 | WPP 2015 |
| 2017–2018 | WPP 2017 |
| 2019–2021 | WPP 2019 |
| 2022–2023 | WPP 2022 |

Pre-2000 vintages are PDF-only at country level (explorer Section B1); for these we rely on the Wittgenstein Centre human-capital reconstructions cross-checked against PDF extractions for the OECD subset. The pre-2000 panel is a robustness extension, not the baseline.

### 8.4 Projection Horizon $H$

- **Baseline:** $H = 20$ years. UN mortality projections are most reliable at this horizon; fertility uncertainty is moderate.
- **Sensitivity:** Report $\gamma_3, \gamma_4$ across $H \in \{10, 15, 20, 25, 30\}$. The OLG model predicts an inverted-U shape in $|\gamma_3|$ as $H$ varies (preserved from Round 1 Section 5.2).

### 8.5 Multicollinearity Check $\phi_{it}$ vs. $\mathbb{E}_t[e_{65,i,t+H}]$

VIF and pairwise correlation reported in descriptive statistics. If correlation exceeds 0.85, use composite index (actuarial PV of retirement = $e_{65}/$ expected working years) as alternative regressor (preserved from Round 1).

---

## 9. Robustness Checks (EXPANDED — addressing critic Major Issues on pension type, capital openness, expectations formation, currency composition)

### 9.1 Pension System Type (NEW — addressing critic Major Issue #5)

The OLG savings mechanics are implicitly conditioned on **private** life-cycle saving being the dominant adjustment margin. Countries with generous pay-as-you-go (PAYG) pension systems mechanically offset demographic effects on private NIIP: governments accumulate (off-balance-sheet) pension liabilities that do not appear in NIIP.

**Implementation:**

- **Source:** OECD Pensions at a Glance — classifies each country's mandatory pillar as PAYG (defined-benefit, financed by current contributions), funded (defined-contribution, financed by accumulated assets), or mixed.
- **Specification:** Construct a country-level **PAYG dummy** (PAYG share of mandatory pension > 70%) and **pension replacement rate** (mandatory replacement rate, OECD data).
- **Robustness:** Interact $\phi_{it}$ and $\mathbb{E}_t[\phi_{i,t+H}]$ with the PAYG dummy. The OLG prediction is that $\gamma_2, \gamma_3$ are attenuated for PAYG-dominant countries.
- Sub-sample robustness: re-estimate on funded-dominant countries only (Australia, Chile, Denmark, Netherlands, Switzerland) and compare $\gamma_2, \gamma_3$ to baseline.

### 9.2 Capital Account Openness (NEW — addressing critic Major Issue #7)

The OLG model presumes frictionless capital mobility; binding capital controls violate this.

**Implementation:**

- **Source:** Chinn & Ito (2008, updated annually) KAOPEN index.
- **Sample restriction:** Robustness sample drops country-years with KAOPEN below the 25th percentile of its country-year distribution. Threshold pre-specified.
- **Interaction:** Re-estimate baseline interacting key regressors ($y_{it}$, $\phi_{it}$, $d^g_{it}$) with continuous KAOPEN. Test whether the OLG predictions strengthen with openness.

### 9.3 Expectations Formation (NEW — addressing critic Major Issue #8)

The vintage WPP construction (Section 8) imposes that agents know UN demographic projections — a form of rational expectations. The Round 1 memo did not test sensitivity to this assumption.

**Implementation:**

- **Adaptive expectations alternative:** Replace $\mathbb{E}_t[\phi_{i,t+H}]$ with $\bar\phi_{i,t}^{\text{MA}} = $ five-year moving average of $\phi_{i,t-4}, \ldots, \phi_{i,t}$. This is the "current-trend extrapolation" benchmark.
- **AR(1) extrapolation alternative:** Estimate country-specific AR(1) on $\phi_{it}$, project $H$ periods forward.
- **Robustness table:** Report $\gamma_3$ under (i) rational expectations (vintage WPP), (ii) adaptive (MA), (iii) AR(1). Large differences in $\hat\gamma_3$ signal sensitivity to the expectations assumption.

### 9.4 Currency Composition of NIIP

NIIP is reported by LMF in US dollars and as a share of GDP. Exchange-rate-driven NIIP movements introduce mechanical correlation with $y_{it}$ and $\phi_{it}$ via valuation effects on foreign-currency assets.

**Implementation:**

- **Source:** LMF EWN provides NIIP in USD and as % of GDP at current and PPP exchange rates.
- **Robustness:** Re-estimate with NIIP/GDP at PPP exchange rates. Compare $\gamma$ estimates.

### 9.5 TFP Endogeneity: Wu–Hausman Test (NEW — addressing critic Major Issue #10 / Gap 3.4)

Round 1 raised TFP simultaneity concerns but proposed no concrete test.

**Implementation:**

- **First-stage instruments for $\tilde a_{it}$:** IT capital share (PWT `csh_i`), patent citations from frontier countries (USPTO data via Acemoglu et al. 2018), TFP growth in trading partners weighted by trade shares.
- **Wu–Hausman test:** Compare DOLS estimates with and without instrumented TFP. Rejection signals significant endogeneity bias.
- **Report 2SLS-DOLS** (Choi & Kurozumi 2012) estimates alongside the baseline.

### 9.6 Sub-Sample Splits

- AE-only sub-sample (24 countries; EU-KLEMS TFP available).
- EM-only sub-sample (21 countries).
- Pre-/post-GFC: 1994–2007 vs. 2008–2023.
- Pre-/post-EMU: 1994–1998 vs. 1999–2023.

### 9.7 Pre-Filtered TFP

Pre-filtered $\tilde a_{it}$ (subtracting the first PC of cross-country `ctfp`) reported as robustness check on the CCE-MG baseline, with the explicit caveat (preserved from Round 1) that pre-filtering before CCE-MG is double-filtering and likely to attenuate $\gamma_{TFP}$.

---

## 10. Valuation Effects: Front-Loaded as Baseline Input (PRESERVED + ELEVATED)

### 10.1 The Decomposition

From the LMF EWN identity:

$$\Delta \text{NIIP}_{it} = \text{CA}_{it} + \text{VAL}_{it} + \text{KA}_{it} + \text{EOM}_{it}$$

The cumulated-CA NIIP is the **savings-driven NIIP**:

$$\text{NIIP}^{\text{sav}}_{it} = \text{NIIP}_{i,t_0} + \sum_{s=t_0+1}^{t} \text{CA}_{is}$$

The valuation component is $\text{VAL}^{\text{cum}}_{it} = \text{NIIP}_{it} - \text{NIIP}^{\text{sav}}_{it}$.

### 10.2 Why Front-Loading Matters

If valuation effects are large and correlated with demographics (older, wealthier countries hold more foreign equity that appreciates during global booms), benchmark $\gamma$ estimates conflate savings behavior with portfolio composition effects.

### 10.3 Three-Panel Table Structure

The valuation-decomposed estimates form a baseline table, not an extension:

- **Panel A:** Dependent variable = total NIIP/GDP (LMF series).
- **Panel B:** Dependent variable = savings-driven NIIP/GDP (cumulated CA).
- **Panel C:** Dependent variable = cumulative valuation component.

Difference between Panels A and B isolates the valuation channel.

### 10.4 Pre-2001 Caveat

Per the explorer report (Critical Gap 3), the LMF decomposition is residual-based pre-2001 and absorbs KA and EOM. The 1994–2000 portion of the panel uses a noisier decomposition; we test sensitivity by restricting the valuation analysis to 2001–2023.

---

## 11. Extensions (PRUNED — bilateral gravity DROPPED per user clarification CL-2)

### 11.1 Global Imbalances Decomposition (RETAINED)

Following the Round 1 design, we decompose the contribution of each structural factor to cumulative global current account imbalances 1994–2023. Methodology: counterfactual NIIP series holding each $x_{k,it}$ at its 1994 value, evaluating the implied $\Delta b_{it}$, summing across countries. This is the explicit aggregate counterpart of the panel estimates.

### 11.2 Bilateral Gravity Extension — DROPPED (addressing critic Major Issue #6 and user clarification CL-2)

**Why the extension is dropped from the present paper:**

The Round 1 memo proposed estimating bilateral portfolio positions from CPIS data with origin-time and destination-time fixed effects. The critic correctly observed that these FEs absorb all the OLG structural variation (current dependency $\phi_{it}$, anticipated dependency $\mathbb{E}_t[\phi_{i,t+H}]$, TFP $\tilde a_{it}$, and public debt $d^g_{it}$) for origin and destination separately. The residual variation is pair-level demographic *differentials*, which the OLG model does not directly speak to (the two-country symmetric OLG model predicts net positions, not bilateral allocations).

To identify the same structural parameters in a bilateral framework would require either (i) pair-level FEs only (losing the multilateral resistance interpretation), or (ii) bilateral demographic differential terms ($\phi_{it} - \phi_{jt}$, etc.) entered alongside the FEs — but the latter is collinear by construction with the FE structure.

**Future-work note:** A separate paper could test pair-level OLG predictions using bilateral differentials with Heckman selection for CPIS zeros (per Round 1 Section 7.4). That is a distinct research design and is not pursued here.

### 11.3 Alternative Extension (RETAINED / OPTIONAL)

A useful and tractable extension is the **TFP decomposition extension**: separate the country-specific TFP component $\tilde a_{it}$ into a frontier-distance component (gap to US TFP) and a within-frontier component, and test whether the income/substitution sign of $\gamma_{TFP}$ depends on the country's position relative to the frontier. This sharpens the structural ambiguity in $\gamma_{TFP}$ flagged in Section 2.

---

## 12. Threats Table

| # | Threat | Source / Mechanism | Mitigation in this design |
|---|--------|-------------------|---------------------------|
| T1 | CS dependence in regressors and dependent variable | Global business cycle, common demographics | CIPS + CD tests; CCE-MG / AMG / CupFM as primary |
| T2 | Slope heterogeneity | Different countries at different demographic stages | Pesaran–Yamagata $\tilde\Delta$ test; lead with CCE-MG if heterogeneity not rejected |
| T3 | I(2) demographics | Slow-moving demographic transition | I(2) pre-tests (IPS on differences, Hadri, Lyhagen); pre-difference or Johansen I(2) if not rejected |
| T4 | Endogeneity of TFP $\tilde a_{it}$ | NIIP → capital imports → TFP feedback | Wu–Hausman test; IV-DOLS with frontier-tech instruments |
| T5 | Measurement error in $\mathbb{E}_t[\phi]$ | UN projection errors (fertility/longevity) | Attenuation bias against finding predicted sign; vintage-matched per Section 8 |
| T6 | Look-ahead bias in vintage projections | Using 2024 WPP for 1994 obs | RESOLVED by vintage construction rule (Section 8) |
| T7 | Structural breaks | EMU 1999, GFC 2008, commodity 2014, COVID 2020 | Bai–Perron + Hansen tests; sub-period splits |
| T8 | Capital controls violate frictionless capital | Some EMs binding | KAOPEN restriction; interaction with key regressors |
| T9 | PAYG pension systems offset demographic effect | Government absorbs life-cycle saving | OECD pension classification; PAYG dummy interaction |
| T10 | Expectations formation assumption | Rational expectations may not hold | Adaptive / AR(1) expectations as robustness |
| T11 | $r^\ast$ measurement error compounds in interactions | Non-attenuating bias in Specification C | Spec C demoted to diagnostic; IV with lagged global factors |
| T12 | Currency composition | FX-driven NIIP movements not structural | PPP-NIIP robustness |
| T13 | Valuation effects conflate savings and portfolio | Equity-rich older countries during booms | Three-panel table: total / savings-driven / valuation NIIP |
| T14 | Multicollinearity $\phi$ vs $e_{65}$ | Aging correlated with longevity | VIF + composite index alternative |
| T15 | CCE-MG finite-sample with N ≈ 45, r = 3–4 | Approximation imprecision | Bootstrap CIs; AMG cross-check |

---

## 13. Pre-Tests and Diagnostics Checklist (≥ 15 items)

| # | Test | Purpose | Timing | Citation |
|---|------|---------|--------|----------|
| 1 | Pesaran CD test on each regressor | CSD in $x_{it}$ | Before estimation | Pesaran (2004/2021) |
| 2 | **Pesaran CD test on $b_{it}$** (NEW) | CSD in dependent variable | Before estimation | Pesaran (2004/2021) |
| 3 | IPS, Fisher-ADF on each series | I(1) test | Before estimation | Im–Pesaran–Shin (2003); Maddala–Wu (1999) |
| 4 | CIPS on each series | I(1) test under CSD | Before estimation | Pesaran (2007) |
| 5 | **IPS / Hadri at first difference** (NEW) | I(2) test | Before estimation | Hadri (2000); Pesaran–Shin (1995) |
| 6 | **Lyhagen panel I(2)** (NEW) | I(2) factor structure | Before estimation | Lyhagen (2000) |
| 7 | Pesaran–Yamagata $\tilde\Delta$, $\tilde\Delta_{adj}$ | Slope homogeneity | Before pooled estimation | Pesaran–Yamagata (2008) |
| 8 | Pedroni seven statistics | Cointegration | Before ECM | Pedroni (1999, 2004) |
| 9 | Westerlund bootstrap | Cointegration under CSD | Before ECM | Westerlund (2007) |
| 10 | Bai–Ng IC$_{p2}$ | Number of factors | Before CupFM | Bai–Ng (2002) |
| 11 | **Bai–Perron multiple breaks** (NEW) | Structural breaks 1999/2008/2014/2020 | Before estimation | Bai–Perron (1998, 2003) |
| 12 | **Hansen cointegration breakdown** (NEW) | Stability of cointegrating relation | Before estimation | Hansen (2001) |
| 13 | CD on cointegrating residuals | Validate cointegration | After estimation | Pesaran (2004/2021) |
| 14 | CIPS on residuals | I(0) of residual | After estimation | Pesaran (2007) |
| 15 | Hausman PMG vs. MG | Long-run homogeneity | After estimation | Pesaran–Shin–Smith (1999) |
| 16 | F-test: $\lambda_t$ vs. $r^\ast_t$ specification | Validity of r* proxy | In Specification C | own |
| 17 | **Wu–Hausman on TFP** (NEW) | TFP endogeneity | Robustness | Wooldridge (2010) Ch. 6 |
| 18 | VIF and pairwise corr $\phi$ vs $e_{65}$ | Multicollinearity | Data description | own |
| 19 | Recursive CCE-MG coefficient plots | Coefficient stability | Diagnostic | own |

---

## 14. Three Priority Recommendations (UPDATED)

### Priority 1: Lock the Sample and Run the Pre-Test Battery Before Any Estimation

Sample (Section 3), pre-tests (Section 4) — especially the I(2) tests and slope-homogeneity test — must be completed before any γ is estimated. The choice of primary estimator (DOLS/FMOLS vs. CCE-MG vs. AMG vs. PMG) is conditional on pre-test outcomes. This is upstream of everything else.

### Priority 2: Treat CCE-MG as Co-Primary Structural Estimator with the Linearity Caveat

CCE-MG with the structural interpretation is co-primary alongside the time-FE specification, with the explicit conditional that $r^\ast_t$ enters the error as a linear function of cross-sectional averages of the regressors. AMG (with a different functional form for the common dynamic process) provides the robustness check on linearity.

### Priority 3: Implement the Valuation Decomposition as a Three-Panel Baseline (Total / Savings-Driven / Valuation)

Section 10. The valuation decomposition is not an extension — it is part of the baseline table. The three-panel structure (total NIIP, savings-driven NIIP, valuation NIIP) is the most natural way to communicate that the structural γ parameters apply to the savings-driven NIIP and that the valuation channel is itself estimable and economically interesting.

---

## 15. References (Corrected)

- Andrews, D.W.K. (1991). Heteroskedasticity and autocorrelation consistent covariance matrix estimation. *Econometrica* 59(3), 817–858.
- Bai, J. (2009). Panel data models with interactive fixed effects. *Econometrica* 77(4), 1229–1279.
- Bai, J., Kao, C., Ng, S. (2009). Panel cointegration with global stochastic trends. *Journal of Econometrics* 149, 82–99.
- Bai, J., Ng, S. (2002). Determining the number of factors in approximate factor models. *Econometrica* 70(1), 191–221.
- Bai, J., Perron, P. (1998). Estimating and testing linear models with multiple structural changes. *Econometrica* 66(1), 47–78.
- Bai, J., Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics* 18, 1–22.
- Bond, S., Eberhardt, M. (2013). Accounting for unobserved heterogeneity in panel time series models. *Oxford Bulletin of Economics and Statistics* 75(2), 220–246. [Published version of Eberhardt & Bond (2009) MPRA 22281.]
- Bound, J., Brown, C., Mathiowetz, N. (2001). Measurement error in survey data. In *Handbook of Econometrics* Vol. 5, Ch. 59. [Cited for interaction-term measurement-error bias.]
- Chinn, M.D., Ito, H. (2008). A new measure of financial openness. *Journal of Comparative Policy Analysis* 10(3), 309–322. [KAOPEN index, updated annually.]
- Choi, I., Kurozumi, E. (2012). Model selection criteria for the leads-and-lags cointegrating regression. *Journal of Econometrics* 169, 224–238.
- Chudik, A., Pesaran, M.H. (2015). Common correlated effects estimation of heterogeneous dynamic panel data models with weakly exogenous regressors. *Journal of Econometrics* 188(2), 393–420.
- Eberhardt, M., Bond, S. (2009). Cross-section dependence in nonstationary panel models: a novel estimator. *MPRA Working Paper 22281*.
- Fernald, J. (2014). A quarterly, utilization-adjusted series on total factor productivity. *Federal Reserve Bank of San Francisco Working Paper* 2012-19.
- Gengenbach, C., Urbain, J.-P., Westerlund, J. (2016). Error correction testing in panels with common stochastic trends. *Journal of Applied Econometrics* 31(6), 982–1004.
- Hadri, K. (2000). Testing for stationarity in heterogeneous panel data. *Econometrics Journal* 3, 148–161.
- Hansen, B.E. (2001). The new econometrics of structural change. *Journal of Economic Perspectives* 15(4), 117–128.
- Holston, K., Laubach, T., Williams, J.C. (2017). Measuring the natural rate of interest: International trends and determinants. *Journal of International Economics* 108, S59–S75.
- Im, K., Pesaran, M.H., Shin, Y. (2003). Testing for unit roots in heterogeneous panels. *Journal of Econometrics* 115, 53–74.
- Kao, C., Chiang, M.-H. (2000). On the estimation and inference of a cointegrated regression in panel data. *Advances in Econometrics* 15, 179–222. [Primary panel DOLS reference.]
- Kapetanios, G., Pesaran, M.H., Yamagata, T. (2011). Panels with non-stationary multifactor error structures. *Journal of Econometrics* 160, 326–348.
- Lane, P.R., Milesi-Ferretti, G.M. (2007, 2018). The external wealth of nations revisited. *IMF Economic Review* and *Journal of International Money and Finance*.
- Lyhagen, J. (2000). Why not use standard panel unit root test for testing PPP. *Working Paper, Stockholm School of Economics*. [Panel I(2) extension.]
- Maddala, G.S., Wu, S. (1999). A comparative study of unit root tests with panel data. *Oxford Bulletin of Economics and Statistics* 61, 631–652.
- Mark, N.C., Sul, D. (2003). Cointegration vector estimation by panel DOLS and long-run money demand. *Oxford Bulletin of Economics and Statistics* 65, 655–680. [Primary panel DOLS reference.]
- Newey, W.K., West, K.D. (1994). Automatic lag selection in covariance matrix estimation. *Review of Economic Studies* 61, 631–653.
- Pedroni, P. (1999). Critical values for cointegration tests in heterogeneous panels with multiple regressors. *Oxford Bulletin of Economics and Statistics* 61, 653–670.
- Pedroni, P. (2000). Fully modified OLS for heterogeneous cointegrated panels. *Advances in Econometrics* 15, 93–130.
- Pedroni, P. (2004). Panel cointegration: Asymptotic and finite sample properties of pooled time series tests with an application to the PPP hypothesis. *Econometric Theory* 20, 597–625.
- Pesaran, M.H. (2004). General diagnostic tests for cross section dependence in panels. *Cambridge Working Paper in Economics 0435*.
- Pesaran, M.H. (2006). Estimation and inference in large heterogeneous panels with a multifactor error structure. *Econometrica* 74(4), 967–1012.
- Pesaran, M.H. (2007). A simple panel unit root test in the presence of cross-section dependence. *Journal of Applied Econometrics* 22, 265–312.
- Pesaran, M.H. (2021). General diagnostic tests for cross-sectional dependence in panels. *Empirical Economics* / published version of Pesaran (2004).
- Pesaran, M.H., Shin, Y. (1995). An autoregressive distributed lag modelling approach to cointegration analysis. *DAE Working Paper 9514, University of Cambridge*. [Cited for IPS at second-difference panel I(2) test.]
- Pesaran, M.H., Shin, Y., Smith, R.P. (1999). Pooled mean group estimation of dynamic heterogeneous panels. *Journal of the American Statistical Association* 94, 621–634.
- Pesaran, M.H., Smith, R. (1995). Estimating long-run relationships from dynamic heterogeneous panels. *Journal of Econometrics* 68, 79–113.
- Pesaran, M.H., Yamagata, T. (2008). Testing slope homogeneity in large panels. *Journal of Econometrics* 142, 50–93.
- Phillips, P.C.B., Moon, H.R. (1999). Linear regression limit theory for nonstationary panel data. *Econometrica* 67, 1057–1111.
- Rachel, L., Smith, T.D. (2015). Secular drivers of the global real interest rate. *Bank of England Staff Working Paper 571*.
- Rachel, L., Summers, L.H. (2019). On secular stagnation in the industrialized world. *Brookings Papers on Economic Activity* Spring, 1–54.
- Stock, J.H., Watson, M.W. (1993). A simple estimator of cointegrating vectors in higher order integrated systems. *Econometrica* 61, 783–820. [Time-series DOLS; theoretical foundation only.]
- Westerlund, J. (2007). Testing for error correction in panel data. *Oxford Bulletin of Economics and Statistics* 69, 709–748.
- Wooldridge, J.M. (2010). *Econometric Analysis of Cross Section and Panel Data*, 2nd ed., MIT Press. [Wu–Hausman test.]
