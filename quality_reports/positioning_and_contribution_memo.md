# Positioning and Contribution Memo
## Dollar Funding Hierarchies, Backstop Architecture, and the Propagation of Liquidity Crises

**Date:** 2026-05-07
**Status:** ROUND 2 — Revised per Strategist-Critic Round 1 feedback (2026-05-07)

---

## Pre-Strategy Report

**Input files loaded:**

1. `/home/user/test/quality_reports/pure_theoretical_model_memo.md` — READ IN FULL. Round 2 approved version (score 83/100). All propositions 1–7, definitions of Δ, ρ, M, and equation tags verified.

2. `/home/user/test/quality_reports/theoretical_discovery_record.md` — READ (Batches 1 and 2, papers 1–39). Key formal entries extracted: Gabaix & Maggiori (2015, paper 1), Bacchetta-Davis-van Wincoop (2024, paper 10), Kloks-Mattille-Ranaldo (2023, paper 6). Papers 2 (Baba-Packer-Nagano), 3 (Nenova-Schrimpf-Shin), 4 (Huang-Ranaldo-Schrimpf-Somogyi), and 14–39 read.

**Scope note:** Brunnermeier & Pedersen (2009), Holmström & Tirole (1998), Diamond & Dybvig (1983), Chang & Velasco (2001), He & Krishnamurthy (2013), Murau-Pape-Pforr (2023), Mehrling (2021), and Cesa-Bianchi-Eguren-Martin-Ferrero (2025) are cited in the model memo as motivating anchors but do NOT appear as standalone fiches in the discovery record. Their mathematical characterization below is drawn exclusively from how the model memo itself describes and deploys these papers, not from independently read source documents. Claims are explicitly flagged as "per model memo" where this applies.

---

## A. Core Novelty Claim

Existing models of dollar funding stress treat segmentation as parametric: either all foreign banks face symmetric balance-sheet constraints (Du-Tepper-Verdelhan 2018; Bacchetta-Davis-van Wincoop 2025) or the policy instrument — a swap line — contracts a single representative foreign bank (Cesa-Bianchi et al. 2025). None derives segmentation from a hierarchy of backstop quality, and none closes the feedback loop running from fire sales through dealer wealth back to swap supply. This paper introduces three structural innovations that did not exist simultaneously in a single internally consistent model. First, a three-tier backstop hierarchy is formalized as a structural primitive of the model environment: $B_1 = M_1$ (US banks, full coverage), $B_2 = \lambda M_2$ (swap-line recipients, partial coverage $\lambda \in [0,1]$), and $B_3 = 0$ (offshore users, no coverage), with residual funding needs $R = (1-\lambda)M_2 + M_3 + \varepsilon$ derived from institutional architecture alone. Second, the fire-sale and dealer-wealth channels are closed in the equilibrium basis formula $b^* = (R - \Gamma\tilde{W})/\Delta$ (EQ), where $\Delta \equiv \Theta(P_0 - \Gamma\gamma\bar{X}_d)$ ($\Delta$-def), producing the directional amplification spiral with multiplier $\mathcal{M} = 1/(1-\rho)$ (M-def), where $\rho \equiv \Gamma\gamma\bar{X}_d/P_0$ ($\rho$-def). Third, regulation $\tau$ and backstop $\lambda$ are shown to be imperfect substitutes along an explicit policy frontier $\tau^{\rm safe}(\lambda, b^{\max})$ (Proposition 6), with $\partial\tau^{\rm safe}/\partial\lambda > 0$ derived from the implicit function theorem.

---

## B. Direct Confrontation (Model vs. Literature)

---

**Gabaix & Maggiori (2015, QJE)**

- *Their contribution:* A two-country model in which a single class of global financial intermediaries ("financiers") absorbs the portfolio imbalance $D_t$ between households at a cost governed by limited commitment. Their equilibrium exchange rate is $e_t = \bar{e} - (1/\Gamma)\cdot D_t$, where $\Gamma$ is the aggregate financier capacity parameter. Their intermediary FOC is $E_t[\Delta e_{t+1}] + (i_t - i^*_t) = \Gamma \cdot Q_t$, generating an endogenous exchange-rate risk premium.

- *Their limit:* The financier population is homogeneous: all intermediaries face the same constraint tightness $1/\Gamma$, and the capacity parameter $\Gamma$ is fixed and exogenous. There is no hierarchy of access to official liquidity backstops, no distinction between a bank with a swap-line guarantee and one without, and no feedback from asset prices (Treasury fire sales) to dealer wealth to swap supply. The model cannot generate contagion from an uncovered segment to a covered one because there is only one intermediary segment.

- *Our advance:* The dealer capacity $\Gamma = \phi/q_S$ (O-star) is derived from Basel leverage parameters and endogenously links to dealer wealth $W(P) = W_0 + P\bar{X}_d$ (W-b). The three backstop tiers $(B_1, B_2, B_3)$ replace the single homogeneous $\Gamma$. Cross-segment contagion is Proposition 4: a shock $d\varepsilon$ to segment 3 raises segment 2 fire sales $dx_2^*/d\varepsilon = \theta_2 \mathcal{M}/(P_0\Theta) > 0$ despite $dR_2 = 0$, a result with no counterpart in Gabaix-Maggiori.

---

**Brunnermeier & Pedersen (2009)**

- *Their contribution (per model memo):* The canonical model of the liquidity spiral, in which margin constraints on speculators create a feedback between asset prices and funding costs. Their mechanism is a two-way reinforcement: funding liquidity tightens when asset prices fall, and falling asset prices follow from the funding constraint binding.

- *Their limit (per model memo):* Brunnermeier-Pedersen model the spiral in a domestic market context. The international dollar-funding dimension — specifically, how the spiral operates through the cross-currency basis, Treasury fire sales by foreign banks, and the leverage constraint of a global swap dealer — is absent. The model does not produce a closed-form multiplier that summarizes the spiral's strength, nor does it characterize how official backstop coverage attenuates the loop.

- *Our advance:* The amplification decomposition in Proposition 2 is the closed-form international-dollar-funding analog of the Brunnermeier-Pedersen liquidity spiral, specialized to the international dollar-funding market: $b^* = b^{\rm pe} \cdot \mathcal{M}$ (AMP), where $\mathcal{M} = 1/(1-\rho)$ (M-def) is the closed-form sum of the geometric series of feedback rounds. The amplification ratio $\rho = \Gamma\gamma\bar{X}_d/P_0$ (ρ-def) identifies which primitives govern spiral intensity: dealer capacity $\Gamma$, Treasury price elasticity $\gamma$, and dealer inventory $\bar{X}_d$. Proposition 3 characterizes the monotone dependence of $\mathcal{M}$ on each parameter, which Brunnermeier-Pedersen do not derive.

---

**Du, Tepper & Verdelhan (2018)**

- *Their contribution (per model memo):* Empirical documentation that covered interest parity (CIP) fails persistently for major currencies since 2008 and that balance-sheet constraints of financial intermediaries drive the deviation. Their fiche (paper 19, discovery record) defines the CIP deviation $x_{i,t} = \rho_{i,t} + F_{i,t} - S_{i,t} - \rho^{USD}_t$ and identifies the regulatory leverage ratio $\text{Tier1Capital}_{b,t}/\text{TotalExposure}_{b,t} \geq \ell$ as the binding constraint.

- *Their limit:* The constraint is symmetric across all foreign intermediaries: all face the same leverage ratio friction. Segmentation — the differential between a bank whose central bank has a swap line and one that does not — is entirely absent. The model cannot speak to how uncovered institutions transmit stress to covered ones, or to how swap-line coverage shifts the equilibrium basis level.

- *Our advance:* The equilibrium basis formula $b^* = (R - \Gamma\tilde{W})/\Delta$ (EQ) has $R = (1-\lambda)M_2 + M_3 + \varepsilon$ (Section B.3), where $\lambda \in [0,1]$ is the swap-line coverage rate. Proposition 5 shows $db^*/d\lambda = -M_2\mathcal{M}/(P_0\Theta) < 0$ (SL): the basis responds to coverage asymmetry in a way that Du-Tepper-Verdelhan's single-segment framework cannot produce. The leverage constraint (LC) for the dealer is the same Basel-type structure as Du et al., but here it is endogenously linked to Treasury prices through $W(P) = W_0 + P\bar{X}_d$.

---

**Bacchetta, Davis & van Wincoop (2025, JIE forthcoming)**

- *Their contribution:* A general equilibrium model jointly determining the spot exchange rate $e_t$ and CIP deviation $\rho_t$ through two market-clearing conditions — $D^{\rm spot}_t(e_t, \rho_t) = 0$ and $D^{\rm swap}_t(e_t, f_t, \rho_t) = 0$ — with an intermediary arbitrage capacity constraint $|z^{CIP}_t| \leq \chi_t$ that is endogenous. This is the most complete existing model for joint determination of $e_t$ and $\rho_t$.

- *Their limit:* The arbitrage capacity $\chi_t$ is endogenous but does not derive from an explicit backstop hierarchy: all CIP arbitrageurs face the same constraint. The model has one class of constrained intermediaries and cannot generate hierarchical contagion — a shock to agents with no backstop propagating through agents with a partial backstop to the dealer. The swap-line coverage rate $\lambda$ does not appear; policy analysis is limited to the comparative statics of $\chi_t$.

- *Our advance:* The three-tier residual funding needs $(R_1 = 0, R_2 = (1-\lambda)M_2, R_3 = M_3 + \varepsilon)$ endogenize the analog of Bacchetta et al.'s $\chi_t$ from institutional architecture. Proposition 4 derives the cross-segment contagion in terms of observable model primitives: $db^*/d\varepsilon = \mathcal{M}/(P_0\Theta)$ (CS-eps), and $dW^*/d\varepsilon = -\gamma\bar{X}_d\mathcal{M}/P_0 < 0$ (part iii). These objects have no counterpart in Bacchetta-Davis-van Wincoop's single-segment framework.

---

**Cesa-Bianchi, Eguren-Martin & Ferrero (2025, JME forthcoming)**

- *Their contribution (per model memo):* Analysis of Federal Reserve swap lines as a mechanism expanding dollar liquidity supply to foreign central banks, relaxing the funding constraint of a representative foreign bank. Single-segment and single-instrument: one class of foreign intermediary, one official facility.

- *Their limit (per model memo):* The treatment abstracts from (i) heterogeneity in backstop coverage across classes of foreign institutions, (ii) fire-sale externalities in collateral markets, and (iii) the endogenous response of dealer capacity to asset price movements triggered by the swap-line regime. The model cannot speak to contagion from uncovered segments to covered ones, or to non-linearity of swap-line effectiveness as a function of aggregate stress.

- *Our advance:* Proposition 5 decomposes swap-line effectiveness into two channels: Channel 1 (demand relief, $-M_2/(P_0\Theta)$, the mechanism in Cesa-Bianchi et al.) and Channel 2 (collateral stabilization, the factor $\mathcal{M}$, which is new). The Corollary to Proposition 5 establishes state-dependence: $\partial|db^*/d\lambda|/\partial\rho > 0$ — swap lines are more effective precisely when the amplification loop is stronger. This non-linearity has no representation in Cesa-Bianchi et al.'s single-segment framework.

---

**Holmström & Tirole (1998)**

- *Their contribution (per model memo):* The inside/outside liquidity framework, in which firms hold claims on each other (inside liquidity) and central banks provide outside liquidity. The key result is that inside liquidity is insufficient to insure all aggregate shocks, motivating a role for government provision of outside liquidity.

- *Their limit (per model memo):* The framework is a domestic model. The international analog — in which the dollar is the outside liquidity for the entire global financial system, and the Federal Reserve's swap lines are the only instrument for providing it to offshore institutions — is not modeled. The hierarchy of backstop access (automatic for US banks, conditional for swap-line recipients, absent for offshore dollar users) is an institutional feature without formal representation.

- *Our advance:* The three-tier backstop structure $(B_1 = M_1, B_2 = \lambda M_2, B_3 = 0)$ is the international analog of Holmström-Tirole's inside/outside liquidity partition, formalized as a structural primitive of the model environment rather than imposed parametrically. Proposition 7 connects to the Holmström-Tirole framework: the run-zone $(\underline\lambda, \bar\lambda)$ characterizes the region where inside liquidity (private markets) is insufficient and outside liquidity (the swap line at coverage $\lambda_{\min} \geq \bar\lambda$) is necessary to eliminate the run equilibrium.

---

**Diamond & Dybvig (1983) / Chang & Velasco (2001)**

- *Their contribution (per model memo):* Diamond-Dybvig is the canonical model of bank runs as self-fulfilling equilibria; Chang-Velasco extends this to the international context, characterizing conditions for currency crises and sudden stops as coordination failures on the exchange-rate regime.

- *Their limit (per model memo):* The coordination failure in both frameworks is over the exchange-rate peg or the bank's liquidity ratio, not over the coverage rate of an official backstop facility. The threshold that separates run from no-run equilibria is not linked to the institutional design of swap lines or to the structural parameters of the dollar funding market (dealer capacity $\Gamma$, fire-sale elasticity $\Theta$, outside-investor elasticity $\gamma$).

- *Our advance:* The model provides the formal input that the global-game extension requires: the closed-form $b^*(\lambda)$ from Proposition 1 (EQ) and its derivative $db^*/d\lambda = -M_2\mathcal{M}/(P_0\Theta) < 0$ from Proposition 5 (SL). Section D.9 of the model memo develops this into an incomplete proof sketch (Proposition 7) establishing conditions for run-zone multiplicity. The thresholds $\underline\lambda$ and $\bar\lambda$ are defined in terms of the equilibrium basis function, but the full verification of global-game uniqueness conditions is flagged as an open item (model memo, Open Question 5) and will be completed before submission.

---

**He & Krishnamurthy (2013)**

- *Their contribution (per model memo):* A dynamic model of intermediary asset pricing in which dealer net worth is the state variable. The model generates endogenous risk premia and asset-price amplification driven by the evolution of intermediary capital over the business cycle. The central mechanism is that constrained dealers must be compensated for holding risky assets, and this compensation varies with their net worth.

- *Their limit (per model memo):* He-Krishnamurthy (2013) is a dynamic model; the amplification operates through the time path of dealer net worth as a state variable. The model does not characterize the international dollar-funding market specifically — the cross-currency basis, the FX swap market, or the role of official backstop facilities in attenuating the amplification.

- *Our advance:* The current model is static; the link to He-Krishnamurthy is structural rather than formal. The dealer wealth channel $W(P) = W_0 + P\bar{X}_d$ (Section C.3) captures the same intuition in closed form within a static setting: dealer net worth determines swap supply through (O-star), and this feeds back into Treasury prices via (P-eq). The amplification multiplier $\mathcal{M} = 1/(1-\rho)$ (M-def) is the static closed-form analog of the dynamic risk-premium amplification in He-Krishnamurthy. Section G (open question 1) explicitly notes that the dynamic extension would follow He-Krishnamurthy by introducing $\rho$ as an endogenous state variable — a natural next step not undertaken in the present paper.

---

**Murau, Pape & Pforr (2023) / Mehrling (2021)**

- *Their contribution (per model memo):* An institutional taxonomy of the international monetary hierarchy — the Federal Reserve at the apex, primary dealers at an intermediate tier, foreign banks with swap lines at a subordinate tier, and offshore dollar users without any official backstop at the periphery. Rich in institutional description and historically grounded.

- *Their limit (per model memo):* These papers provide a conceptual architecture without a formal model: no equilibrium conditions, no optimization problems, no formal mechanism linking backstop architecture to the cross-currency basis. The notions of "hierarchy," "backstop quality," and "propagation" remain descriptive.

- *Our advance:* The model converts the Murau-Pape-Pforr taxonomy into a formal static equilibrium. The four levels of their hierarchy map to: Fed (backstop provider, not modeled explicitly), segment 1 (US commercial banks, $R_1 = 0$), segment 2 (swap-line recipients, $R_2 = (1-\lambda)M_2$), and segment 3 (offshore users, $R_3 = M_3 + \varepsilon$). The cross-currency basis $b^*$ in (EQ) is the equilibrium object that quantifies what Murau et al. can only describe qualitatively: the price of being at a lower tier of the hierarchy. Proposition 4 formalizes "propagation" as a precise comparative static with closed-form coefficients.

---

**Kloks, Mattille & Ranaldo (2023)**

- *Their contribution:* An empirical characterization of FX swap liquidity, distinguishing tightness $\text{Spread}^{\rm FX\,swap}_{j,t} = (F^{\rm ask}_{j,t} - F^{\rm bid}_{j,t})/F^{\rm mid}_{j,t}$ and depth $\text{Depth}_{j,t} = \text{Volume dealer-intermediated}_{j,t}$. The key empirical finding is a new demand channel: non-bank financial institutions use FX swaps for short-term funding precisely when liquidity deteriorates, driven by the regulatory window-dressing of G-SIB dealers at quarter-end ($\text{Constraint}_{d,t} = \mathbf{1}[\text{G-SIB}_d] \cdot \mathbf{1}[\text{Quarter-end}_t]$), with volume rising even as liquidity falls.

- *Their limit:* Kloks et al. do not derive a formal equilibrium model: the relationship between dealer constraints and the basis is documented empirically without a mechanism linking dealer balance sheets to Treasury fire sales and back to swap supply. The paper cannot characterize how a backstop facility (like a swap line) would affect the volume-liquidity relationship, nor does it provide a multiplier linking the intensity of the dealer constraint to the size of the basis widening.

- *Our advance:* The dealer optimization (P-D) subject to leverage constraint (LC) formalizes the G-SIB constraint Kloks et al. document. The binding constraint yields $O^* = \Gamma W(P)$ (O-star), where the feedback $W(P) = W_0 + P\bar{X}_d$ is the structural mechanism behind the empirical observation that "volume rises as liquidity falls" — dealers' wealth compression reduces swap supply precisely when demand is highest. Proposition 3(i) shows $\partial\mathcal{M}/\partial\Gamma > 0$: a larger dealer amplifies more, consistent with the finding that G-SIBs are disproportionately responsible for the quarter-end pattern.

---

## C. Battle Plan for the Introduction

- Proposition 2: the equilibrium basis satisfies $b^* = b^{\rm pe} \cdot \mathcal{M}$ with $\mathcal{M} = 1/(1-\rho)$, $\rho \equiv \Gamma\gamma\bar{X}_d/P_0$, amplifying any funding shock by the closed-form multiplier.

- Proposition 4: shock $d\varepsilon > 0$ to uncovered segment 3 raises segment 2 fire sales by $dx_2^*/d\varepsilon = \theta_2\mathcal{M}/(P_0\Theta) > 0$ with no direct shock to segment 2.

- Proposition 6: the policy frontier $\tau^{\rm safe}(\lambda, b^{\max})$ satisfies $\partial\tau^{\rm safe}/\partial\lambda > 0$ — a stronger backstop expands the set of stable regulatory tightening.

---

*End of Positioning and Contribution Memo.*
