# Strategy Memo Review — Round 2
**Date:** 2026-05-19
**Reviewer:** strategist-critic
**Paper:** Net Foreign Assets, Demographics, and the Structural Determinants of External Imbalances: A Two-Country OLG Approach
**Memo under review:** `paper/design/strategy_memo_olg_v2.md`
**Round 1 report:** `quality_reports/strategist_critic_report_olg.md` (37/100, Reject)
**Severity:** Strategy phase — Medium (constructive). Threshold for approval: 80/100.

---

## Phase 1: Claim Assessment

### Paper type and estimands
v2 preserves the Type III ("theory-disciplined empirics") classification and explicitly re-states all seven structural predictions in §2: $\gamma_1>0$ (income), $\gamma_2<0$ (current $\phi$), $\gamma_3>0$ (anticipated $\phi$), $\gamma_4>0$ (retirement duration), $\gamma_{TFP}$ ambiguous, $\gamma_D<0$, and the GE channel via $r^\ast_t$. Cross-checking against `paper/sections/theoretical_model.tex` §`theory:summary`, Eq. `eq:structural-reg`, and Table `tab:signs`:

| Theory prediction | Estimable counterpart in v2 | Mapped where? |
|---|---|---|
| $\gamma_y>0$ | $\gamma_1$ on $y_{it}$ | §2, §6.1 Spec A/B/C |
| $\gamma_\phi<0$ | $\gamma_2$ on $\phi_{it}$ | §2, §6.1 |
| $\gamma_{\phi^e}>0$ | $\gamma_3$ on $\mathbb{E}_t[\phi_{i,t+H}]$ | §2, §6.1 |
| $\gamma_{\omega^e}>0$ | $\gamma_4$ on $\mathbb{E}_t[e_{65,i,t+H}]$ | §2, §6.1 |
| $\gamma_{TFP}$ ambiguous | $\gamma_{TFP}$ on $\tilde a_{it}$, decomposed | §2, §9.5 (Wu–Hausman), §9.7, §11.3 (frontier extension) |
| $\gamma_D\in(-(r^\ast-g^Y)^{-1},0)$ | $\gamma_D$ on $d^g_{it}$ | §2, §6.1 |
| $r^\ast$ absorbed by $\lambda_t$ | Spec A: time FEs; Spec B: CCE cross-sectional averages | §6.1 |

One small notational mismatch — the theory uses $\omega_{i+H}$ for retirement duration whereas v2 uses $e_{65,i,t+H}$. Not a deduction (the memo treats $e_{65}$ as an operationalization of $\omega$ and the explorer report supports this), but the author should flag this aliasing in the empirical section to forestall referee confusion. **Phase 1: PASS.**

---

## Phase 2: Core Design Validity (verify each R1 fix)

| R1 Issue | Severity (R1) | Was it fixed? | Notes |
|---|---|---|---|
| I(2) demographics not pre-tested | CRITICAL (−25) | **YES** | §4.2 adds IPS-at-first-difference (Pesaran–Shin 1995 / IPS 2003), Hadri (2000) stationarity, and Lyhagen (2000) panel I(2). Decision rule documented (pre-difference, or Johansen I(2) / Lyhagen extension). Upstream of DOLS/FMOLS. Adequate. |
| $r^\ast\times\phi$ interaction measurement error | CRITICAL (−20) | **YES (with caveat)** | §6.2 derives the non-attenuating bias (Bound–Brown–Mathiowetz 2001), demotes Spec C to diagnostic, and proposes IV with lagged global demographic/TFP averages. The IV proposal is partly credible but the exclusion restriction is asserted, not argued — see Phase 3 New Issue N1 (residual concern, not full deduction). |
| Vintage WPP look-ahead | CRITICAL (−15) | **YES (per user CL-1)** | §8 formalizes the rule; §8.3 provides an operational vintage map 1994–2023. Per orchestrator instructions, this is RESOLVED by user clarification and not re-deductible. |
| Structural break tests absent | MAJOR (−10) | **YES** | §4.6 adds Bai–Perron (1998, 2003) with pre-specified candidates 1999/2008/2014/2020, Hansen (2001) cointegration breakdown, recursive CCE-MG plots, and sub-period splits (1994–2007, 2008–2023). Pre-specification forestalls selective reporting. See Phase 3 New Issue N2 on heterogeneous breaks (residual concern). |
| Pension type not controlled | MAJOR (−10) | **YES** | §9.1 implements OECD Pensions at a Glance, PAYG dummy (threshold 70%), interaction with $\phi_{it}$ and $\mathbb{E}_t[\phi_{i,t+H}]$, and a funded-only sub-sample (Australia, Chile, Denmark, Netherlands, Switzerland). Five-country funded sub-sample is on the thin side for CCE-MG (see N3). |
| Bilateral gravity FEs absorb variation | MAJOR (−10) | **YES** (DROPPED) | §11.2 cleanly explains the FE incompatibility (origin-time × destination-time absorbs all OLG structural variation) and records the extension as future work. Per CL-2, this is RESOLVED. §11.3 substitutes a tractable TFP frontier-distance extension that preserves identification. |
| Capital account openness | MAJOR (−5) | **YES** | §9.2 adopts Chinn–Ito KAOPEN (2008), with a pre-specified 25th-percentile sample restriction and a continuous interaction. Tied to §7.2 (slow $\hat\alpha_i$ interpreted via KAOPEN). Adequate. |
| Expectations formation | MAJOR (−5) | **YES** | §9.3 specifies adaptive (five-year MA) and AR(1) alternatives with a side-by-side robustness table for $\hat\gamma_3$. Adequate. |
| DOLS citation error | MAJOR (−3) | **YES** | §5.1 and §15: panel DOLS now correctly attributed to Kao–Chiang (2000) *Advances in Econometrics* 15 and Mark–Sul (2003) *Oxford Bulletin* 65. Stock–Watson (1993) cited as theoretical foundation only. AMG attributions cleaned (Eberhardt–Bond 2009 MPRA; Bond–Eberhardt 2013 OBES). Pesaran 2004 + 2021 both cited. |
| Estimator assumption gaps (DOLS lag, FMOLS bandwidth, CCE-MG N≫r) | MAJOR (−5 representative) | **YES** | §5.2 table states: DOLS lags by BIC over $\{1,\ldots,\lfloor T^{1/3}\rfloor\}$ with AIC sensitivity (Choi–Kurozumi 2012); FMOLS Bartlett kernel with Andrews 1991 bandwidth, Newey–West 1994 sensitivity; CCE-MG N≫r with Chudik–Pesaran 2015 Monte Carlo rule; CupFM factors by Bai–Ng (2002) $IC_{p2}$ with $r\pm 1$; PMG ARDL lags by BIC; CS-ARDL truncation $\lfloor T^{1/3}\rfloor$. Comprehensive. |
| TFP Wu–Hausman | MAJOR (−5) | **YES (partial)** | §9.5 specifies three first-stage instruments (PWT `csh_i` IT capital share, USPTO patent citations à la Acemoglu et al. 2018, trade-weighted partner TFP) and reports 2SLS-DOLS (Choi–Kurozumi 2012) alongside baseline. Instruments are plausible but their exclusion restrictions are not separately argued (residual gap — see N4). |
| CD test on dependent variable (Minor #11) | Minor | **YES** | Checklist item #2 (§13). |
| CCE-MG finite-sample with N≈45, r=3–4 (Minor #13) | Minor | **YES** | §5.2 acknowledgement + bootstrap CIs as robustness. |
| Currency composition of NIIP | MAJOR (−5) | **YES** | §9.4: PPP-NIIP robustness alongside LMF baseline. |

**Verdict on Phase 2:** Every R1 deduction is addressed in a non-cosmetic way. The I(2) and structural-break additions are particularly well-executed: they are placed upstream of estimation, with decision rules, not relegated to a footnote. Citations are now precise. Estimator assumptions are now operational.

---

## Phase 3: Assumptions and Gaps (new issues introduced or residual)

### N1 (residual, Spec-C IV exclusion). Lagged global demographic and TFP averages as instruments for $r^\ast$
The proposed instruments — global UN demographic averages and global TFP, lagged — are correlated with rest-of-world fundamentals that themselves enter the structural cointegrating relation through cross-sectional averages in Spec B (CCE-MG). The memo argues predeterminedness (the lag fixes timing of measurement noise $\eta_t$), but exclusion is asserted, not argued: if global TFP at $t-1$ affects country $i$'s long-run NIIP through channels other than $r^\ast_t$ (e.g., trade-partner income spillovers feeding into $y_{it}$ in the next period), the IV identification fails. Since Spec C is now diagnostic only and the primary results rest on Specs A and B, the practical consequence is bounded. **Deduction: −3 (minor, IV exclusion argument incomplete in a diagnostic specification).**

### N2 (residual, structural break test). Heterogeneous break dates across countries
The memo applies Bai–Perron to "the time series of cointegrating residual averages" (§4.6) — which presumes a common break date across countries. In an N≈45 panel spanning 1994–2023, breaks are plausibly heterogeneous (e.g., EMU 1999 binds only for the EA-12; the 2014 commodity shock hits Russia, Saudi Arabia, Brazil differently). The right framework here is a panel break test allowing country-specific dates (e.g., Bai 2010, Baltagi–Feng–Kao 2016, or country-by-country Bai–Perron with multiple-testing correction) or, at minimum, country-by-country recursive CCE-MG. The recursive plots are mentioned (item #19 in §13) and the sub-period splits provide a fallback, so the threat is partly mitigated. **Deduction: −3 (minor, common-break formulation insufficient for heterogeneous panels).**

### N3 (residual, funded sub-sample power). N=5 for the funded-pension robustness
§9.1's funded-dominant sub-sample (Australia, Chile, Denmark, Netherlands, Switzerland) is N=5. With T=30 and r≈3–4 latent factors, CCE-MG/AMG inference on this sub-sample is essentially infeasible — N≪r. The PAYG-dummy interaction in the full sample is the more credible test; the funded-only re-estimation should be flagged as illustrative rather than a formal robustness check. **Deduction: −2 (minor — sub-sample described as robustness when it cannot bear that load).**

### N4 (residual, TFP IV exclusion). Trade-weighted partner TFP and patent-citation instruments
Trade-weighted partner TFP is plausibly correlated with country $i$'s NIIP through trade-balance channels independent of own-country TFP (a clear exclusion violation in a NIIP regression). USPTO patent citations from frontier countries are stronger but lean heavily on Acemoglu et al. (2018)'s identifying assumptions. The IT capital share (PWT `csh_i`) is the cleanest but is itself an outcome of investment decisions. As with N1, the exclusion restrictions are asserted; a serious referee will ask. **Deduction: −2 (minor, IV exclusion arguments not separately developed).**

### N5 (residual, ordering of pre-tests in §13). CSD before slope homogeneity before unit roots
The current §13 checklist runs (1) CD on regressors → (3) IPS/Fisher-ADF → (4) CIPS → (5) IPS at first difference → (7) Pesaran–Yamagata. The Pesaran–Yamagata $\tilde\Delta$ test maintains CS independence; under strong CSD, its size is distorted, so CSD should be tested *first*, and slope homogeneity tested using the CSD-robust variant or after CCE-style filtering. The current ordering does run CD before $\tilde\Delta$, which is correct — but the memo does not explicitly say "if CD rejects, use the CSD-robust $\tilde\Delta_{HAC}$ variant (Blomquist & Westerlund 2013) or apply $\tilde\Delta$ on CCE-defactored residuals." A small but real gap. **Deduction: −2 (minor, $\tilde\Delta$ size under CSD not discussed).**

### N6 (residual, Lucas critique on pension regime changes)
§4.6's structural break list (EMU 1999, GFC 2008, commodity 2014, COVID 2020) misses an OLG-specific risk: **pension-policy reforms** during the sample (Sweden 1999; Germany 2007 Riester/raising retirement age; France 2010, 2023; Italy Fornero 2011; multiple EM reforms). These reforms change the very mapping from demographics to private saving that the OLG model leverages — a Lucas-critique-style failure that no break test on the cointegrating residual will detect if the breaks are gradual or non-coincident with the candidate dates. The PAYG dummy in §9.1 partially addresses this, but does not exploit reform-event variation. **Deduction: −3 (minor, important OLG-relevant regime-change channel not addressed).**

### N7 (residual, sample design and explorer constraint). Pre-2000 vintages
The explorer report (Gap 2) is explicit that pre-2000 WPP vintages are PDF-only and would require manual extraction. v2 §3.2 sets the baseline at 1994–2023, but the vintage map in §8.3 includes WPP 1994, 1996, 1998 — which the explorer flagged as the labor-intensive portion. §8.3 mitigates by deferring to Wittgenstein Centre reconstructions cross-checked against PDF extractions and noting that "the pre-2000 panel is a robustness extension, not the baseline" — but then the baseline panel 1994–2023 contains six pre-2000 observation years that use these problematic vintages. There is an internal tension: either the baseline is 2000–2023 (clean vintages, T=24) or the baseline is 1994–2023 with the documented pre-2000 imputation rule applied. The memo straddles. **Deduction: −2 (minor internal inconsistency between §3.2 baseline period and §8.3 pre-2000 caveat).**

### N8 (positive — no new fatal issue introduced)
No new threat to identification was introduced by the revisions. The CCE-MG conditional-linearity statement (§5.3) and the AMG cross-check are well-judged. The valuation decomposition (§10) correctly enters as input — the structural $\gamma$ coefficients in Panel B are interpreted as savings-driven NIIP coefficients, isolating the OLG mechanism from valuation noise.

### Slope homogeneity test ordering and action rule (verification)
§4.4 specifies $\tilde\Delta$ and $\tilde\Delta_{adj}$ are "reported **before** any pooled estimator." Action rule: "lead with CCE-MG / AMG if heterogeneity is rejected; otherwise DOLS/FMOLS is the appropriate benchmark." That is the correct conditional structure and is operationally clear.

### Demoted r* specification
Spec C is clearly demoted to diagnostic in §6.1 and §6.2, with the structural primary estimates resting on Specs A (time FEs) and B (CCE-MG). The decomposition of direct vs. total effects under the demotion is appropriate: Specs A and B identify partial-equilibrium $\gamma$ coefficients; Spec C, when validly estimated (under the IV), provides a sign check on the GE channel. The non-attenuating bias derivation in §6.2 (Eq.) is technically correct.

### Theory–strategy concordance
All seven theory predictions (Eq. `eq:structural-reg`, Table `tab:signs`) have estimable counterparts in v2. The GE channel via $\lambda_t$ in Specs A/B is exactly what the theory's Step (d) requires.

---

## Phase 4: Quality and Linkage

### Citations (full audit)
- Kao–Chiang (2000), Mark–Sul (2003): present in §5.1 and §15. ✓
- Bond–Eberhardt (2013) OBES + Eberhardt–Bond (2009) MPRA: both in §15. ✓
- Pesaran (2004) WP + Pesaran (2021): both cited; the 2021 entry in §15 is vague ("*Empirical Economics* / published version of Pesaran (2004)") — the actual published version is Pesaran (2021) *Journal of Econometrics* 222(1), 87–101. **Citation error (minor).** Deduction: −1.
- Andrews (1991), Newey–West (1994), Choi–Kurozumi (2012): all present. ✓
- Hadri (2000), Lyhagen (2000): present. ✓
- Bai–Perron (1998, 2003), Hansen (2001): present. ✓
- Chinn–Ito (2008): present. ✓
- Bound–Brown–Mathiowetz (2001): present. ✓
- Bai–Ng (2002), Chudik–Pesaran (2015): present. ✓

### Internal consistency
- Threats Table (§12) and Diagnostics Checklist (§13) are now consistent — every threat T1–T15 has a corresponding test or mitigation. T7 (breaks) maps to checklist items #11 and #12. The R1 internal inconsistency (threat without test) is closed.
- The R1 gravity FE inconsistency is closed by dropping the extension.
- Minor residual inconsistency on pre-2000 baseline (N7 above).

### Three Priority Recommendations
§14 is updated to reflect the v2 design (pre-tests upstream; CCE-MG co-primary with linearity caveat; valuation as three-panel baseline). Ordering is correct (pre-test → estimator choice → valuation decomposition).

### Linkage to theory
The strategy now operationalizes every term in the theory's Eq. `eq:structural-reg` (lines 556–559 of `theoretical_model.tex`). The cointegration → ECM bridge (theory `eq:ecm`, v2 §7) is correctly handled. PMG with Hausman vs. MG (v2 §7.2) is the right specification test for long-run pooling.

---

## R1 → R2 Score Comparison

| Issue | R1 deduction | R2 status | R2 deduction |
|---|---|---|---|
| I(2) demographics | −10 | Fixed (§4.2) | 0 |
| Structural breaks (common-date only) | −5 | Fixed but common-break formulation (N2) | −3 |
| Capital controls | −5 | Fixed (§9.2) | 0 |
| Pension type | −5 | Fixed (§9.1), funded sub-sample thin (N3) | −2 |
| Expectations formation | −5 | Fixed (§9.3) | 0 |
| Vintage WPP look-ahead | −5 | RESOLVED by CL-1 | 0 (not deductible) |
| Currency composition | −5 | Fixed (§9.4) | 0 |
| Bilateral FE inconsistency | −5 | RESOLVED by CL-2 (cleanly dropped, §11.2) | 0 (not deductible) |
| $r^\ast \times \phi$ interaction error | −5 | Spec C demoted + IV; IV exclusion thin (N1) | −3 |
| TFP Wu–Hausman | −5 | Fixed (§9.5); IV exclusions thin (N4) | −2 |
| Estimator assumptions | −5 | Fixed (§5.2) | 0 |
| Stock–Watson citation | −3 | Fixed (§5.1, §15) | 0 |
| **NEW: $\tilde\Delta$ size under CSD** | — | not discussed (N5) | −2 |
| **NEW: Pension-reform Lucas critique** | — | unaddressed (N6) | −3 |
| **NEW: Pre-2000 baseline tension** | — | internal inconsistency (N7) | −2 |
| **NEW: Pesaran 2021 journal mis-cited** | — | Phase 4 audit | −1 |

**Net deductions in R2: 18**

**Round 2 score: 100 − 18 = 82 / 100**

---

## Summary

- **Round 2 score: 82 / 100**
- **Verdict: APPROVE** (≥ 80 threshold met)
- **Critical issues remaining: 0**
- **Major issues remaining: 0**
- **Minor issues remaining: 7** (N1–N7 above)

### Reasoning for approval
All three R1 CRITICAL issues are resolved (I(2) tested, r*×φ interaction demoted + IV, vintage WPP formalized per user clarification). All seven R1 MAJOR issues are resolved with non-cosmetic, operational fixes. The estimator-assumption table in §5.2 and the 19-item diagnostics checklist in §13 are now publication-grade. Citations are clean.

The remaining issues are minor — they would each generate referee comments at a top-5 journal, but none invalidates the design, and several (N1, N4) admit straightforward responses in a revision (separate exclusion-restriction arguments per instrument; reformulate as identification-from-functional-form).

### Priority recommendations for the strategist (optional, not blocking)

1. **(N6, highest residual priority)** Add a brief discussion of pension-reform events (Sweden 1999, Germany 2007, France 2010/2023, Italy 2011) as a regime-change channel that the PAYG dummy in §9.1 only partially addresses. Either (a) include reform-event dummies, or (b) explicitly bound this as an unmodeled threat with an interpretive caveat on $\gamma_2, \gamma_3$.
2. **(N2)** Upgrade §4.6 from common-date Bai–Perron to a heterogeneous-break specification — Bai (2010) panel breaks, or country-by-country Bai–Perron with FDR control, or at minimum present the recursive CCE-MG plots country by country.
3. **(N1, N4)** Develop the IV exclusion-restriction arguments separately for each instrument (lagged global demographics, lagged global TFP, IT capital share, patent citations, trade-weighted partner TFP), not as a single block.
4. **(N7)** Resolve the baseline-period tension: either set the baseline to 2000–2023 (clean vintages, T=24) and present 1994–1999 as a robustness extension, or commit to the 1994–1999 inclusion with the explicit imputation rule.
5. **(N5)** Note in §4.4 that under CSD-positive panels (CD test rejects), the Pesaran–Yamagata $\tilde\Delta$ should be applied to CCE-defactored residuals or replaced by the Blomquist–Westerlund (2013) HAC variant.

### Positive findings

1. **The I(2) and structural-break additions (§4.2, §4.6) are exemplary** — placed upstream of estimation with decision rules, not relegated to a footnote. The Lyhagen (2000) extension as a backup to Johansen I(2) is a sophisticated choice.
2. **The §6.2 derivation of the non-attenuating interaction-error bias is technically correct and well-pitched.** Demoting Spec C to diagnostic while preserving its sign-check value is the right call — it preserves what is salvageable without staking primary claims on a biased estimator.
3. **The §5.2 estimator-assumption table is publication-quality.** Each row states the actual selection rule used (BIC vs. AIC, Andrews vs. Newey–West, Bai–Ng $IC_{p2}$ with $r\pm 1$), not vague gestures. This is what methodology-focused referees want.
4. **The CCE-MG linearity caveat in §5.3 is exactly the conditional statement R1 requested.** Pairing it with the AMG robustness (which uses a different functional form for the common dynamic process) is the right defensive design.
5. **The valuation decomposition in §10 is correctly elevated to a three-panel baseline.** Panel B (savings-driven NIIP) is the structural quantity the OLG model speaks to; Panels A and C bracket the valuation noise. Pre-2001 caveat is documented.
6. **The bilateral extension is dropped cleanly** with a precise FE-incompatibility explanation, and an alternative (TFP frontier-distance, §11.3) is offered. This is intellectually honest design pruning.
7. **The 19-item diagnostics checklist in §13** with explicit timing (before estimation / after estimation / diagnostic) gives the empirical team a clear runbook.
8. **The §1.2 user-clarification block** documents CL-1 and CL-2 transparently so that future readers understand the rule-rather-than-litigation status of the vintage decision.

---

**Score: 82 / 100. APPROVED. Strategy memo cleared for execution phase.**
