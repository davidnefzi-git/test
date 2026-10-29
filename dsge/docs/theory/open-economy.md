# The small open economy

The derivations behind `core-soe-gm`, `calvo-prices-domestic` and the four policy
components of the Galí–Monacelli family.

**What is established here.** The relations are Galí and Monacelli's (2005); the
equation numbers are those recorded in the component files, read from the article and
cross-read against a third party's annotations, which agree. Sections 2 to 5 reproduce
the chain from primitives to the library's equations, because several of those equations
are *results* of a chain rather than primitives, and a reader who takes them as
primitives will transplant them wrongly. Section 7 treats the four monetary regimes and
the property that distinguishes them from every closed-economy entry in the library.

---

## 1. Environment and primitives

**Countries.** A continuum of small open economies on $[0,1]$, each of measure zero.
"Small" has a precise content used throughout: the domestic economy takes world output,
world prices and the world interest rate as given, and its own variables do not enter
world aggregates. World output is therefore an exogenous process, not an equilibrium
object.

**Consumption.** The domestic household consumes a bundle of domestic and imported
goods,

$C_t = \left[(1-\alpha)^{1/\eta} C_{H,t}^{(\eta-1)/\eta} + \alpha^{1/\eta} C_{F,t}^{(\eta-1)/\eta}\right]^{\eta/(\eta-1)},$

with $\alpha$ the share of imports — the **degree of openness** — and $\eta$ the
elasticity of substitution between domestic and foreign goods. Imports are themselves a
bundle across countries with elasticity $\gamma$. The library names the openness
parameter `alpha_open` to keep it apart from the production exponent $\alpha$ used
elsewhere.

**Three substitution elasticities, and why they are not interchangeable.** $\sigma$
governs substitution over *time*, $\eta$ between domestic and foreign goods, $\gamma$
among foreign goods. At the article's baseline all three equal one, and in that case —
and only in that case — several composites below collapse to simple expressions. The
library's second calibration exists for exactly that reason: at the baseline the
openness terms are algebraically invisible, so a coefficient error in them cannot be
detected.

**Law of one price.** Each good sells for the same price everywhere once converted at
the nominal exchange rate. Together with symmetric preferences this is what makes the
real exchange rate a function of the terms of trade alone (§3).

**Complete international asset markets.** Households can trade a full set of
state-contingent claims internationally. This is the strongest assumption in the block
and §4 is about it.

**Price setting.** Domestic firms set prices for domestic goods à la Calvo; import prices
are given by the law of one price. Domestic inflation and CPI inflation are therefore
distinct objects (§2).

---

## 2. Relative prices and the two inflation rates

**The terms of trade** are the price of imports relative to domestically produced goods,

$S_t \equiv \frac{P_{F,t}}{P_{H,t}}, \qquad s_t = p_{F,t} - p_{H,t}.$

**The CPI.** To a first-order approximation around the symmetric steady state,

$p_t = (1-\alpha)\,p_{H,t} + \alpha\,p_{F,t} = p_{H,t} + \alpha\, s_t,$

and differencing,

$\pi_t = \pi_{H,t} + \alpha\,\Delta s_t$

which is the component's `cpi-domestic-link`. **This is the single most consequential distinction in the block.** CPI inflation and domestic inflation differ by the change in the terms of trade, so a policy rule written in $\pi_t$ and one written in $\pi_{H,t}$ are different rules with different equilibria — which is precisely what the article's regime comparison is about. A component that sets domestic prices must write $\pi_{H}$;
conflating the two is the open-economy counterpart of conflating output with the output gap.

**The law of motion of the terms of trade.** With the law of one price,
$p_{F,t} = e_t + p^{f}_t$, so

$s_t = e_t + p^f_{t} - p_{H,t} \quad \Longrightarrow \quad \Delta s_t = \Delta e_t + \pi^f_{t} - \pi_{H,t}.$

The library sets world inflation to zero, as the article does on p. 724, giving `terms-of-trade`: $\Delta s_t = \Delta e_t - \pi_{H,t}$. The assumption is recorded in the component; it is a simplification of the environment, not an identity, and a model with non-zero world inflation must restore $\pi^{f}_t$ here.

**Anchor: `relative-prices`.**

---

## 3. The real exchange rate

$Q_t \equiv \frac{\mathcal{E}_t P^f_t {P_t}, \qquad q_t = e_t + p^f_t - p_t.$

Substituting $p_t = p_{H,t} + \alpha s_t$ and $e_t + p^f_t = p_{H,t} + s_t$,

$q_t = (1-\alpha) s_t$

the component's `real-exchange-rate`. The real exchange rate is not an independent state: under the law of one price and symmetric preferences it is proportional to the terms of trade, and the factor is one minus openness. A closed economy ($\alpha = 0$) would have $q_t = s_t$, which is vacuous; a fully open one ($\alpha = 1$) would have $q_t = 0$, purchasing power parity holding exactly.

**A note on sign conventions.** Both $e_t$ and $q_t$ are defined so that a **rise is a depreciation**. The library records this in `taxonomy/variables.yaml` for both variables, because the opposite convention is at least as common in the literature and a sign inversion here is invisible to any test that does not look at the direction of a response.

**Anchor: `real-exchange-rate`.**

---

## 4. International risk sharing

This is the block's central assumption and the one a reader is most likely to need to replace.

**The condition.** With complete international asset markets and the law of one price, equating marginal utilities of consumption across countries state by state gives

$c_t = c^{f}_t + \frac{1}{\sigma} q_t.$

Domestic consumption moves with world consumption up to the real exchange rate: a real
depreciation makes domestic goods cheap, and the household is compensated through the
asset market.

**The library's form.** Combining that condition with the goods-market clearing relation and the definition of $\sigma_\alpha$ below yields the article's equation (29),

$y_t = y^{f}_t + \frac{1}{\sigma \alpha}\,s_t$

which is what `core-soe-gm.risk-sharing` states. Domestic output is tied to world output and the terms of trade, with no role for net foreign assets, no current-account dynamics and no wealth effects.

**What replacing it would require.** Under incomplete markets the condition becomes an Euler equation for the net foreign asset position, and the following change together: the risk-sharing equation is replaced by a current-account identity plus a debt-elastic premium or a portfolio condition; net foreign assets become a state variable; the consumption-output relation acquires a wealth term; and a stationarity
device is needed, since the model otherwise has a unit root in net foreign assets. That is four coupled changes, not one substitution, and the component says so in its `assumptions` field rather than implying that an incomplete-markets block could simply be mounted in place.

**Why it is a separate equation in the core.** `core-soe-gm` keeps risk sharing as an equation of its own rather than folding it into the IS curve, so that it is visible,
nameable and replaceable. It is a maintained *assumption*, not a friction, and the library marks it as such.

**Anchor: `risk-sharing`.**

---

## 5. Openness in the IS curve, natural output and the natural rate

Four composites carry openness through the model. All are the article's.

$\omega \equiv \sigma\gamma + (1-\alpha)(\sigma\eta - 1), \qquad \sigma_\alpha \equiv \frac{\sigma}{(1-\alpha) + \alpha\,\omega},$

$\Theta \equiv (\sigma\gamma - 1) + (1-\alpha)(\sigma\eta-1), \qquad \Gamma \equiv \frac{1+\varphi}{\sigma_\alpha+\varphi}, \qquad \Psi \equiv, \frac{\Theta \sigma \alpha}{\sigma \alpha+\varphi}.$

**$\sigma_\alpha$ replaces $\sigma$ in the IS curve.** The open-economy IS curve is $x_t = \mathbb{E}_t x_{t+1} - \frac{1}{\sigma \alpha} (i_t - \mathbb{E}_t \pi_{H,t+1} - rn_t)$: the same shape as the closed-economy curve with the intertemporal elasticity rescaled. At $\alpha = 0$, $\sigma \alpha = \sigma$. The rescaling exists because a change in the real rate now moves the terms of trade as well as the consumption path.

**Natural output.** $y^n_t = \Gamma\,a_t + \alpha\,\Psi y^{f}_t$. Openness enters twice: through $\Gamma$, which is the closed-economy elasticity with $\sigma \alpha$ in place of $\sigma$; and through the foreign term, whose coefficient is proportional to $\Theta$.

**$\Theta$ vanishes at the article's baseline.** At $\sigma = \eta = \gamma = 1$, $\Theta = 0$ exactly, so natural output does not respond to world output at all and the foreign terms in the natural rate disappear. Every coefficient multiplying $\Theta$ is then unidentified by any numerical check performed at that calibration. The library's second calibration — $\eta = 2$, $\gamma = 1.5$, $\alpha = 0.3$, $\sigma = 2$ — exists to
make $\Theta \neq 0$ and $\sigma_\alpha \neq \sigma$, and the entry's foreign-shock targets sit there. The second calibration is therefore needed to identify the foreign-output terms in analytical or numerical checks.

**The natural rate.** $rn_t = -\sigma_\alpha\Gamma(1-\rho_a)a_t + \alpha\sigma_\alpha(\Theta+\Psi)\,\mathbb{E}_t\Delta y^{*}_{t+1}$ in the article's notation; the component's equation is the same relation rearranged to a residual. Note the sign on the technology term: a persistent rise in productivity **lowers** the natural rate. This sign follows from the expected reversal of a stationary productivity disturbance, and it is already present in Galí and Monacelli (2005), eq. (37).

**Anchor: `openness-composites`.**

---

## 6. The domestic Phillips curve

Domestic-goods inflation follows a Calvo curve in domestic marginal cost,

$\pi_{H,t} = \beta\,\mathbb{E}_t \pi_{H,t+1} + \kappa_\alpha\, x_t, \qquad \kappa_\alpha = \lambda\,(\sigma_\alpha + \varphi),$

with $\lambda$ as in `price-setting.md` §3. The slope involves $\sigma_\alpha$, so **openness flattens or steepens the Phillips curve** depending on the substitution elasticities: the same nominal rigidity has different real consequences in an open economy. This is why `calvo-prices-domestic` is a distinct component from `calvo-prices` rather than the same block with a different calibration.

**Anchor: `domestic-phillips-curve`.**

---

## 7. The four monetary regimes

The article compares four closures of the nominal side, and the library makes each a component so that the comparison is a matter of swapping one block:

| component | rule | pins |
|---|---|---|
| `rule-domestic-inflation` | $i_t = \phi_\pi\,\pi_{H,t}$ | domestic inflation |
| `rule-cpi-inflation` | $i_t = \phi_\pi\,\pi_t$ | CPI inflation |
| `rule-exchange-rate-peg` | $e_t = 0$ | the nominal exchange rate |
| `rule-optimal-domestic-price-stability` | $\pi_{H,t} = 0$ | domestic prices exactly |

They are mutually exclusive: each provides the same variable, so composing two is
refused by the assembler rather than silently over-determining the model.

**The property that distinguishes this family.** Under either inflation rule, and under
the optimal rule, the solution carries a **unit root**. A rule in an inflation *rate*
pins the rate and not the price *level*, so the price level wanders, and with it the
nominal exchange rate and the level of the terms of trade. The exchange-rate peg pins the
price level and removes the root.

This matters beyond bookkeeping. Every closed-economy entry in the library is stationary,
and anything computing unconditional moments from this family must detrend first. The
arithmetic is right either way; only the economics says which to expect. The entry records
the property, and the library has no moments tier precisely because the detrending
convention it would need has not been settled.

**Anchor: `monetary-regimes`.**

---

## 8. What a transplant requires

| If the new environment changes | then |
|---|---|
| complete to incomplete markets | §4: four coupled changes, listed there |
| the law of one price (local-currency pricing, incomplete pass-through) | §2 and §3 both fail: import prices are no longer $e_t + p^{*}_t$, the CPI link changes, and the real exchange rate stops being proportional to the terms of trade |
| the small-economy assumption (two large economies) | world output becomes endogenous; §1's exogenous process and the whole risk-sharing form change |
| preferences away from symmetry across countries | §3's proportionality fails even under the law of one price |
| world inflation away from zero | §2's terms-of-trade law of motion must restore $\pi^{*}_t$ |
| the substitution elasticities away from unity | nothing fails, but every composite in §5 becomes operative; this is the case the library's second calibration covers |
| a non-traded sector, or distribution costs | the two-good structure of §1 is insufficient and the price indices must be rebuilt |

---

## References

- Galí, J. and T. Monacelli (2005). Monetary policy and exchange rate volatility in a
  small open economy. *Review of Economic Studies* 72(3), 707–734.
- Galí, J. (2015). *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed.,
  chapter 8.
