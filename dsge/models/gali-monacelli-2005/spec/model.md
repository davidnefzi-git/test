# The small open economy

Galí and Monacelli (2005). Assembled from `core-soe-gm` + `calvo-prices-domestic` + one
of four mutually exclusive policy components.

The derivations are in
[`docs/theory/open-economy.md`](../../../docs/theory/open-economy.md), which treats
relative prices, the two inflation rates, the real exchange rate, risk sharing and the
openness composites. This document describes the model and the regime comparison.

---

## 1. Environment

**A continuum of small open economies.** Each is of measure zero in the world, so world
output, world prices and the world interest rate are exogenous to it and its own
variables do not enter world aggregates. World output is an AR(1) process, not an
equilibrium object; world inflation is zero, as the article sets it.

**Consumption.** A bundle of domestic and imported goods with import share $\alpha$ — the
degree of openness — and elasticity $\eta$ between them; imports are themselves a bundle
across countries with elasticity $\gamma$.

**Three substitution elasticities that are not interchangeable.** $\sigma$ governs
substitution over time, $\eta$ between domestic and foreign goods, $\gamma$ among foreign
goods. **At the article's baseline all three equal one**, and in that case several
composites collapse: $\Theta = 0$ exactly, so natural output does not respond to world
output at all, and $\sigma_\alpha = \sigma$. Every coefficient multiplying $\Theta$ is
then unidentified by any check performed there. This entry's second calibration —
$\eta = 2$, $\gamma = 1.5$, $\alpha = 0.3$, $\sigma = 2$ — exists for that reason, and
the foreign-shock targets sit there. A mutation test had found every foreign term in this
core unverified before it was added.

**Law of one price.** Each good sells for the same price everywhere once converted at the
nominal exchange rate: pass-through is complete and immediate.

**Complete international asset markets.** The strongest assumption in the model, and the
one §4 is about.

**Price setting.** Domestic firms set prices for domestic goods à la Calvo; import prices
follow the law of one price. Domestic inflation and CPI inflation are therefore distinct.

## 2. The agents' problems

| agent | chooses | yields |
|---|---|---|
| household | consumption of the two bundles, labour, domestic bonds and state-contingent foreign claims | Euler equation; labour supply; the risk-sharing condition |
| domestic firm | the reset price of its variety | reset price as a markup over expected marginal costs |
| central bank | the nominal rate, or the exchange rate | one of four rules |
| rest of the world | — | exogenous |

## 3. Equilibrium and the complete system

Sixteen equations in sixteen variables, under the domestic-inflation rule.

| | equation | what it is |
|---|---|---|
| 1 | $x_t = \mathbb{E}_tx_{t+1} - \frac{1}{\sigma_\alpha}(i_t - \mathbb{E}_t\pi_{H,t+1} - rn_t)$ | IS curve, with **$\sigma_\alpha$ in place of $\sigma$** |
| 2 | $rn_t = -\sigma_\alpha\Gamma(1-\rho_a)a_t + \alpha\sigma_\alpha(\Theta+\Psi)\mathbb{E}_t\Delta y^{*}_{t+1}$ | natural rate |
| 3 | $y^n_t = \Gamma a_t + \alpha\Psi y^{*}_t$ | natural output |
| 4 | $x_t = y_t - y^n_t$ | the output gap |
| 5 | $y_t = y^{*}_t + \frac{1}{\sigma_\alpha}s_t$ | **risk sharing**, under complete markets |
| 6 | $\pi_t = \pi_{H,t} + \alpha\Delta s_t$ | CPI against domestic inflation |
| 7 | $\Delta s_t = \Delta e_t - \pi_{H,t}$ | terms of trade, with world inflation at zero |
| 8 | $q_t = (1-\alpha)s_t$ | real exchange rate |
| 9 | $y_t = a_t + n_t$ | employment |
| 10 | $nx_t = \alpha(\frac{\omega}{\sigma}-1)s_t$ | net exports |
| 11 | $y_t = c_t + \alpha\frac{\omega}{\sigma}s_t$ | consumption and output |
| 12 | $w_t = \sigma c_t + \varphi n_t$ | labour supply |
| 13 | $\pi_{H,t} = \beta\mathbb{E}_t\pi_{H,t+1} + \kappa_\alpha x_t$ | domestic Phillips curve |
| 14 | $i_t = \phi_\pi \pi_{H,t}$ | the policy rule, one of four |
| 15–16 | $a_t$, $y^{*}_t$ AR(1) | the two processes |

**Equations 6, 7 and 8 are the block's identity backbone** and they are easy to get
subtly wrong. Three cautions.

Equation 6 is why a rule in $\pi_t$ and a rule in $\pi_{H,t}$ are *different rules*: CPI
and domestic inflation differ by the change in the terms of trade. Conflating them is the
open-economy counterpart of conflating output with the output gap.

Equation 7 assumes world inflation is zero. It is a simplification of the environment, not
an identity, and a model with non-zero world inflation must restore the world inflation
term. `core-soe-gm` declares the assumption.

Equation 8 holds only under the law of one price **and** symmetric preferences across
countries. Both are declared in `core-soe-gm.assumptions`, with what replacing them would
require.

**Sign conventions.** Both $e_t$ and $q_t$ are defined so that a rise is a
**depreciation**. The opposite convention is at least as common, and a sign inversion here
is invisible to any test that does not look at the direction of a response.
`taxonomy/variables.yaml` records the convention for both.

**The sign on the natural rate.** Equation 2's technology term is negative: a persistent
rise in productivity *lowers* the natural rate. The closed-economy counterpart of that
sign was wrong in an early version of this library and no test caught it, because every
target then used a monetary shock, under which technology is identically zero.

## 4. International risk sharing, and what replacing it would require

Equation 5 is the model's central assumption. With complete markets and the law of one
price, marginal utilities are equalised across countries state by state, so domestic
output is tied to world output and the terms of trade. Net foreign assets and the current
account are **degenerate**: this entry reports neither, and its family declares both.

Replacing complete markets is not a syntactic substitution. Four things change together:
the risk-sharing equation gives way to a current-account identity plus a debt-elastic
premium or a portfolio condition; net foreign assets become a state variable; the
consumption-output relation acquires a wealth term; and a stationarity device is needed,
since the model otherwise has a unit root in net foreign assets.

`core-soe-gm` keeps risk sharing as an equation of its own rather than folding it into the
IS curve, precisely so that it is visible, nameable and replaceable; and its
`assumptions` field states the four consequences rather than implying that an
incomplete-markets block could simply be mounted in place. The library documents the
adaptation without performing it.

## 5. Steady state

Symmetric, with zero inflation and balanced trade. The model is written directly in log
deviations about that point.

## 6. The four regimes, and the property that distinguishes this family

| component | rule | pins the price level? |
|---|---|---|
| `rule-domestic-inflation` | $i_t = \phi_\pi\pi_{H,t}$ | no |
| `rule-cpi-inflation` | $i_t = \phi_\pi\pi_t$ | no |
| `rule-exchange-rate-peg` | $e_t = 0$ | **yes** |
| `rule-optimal-domestic-price-stability` | $\pi_{H,t} = 0$ | no |

Each provides the same variable, so composing two is refused rather than silently
over-determining the model.

**A unit root under three of the four.** A rule in an inflation *rate* pins the rate and
not the price *level*, so the price level wanders, and with it the nominal exchange rate
and the level of the terms of trade. The peg pins the price level and removes the root.

This breaks an assumption every closed-economy entry in the library satisfies. Anything
computing unconditional moments from this family must detrend first; the arithmetic is
right either way and only the economics says which to expect. The library has no moments
tier in part because the detrending convention it would need has not been settled, and
that convention belongs in `taxonomy/families.yaml` beside the family's common variables.

**The article's headline result** — the ranking of regimes by welfare — is **out of
reach**. It requires a second-order treatment. This entry reproduces the dynamics and the
ordering of output-gap responses across regimes, which its tests check; it does not
reproduce the welfare ranking and does not claim to.

## 7. The library's representation, and what it simplifies

| | |
|---|---|
| four regimes as swappable components | the article's comparison becomes a matter of exchanging one block; the alternative — four entries differing in one equation — would maintain the other fifteen four times over |
| complete markets isolated, not extracted | risk sharing is its own equation in the core, documented as a maintained assumption with its substitution consequences, rather than a separate component. Extracting it would leave the core not closed on its own and would change every existing composition, for a documentation gain that the `assumptions` field already delivers |
| world inflation zero | §3, equation 7 |
| cross-checked against an independent implementation | twelve variables, four periods, both shocks, all four regimes and both calibrations, worst residual 2.0e-15. That check fixes the scale of each shock at one, so it verifies the equations' structure **and** their normalisation; see `docs/composition/README.md` §2.2c for the case where it would not |
| no net foreign assets, no current account | degenerate under complete markets; §4 |
