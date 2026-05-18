# Strategy Memo
## Paper: "Inside Synthetic Dollar Liquidity and the Microstructure of FX Swap Markets"
## Agent: Strategist | Date: 2026-05-18

---

## Revision Log

| Round | Date | Changes | Anticipated Score |
|-------|------|---------|-------------------|
| Round 2 | 2026-05-18 | B1: Added no-stigma assumption paragraph for swap line event study (P5); B2: Added σ ≤ 1 failure-mode paragraph for run mechanism (Task 1, σ section); B3a: Added exclusion restriction paragraph for interaction instrument (Task 4, P2 row); B3b: Added pre-trend diagnostic item to robustness plan | 81–83/100 |

---

## Pre-Strategy Report

### Documents Read

| Document | Path | Status |
|----------|------|--------|
| Theoretical framework | `paper/theory/sections/inside-synthetic-dollar.tex` | Read — 415 lines, 15 sections |
| Empirical design v8 | `paper/design/empirical-roadmap-v8.md` | Read — 448 lines, 13 sections |
| Explorer feasibility assessment (Phase 1) | `quality_reports/explorer/feasibility-assessment.md` | Read — 367 lines, R2 revision at 68/100 |
| Explorer-Critic Round 2 review | `quality_reports/explorer/explorer-critic-review-r2.md` | NOT FOUND — file does not exist |

**Missing input:** The Explorer-Critic Round 2 review file was not found at the specified path. The feasibility-assessment.md is itself the R2-revised document (revised from 72 → 68/100 following critic feedback per its revision log), so the substantive content of the critic's Round 2 findings is embedded in that document. The strategy memo proceeds from the R2-revised feasibility assessment as the operative input, noting that the separate critic review file is absent.

### Summary of Inputs

**Theory document:** A 15-section framework in French combining (1) a CES dollar liquidity aggregator with quality parameter $q_t$, (2) a Cobb-Douglas search-and-matching function for conversion, (3) intermediary capacity decomposition by institution type, (4) six formal propositions, and (5) a Koijen-Yogo-style demand system. The core conceptual contribution is the inside/outside dollar liquidity distinction and the run-from (not run-against) framing. No formal proofs are present — the current draft is a first-pass framework sketch.

**Empirical design v8:** A nine-prediction, five-approach design centered on bilateral regulatory FX swap transaction data. Primary identification: shift-share IV (MMF funding shocks × pre-determined currency-pair exposure) for the demand-pressure → price-impact channel. Secondary: demand system estimation (Koijen-Yogo linearized) for structural decomposition and counterfactuals.

**Feasibility assessment (R2):** Overall score 68/100. Core data (bilateral FX transaction data) not yet in hand (6–18 months access). Outcome variable (PriceUSD = −TIB) grades A. Demand variable ($Q_{FB}$) grades B−. Capacity variable ($B_t$) grades C. P1 and P4 downgraded to Partial. P3 assessed as Not Testable with current design.

---

## Paper Classification

**Primary type: Theory + Empirics**

The paper makes two distinct contributions that each require dedicated methodology:

1. **Theoretical contribution:** A search-and-matching model of FX swap market intermediation, embedded in a CES dollar liquidity aggregator, generating six propositions about how demand pressure, intermediary capacity, and institutional structure determine the synthetic dollar premium. This is a genuine theoretical contribution, not merely a motivating framework — the model has a formal equilibrium definition (Section 10), an endogenous quality variable, a matching externality amplification mechanism, and structural counterfactuals.

2. **Empirical contribution:** A causal reduced-form design (shift-share IV) that tests the central proposition ($\partial\mu_t/\partial U_t > 0$) using bilateral regulatory microstructure data, plus a structural demand system estimation that enables counterfactual decomposition.

**Secondary type: Descriptive / measurement.** Part 2 of the paper ("Microstructure bilatérale") is a standalone measurement contribution documenting who demands and who supplies synthetic dollars — a descriptive fact that revises beliefs regardless of the causal design.

The paper is most appropriately classified as **Theory + Empirics with a structural demand system extension**, where the theory generates testable reduced-form predictions tested via shift-share IV, and the demand system provides structural quantification for selected predictions.

---

## Task 1 — Model Audit: Parameter Identification and Testability

The full parameter set appearing in the theory document: {$\alpha_t$, $\rho$, $\sigma$, $q_t$, $\eta$, $\gamma$, $\theta_t$, $\mu_t$, $\psi$, $\omega$, $\nu$, $\phi$}. I assess each in turn.

### $\alpha_t$ — Preference weight for outside (safe) dollar liquidity in CES

**Identified?** No — not separately identified from $q_t$ and the demand ratio $I_t/O_t$ in the CES cost-minimization.

**Variation that would identify it:** Cross-period variation in $O_t$ and $I_t$ holdings at a fixed relative price $R_O/R_I$. This requires observing $O_t$ and $I_t$ separately, which is not feasible with the bilateral FX data alone.

**Identification assumption stated?** No. The theory refers to $\alpha_t$ as a "preference for outside liquidity" that rises in stress ($\alpha_t \uparrow$ in Section 11) but provides no identification strategy.

**Flag:** $\alpha_t$ appears in Equation (3) (demand ratio) and in the crisis mechanism (Section 11). If the Propositions depend on the sign of $\partial\alpha_t/\partial S_t$, and $\alpha_t$ is unidentified, those propositions are reduced to qualitative predictions. In the current draft, $\alpha_t$ shifts in stress are asserted rather than derived or estimated. **This is a free parameter in the testable propositions.** Recommend either (a) imposing a parametric restriction relating $\alpha_t$ to observables (e.g., $\alpha_t = \alpha_0 + \alpha_1 \cdot \text{VIX}_t$) or (b) treating $\alpha_t$ as an unobservable state variable that is subsumed into the reduced-form error and acknowledging that the structural interpretation of the CES weight is not separately identified.

### $\rho$ — CES substitution parameter (related to $\sigma = 1/(1-\rho)$)

**Identified?** Partially — $\sigma$ is identified in principle from price elasticity in the demand system. Equation (9.2) gives the linearized net-demand function with slope $\beta_s$ (price sensitivity by sector). The aggregate $B = \sum_s \beta_s$ is the elasticity-based slope, from which $\sigma$ can be recovered if the demand system is fully estimated.

**Variation that would identify it:** Cross-sectoral price sensitivity differences — specifically, the sector-specific $\beta_s$ estimates from the demand system (DS1 baseline). The cross-instrument design ($Z^{MMF}$ shifts FB demand, $Z^{EPFR}$ shifts NBFI demand) provides the price variation needed to identify $\beta_{FB}$ and $\beta_{NBFI}$ separately.

**Identification assumption stated?** The cross-sectoral exclusion restrictions are stated in v8 §6.3 but the theory document does not reference them. **This is a notation/alignment gap.** The CES parameter $\rho$ does not appear in the empirical design by name; the demand system estimates $\beta_s$ which are the empirical counterparts of $\rho$ via $\sigma = -1/B_{normalized}$. This mapping should be made explicit in the paper.

**Flag:** $\rho$ is free in all six propositions that rely only on sign conditions ($\partial\mu/\partial U > 0$, etc.) — the sign results hold for any $\rho < 1$. However, the counterfactuals (Section 14) require a specific value of $\sigma$ to produce magnitudes. Without demand system estimation, counterfactuals are not identified.

### $\sigma$ — Elasticity of substitution ($= 1/(1-\rho)$)

Same identification as $\rho$. Not separately discussed. See above. The assumption $1 < \sigma < \infty$ (imperfect substitutes) is testable: $\sigma \to \infty$ would imply perfect substitution (basis = 0 always); $\sigma \to 1$ would imply log-complementarity. Testing whether the estimated $\hat\sigma$ is finite and greater than 1 is an internal validity check for the CES framework.

**[Fix B2] Critical failure mode — σ ≤ 1 and the run mechanism:** The run-from-inside-to-outside mechanism requires $\sigma > 1$ (imperfect substitutes). If $\sigma \leq 1$, inside and outside dollar liquidity are gross complements in the CES aggregator: an increase in $O_t$ would reduce demand for $I_t$, which is the opposite of the substitution story. In the complement case, a stress shock would not generate a run from $I$ to $O$ — it would generate co-movement. The paper's central theoretical contribution (dollar funding crises as runs within the dollar ecosystem) fails if $\sigma \leq 1$. We treat $\sigma > 1$ as a testable maintained assumption. The internal validity check is: if the demand system estimation yields $\mathcal{B} = \sum_s \beta_s \geq 0$ (upward-sloping aggregate net demand), the substitution assumption is rejected by the data, and the run mechanism is not supported empirically. We report this test as part of the demand system results.

### $q_t$ — Effective quality of synthetic dollar liquidity

**Identified?** No — $q_t$ is a latent variable. The theory defines $q_t = q(p_t)$ with $q' > 0$ but does not specify the functional form. The feasibility assessment (Section 1) proposes price dispersion as a proxy but acknowledges this is a symptom, not the object itself.

**Variation that would identify it:** $q_t$ would be identified if we observed both the quantity $I_t$ demanded and the service flow it provides (which requires independent observation of $L_t$). Neither is directly observable.

**Flag:** $q_t$ appears in the demand ratio equation (Eq. 3), the quality-endogeneity equation (Eq. 6), and the crisis mechanism (Section 11). However, none of the six formal Propositions require measuring $q_t$ directly — they are stated in terms of $\mu_t$ (observable), $U_t$ (partially observable), and $B_t$ (partially observable). **The paper can proceed without estimating $q_t$** as long as the theoretical claims about $q_t$'s role are presented as structural interpretation rather than empirical results. The distinction must be stated clearly to avoid referee challenges.

### $\eta$ — Matching efficiency parameter

**Identified?** No. $\eta$ is a scale parameter in the Cobb-Douglas matching function (Eq. 4). It appears in $p_t = \eta(B_t/U_t)^{1-\gamma}$ but is not separately identified from the level of $p_t$ without an independent observation of matching probability.

**Variation that would identify it:** Level of the taker/maker ratio at a known $B_t/U_t$ ratio. This is not feasible given the partial observability of $B_t$.

**Flag:** $\eta$ does not appear in any of the six Propositions — it drops out of the sign conditions. It is not a free parameter in the testable predictions. However, it is needed for the structural matching-function interpretation and for any calibration exercise. **Recommend acknowledging $\eta$ as a calibration parameter not separately identified from the data, and removing it from any claims about structural estimation.**

### $\gamma$ — Matching function elasticity (demand side)

**Identified?** In principle, yes — from the elasticity of $p_t$ with respect to $U_t/B_t$. Specifically, $\partial \log p_t / \partial \log(B_t/U_t) = 1 - \gamma$. If both $p_t$ (taker ratio) and $B_t/U_t$ (demand/capacity ratio) have sufficient variation, $\gamma$ is identified from this elasticity.

**Variation that would identify it:** Time-series variation in $B_t/U_t$ (the market tightness ratio) and in the taker ratio $\pi^{taker}$. The feasibility assessment grades $B_t$ as C and $\theta_t = U_t/B_t$ as C, so identification of $\gamma$ is unlikely to be precise.

**Flag:** $\gamma$ appears in the matching function (Eq. 4) but drops out of the sign conditions for Propositions 1–5. It matters for the amplification magnitude in the crisis mechanism (Section 11) and for counterfactuals. **Recommend treating $\gamma$ as a calibrated parameter (e.g., calibrated to 0.5 per the matching function literature) and reporting sensitivity to $\gamma \in \{0.3, 0.5, 0.7\}$ in the appendix.**

### $\theta_t = U_t/B_t$ — Market tightness

**Identified?** Partially — as a constructed ratio with noise. See feasibility assessment Section 1 (grade C). The regime-indicator approach (QuarterEnd, DealerConstraint binary) is more credible than the continuous ratio.

**Flag:** $\theta_t$ is the central state variable for Proposition 3 (non-linearity) and the crisis mechanism (Section 11). Its partial observability is the binding constraint on the most ambitious theoretical predictions. **The threshold test in Proposition 3 is not identified with the current design** (confirmed by feasibility assessment P3: Not Testable).

### $\mu_t$ — Funding spread / cost of inside-to-outside conversion

**Identified?** Yes — grade A. $\mu_t = \text{PriceUSD}_{m,t} = -\text{TIB}_{m,t}$. Direct, high-quality proxy from transaction data.

**Flag:** None. This is the best-identified object in the model and the primary outcome variable. Market-clearing validation ($\sum_s Q_{s,m,t} \approx 0$) provides internal consistency.

### $\psi$ — Sensitivity of FBO capacity to financial stress ($B^{FBO} = \bar{B}^{FBO} - \psi S_t - \omega Q_t + \nu A_t^{reg}$)

**Identified?** In principle, from time-series variation in $S_t$ and FBO-revealed supply $Q_{D,m,t}$. In practice, $\psi$ is a coefficient in a structural equation for $B_t^{FBO}$ — identification requires separating the $S_t$ and $Q_t$ channels, which is collinear in stress periods.

**Flag:** $\psi$, $\omega$, and $\nu$ are structural parameters of the FBO capacity equation (Eq. 7). They do not appear in the six Propositions by name — the Propositions reference $B_t$ as a whole. **These sub-parameters are not testable with the current design and should be demoted to illustrative structural discussion, not estimation targets.** Their inclusion adds notation complexity without empirical traction.

### $\omega$ — Sensitivity of FBO capacity to quarter-end reporting ($Q_t$ indicator)

**Identified?** Partially — from the quarter-end interaction. But the causal attribution (supply vs. demand channel) is not separately identified, as noted in feasibility P4. $\omega$ would require an instrument that affects FBO supply at quarter-end without affecting demand — not available.

**Flag:** $\omega$ is the structural parameter behind Proposition 4. Proposition 4 as stated is testable in reduced form ($\mu_t \uparrow$ at quarter-end). The structural claim ($B_t \downarrow$ because $\omega > 0$) is not separately identified. **State Proposition 4 as a reduced-form prediction, not a structural parameter estimate.**

### $\nu$ — Sensitivity of FBO capacity to regulatory advantage ($A_t^{reg}$)

**Identified?** No — $A_t^{reg}$ (FBO regulatory advantage) is not defined operationally in the theory document, and no empirical proxy is proposed in v8. This is a free parameter.

**Flag:** $\nu$ and $A_t^{reg}$ should be removed from the empirical claims section or relegated to theoretical discussion only. If the paper wishes to identify regulatory advantage effects, it would need a specific regulatory event study (e.g., Basel III leverage ratio phase-in dates), which is listed in the feasibility report (Gap 5, Remedy 1) but not currently incorporated in the design.

### $\phi$ — Hedge fund capacity sensitivity to spread above cost ($c^{HF}$)

**Identified?** No — not in the current design. The HF capacity equation (Eq. 8: $B_t^{HF} = \phi \cdot \max(\mu_t - c^{HF}, 0) \cdot \text{RiskCapacity}_t$) makes $B_t^{HF}$ endogenous to $\mu_t$, creating simultaneity. $\phi$ is a structural parameter of this equation. The v8 explicitly acknowledges that $Z^{HF}_{m,t} = (-\text{TIB}_{m,t-1}) \times \text{RiskCapacity}_t$ is "pas un instrument strict" (v8 §4.4).

**Flag:** The HF capacity equation is endogenous by construction — HF enter when the spread is attractive. This makes $B_t^{HF}$ endogenous to $\mu_t$, not exogenous. The structural claim in Proposition 6 (HF are pro-cyclical capacity providers) is testable descriptively via the intermediation matrix, but $\phi$ is not identified without a valid instrument for HF entry decisions orthogonal to $\mu_t$. **Recommend framing the HF result as a descriptive finding (from the bilateral intermediation matrix) rather than a structural parameter estimate.**

### Summary Audit Table

| Parameter | Identified? | Data variation | Appears in Proposition? | Action |
|-----------|-------------|----------------|------------------------|--------|
| $\alpha_t$ | No | Not available | Yes (implicit in crisis mechanism) | Free parameter — restrict parametrically or relegate to qualitative |
| $\rho$ / $\sigma$ | Partially | Demand system price variation | Implicit in all props (sign conditions hold for any $\rho$) | Estimate via DS1; map to $\beta_s$ in empirical design; test $\sigma > 1$ as maintained assumption |
| $q_t$ | No | Not directly observable | Not in proposition statements | Latent — drop from empirical claims; keep in structural interpretation |
| $\eta$ | No | Not available | Not in propositions | Calibration parameter only |
| $\gamma$ | Partially | $\theta_t$ / taker ratio variation (noisy) | Not in propositions (magnitudes only) | Calibrate to 0.5; sensitivity analysis |
| $\theta_t$ | Partially (grade C) | Ratio + regime indicators | Proposition 3 explicitly | Continuous $\hat\theta$ not identified; use regime indicators for P2/P4 |
| $\mu_t$ | Yes (grade A) | TIB from transaction data | All propositions (outcome) | No action needed |
| $\psi$ | No | Collinear with stress | Not in propositions | Remove from estimation; discuss structurally |
| $\omega$ | Partially | Quarter-end variation | Proposition 4 (structural) | Restate P4 as reduced-form |
| $\nu$ | No | $A_t^{reg}$ undefined | Not in propositions | Remove from paper |
| $\phi$ | No | Endogenous to $\mu_t$ | Proposition 6 (structural) | Descriptive only |

---

## Task 2 — Paper Classification and Structural Assessment

### Is the theoretical contribution sufficient for a top-5 theory+empirics paper?

**Assessment: Yes, with significant development needed.**

The current theory document is a first-draft framework sketch (stated explicitly: "First Draft"). It is in French, lacks formal proofs, and several results are stated as assertions rather than derived propositions. However, the **conceptual contribution is genuine and at the frontier**: the inside/outside dollar liquidity distinction applied to FX swap market microstructure is a new lens on dollar funding crises that is distinct from existing frameworks (Du-Tepper-Verdelhan, Rime-Schrimpf-Syrstad, Khetan 2025).

The search-and-matching layer is the most original theoretical element — it converts a static asset-market result (CIP deviation) into a dynamic rationing story (matching probability, quality endogeneity, amplification externality). This is not present in the comparable empirical papers.

**The theory is currently a "motivating framework" but has the structure to be elevated to a genuine theoretical contribution** if: (a) formal propositions are stated with assumptions and proofs, (b) the equilibrium characterization (Section 10) is developed rigorously, and (c) the amplification mechanism (Section 11) is derived rather than asserted.

The critical distinction for a top-5 journal: the theory must generate a prediction that competing models do not make. The current document's clearest candidate for a distinct prediction is the **non-monotone response of HF capacity to stress** (Eq. 8: HF provide capacity when spread > $c^{HF}$ but withdraw in extreme stress when RiskCapacity falls). This is not in Holmström-Tirole, Bolton-Santos-Scheinkman, or the comparable empirics papers. It needs to be formalized.

### Key Structural Assumptions

**[Fix B1] No-stigma assumption for swap line event study (Proposition 5):** We assume that central bank swap line drawdowns reflect genuine demand for dollar liquidity and are not distorted by stigma concerns. The swap line event study (P5) depends on this assumption: if foreign central banks (or the commercial banks they fund) face reputational costs from revealing dollar shortfalls, they may under-draw even when liquidity-constrained, and observed drawdown volumes would identify only the "willing-to-reveal" sub-population rather than all genuinely constrained counterparties (a LATE with non-random selection into treatment). Three features of the swap line setting limit stigma concerns relative to comparable facilities: (a) drawdowns are by foreign central banks acting as pass-through intermediaries, not by individual commercial banks directly — reputational exposure is diffuse; (b) the sample includes March 2020, when crisis severity has been documented to overwhelm stigma concerns at comparable facilities (consistent with Armantier et al. 2015, AER, who document that TAF auction stigma dissipates in acute stress; the ECB's LTRO experience provides a parallel); (c) as a direct robustness check, the event study can be run on swap line announcement dates rather than drawdown dates — if the price effect appears at announcement (before any stigma-contaminated drawdown), it is not confounded by selection into drawdowns. The empirical implication of a stigma violation, if present, is a downward bias in the event study estimate: the estimated price impact of swap line capacity would understate the true counterfactual effect.

### Structural vs. Reduced-Form Propositions

| Proposition | Classification | Justification |
|-------------|---------------|---------------|
| P1 ($\partial\mu/\partial U > 0$) | Reduced-form testable | Sign condition holds for any $\rho < 1$; no structural parameters required |
| P2 ($\partial\mu/\partial B < 0$) | Reduced-form testable (as heterogeneity) | Sign condition holds generically; causal identification of $B_t$ not available |
| P3 (Non-linearity / threshold) | Structural — requires $\theta_t$ estimation | Threshold test requires continuous $\hat\theta_t$ and structural identification of $B_t$ |
| P4 (Quarter-end) | Reduced-form testable | Deterministic conditioning variable; supply vs. demand attribution not separately identified |
| P5 (Swap lines) | Reduced-form testable (event study) | Reduced-form price effect; collateral-stabilization channel not separately identified; no-stigma assumption required |
| P6 (Provider heterogeneity) | Descriptive / structural hybrid | HF pro-cyclicality descriptively testable; $\phi$ structural parameter not identified |

### Should the Demand System be Main Result or Appendix?

**Recommendation: Position as a main section but with explicit framing as "structural extension" — not as a third main result competing with the IV design.**

Arguments for main section:
- The demand system provides the only pathway to counterfactual decomposition (CF1–CF4 in Section 14), which is a distinctive contribution over Khetan (2025) who only reports the reduced-form price impact
- The bilateral counterparty data uniquely enables cross-sectoral identification ($Z^{MMF}$ for FB, $Z^{EPFR}$ for NBFI) that other papers cannot replicate
- The structural interpretation of $\beta_{IV} \approx -\gamma_{FB}/B$ (connecting the IV estimate to demand system parameters) is a clean bridge between the two approaches

Arguments for appendix:
- The cross-sectoral exclusion restrictions are maintained assumptions, not testable with the data
- The Explorer grades P6 (provider heterogeneity, which requires the demand system) as "Partial"
- Top-5 reviewers will be more skeptical of the demand system than the IV simple design

**Compromise position:** Make the demand system the **fourth part of a four-part structure**, explicitly labeled "Demand system and counterfactuals." The paper's "main results" are Parts 1–3 (conceptual framework, microstructure description, IV causal design). The demand system is framed as "we now use the structural model to interpret the IV estimate and produce counterfactuals." This is the v8's own framing ("extension structurelle") — it should be preserved in the paper structure.

---

## Task 3 — Model Improvement Plan

### Missing Elements

**A. The outside option and entry/exit conditions for intermediaries**

The current model has a reduced-form FBO capacity equation (Eq. 7) but no formal outside option for intermediaries — there is no decision problem for the dealer/FBO. A fully specified model would have dealers solving a profit-maximization problem subject to a balance sheet constraint, choosing how much FX swap capacity to provide. This would endogenize $B_t$ and generate richer predictions about when dealers withdraw (not just that they do).

Specifically: adding a dealer problem where dealers maximize expected profit from FX swap intermediation subject to a Value-at-Risk or leverage constraint would generate the non-linear capacity withdrawal that is currently asserted in the crisis mechanism (Section 11). This would turn Proposition 2 ($\partial\mu/\partial B < 0$) from an accounting identity into a behavioral result.

**Implementation priority:** Medium. The current propositions hold without this extension, but it would strengthen the theory's claim to originality. A two-page formal appendix section specifying the dealer's problem and deriving $B^* = B(S_t, \Gamma, W_t)$ as an equilibrium capacity function would suffice.

**B. Dynamics and the run mechanism**

The current model is static (equilibrium is characterized for a given $t$). The "run" framing in the title and abstract refers to a dynamic process — agents sequentially switching from inside to outside dollar liquidity as quality degrades. The static model captures the level of $\mu_t$ at a given tension $\theta_t$, but cannot formally characterize the speed or self-reinforcing nature of the run.

A two-period extension would be sufficient: in period 1, $q_t$ is high and inside liquidity is demanded; in period 2, if a shock raises $\theta_t$ past a threshold, $q_t$ collapses and agents prefer outside liquidity. The key prediction (Proposition 3) — that there is a threshold above which the system tips — would then be a formal result rather than an assertion.

This is the most valuable theoretical extension (see Section 11 discussion below).

**C. Equilibrium uniqueness and multiplicity**

The current equilibrium definition (Section 10) does not address whether the equilibrium is unique or whether multiple equilibria are possible. The amplification mechanism in Section 11 ($q_t \downarrow \to U_t \uparrow \to p_t \downarrow \to q_t \downarrow$) is a description of a potentially multiple-equilibrium system: there may be a "good" equilibrium (high $q_t$, low $\mu_t$) and a "bad" equilibrium (low $q_t$, high $\mu_t$) for the same parameter values. If so, the model predicts sudden transitions between equilibria (crises), and the swap lines restore the good equilibrium. This would be a strong theoretical result.

**Implementation priority:** High. Showing that the model has two stable equilibria (with a Proposition establishing existence conditions) would dramatically strengthen the theory's contribution. The formal argument can be made with a fixed-point diagram: define $\Phi(\theta_t) = $ price consistent with demand given $q(\theta_t)$; show that $\Phi$ can cross the supply curve at two points.

### Redundant or Underpowered Propositions

**Proposition 4 (Quarter-end) is the weakest.** The result is:
- Mechanically true by definition: $Q_t = 1 \Rightarrow B_t \downarrow$ follows from the FBO capacity equation by substitution of $\omega > 0$
- Empirically conflated: the reduced-form test identifies $\mu_t \uparrow$ at quarter-end but cannot attribute it to the supply channel (which is the proposition's claim) vs. the demand channel
- Already documented in the literature (Kloks-Mattille-Ranaldo 2024 on quarter-end in FX swaps; Du-Tepper-Verdelhan on regulatory effects)

**Recommendation:** Demote Proposition 4 to an illustrative corollary of Proposition 2 rather than a standalone proposition. Frame the quarter-end result as "the supply-channel mechanism generates a specific prediction about regulatory reporting dates — consistent with documented quarter-end patterns." This removes a weakness without eliminating the empirical result.

**Proposition 6 (Provider heterogeneity) is too broad.** The proposition as stated covers three distinct claims: (a) HF pro-cyclicality, (b) dealer market-making obligation, (c) CB countercyclicality. Each requires different evidence. As a single proposition, it is either too weak (any one finding partially confirms it) or too demanding (all three must be established). **Recommend splitting into:** Proposition 6a (dealer constrained capacity — linked to P2), Proposition 6b (HF pro-cyclical entry/exit — testable descriptively from intermediation matrix), and Proposition 6c (CB swap lines countercyclical — linked to P5).

### High-Value Extension: Formal Treatment of Run Dynamics (Section 11)

Section 11 describes the crisis mechanism narratively but does not formalize it as a dynamic game or sequential equilibrium. The three simultaneous effects ($U_t \uparrow$, $B_t \downarrow$, $\alpha_t \uparrow$) are asserted to produce amplification but the mechanism is not formally derived.

**Proposed formalization:**

Define a two-period model where:
- Period 1: agents hold inside dollar liquidity at quality $q_1 = q(\theta_1)$, where $\theta_1 = U_1/B_1$ is determined in equilibrium
- A shock $S_2$ hits at the start of period 2: $S_2$ simultaneously raises $U_2$ (more agents need conversion) and lowers $B_2$ (dealers constrained)
- The feedback: if $q_2 < \bar q$, agents who held inside liquidity attempt to convert, further raising $U_2$

**Key result to derive:**
There exists a threshold $\theta^* = f(\eta, \gamma, \sigma)$ such that:
- For $\theta_t < \theta^*$: unique stable equilibrium with $q_t$ bounded away from zero
- For $\theta_t > \theta^*$: the interior equilibrium is unstable; the system converges to the corner solution $q_t \approx 0$ (dollar shortage / market freeze)

**This would convert Proposition 3 from an assertion ("non-linearity exists") into a formal result ("threshold $\theta^*$ exists with closed-form expression").**

The threshold would then be a structural estimand: from the demand system, $\sigma$ is estimated; from the matching function, $\gamma$ is calibrated; $\eta$ is normalized. This gives a testable implication: the estimated $\hat\theta^*$ should be consistent with the historical crisis episodes (GFC, COVID) being above-threshold and normal periods being below-threshold.

**Implementation:** A 4–6 page formal appendix section. The mathematics involve a fixed-point argument — not technically demanding for a QJE/JPE audience. The payoff is large: this converts the most theoretically interesting claim (threshold non-linearity) from not-testable to structural-calibration-testable.

### Notation Inconsistencies Between Theory and Empirical Design

| Object | Theory notation | v8 notation | Resolution |
|--------|----------------|-------------|------------|
| Demand for conversion | $U_t$ | $Q_{FB,m,t}$ | Theory is aggregate; v8 proxies with FB only. Clarify explicitly |
| Funding spread | $\mu_t = R_I - R_O$ | $\text{PriceUSD}_{m,t} = -\text{TIB}_{m,t}$ | Sign convention: PriceUSD > 0 when inside dollar is expensive — consistent with $\mu_t > 0$. State explicitly |
| Matching probability | $p_t$ | $\pi^{taker}_{FB,m,t}$ (proxy only) | Theory has $p_t$ cardinal; v8 uses ordinal proxy. State clearly that $\pi^{taker}$ is an indirect indicator |
| Market tightness | $\theta_t = U_t/B_t$ | Not directly mapped in v8 | v8 uses DealerConstraint (binary) and VIX/MOVE — state this is a regime approximation of $\theta_t$ |
| Capacity | $B_t = B^{FBO} + B^{US} + B^{dealer} + B^{HF} + B^{CBswap}$ | $\text{DealerCapacity}_t$ (composite) | v8 proxy conflates multiple theory components. Add note that v8 DealerCapacity proxies the subset $B^{US} + B^{dealer}$, not the full $B_t$ |
| Equilibrium price equation | $\text{PriceUSD}_{m,t} = -(1/B)\sum_s[\alpha_{s,m} + \gamma_s X_{s,m,t} + \varepsilon_{s,m,t}]$ | Same (v8 §2.4) | Consistent. $B = \sum_s \beta_s$ — use consistent notation ($B$ is the aggregate slope, not the capacity parameter $B_t$; risk of symbol collision — rename aggregate slope to $\mathcal{B}$ or $\mathbf{B}$) |

**Critical notation collision:** The symbol $B_t$ is used for intermediary capacity in the matching function, and $B = \sum_s \beta_s$ is used for the aggregate demand slope in the price equation. These are different objects. Using the same letter risks confusion and will be flagged by referees. **Rename the aggregate slope to $\mathcal{B}$ or $\bar\beta$ throughout.**

---

## Task 4 — Theory–Empirics Alignment Map

The mapping below uses the formal Proposition numbering from the theory (Sections 12–13) and the v8 prediction numbering (§9 table). Note the theory has 6 propositions; v8 has 9 predictions — the extra three (P5 tenor heterogeneity, P6 dealer absorption, P7 quarter-end in v8 numbering, P8 channel distinction, P9 spot FX) are empirical extensions not formally derived as propositions in the theory.

| Theory Proposition | v8 Prediction | Empirical Specification | Identification Strategy | Mapping Quality | Critical Data Req. | Status |
|-------------------|--------------|------------------------|------------------------|----------------|-------------------|--------|
| **P1: $\partial\mu/\partial U > 0$** (demand pressure raises spread) | P1+P2 | 2-stage IV: $Q_{FB} \to \text{PriceUSD}$, instrumented by $Z^{MMF}_{m,t}$ (Eq. v8 §5.1–5.2) | Shift-share IV; cross-market variation in MMF exposure × aggregate funding shock; FE absorb common time variation | **Partial** — theory states effect is for aggregate $U_t$; v8 proxies with FB-only $Q_{FB}$; systematic truncation of NBFI demand understates $\theta_t$ in stress | Bilateral FX data + N-MFP for IV construction; CDS for controls | **Yellow** — testable; attenuation from FB-only proxy and shift-share exogeneity require explicit treatment |
| **P2: $\partial\mu/\partial B < 0$** (capacity reduces spread) | P6 (v8 §5.3 interaction) | Interaction: $\hat Q_{FB} \times \text{DealerConstraint}$, $\beta_2 > 0$; two-instrument IV for interaction | Effect heterogeneity design; DealerConstraint is conditioning variable, not IV; two endogenous regressors instrumented by $Z^{MMF}$ and $Z^{MMF} \times \text{DealerConstraint}$ | **Partial** — theory claims causal $B_t$ effect; v8 estimates state-dependent heterogeneity, not causal $B_t$ variation; DealerConstraint is endogenous; no valid instrument for $B_t$ | Bilateral FX data + Primary Dealer repo + H.8 for DealerCapacity construction | **Yellow** — identifies effect heterogeneity by capacity regime; cannot establish causality of $B_t$ channel without exogenous $B_t$ variation |
| **P3: Threshold non-linearity** ($\theta_t$ crossing $\theta^*$ causes $q_t$ collapse) | Not in v8 predictions | Not specified; would require threshold regression on $\hat\theta_t$ or structural-break detection | Would need: continuous $\hat\theta_t$ series + threshold/spline regression + sufficient crisis variation | **Gap** — theory predicts discrete threshold; v8 has no corresponding specification; the interaction design in P2 tests monotone heterogeneity, which is a necessary but not sufficient condition for a threshold | Continuous $B_t$ series (not currently feasible); multiple crisis episodes (limited to post-2015 data) | **Red** — not testable with current design; can only be calibration-consistent |
| **P4: Quarter-end** ($Q_t = 1 \Rightarrow B_t \downarrow \Rightarrow \mu_t \uparrow$) | P7 (v8 §5.3 interaction) | Interaction: $\hat Q_{FB} \times \text{QuarterEnd}$, $\beta_2 > 0$ (v8 §5.3 table) | QuarterEnd is deterministic — no endogeneity in the conditioning variable; but attribution of the effect to supply-side $B_t$ vs. demand-side $U_t$ is not separately identified | **Partial** — reduced-form identification is clean; structural channel attribution is not | Bilateral FX data; QuarterEnd is deterministic (no data requirement) | **Yellow** — testable as reduced-form; supply vs. demand channel not separately identified; restate as reduced-form prediction |
| **P5: Swap lines** ($B_t \uparrow \Rightarrow \mu_t \downarrow$) | Not directly in v8 predictions (mentioned in §7.2 "Dynamique événementielle") | Event study around swap line activation dates; cross-pair variation (covered vs. uncovered pairs) | Event study; identification via cross-pair heterogeneity (pairs with/without swap line coverage); comparison group = uncovered currency pairs; no-stigma assumption required (see Key Structural Assumptions above) | **Partial** — event study conflates policy effect with natural stress resolution; second channel (collateral stabilization via $\rho$ variation) not measurable; cross-pair design partially addresses confounding; no-stigma assumption is a maintained condition | Fed swap line drawdown data (public, episodic); crisis event dates | **Yellow** — testable as event study; LATE interpretation requires no-stigma assumption and assumption that treated pairs not systematically different from control pairs; add did-not-receive-swap-line as placebo; run on announcement dates as robustness |
| **P6: Provider heterogeneity** (HF pro-cyclical, dealers constrained, CB countercyclical) | P4 (dealer > 40%) + P3 (FB more inelastic than HF) + P8 (channel distinction) | (a) Descriptive: intermediation matrix by sector × stress regime; (b) Structural: DS1 demand system with $\beta_{FB}$ vs. $\beta_{HF}$ comparison; (c) Event study: dealer vs. HF share at quarter-end and in crises | (a) Descriptive — no causal claim; (b) Cross-sectoral IV in demand system (cross-equation exclusion restrictions); (c) Event study on intermediation shares | **Partial** — descriptive matrix is clean; demand system requires maintained exclusions for $Z^{MMF}$ / $Z^{EPFR}$ cross-sector restrictions; HF instrument not valid (v8 acknowledges); structural $\phi$ not identified | Full bilateral sector data (all 6 sectors); EPFR for AM shifter; valid HF capacity instrument (not currently available) | **Yellow (descriptive) / Red (structural)** — descriptive intermediation matrix is Green; structural HF price sensitivity is Red; frame as descriptive |

**[Fix B3a] Exclusion restriction for the interaction instrument (P2 specification):** The two-endogenous/two-instrument specification for Proposition 2 instruments $Q_{FB} \times \text{DealerConstraint}$ with $Z^{MMF} \times \text{DealerConstraint}$. The exclusion restriction requires: conditional on $Q_{FB}$ and all controls, the interaction instrument $Z^{MMF} \times \text{DealerConstraint}$ affects PriceUSD only through the interaction term $Q_{FB} \times \text{DealerConstraint}$, and not through a direct effect on the outcome. This exclusion restriction is non-trivial: in periods of dealer constraint, any MMF-driven demand shock may be amplified in prices through channels other than the interaction term — for example, dealers may directly widen spreads to manage inventory during constrained periods regardless of realized demand. We argue for plausibility on three grounds: (a) DealerConstraint is measured at the previous quarter-end, lagged by construction, which reduces simultaneity between the conditioning variable and current period spreads; (b) the direct channel — dealers widening spreads independently of demand in constrained periods — is absorbed by the DealerConstraint main effect in the regression, so only residual variation in the interaction enters the instrument; (c) as a sensitivity check, we re-estimate the interaction specification with DealerConstraint × year fixed effects, allowing the direct constraint effect on pricing to vary freely over time. If the interaction estimate is robust to this additional flexibility, the exclusion restriction for the interaction instrument is credible.

### Notes on Status Color Coding

**Green:** The empirical test is clean, the data exists (or is obtainable), and the mapping from proposition to specification requires no untested structural assumptions.

**Yellow:** The empirical test is feasible but requires one or more of: (a) a maintained assumption that is stated but not testable, (b) a limitation acknowledged in the paper with appropriate hedging, or (c) the result provides evidence consistent with the proposition but does not rule out alternative interpretations.

**Red:** The empirical test is not feasible with the current design — either the required data is not available, or the identification assumption is not credible.

**Overall alignment assessment:** Zero propositions are Green, four are Yellow, one is Red (P3), and P3 has no corresponding v8 specification at all. This is a Yellow paper: the primary causal result (P1) is feasible with caveats, the heterogeneity results (P2, P4) are feasible as reduced-form, and the most theoretically interesting proposition (P3) is not testable. The paper can be published on the strength of P1 + the descriptive contribution (bilateral microstructure) + the demand system decomposition, but the theory's most ambitious claim (threshold non-linearity, amplification) cannot be empirically validated with the current design.

---

## Task 5 — Five Main Referee Objections

### Objection 1: The shift-share instrument is invalid

**Precise statement:** "The shift-share instrument ($Z^{MMF}_{m,t} = \text{Exposure}^{MMF}_{m,m-1} \times \text{FundingShock}_t$) is not exogenous. The pre-determined exposure weights ($w^{pre}_{i,m}$) are not random — banks with high prime MMF exposure are systematically more dollar-dependent, shorter-duration, and more likely to face dollar funding stress for reasons other than the MMF shock. The Goldsmith-Pinkham et al. (2020) critique applies: you need to show that the dominant-share banks' characteristics are orthogonal to future FX swap pricing, not merely that the weights are pre-determined."

**Severity:** Major. This is the primary identification threat and the most likely first referee comment at any top journal.

**Best response:** Three-part:
1. **Balance tests on dominant-share banks.** For each currency pair market $m$, identify the bank(s) with dominant MMF exposure shares. Test whether these banks differ systematically from non-dominant banks on pre-treatment characteristics: pre-period FX swap volume, tenor composition, CDS spread level, credit rating, regulatory status. Report a balance table. This is a prerequisite, not optional.
2. **Adão-Kolesár-Morales (2019) inference.** Report AKM shift-share standard errors that account for cross-market correlation induced by the common FundingShock component. This is already mentioned in v8 §11 — implement it as the baseline, not as a robustness check.
3. **Bartik control strategy.** Following Goldsmith-Pinkham et al. (2020), report the just-identified IV using the single largest exposure-weight bank as the instrument for each market. This provides a cleaner (if less efficient) identification that explicitly uses only cross-sectional variation in exposures, holding the shock constant.

### Objection 2: You are testing a price effect, not the mechanism

**Precise statement:** "Your IV identifies that MMF funding shocks raise FX swap costs. This is a supply-demand result that requires no theory — any demand shock to a market with limited supply will raise prices. The inside/outside dollar liquidity distinction, the matching function, and the quality degradation mechanism are not tested. The theory is window dressing."

**Severity:** Major. This is a structural challenge to the theory+empirics claim.

**Best response:** Two-part:
1. **Mechanism evidence.** The taker/maker decomposition provides direct evidence of the search mechanism: if the matching-function interpretation is correct, the instrument should affect taker demand ($Q^{taker}_{FB}$) more than maker demand ($Q^{maker}_{FB}$), because takers are the active seekers in the model. Test this with separate first-stage regressions for $Q^{taker}$ and $Q^{maker}$ and show $\pi^{taker} >> \pi^{maker}$. This is already planned in v8 §5.1 — make it the central mechanism test, not a diagnostic.
2. **Quality degradation.** The model predicts that when $\theta_t$ is high (high demand, low capacity), not only does $\mu_t$ rise but $q_t$ falls — specifically, price dispersion across sectors should widen (rationing with price discrimination). Test whether the interaction $Q_{FB} \times \text{DealerConstraint}$ predicts not only a higher average $\mu_t$ but also higher cross-sectoral price dispersion $\text{Spread}_{s,m,t}$. If the model is correct, both predictions must hold simultaneously; if only the price level rises, simpler models suffice.

### Objection 3: The $B_t$ capacity channel is endogenous

**Precise statement:** "Your interaction term $Q_{FB} \times \text{DealerConstraint}$ is problematic because DealerConstraint is determined simultaneously with the basis — both reflect the state of dollar stress. You cannot identify the capacity mechanism separately from the demand mechanism because they both spike in crises. The coefficient $\beta_2$ on the interaction is confounded."

**Severity:** Major (for the P2 capacity claim); minor (for the P1 level claim, which doesn't require DealerConstraint).

**Best response:**
1. **Reframe the claim.** P2's empirical claim should be explicitly stated as "the price impact of demand shocks is larger when dealer capacity is constrained" — a statement about effect heterogeneity, not about the causal effect of $B_t$. This is a weaker but defensible claim that does not require $B_t$ to be exogenous, only that DealerConstraint is a valid conditioning variable for effect heterogeneity.
2. **Provide exogenous variation in capacity.** The clearest available source: Basel III leverage ratio phase-in dates (known in advance, applied uniformly to all dealers). Construct a "regulatory capacity shock" instrument: the interaction of a dealer's initial leverage ratio with the post-announcement indicator. This identifies exogenous variation in dealer capacity from regulatory requirements rather than from market conditions.
3. **Within quarter-end.** Quarter-end is deterministic and supply-side (dealers cut capacity for regulatory reporting). Use only the supply-side quarter-end variation (the $\omega$ channel in the FBO equation) and compare the price impact on quarter-end days (low $B_t$) vs. adjacent days at similar demand levels. This partially separates the supply channel.

### Objection 4: The demand system exclusion restrictions are not credible

**Precise statement:** "Your demand system requires that $Z^{MMF}$ affects only foreign bank demand and that $Z^{EPFR}$ affects only NBFI demand. But prime MMF funding shocks affect the entire dollar funding ecosystem — they likely also reduce hedge fund risk appetite (via prime brokerage channels) and disrupt asset manager rebalancing. The cross-equation exclusions are implausible."

**Severity:** Minor for the IV simple design (Part 3); major for the demand system (Part 5).

**Best response:**
1. **Hansen J overidentification test.** The overidentified demand system GMM produces a Hansen J statistic — report it and interpret it. While J-test failure is not definitive evidence of exclusion restriction violation (it may reflect other specification issues), J-test passage is supportive evidence.
2. **Spillover test.** Regress $Z^{MMF}_{m,t}$ on lagged NBFI FX swap flows ($Q_{NBFI,m,t-1}$). If the instrument is sector-specific, $Z^{MMF}$ should not predict NBFI flows after controlling for common time variation (absorbed by $\tau_t$). Report this test in the online appendix.
3. **Structural framing.** State clearly in the paper: "The demand system estimates require the exclusion restriction that each instrument shifts only its own sector's demand. We present evidence consistent with this assumption and note that the IV simple design (Part 3) does not require this restriction — it requires only that $Z^{MMF}$ is correlated with total foreign bank demand and uncorrelated with supply-side pricing after conditioning on market and time fixed effects."

### Objection 5: The theoretical contribution is not differentiated from the existing literature

**Precise statement:** "The inside/outside money distinction is from Gurley-Shaw (1960) and Holmström-Tirole (1998). The search-and-matching framework for OTC markets is from Duffie-Gârleanu-Pedersen (2005). The demand system is from Koijen-Yogo (2019). What is the new theoretical result? Applying three existing frameworks to FX swaps is a contribution to empirics, not to theory."

**Severity:** Major (for the theory contribution claim); minor (if the paper is repositioned as primarily empirical with theoretical motivation).

**Best response:**
1. **Identify the novel theoretical result.** The model has one candidate for a genuinely new proposition: the **quality endogeneity amplification loop** ($q_t \downarrow \to U_t \uparrow \to p_t \downarrow \to q_t \downarrow$). This feedback mechanism is absent in Gurley-Shaw (static), Holmström-Tirole (no search friction), Duffie-Gârleanu-Pedersen (no quality variable, no CES aggregator), and Koijen-Yogo (no matching, no amplification). The combination of CES quality + matching probability feedback produces a result those individual frameworks do not: a threshold above which inside dollar liquidity collapses discontinuously. **This is the result to develop formally (see Task 3 extension) and to position as the theoretical contribution.**
2. **Acknowledge the synthesis nature.** The paper's theoretical contribution is the synthesis — applying and combining these frameworks to the specific institutional setting of FX swap markets produces novel empirical predictions (sector-specific price elasticities, taker/maker search intensity, intermediation matrix dynamics). Acknowledge that no single element is novel but the combination generates new testable implications that existing frameworks do not produce.
3. **Comparative statics that distinguish the model.** Provide at least one comparative static that is observationally distinguishable from a simpler model. Candidate: a simpler supply-demand model (without the matching friction) predicts a continuous price response to demand shocks. The matching friction model predicts a non-linear (convex) price response: the same demand shock has a larger price impact when $\theta_t$ is already high. If this convexity is documented in the data (interacted with regime indicators), it is evidence for the matching framework over the simpler model.

---

## Recommended Primary Empirical Strategy

**Primary strategy: Shift-share IV (Approach A)**

Lead with the IV design. The primary estimand is the LATE for foreign banks affected by the MMF funding shock: the price impact of an exogenous demand shock on the FX swap basis. Specification:

**First stage:**
$$Q_{FB,m,t} = \alpha_m + \tau_t + \pi Z^{MMF}_{m,t} + \gamma \text{CDSAgg}_{m,t} + \delta Z^{EPFR}_{m,t} + u_{m,t}$$

**Second stage:**
$$\Delta\text{PriceUSD}_{m,t} = \alpha_m + \tau_t + \beta \hat Q_{FB,m,t} + \gamma \text{CDSAgg}_{m,t} + \varepsilon_{m,t}$$

**Inference:** Two-way clustered SE (market × week); wild cluster bootstrap given $\sim$36 markets; AKM SE in robustness.

**Secondary strategies (in order):**

1. Taker/maker mechanism test: separate first stages for $Q^{taker}$ and $Q^{maker}$ to demonstrate search-friction mechanism
2. Interaction heterogeneity: condition on DealerConstraint and QuarterEnd to document state-dependent amplification
3. Intermediation matrix: descriptive by sector and stress regime (no causal claim)
4. Demand system DS1: structural price sensitivity estimation and counterfactuals (clearly labeled structural extension)
5. Event study: swap line activations with cross-pair identification

**Robustness plan:**

1. Option A instrument (monthly MMF losses) vs. Option B shift-share (baseline)
2. Alternative weight windows (6m, 24m, fixed pre-period)
3. Anderson-Rubin confidence sets if F-stat approaches 10
4. Adão-Kolesár-Morales shift-share inference (baseline)
5. Alternative FX data: forwards and CCS (v8 §3.1 note: FX swaps baseline; these in robustness)
6. Full-sector aggregate $Q_{all,m,t}$ instead of FB-only (addresses $U_t$ truncation)
7. Balance tests on dominant-share banks (prerequisite for validity, not optional robustness)
8. **[Fix B3b] Pre-trend diagnostic:** Regress $\Delta\text{PriceUSD}_{m,t}$ on $Z^{MMF}_{m,t-k}$ for $k = 1, 2, 3$ periods prior to the funding shock. Coefficients should be statistically indistinguishable from zero if the instrument captures genuinely unexpected demand variation. Pre-trend evidence would suggest either (a) the MMF exposure weights predict future price movements for reasons unrelated to funding shocks, or (b) the $\text{FundingShock}_t$ captures anticipated rather than unexpected demand changes. This test is required before reporting the main IV results.
9. Swap line event study re-run on announcement dates (robustness for no-stigma assumption)
10. DealerConstraint × year fixed effects re-estimation (robustness for interaction instrument exclusion restriction)

---

## Overall Assessment and Phase 3 Readiness

**The paper is ready for Phase 3 activation with four conditions:**

1. **Theory language:** The theory document must be translated to English, propositions must be stated with formal assumptions (not just as equations), and the notation collision ($B_t$ for capacity vs. $B$ for demand slope) must be resolved before any code is written.

2. **P1 balance tests:** The shift-share instrument validity requires dominant-share bank balance tests as a prerequisite. Code for balance tests should be the first script produced in Phase 3.

3. **Demand system positioning:** The demand system (Approach B) should be coded as a separate module from the IV design (Approach A), with explicit acknowledgment in the code structure that the IV estimates do not depend on the demand system assumptions.

4. **P3 editorial decision:** Proposition 3 (threshold non-linearity) cannot be tested with the current empirical design. An editorial decision is needed before Phase 3 begins: (a) remove P3 from the formal propositions and treat it as structural interpretation only, (b) add the two-period extension to the theory and test it via calibration/structural-break methods, or (c) propose a dedicated threshold specification using the regime-indicator design as an approximation. **Recommendation: option (b) — add the two-period formal model and treat P3 as a calibration-consistent result, not an econometrically estimated result.**

---

*Strategy memo produced by: Strategist agent*
*Inputs read: `paper/theory/sections/inside-synthetic-dollar.tex`, `paper/design/empirical-roadmap-v8.md`, `quality_reports/explorer/feasibility-assessment.md`*
*Missing input: `quality_reports/explorer/explorer-critic-review-r2.md` (file not found)*
*Phase: Strategy — Round 2 revision*
*Target: Strategist-Critic scoring against 4-phase rubric (identification design, fundamental assumptions, theory-code alignment, robustness planning)*

---

## Phase 2 Completion Record

| Agent | Final Score | Rounds | Status |
|-------|-------------|--------|--------|
| Explorer | 82/100 | 2 | ✅ PASS |
| Explorer-Critic | 82/100 | 2 | ✅ PASS |
| Strategist | 89/100 | 2 | ✅ PASS |
| Strategist-Critic | 89/100 | 2 | ✅ PASS |
| Theorist | 86/100 | 3+exceptional | ✅ PASS |
| Theorist-Critic | 86/100 | 3+exceptional | ✅ PASS |

**Phase 2 gate cleared. Phase 3 (Data-Engineer + Writer) pending user validation.**
