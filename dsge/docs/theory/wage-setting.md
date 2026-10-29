# Wage setting

The derivations behind `calvo-wages`, `calvo-wages-kimball` and `wage-indexation`, and behind the two identities those components rely on.

The component files carry the equations the solver uses and point here. This document is the single source of truth for the algebra.

**What is established here.** Sections 1 to 3 present the Galí (2015, chapter 6) formulation of staggered wages, and the relevant source relations are derived below. Sections 4 and 5 demonstrate the real-wage-gap identity and the marginal-cost relation explicitly. Section 6 states the Smets–Wouters variant and its distinct parameterisation.

---

## 1. Environment

**Labour types.** The household supplies a continuum of differentiated labour services indexed by $j \in [0,1]$. Firms hire a composite,

$$ N_t = \left(\int_0^1 N_t(j)^{1-1/\varepsilon_w} dj\right)^{\varepsilon_w/(\varepsilon_w-1)}, \qquad \varepsilon_w > 1 $$

with the implied demand for each type and the wage index

$$ N_t(j) = N_t\left(\frac{W_t(j)}{W_t}\right)^{-\varepsilon_w}, \qquad W_t = \left(\int_0^1 W_t(j)^{1-\varepsilon_w} dj\right)^{1/(1-\varepsilon_w)} $$

Differentiation is what gives the wage setter market power; $\varepsilon_w$ governs how much.

**Preferences.** For the log-consumption case ($\sigma=1$), period utility is $U(C_t, \lbrace N_t(j)\rbrace) = \log C_t - \frac{1}{1+\varphi}\int_0^1 N_t(j)^{1+\varphi} dj$ in the Galí chapter 6 case, so that $\varphi$ is the inverse Frisch elasticity. The marginal rate of substitution between consumption and the supply of type $j$ is

$$ MRS_t(j) = \frac{-U_{N(j)}}{U_C} = C_t N_t(j)^{\varphi} $$

In log deviations, and at the symmetric allocation, $mrs_t = \sigma c_t + \varphi n_t$, which is the natural real wage when wages are flexible.

**Wage rigidity.** Each period a wage can be reset with probability $1-\theta_w$, independently of history. The structure is Calvo's, applied to differentiated labour services.

---

## 2. The wage setter's problem

A household resetting the wage for type $j$ at $t$ chooses $W_t^{\ast}$ to maximise

$$ \max_{W_t^{\ast}} \sum_{k=0}^{\infty} (\beta\theta_w)^{k} \mathbb{E}_t \Big\lbrace U\big(C_{t+k}, N_{t+k|t}\big) \Big\rbrace \quad\text{s.t.}\quad N_{t+k|t} = N_{t+k}\left(\frac{W_t^{\ast}}{W_{t+k}}\right)^{-\varepsilon_w} \text{ and the budget constraint.} $$

**First-order condition.** Collecting terms,

$$ \sum_{k=0}^{\infty} (\beta\theta_w)^{k} \mathbb{E}_t \Big\lbrace N_{t+k|t} U_{C,t+k} \Big[ \frac{W_t^{\ast}}{P_{t+k}} - \mathcal{M}_w MRS_{t+k|t} \Big] \Big\rbrace = 0, \qquad \mathcal{M}_w \equiv \frac{\varepsilon_w}{\varepsilon_w-1} $$

The reset wage is a markup over a weighted average of expected future marginal rates of substitution — the exact counterpart of the reset price over marginal costs.

**The wage markup.** Define the (log) wage markup as the gap between the real wage and the marginal rate of substitution,

$$ \mu^w_t \equiv w_t - p_t - mrs_t $$

Under flexible wages $\mu^w_t$ is constant at $\log \mathcal{M}_w$; under staggering it moves, and its movement is what the wage Phillips curve describes.

---

## 3. The wage Phillips curve

Log-linearising the first-order condition, aggregating the wage index exactly as Step 3 of `price-setting.md` aggregates the price index, and eliminating the reset wage,

$$ \boxed{\pi^w_t = \beta \mathbb{E}_t\pi^w_{t+1} - \lambda_w\big(\mu^w_t - \mu^w\big)} \qquad \lambda_w = \frac{(1-\theta_w)(1-\beta\theta_w)}{\theta_w(1+\varepsilon_w\varphi)} $$

Wage inflation rises when the wage markup is below its desired level, because wage setters who get to reset then raise wages.

Two features of the slope deserve note. The factor $(1+\varepsilon_w\varphi)$ is the wage counterpart of $\Theta$ in the price block: it comes from the dependence of a type's own marginal rate of substitution on its own hours, which depend on its relative wage. And $\varepsilon_w$ enters the slope but **not** the steady-state allocation at first order, which is why it is not separately identified and why the library records Galí's calibrated value with its source rather than treating it as free.

The **wage-markup deviation** is $\widehat\mu^w_t = \tilde\omega_t - (\sigma + \varphi/(1-\alpha))x_t$, where $\tilde\omega_t$ is the **real-wage gap** (actual real wage minus its flexible-price-and-wage counterpart). These are distinct objects. Consequently $\pi^w_t = \beta E_t\pi^w_{t+1} + \lambda_w[(\sigma + \varphi/(1-\alpha))x_t - \tilde\omega_t]$, as in Galí (2015), ch. 6, eqs. (19)–(20).

**Anchor: `wage-phillips-curve`.**

---

## 4. The real wage gap identity

`calvo-wages.real-wage-gap` is

$$ \tilde\omega_t - \tilde\omega_{t-1} - \pi^w_t + \pi_t + \psi_{wa}(a_t - a_{t-1}) = 0 $$

It is an identity given two definitions, and here is the derivation in full.

**Definitions.** The real wage gap is the real wage less its natural level, $\tilde\omega_t \equiv w_t - w^n_t$, where $w^n_t$ is the real wage that would obtain under flexible wages and prices. The natural real wage is proportional to technology, $w^n_t = \psi_{wa} a_t$.

**Step 1.** The real wage is a ratio of two nominal levels, so it grows at the difference of their inflation rates:

$$ w_t = w_{t-1} + \pi^w_t - \pi_t $$

**Step 2.** Substitute the definition of the gap into Step 1:

$$ \tilde\omega_t + w^n_t = \tilde\omega_{t-1} + w^n_{t-1} + \pi^w_t - \pi_t $$

**Step 3.** Replace the natural wage by $\psi_{wa} a_t$ and rearrange:

$$ \tilde\omega_t = \tilde\omega_{t-1} + \pi^w_t - \pi_t - \psi_{wa}(a_t - a_{t-1}) $$

which is the component's equation. $\square$

**Why it matters more than it looks.** Step 1 carries a lag. The real wage is a ratio of two *sticky* nominal levels, so it inherits history even when both inflation rates are forward-looking, and the gap is therefore an endogenous **state** of the two-friction model. A contributor who declares $\tilde\omega$ as purely contemporaneous gets a model that assembles cleanly and has no wage dynamics at all. `taxonomy/variables.yaml` records the timing for that reason.

**The elasticity.** $\psi_{wa} = \dfrac{1-\alpha\psi_{ya}}{1-\alpha}$, equivalently $1 - \dfrac{\alpha(\psi_{ya}-1)}{1-\alpha}$, where $\psi_{ya}$ is the elasticity of natural output to technology. The two forms are algebraically identical; the component uses the second and records the first in its source.

**Anchor: `real-wage-gap`.**

---

## 5. Marginal cost when wages are sticky

`calvo-wages.mc-sticky-wage` is

$$ mc_t - \tilde\omega_t - \frac{\alpha}{1-\alpha} x_t = 0 $$

**Derivation.** Real marginal cost is the real wage less the marginal product of labour, $mc_t = w_t - mpl_t$. With $Y_t = A_t N_t^{1-\alpha}$,

$$ mpl_t = a_t - \alpha n_t \quad\text{and}\quad y_t = a_t + (1-\alpha) n_t \;\Rightarrow\; n_t = \frac{y_t - a_t}{1-\alpha} $$

so $mpl_t = \dfrac{a_t - \alpha y_t}{1-\alpha}$ and

$$ mc_t = w_t - \frac{a_t - \alpha y_t}{1-\alpha} $$

Under flexible prices marginal cost is constant, $mc^n_t = 0$, which pins the natural real wage at $w^n_t = \dfrac{a_t - \alpha y^n_t}{1-\alpha}$. Subtracting,

$$ mc_t = \underbrace{w_t - w^n_t}_{\tilde\omega_t} + \frac{\alpha(y_t - y^n_t)}{1-\alpha} = \tilde\omega_t + \frac{\alpha}{1-\alpha} x_t \qquad\square $$

**What this equation replaces, and why.** It displaces the core's flexible-wage condition, which is the special case $\tilde\omega_t = 0$: $mc_t = \big(\sigma + \frac{\varphi+\alpha}{1-\alpha}\big)x_t$. Exposing $mc$ as a variable of the core, rather than folding the flexible-wage substitution into the Phillips curve's slope, is what allows the price block to be composed with or without a wage friction without being touched. This representation keeps the price-setting block valid when the wage-setting mechanism is changed.

**Anchor: `marginal-cost-sticky-wage`.**

---

## 6. The Smets–Wouters form

`calvo-wages-kimball` and `wage-indexation` state the same mechanism in a different parameterisation, and the differences are not cosmetic.

**Kimball labour aggregator.** As in `price-setting.md` §5, with curvature $\varepsilon_w$ and steady-state wage markup $\lambda_w$:

$$ \kappa_w = \frac{(1-\xi_w)(1-\bar\beta\gamma\xi_w)}{\xi_w\big[(\lambda_w-1)\varepsilon_w+1\big]} $$

Note that $\varepsilon_w$ here is a **curvature**, not an elasticity of substitution. The library names it `curv_w` in that component precisely to keep the two apart: Galí's `epsilon_w` in `calvo-wages` is an elasticity of substitution with a different default, and conflating them changes the slope by a factor of roughly two.

**Indexation.** Non-reset wages rise by a fraction $\iota_w$ of last period's **price** inflation. The resulting curve carries $\pi_{t-1}$ and a modified coefficient on $\pi_t$; at $\iota_w = 0$ it is the unindexed one, term for term.

**The level of the real wage, not wage inflation.** The Smets–Wouters form is written in $w_t$ rather than in $\pi^w_t$, and measures the markup against the marginal rate of substitution the core supplies as a variable. Keeping `mrs` explicit prevents the wage-setting block from depending on a particular consumption specification. Under the Smets–Wouters consumption block, substituting the household first-order condition yields the same wage equation.

**Multiplied through.** As with the price curve, the equation is scaled by $\kappa_w^{-1}(1+\bar\beta\gamma)$ so that the limit $\xi_w \to 0$ is the core's flexible-wage closure exactly. `price-setting.md` §4.1 gives the argument; the symbolic check is in the entry's tests.

**Anchor: `smets-wouters-wage-curve`.**

---

## 7. What a transplant requires

| If the new environment changes | then |
|---|---|
| the labour aggregator | the factor $(1+\varepsilon_w\varphi)$, or its Kimball counterpart, must be re-derived |
| preferences over consumption and leisure | $mrs_t$ changes, and with it the markup's definition; §4 and §5 are unaffected, since both are identities given the natural wage |
| the consumption specification (habit, non-separability, heterogeneity) | nothing in §3 changes **provided** the marginal rate of substitution is supplied as a variable, which is the architectural point of §6 |
| wage indexation or contract length | §3's aggregation step must be redone, as in §6 |
| the labour market structure (search and matching, bargaining, participation) | the whole block is inapplicable: there is no wage markup over a marginal rate of substitution to speak of, and a search block replaces this one rather than modifying it |

The last row is the important one. These components describe monopolistic wage setting by households. They are not a model of unemployment, and composing them with a search block would be composing two theories of the same object.

---

## References

- Galí, J. (2015). *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed., chapter 6.
- Smets, F. and R. Wouters (2007). Shocks and frictions in US business cycles. *American Economic Review* 97(3), 586–606.
