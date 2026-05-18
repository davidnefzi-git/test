# Explorer Feasibility Report
## Theoretical Object Mapping and Empirical Feasibility Assessment
## Paper: "Who Supplies Synthetic Dollars? Bilateral Microstructure of Demand and Supply in FX Swap Markets"

**Date:** 2026-05-18
**Input documents:**
- `paper/theory/sections/inside-synthetic-dollar.tex` (theoretical framework)
- `paper/design/empirical-roadmap-v8.md` (empirical roadmap v8)

---

## A. Theoretical Object Inventory

### 1. U_t — Mass of agents seeking to convert inside to outside dollars (demand)

**Definition (theory §6.1):** Mass of agents seeking to convert inside synthetic dollar liquidity (I_t) to outside safe dollar liquidity (O_t). Enters the matching function M_t = η · U_t^γ · B_t^(1−γ). Rises in stress: S_t ↑ → U_t ↑ (§11).

**Proposed proxy (v8 §2.5, §3.4):** Q_{FB,m,t} = NetUSDTaking of foreign banks in currency pair m at date t. Constructed as:
```
Q_{FB,m,t} = Σ_{c ∈ m, sector=FB} SignedUSDFlow_{c,t}
```
where SignedUSDFlow > 0 denotes the leg on which the agent receives USD.

**Data source:** Bilateral regulatory FX swap transaction data (v8 §3.1). Both counterparties identified by name, sector, country.

**Coverage:**
- Currency pairs: ~36 markets (inferred from v8 §11 "~36 marchés")
- Tenors: ON, 1W, 1M, 3M, 6M, 1Y+ (v8 §3.3)
- Sectors: foreign banks (FB), NBFI, dealers, hedge funds, asset managers, corporates
- Time period: not explicitly stated in either document, but implied to cover at least pre/post 2016 MMF reform and COVID March 2020 (v8 §7.2)

**Feasibility grade: B**

**Notes:** The proxy is compelling and directly motivated by the theory (§6.3 of the theory file explicitly maps U_t to "la demande nette de USD des banques étrangères (Q_{FB} dans la v8)"). However, U_t in the model refers to the mass of ALL agents seeking conversion, not just foreign banks. The v8 focuses on the FB sector as the primary demand group but the theory is broader. This means the proxy captures the main empirically relevant component of U_t (foreign bank wholesale dollar demand) but not corporate or NBFI demand for conversion. The taker/maker decomposition (v8 §3.5) strengthens the proxy: takers are placing urgent demand, closer to the model's "agents seeking conversion."

---

### 2. B_t — Aggregate conversion capacity of intermediaries (supply)

**Definition (theory §7.1):** Aggregate balance sheet capacity of conversion intermediaries:
B_t = B_t^FBO + B_t^USbank + B_t^dealer + B_t^HF + B_t^CBswap

Each component has its own determinants (§7.2–7.3): FBO capacity decreases in stress S_t and at quarter-ends Q_t; HF capacity is profit-driven and state-dependent.

**Proposed proxy (v8 §4.4, §2.5):** DealerCapacity_t, constructed as:
```
DealerCapacity_t = f(Primary Dealer repo, H.8 Borrowings, leverage)
```
Supplemented by: (i) Primary Dealer data from Fed; (ii) H.8 bank balance sheet data; (iii) quarter-end indicator Q_t (Proposition 4 of theory).

**Data source:**
- Primary Dealer data: Federal Reserve (listed in v8 §12 "Disponibles")
- FED H.8 release: Federal Reserve (v8 §12)
- B^CBswap component: Fed swap line drawings (theory §7.4, also v8 §7.2 "COVID mars 2020 — tous se retirent sauf Fed swap lines?")

**Coverage:**
- Primary Dealer data: US dealers, weekly frequency
- H.8: US commercial banks, weekly
- Swap line drawdowns: published by Fed, episodic (crisis periods)
- HF component (B_t^HF): NOT directly observed; inferred residually

**Feasibility grade: C**

**Notes:** This is the weakest link in the empirical chain. The theory specifies a rich decomposition (§7.1 equation) with five distinct components. The v8 proxies the aggregate with dealer-centric balance sheet measures. Three specific gaps:
1. B_t^FBO (FBO branch capacity) is not directly observable in the stated data sources — FBO balance sheets are not in H.8 in disaggregated form.
2. B_t^HF is not measured directly; hedge fund capacity is only inferred from Z^HF = (−TIB_{m,t−1}) × RiskCapacity_t, which v8 explicitly labels "pas un instrument strict" (§4.4).
3. The theory's B_t is the denominator of θ_t = U_t/B_t (market tightness), but the empirical design primarily uses B_t as a conditioning variable (DealerConstraint interaction) rather than directly constructing θ_t.

---

### 3. q_t — Effective quality of synthetic dollar liquidity

**Definition (theory §4.1, §6.2):** q_t ∈ (0,1] measures how much service of safe dollar liquidity one unit of synthetic dollar liquidity provides. Endogenous: q_t = q(p_t) with q'(p) > 0. Deteriorates when matching probability falls.

**Proposed proxy (v8 §2.5):** Three complementary proxies:
1. TIB = Transaction-Implied Basis (level of the basis, primary measure of conversion cost)
2. Dispersion of prices (bid-ask spread, cross-sectional dispersion of PricePaid across sectors)
3. Taker/maker ratio: π^taker (share of volume initiated by takers vs. makers)

**Data source:** Bilateral regulatory FX swap transaction data (v8 §3.2, §3.6):
```
TIB_{m,t} = volume-weighted median of forward points in m
Spread_{s,m,t} = PricePaid_{s,m,t} − PricePaid_{interdealer,m,t}
```

**Coverage:** Same as FX transaction data: ~36 currency pairs, all tenors, daily/weekly.

**Feasibility grade: B**

**Notes:** q_t is a latent variable in the model — it cannot be measured directly. The three proxies each capture a dimension of "quality of synthetic dollar liquidity" but none maps cleanly to the CES parameter q_t in equation (1) of the theory. Specific concerns:
- TIB measures the PRICE of conversion, which is μ_t in the model. Using it also as a proxy for q_t creates potential circular reasoning (the theory derives μ_t as a function of q_t, so they are correlated by construction).
- The taker/maker ratio is the cleanest proxy for p_t (matching probability), not q_t directly — q_t = q(p_t) by equation (4) of the theory, so the taker ratio is an indirect proxy for q_t.
- Price dispersion (Spread_{s,m,t}) proxies rationing: when q_t is low, the same synthetic dollar is priced differently across sectors. This is a valid and distinct proxy from TIB.

---

### 4. p_t — Matching probability for a demander

**Definition (theory §6.1):** p_t = M_t/U_t = η · (B_t/U_t)^(1−γ). Probability that a demander finds a conversion counterparty. Falls when θ_t = U_t/B_t rises.

**Proposed proxy (v8 §2.5):** "Approximé par le taker ratio, la dispersion des prix, ou le spread client-interdealer."

Specifically, from v8 §3.5:
```
Q_{s,m,t} = Q^{taker}_{s,m,t} + Q^{maker}_{s,m,t}
```
The taker fraction (Q^taker/Q_total) proxies the fraction of demand that was successfully matched on urgent (taker) terms — higher taker share implies agents had to pay up to find a counterparty, consistent with lower p_t.

**Data source:** Bilateral regulatory FX swap transaction data (v8 §3.5). Taker/maker flag directly observed.

**Coverage:** Same as FX transaction data.

**Feasibility grade: B**

**Notes:** The taker/maker flag is a credible proxy because takers initiate trades and pay the spread; higher taker share is consistent with lower matching probability (agents must search harder). The v8 uses this as a diagnostic (§5.1: "π^{taker} >> π^{maker} attendu") not as a left-hand-side variable, which is appropriate. However, p_t in the model is a continuous probability — the taker ratio is a discrete operational construct that conflates "urgency of demand" with "difficulty of matching." In liquid markets, high taker share can reflect convenience rather than search friction.

---

### 5. θ_t = U_t/B_t — Market tightness

**Definition (theory §6.1):** θ_t = U_t/B_t is the ratio of demand for conversion to supply capacity. θ_t ↑ → p_t ↓ → q_t ↓. Central to the amplification mechanism (§11).

**Proposed proxy (v8 §2.5):** "Ratio demande/capacité." No dedicated variable construction is described; it is implied by interacting Q_{FB,m,t} (proxy for U_t) with DealerCapacity_t inverse (proxy for 1/B_t).

**Data source:** Constructed from FX transaction data (numerator Q_{FB}) and Primary Dealer/H.8 data (denominator DealerCapacity).

**Coverage:** Inherits coverage of U_t and B_t proxies. Not constructed as a standalone time series in v8; appears only as a conceptual motivation for the interaction specifications in §5.3 (P6, P7).

**Feasibility grade: C**

**Notes:** θ_t is the most important unobserved variable for the theory's amplification mechanism (§11: "θ_t ↑↑ → p_t ↓↓ → q_t ↓↓ → μ_t ↑↑"). The v8 does not directly construct this ratio. Instead:
- P6 (v8 §9) tests whether price impact is amplified when DealerConstraint is high — this is equivalent to testing whether high θ_t (low B_t) amplifies the effect of a U_t shock, but it is not a direct measurement of θ_t.
- P7 tests quarter-end effects, which map to Proposition 4 of the theory (Q_t = 1 ⟹ B_t ↓ ⟹ μ_t ↑).
- The non-linearity in Proposition 3 (threshold effect in θ_t) is not directly tested in the v8 design.

---

### 6. μ_t — Synthetic dollar funding spread (PriceUSD in v8)

**Definition (theory §5, §10):** μ_t = R_I − R_O = the spread between the cost of inside synthetic dollar liquidity and outside safe dollar liquidity. The equilibrium price of conversion. Also the cross-currency basis.

**Proposed proxy (v8 §2.2, §3.2):** PriceUSD_{m,t} = −TIB_{m,t}, where TIB is the Transaction-Implied Basis computed as the volume-weighted median of forward points in currency pair m. PriceUSD > 0 means synthetic dollars are expensive relative to safe dollars.

Sector-specific price: PricePaid_{s,m,t} = −TIB_{s,m,t}.

**Data source:** Bilateral regulatory FX swap transaction data (v8 §3.6). Validated against Bloomberg CCBS quotes (v8 §12 "À obtenir: CCBS Bloomberg").

**Coverage:** ~36 currency pairs, all tenor buckets, daily/weekly frequency.

**Feasibility grade: A**

**Notes:** This is the strongest mapping in the entire framework. μ_t = PriceUSD is motivated identically in both the theory file (§5: "empiriquement, c'est le cross-currency basis (ou PriceUSD dans la v8)") and the v8 (§2.2: "Le prix de cette conversion est le Transaction-Implied Basis (TIB)"). The transaction-based TIB is superior to Bloomberg CCBS quotes because it is computed from actual bilateral transactions rather than indicative quotes, allowing sector-specific price dispersion measurement (Spread_{s,m,t}). One caveat: the market-level TIB uses a volume-weighted median, which could be influenced by the composition of transactors in that period — creating a potential endogeneity between measured price and the sector composition of demand.

---

## B. Proposition Testability Assessment

### Proposition 1 — Synthetic Liquidity Premium
**Theory (§12):** ∂μ_t/∂U_t > 0 — holding capacity constant, higher conversion demand raises the spread.

**Empirical counterpart:** P2 (v8 §9) — "Cette demande instrumentée rend le dollar synthétique plus cher." β > 0 in the second stage of the IV.

**Testable condition:**
```
ΔPriceUSD_{m,t} = α_m + τ_t + β Q̂_{FB,m,t} + γ CDSAgg_{m,t} + ε_{m,t}
H₀: β = 0 vs. H₁: β > 0
```

**Data requirements:** FX swap transaction data (Q_{FB,m,t} and PriceUSD_{m,t}), MMF data for the instrument Z^MMF, CDS data for CDSAgg.

**Identification challenge:** The main threat is that the MMF funding shock is correlated with aggregate dollar shortage stress (τ_t absorbs the common component, but cross-market variation in exposure must be genuinely predetermined). If bank-currency-pair exposures to prime MMFs were endogenously allocated based on anticipated stress, the shift-share instrument is invalid.

**Feasibility verdict: TESTABLE**

---

### Proposition 2 — Stabilizing Role of Capacity
**Theory (§12):** ∂μ_t/∂B_t < 0 — higher capacity reduces the spread.

**Empirical counterpart:** P6 (v8 §9) — "Le price impact est amplifié quand les dealers sont contraints." β₂ > 0 in the interaction specification:
```
ΔPriceUSD = α_m + τ_t + β₁ Q̂ + β₂ [Q × DealerConstraint]̂ + ε
```
If β₂ > 0, then when B_t is low (DealerConstraint high), the same demand shock produces a larger price response — consistent with ∂μ_t/∂B_t < 0.

**Testable condition:** β₂ > 0 in the interaction specification.

**Data requirements:** FX swap data (PriceUSD, Q_{FB}), Primary Dealer data and H.8 for DealerCapacity_t.

**Identification challenge:** DealerConstraint_t is endogenous — dealer constraints tighten precisely when USD stress is high, making the interaction term potentially contaminated by omitted stress variables not absorbed by τ_t. The v8 uses two endogenous variables with two instruments (v8 §5.3) but the interaction instrument Z × DealerConstraint inherits the endogeneity of DealerConstraint.

**Feasibility verdict: PARTIALLY TESTABLE** — the sign and significance of β₂ is testable, but clean causal identification of the capacity channel requires exogenous variation in B_t, which is not available in the stated design.

---

### Proposition 3 — Non-linearity
**Theory (§12):** When θ_t = U_t/B_t crosses a threshold, q_t can drop rapidly (threshold/regime effect).

**Empirical counterpart:** Not directly mapped to a single prediction in v8 §9. Partially captured by P6 (amplification when DealerConstraint high) but the threshold non-linearity is not explicitly modeled.

**Testable condition:** A non-linear (spline, threshold regression, or quantile regression) specification of the form:
```
ΔPriceUSD = f(Q_{FB}, DealerCapacity, Q_{FB}/DealerCapacity) with structural break
```
This is not in the current v8 design.

**Data requirements:** Sufficient time-series variation in θ_t proxies to identify threshold; crisis episodes (COVID, GFC, 2008) required.

**Identification challenge:** Threshold models require precise knowledge of the threshold value θ* and are sensitive to the proxy for θ_t. With B_t only partially observed, the θ_t = U_t/B_t ratio is noisy.

**Feasibility verdict: NOT TESTABLE WITH STATED DATA** — the non-linearity proposition requires either a structural break test on θ_t or a quantile IV approach, neither of which is in v8. The current interaction design tests effect heterogeneity, not threshold non-linearity.

---

### Proposition 4 — Quarter-End
**Theory (§12):** Q_t = 1 ⟹ B_t ↓ ⟹ μ_t ↑.

**Empirical counterpart:** P7 (v8 §9) — "Le price impact est amplifié en quarter-end." β₂ > 0 in:
```
ΔPriceUSD = α_m + τ_t + β₁ Q̂ + β₂ [Q̂ × QuarterEnd] + ε
```

**Testable condition:** β₂ > 0 when QuarterEnd = 1.

**Data requirements:** FX swap data; quarter-end indicator is a deterministic variable. No additional data needed beyond what is already in the v8.

**Identification challenge:** Quarter-end effects are well-documented (Kloks-Mattille-Ranaldo 2024 is cited in v8 §1.1). The challenge is distinguishing B_t ↓ (supply side) from U_t ↑ (demand side) at quarter-ends, since both could rise simultaneously. The theory attributes the quarter-end effect to B_t ↓ (regulatory reporting), but the IV design does not separately identify the two channels.

**Feasibility verdict: TESTABLE** — P7 is cleanly testable, though attribution to the supply-side (B_t) mechanism rather than demand-side requires auxiliary evidence.

---

### Proposition 5 — Swap Lines
**Theory (§12):** Swap lines ⟹ B_t ↑ ⟹ p_t ↑ ⟹ q_t ↑ ⟹ μ_t ↓. B^CBswap component of B_t (theory §7.1).

**Empirical counterpart:** Referenced in theory §7.4 ("Fed swap lines → B^CBswap — observable via les tirages de swap lines") and v8 §7.2 (event study "COVID mars 2020 — tous se retirent sauf Fed swap lines?") and counterfactual CF3 (v8 §6.5: "CF3 — Activation des swap lines: B^CBswap augmente → B augmente → price impact diminue").

**Testable condition:** Event study: ΔPriceUSD_{m,t} falls following Fed swap line activation announcement (discontinuity or synthetic control). Or: inclusion of swap line drawdown volume as a regressor in the price equation.

**Data requirements:** Fed swap line drawdown data (publicly available from Fed). Event dates for swap line activations (March 19, 2020; October 2008; etc.).

**Identification challenge:** Swap lines are activated precisely during crises, making causal identification from an event study difficult: the price decline post-activation confounds the policy effect with natural stress resolution. A plausible design would use cross-currency variation (some currency pairs covered by swap lines, others not) but this requires careful matching.

**Feasibility verdict: PARTIALLY TESTABLE** — the event study design is feasible with stated data but the identification of the causal effect (vs. coincident stress resolution) is not clean. Counterfactual CF3 is labeled "model-based simulation" in v8, not a causal estimate.

---

### Proposition 6 — Provider Heterogeneity
**Theory (§12):** Hedge funds supply capacity when basis is attractive but withdraw in extreme stress. Dealers supply by market-making obligation but are balance-sheet constrained. Swap lines are countercyclical.

**Empirical counterpart:** P3 (v8 §9) — "|β_{FB}| < |β_{HF}|" (FB more price-inelastic than HF); P4 — "dealers US absorbent la majorité de la demande excédentaire"; and the intermediation matrix analysis (v8 §7.1).

**Testable condition:** DS1/DS2 demand system estimates showing:
- β_{FB} < 0 (banks demand USD regardless of price)
- β_{HF} > 0 (hedge funds supply more when price rises)
- Dealer share > 40% in the intermediation matrix

**Data requirements:** Sector-identified bilateral FX swap data (directly available); EPFR for AM shifter; Z^HF for hedge fund instrument (though v8 notes this is "pas un instrument strict," §4.4).

**Identification challenge:** The demand system requires cross-sectional exclusion restrictions (Z^MMF only shifts FB; Z^EPFR only shifts NBFI). The exclusion assumption for the HF equation is weak — the lagged basis instrument Z^HF is likely correlated with current market conditions.

**Feasibility verdict: PARTIALLY TESTABLE** — heterogeneity in price sensitivities (β_{FB} vs. β_{HF}) is testable under the demand system assumptions. The specific claim that HF withdraw in "extreme stress" requires a crisis subsample analysis that is mentioned in v8 §7.2 but not formally specified in the prediction table.

---

## C. Data Coverage Matrix

| Object | FX Swap data | MMF data (N-MFP) | CDS data | EPFR data | Primary Dealer data | BIS LBS |
|--------|-------------|------------------|----------|-----------|--------------------|---------| 
| U_t | ✓ (Q_{FB,m,t} = SignedUSDFlow aggregated over FB sector) | ~ (MMF exposure constructs the IV for U_t shocks, not U_t itself) | ✗ | ~ (EPFR shifter for NBFI demand component) | ✗ | ~ (aggregate cross-border flows as validation) |
| B_t | ~ (dealer residual Q_D = −Σ other sectors; taker/maker as proxy for capacity utilization) | ✗ | ✗ | ✗ | ✓ (DealerCapacity_t from repo + H.8 Borrowings) | ~ (bank balance sheet capacity proxy) |
| q_t | ~ (taker ratio; price dispersion Spread_{s,m,t}) | ✗ | ✗ | ✗ | ✗ | ✗ |
| μ_t | ✓ (PriceUSD_{m,t} = −TIB_{m,t}; PricePaid_{s,m,t} sector-specific) | ✗ | ~ (CDSAgg_{m,t} as control/confounder for credit component of basis) | ✗ | ✗ | ~ (BIS publishes CIP deviations, validation use) |

**Legend:** ✓ = directly available, ~ = partial coverage or indirect, ✗ = not available

---

## D. Critical Gaps

### Gap 1: B_t is partially unobserved and the θ_t ratio is not directly constructable

**What the theory requires:** B_t = B_t^FBO + B_t^USbank + B_t^dealer + B_t^HF + B_t^CBswap (theory §7.1). Market tightness θ_t = U_t/B_t drives all amplification in the model (§11). Propositions 2, 3, and 5 are all statements about B_t or θ_t.

**What the data provide:** DealerCapacity_t from Primary Dealer repo and H.8 captures the US dealer/bank component but misses FBO branches (B_t^FBO) and hedge funds (B_t^HF). The v8 does not construct θ_t as a ratio; it uses DealerConstraint as a binary conditioning variable.

**Threat level:** This is a threat to the MAIN identification for Proposition 2 (capacity stabilization) and Proposition 3 (non-linearity). The core comparative statics ∂μ_t/∂B_t < 0 and the threshold effect in θ_t are not cleanly testable. However, this does not threaten the primary β > 0 result (Proposition 1 / P2), which only requires U_t and μ_t, both of which are well-proxied. **Assessment: Main identification partially threatened; robustness concern for amplification channel.**

---

### Gap 2: q_t (synthetic dollar quality) has no direct empirical proxy

**What the theory requires:** q_t ∈ (0,1] is the quality-adjusted value of synthetic dollars in the CES aggregator (theory §4, equation 1). It is endogenous via q_t = q(p_t) (equation 4). Changes in q_t are the core mechanism connecting market tightness to the preference shift α_t ↑ in stress (§11).

**What the data provide:** Three indirect proxies (taker ratio, TIB, price dispersion) are proposed in v8 §2.5, but each has problems:
- TIB proxies μ_t (the price), not q_t (the quality). Using TIB for both creates a conceptual overlap.
- The taker ratio proxies p_t (matching probability), from which q_t = q(p_t) is inferred — this is two steps removed.
- Price dispersion (Spread_{s,m,t}) is the most distinctive proxy for q_t: a high dispersion suggests that different agents face different qualities of synthetic dollar access.

**Threat level:** q_t is a latent theoretical variable — it is common in structural models to have latent objects without direct proxies. The empirical strategy does not require measuring q_t directly; it tests the implications of q_t's variation through μ_t and sector behavior. **Assessment: Robustness concern only; the main empirical approach does not depend on measuring q_t.**

---

### Gap 3: The cross-sectoral exclusion restrictions for the demand system are not validated

**What the theory requires:** The demand system (theory §9, v8 §6) requires that Z^MMF only shifts the FB sector's demand and Z^EPFR only shifts the NBFI sector's demand. The theory formalizes this as sector-specific cost shifters (equation 9.2 of theory: q_{s,m,t} = α_{s,m} + β_s · PriceUSD + γ_s X_{s,m,t} + ε).

**What the data provide:** MMF data (N-MFP) and EPFR data are both in the "À obtenir" list in v8 §12, meaning they are not yet in hand. Even when obtained, the exclusion assumption (Z^MMF ⊥ NBFI demand conditional on controls) requires that prime MMF funding shocks do not affect hedge fund or asset manager behavior in FX markets — this is not obviously true if HFs and AMs also hold bank paper or if they respond to the same global stress events.

**Threat level:** This threatens the validity of the demand system estimates (Part 5 of the paper / Propositions 3 and 6). The IV simple approach (Part 3) only requires Z^MMF to shift Q_{FB}, a weaker condition. **Assessment: Main identification for the IV simple is not threatened; the demand system extension is the primary casualty if exclusion fails.**

---

## E. Recommended Extensions

### For Gap 1 (B_t partially unobserved):

**Option (a) — Reinterpretation:** Reframe θ_t not as a directly constructed ratio but as a state-dependent latent variable identified by crisis indicators (quarter-end dummies, VIX percentiles, Primary Dealer constraint index). The theory's amplification predictions then become testable as effect heterogeneity across pre-defined stress regimes. This is essentially what v8 §5.3 already does for P6 and P7 — formalize this reinterpretation explicitly.

**Option (b) — Additional data:** FR Y-9C or FR 2886b regulatory filings for FBO branch balance sheets (available through the Fed, restricted access). These would allow direct construction of B_t^FBO. Timeline: restricted data application, 6–12 months. The BIS LBS (listed in v8 §12 as available) provides cross-border bank claims by nationality — this can proxy B_t^FBO at the country level as an available-now alternative.

### For Gap 2 (q_t unobserved):

**Option (a) — Reinterpretation:** Adopt price dispersion Spread_{s,m,t} = PricePaid_{s,m,t} − PricePaid_{interdealer,m,t} as the canonical proxy for q_t variation. The theory predicts that when q_t falls, heterogeneous agents face different conversion costs — this manifests in cross-sectoral price dispersion. This proxy is directly constructable from the stated FX data (v8 §10.1 already plans this analysis). The connection to the theory should be made explicit: Spread_{s,m,t} ↑ ⟺ q_t ↓ in sector s.

**Option (b) — Additional data:** Not needed; the price dispersion measure is already available within the FX transaction dataset. The v8 plans this as an "extension" (§10.1) but given it is the best observable proxy for q_t, it should be elevated to a primary diagnostic.

### For Gap 3 (exclusion restrictions for demand system):

**Option (a) — Reinterpretation:** Present the demand system estimates explicitly as "structural under maintained exclusion assumptions" (as v8 §6 already labels it "Extension structurelle (plus hypothétique)"). The Appendix should include a formal test of the exclusion: regress Z^MMF on lagged NBFI flows and show the first-stage residuals are orthogonal to NBFI quantities.

**Option (b) — Additional data:** Hedge fund FX positions from CFTC Commitments of Traders (COT) data could provide a direct time-series for B_t^HF and validate whether HF activity is orthogonal to MMF shocks. The COT is publicly available at weekly frequency for currency futures (a less clean proxy for OTC FX swaps but directionally useful). This is not listed in v8 §12, making it a genuine new data suggestion for this gap.

---

## Summary Scorecard

| Object | Grade | Primary risk |
|--------|-------|-------------|
| U_t (conversion demand) | B | FB-only proxy misses corporate/NBFI demand |
| B_t (intermediary capacity) | C | FBO and HF components unobserved |
| q_t (synthetic dollar quality) | C | No direct proxy; TIB conflates price with quality |
| p_t (matching probability) | B | Taker ratio is valid but approximate |
| θ_t = U_t/B_t (market tightness) | C | Not directly constructed; B_t measurement limits this |
| μ_t (funding spread / PriceUSD) | A | Direct transaction-based measure; clean mapping |

**Overall assessment:** The empirical design is well-grounded for the primary causal question (P2: demand shock → price impact) and for the descriptive analysis of market structure (P4, intermediation matrix). The theoretical amplification mechanism (Propositions 2 and 3, centered on B_t and θ_t) is supported by the evidence design only partially. The demand system extension (Propositions 3 and 6) carries identification assumptions that are maintained rather than tested. The paper's credibility hierarchy — IV simple (strongest) → who absorbs? (semi-causal) → demand system (structural/hypothetical) — as stated in v8 §1.4 — correctly reflects the actual empirical feasibility of each component.
