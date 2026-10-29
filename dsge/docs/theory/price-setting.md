# Price setting

The derivations behind `calvo-prices`, `calvo-prices-domestic`, `calvo-prices-kimball`, `price-indexation` and `rotemberg-prices`.

This document is the single source of truth for the algebra. The component files carry the equations the solver uses and point here; they do not restate the steps.

**Source basis.** The Galí (2015) chapter-3 equations have been checked against the supplied original chapter: eq. (17) is the marginal-cost Phillips curve and eq. (22) its output-gap form. The Smets–Wouters Kimball curvature derivation remains incomplete beyond the outline in §5; verification of Rotemberg's own 1982 paper is pending. First-order equivalence between Calvo and Rotemberg is stated under the given zero-trend-inflation restrictions.

---

## 1. Environment and primitives

A continuum of firms indexed by $i \in [0,1]$, each producing a differentiated good.

**Demand.** Final output is a Dixit–Stiglitz aggregate of the varieties,

$$ Y_t = \left(\int_0^1 Y_t(i)^{1-1/\varepsilon} di\right)^{\varepsilon/(\varepsilon-1)}, \qquad \varepsilon > 1 $$

so that cost minimisation by the final-good producer gives the demand curve and the price index

$$ Y_t(i) = Y_t\left(\frac{P_t(i)}{P_t}\right)^{-\varepsilon}, \qquad P_t = \left(\int_0^1 P_t(i)^{1-\varepsilon} di\right)^{1/(1-\varepsilon)} $$

The constant elasticity $\varepsilon$ is the assumption Section 5 relaxes.

**Technology.** $Y_t(i) = A_t N_t(i)^{1-\alpha}$, with $\alpha \in [0,1)$. Decreasing returns matter for price setting and not only for the production side: a firm that resets its price commits to a quantity path, and under $\alpha > 0$ its marginal cost rises with its own output. This is the whole content of the factor $\Theta$ below.

**Price rigidity.** Each period a firm resets its price with probability $1-\theta$, independently of its history and of how long its price has stood. $\theta \in [0,1)$.

---

## 2. The firm's problem

A firm resetting in period $t$ chooses $P_t^{\ast}$ to maximise the expected discounted value of profits over the random interval during which that price stands:

$$ \max_{P_t^{\ast}} \sum_{k=0}^{\infty} \theta^{k} \mathbb{E}_t \Big\{ Q_{t,t+k}\big[ P_t^{\ast} Y_{t+k|t} - \Psi_{t+k}(Y_{t+k|t}) \big] \Big\} $$

subject to $Y_{t+k|t} = Y_{t+k}(P_t^{\ast}/P_{t+k})^{-\varepsilon}$, where $Q_{t,t+k}$ is the stochastic discount factor and $\Psi_{t+k}(\cdot)$ the nominal cost function.

$\theta^{k}$ appears because the price survives $k$ periods with that probability; the firm discounts by survival as well as by time, which is why the Phillips curve's discount factor is $\beta$ and its slope carries $(1-\beta\theta)$.

**First-order condition.**

$$ \sum_{k=0}^{\infty} \theta^{k} \mathbb{E}_t \Big\{ Q_{t,t+k} Y_{t+k|t} \big[ P_t^{\ast} - \mathcal{M} \Psi'_{t+k}(Y_{t+k|t}) \big] \Big\} = 0, \qquad \mathcal{M} \equiv \frac{\varepsilon}{\varepsilon-1} $$

The reset price is a markup $\mathcal{M}$ over a weighted average of expected future nominal marginal costs, the weights being survival-and-discount weighted revenues. $\mathcal{M}$ is the steady-state gross markup: at $\varepsilon = 9$, the library's default, $\mathcal{M} = 1.125$.

---

## 3. Aggregation and log-linearisation

Write lower case for log deviations from the zero-inflation steady state. Let $p_t^{\ast}$ be the log reset price, $p_t$ the log price index, $\pi_t = p_t - p_{t-1}$, and $mc_t$ the log deviation of **average real** marginal cost.

**Step 1 — the reset price.** Log-linearising the first-order condition about the zero-inflation steady state,

$$ p_t^{\ast} - p_{t-1} = (1-\beta\theta)\sum_{k=0}^{\infty}(\beta\theta)^{k} \mathbb{E}_t\big\{ \widehat{mc}_{t+k|t} + (p_{t+k}-p_{t-1}) \big\} $$

where $\widehat{mc}_{t+k|t}$ is the marginal cost of a firm that last reset at $t$.

**Step 2 — firm-specific against average marginal cost.** Under decreasing returns a firm's own marginal cost depends on its own output, and its output depends on its relative price:

$$ \widehat{mc}_{t+k|t} = mc_{t+k} + \frac{\alpha}{1-\alpha}\big( y_{t+k|t} - y_{t+k} \big) = mc_{t+k} - \frac{\alpha\varepsilon}{1-\alpha}\big(p_t^{\ast}-p_{t+k}\big) $$

**Step 3 — the price index.** $p_t = \theta p_{t-1} + (1-\theta) p_t^{\ast}$, hence $\pi_t = (1-\theta)(p_t^{\ast}-p_{t-1})$.

**Step 4 — eliminating $p_t^{\ast}$.** Combining the three steps and collecting the coefficient on marginal cost,

$$ \boxed{\pi_t = \beta \mathbb{E}_t \pi_{t+1} + \lambda mc_t} \qquad \lambda = \frac{(1-\theta)(1-\beta\theta)}{\theta}\Theta, \qquad \Theta = \frac{1-\alpha}{1-\alpha+\alpha\varepsilon} $$

$\Theta$ is exactly the correction from Step 2: at $\alpha = 0$ it is one and the firm-specific and average marginal costs coincide; as $\alpha$ rises, a reset firm's own marginal cost moves against it, resetting becomes less attractive, and the curve flattens.

This is the equation `calvo-prices.nkpc`, written in marginal cost. It is the library's form because marginal cost is a variable of the core: a Phillips curve written in the output gap has the flexible-wage substitution folded into its slope, and such a component cannot be composed with a wage friction.

**Anchor: `calvo-phillips-curve`.**

### 3.1 The output-gap form, and why the library does not use it

Substituting the flexible-wage condition $mc_t = \big(\sigma + \frac{\varphi+\alpha}{1-\alpha}\big) x_t$ gives the familiar

$$ \pi_t = \beta \mathbb{E}_t\pi_{t+1} + \kappa x_t, \qquad \kappa = \lambda\left(\sigma + \frac{\varphi+\alpha}{1-\alpha}\right) $$

$\kappa$ is retained as a derived parameter of `calvo-prices` because the entry's closed-form targets and the component's nesting rate are stated in terms of it. It enters no equation. The parameter's own description says so.

**Anchor: `output-gap-form`.**

---

## 4. Indexation

Non-reset prices are not frozen but raised by a fraction $\iota_p$ of last period's inflation: a firm that last reset at $t$ charges $P_t^{\ast}\prod_{j=1}^{k}\Pi_{t+j-1}^{\iota_p}$ at $t+k$. Repeating Sections 2 and 3 with that rule, and allowing for trend growth so that the effective discount factor is $\bar\beta\gamma$ rather than $\beta$ (see `consumption-and-capital.md` §5),

$$ \pi_t = \frac{1}{1+\bar\beta\gamma\iota_p} \Big( \bar\beta\gamma \mathbb{E}_t\pi_{t+1} + \iota_p \pi_{t-1} + \kappa_p mc_t \Big) + \varepsilon^{p}_t $$

Indexation adds a lag and so makes inflation itself a state variable. At $\iota_p = 0$ the equation is the unindexed one, term for term — which is why `price-indexation` replaces the Phillips curve of `calvo-prices-kimball` rather than adding an equation, and why its nesting limit is exact rather than approximate.

**Anchor: `indexed-phillips-curve`.**

### 4.1 Why the library writes it multiplied through

The equation above has no limit at $\xi_p \to 0$: the slope $\kappa_p$ diverges, so the flexible-price limit cannot be taken and a nesting test has nothing to converge to. Multiplying by $\kappa_p^{-1}$ and rearranging,

$$ \kappa_p^{-1}\Big[(1+\bar\beta\gamma\iota_p)(\pi_t - \varepsilon^p_t) - \bar\beta\gamma \mathbb{E}_t\pi_{t+1} - \iota_p \pi_{t-1}\Big] - mc_t = 0 $$

which at $\xi_p = 0$ reads $mc_t = 0$: the core's flexible-price closure, equation for equation. Scaling an equation by a non-zero constant cannot change its solution, so the two forms are the same equation; the second has a limit and the first does not.

`tests/test_medium_scale.py` checks the identity symbolically, for all parameter values, rather than relying on solutions agreeing.

**Anchor: `multiplied-through`.**

---

## 5. The Kimball aggregator

Smets and Wouters replace Dixit–Stiglitz by a Kimball (1995) aggregator, defined implicitly by

$$ \int_0^1 G\left(\frac{Y_t(i)}{Y_t}\right) di = 1, \qquad G(1)=1, \quad G'>0, \quad G''<0 $$

Under Dixit–Stiglitz a firm's demand elasticity is the constant $\varepsilon$. Under Kimball it **rises with the firm's relative price**: a firm that has not reset, and whose relative price has drifted, faces a more elastic demand and loses more by not resetting. Reset prices therefore respond less to marginal cost, and the Phillips curve is flatter at a given reset probability.

To first order the effect enters through one additional factor, the curvature $\varepsilon_p \equiv -G''(1)/G'(1)$:

$$ \kappa_p = \frac{(1-\xi_p)(1-\bar\beta\gamma\xi_p)}{\xi_p} \cdot \frac{1}{(\phi_p-1)\varepsilon_p + 1} $$

where $\phi_p$ is the steady-state gross price markup, which in Smets and Wouters equals one plus the share of fixed costs in production.

**What is not derived here.** The step from the implicit aggregator to that factor is reproduced in outline only: the full derivation requires the second-order properties of $G$ at the symmetric point and is given in Smets and Wouters's own appendix and in Kimball (1995). The library uses the slope as the article states it. A reader needing the intermediate step should consult those sources; the library does not claim to establish it.

Note also that $\varepsilon_p$ and $\xi_p$ are not separately identified from aggregate data, which is why the article fixes $\varepsilon_p = 10$ and estimates $\xi_p$. The library records the same choice, and `calvo-prices-kimball` says so in the parameter's source.

**Anchor: `kimball-slope`.**

---

## 6. Rotemberg pricing, and its first-order equivalence with Calvo

Rotemberg (1982) replaces staggering by a convex cost of changing prices. A single representative firm pays $\frac{\phi}{2}\big(\frac{P_t}{P_{t-1}}-1\big)^2 Y_t$ and chooses its price every period. Its first-order condition, log-linearised about the zero-inflation steady state, gives

$$ \pi_t = \beta \mathbb{E}_t\pi_{t+1} + \frac{\varepsilon-1}{\phi} mc_t $$

The two models therefore produce the **same first-order dynamics** whenever

$$ \frac{\varepsilon-1}{\phi} = \frac{(1-\theta)(1-\beta\theta)}{\theta}\Theta \quad\Longleftrightarrow\quad \phi = \frac{\varepsilon-1}{\lambda} $$

This is the sense, and the only sense, in which the library treats them as interchangeable. They are declared `incompatible_with` each other because a model has one price-setting mechanism, not two; and the equivalence does **not** extend beyond first order, since Rotemberg's adjustment cost is a resource cost while Calvo's staggering is a distribution of relative prices. That difference is the reason to keep both, and it is unreachable while the library's equations are supplied log-linearised.

**Two cautions about the library's representation.**

First, the frictionless limit runs the opposite way to Calvo's. In Calvo, $\theta \to 0$ removes the friction. In Rotemberg, $\phi \to 0$ does. A reader who assumes that "the friction parameter goes to zero" has the same meaning in both gets the direction of one of them wrong, and `rotemberg-prices` records the direction explicitly for that reason.

Second, the component's slope is a coefficient on marginal cost, not the output gap. The two coefficients differ by the factor $\big(\sigma+\frac{\varphi+\alpha}{1-\alpha}\big)$. The equation and parameter metadata consistently use the marginal-cost coefficient.

**Anchor: `rotemberg-equivalence`.**

---

## 7. What a transplant requires

The equations above are not universally transposable, and this section says what has to hold for them to be used elsewhere.

| If the new environment changes | then |
|---|---|
| the demand structure (non-constant elasticity, strategic complementarity, limited substitutability) | $\Theta$ and the slope must be re-derived from Step 2; §5 is the worked case |
| the production function (constant returns, capital in the firm's problem, firm-specific labour) | Step 2 changes, since it is where own-output effects on marginal cost enter |
| the discount factor (trend growth, recursive preferences, a financial wedge in $Q_{t,t+k}$) | $\beta$ in Step 1 is replaced by the relevant stochastic discount factor; §4 is the trend-growth case |
| the reset rule (indexation, menu costs, state-dependent pricing) | only Calvo's constant hazard yields Step 3 as written; Step 3 must be redone |
| the steady state (non-zero trend inflation) | the whole log-linearisation changes, because relative price dispersion is then first order |

The last row is worth emphasising. Every equation in this document is an approximation about a **zero-inflation** steady state. At non-zero trend inflation the Calvo Phillips curve acquires additional terms and the slope is no longer $\lambda$. No component in this library is valid at trend inflation, and none claims to be.

---

## References

- Calvo, G. (1983). Staggered prices in a utility-maximizing framework. *Journal of Monetary Economics* 12(3), 383–398.
- Galí, J. (2015). *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed., chapters 3 and 6.
- Kimball, M. (1995). The quantitative analytics of the basic neomonetarist model. *Journal of Money, Credit and Banking* 27(4), 1241–1277.
- Rotemberg, J. (1982). Monopolistic price adjustment and aggregate output. *Review of Economic Studies* 49(4), 517–531.
- Smets, F. and R. Wouters (2007). Shocks and frictions in US business cycles. *American Economic Review* 97(3), 586–606.
