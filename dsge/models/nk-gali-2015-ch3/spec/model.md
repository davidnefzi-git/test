# The basic New Keynesian model

Galí (2015), chapter 3. The three-equation benchmark, assembled from `core-nk-classical` + `calvo-prices` + `taylor-rule`.

This document describes the **model**. The derivations are in [`docs/theory/price-setting.md`](../../../docs/theory/price-setting.md) and [`docs/theory/wage-setting.md`](../../../docs/theory/wage-setting.md); the equations the solver uses are in the component files, each with a `status` saying what it is with respect to the source. Nothing is restated here that is written there.

---

## 1. Environment

A closed economy with no capital. Time is discrete and quarterly.

**Household.** One infinitely-lived representative household, with separable preferences over consumption and labour, holding a riskless one-period nominal bond. It prices state-contingent claims, faces no borrowing constraint, and supplies homogeneous labour at a competitive wage. Hence a single Euler equation describes the economy's intertemporal margin.

**Firms.** A continuum of monopolistically competitive firms, each producing a differentiated variety with technology $Y_t(i) = A_t N_t(i)^{1-\alpha}$. Varieties are aggregated with constant elasticity $\varepsilon$. Each period a firm resets its price with probability $1-\theta_p$.

**Central bank.** Sets the nominal rate by rule.

**Shocks.** Technology $a_t$ and a monetary policy disturbance $v_t$, both AR(1).

## 2. The agents' problems

| agent | chooses | subject to | yields |
|---|---|---|---|
| household | consumption, labour, bond holdings | budget constraint, no-Ponzi | Euler equation; labour supply |
| firm resetting its price | the reset price | the demand curve it faces and the Calvo hazard | reset price as a markup over expected marginal costs |
| central bank | the nominal rate | the rule | the rule |

The household's labour-supply condition, combined with the firm's cost minimisation, gives real marginal cost as a function of the output gap alone — which is the equation the model's flexible-wage closure states and which `ehl-2000` replaces.

## 3. Equilibrium and the complete system

Nine equations in nine variables. In the library's notation, with lower case for log deviations from the zero-inflation steady state:

| | equation | what it is |
|---|---|---|
| 1 | $x_t = E_t x_{t+1} - \frac{1}{\sigma}(i_t - E_t\pi_{t+1} - rn_t)$ | dynamic IS curve |
| 2 | $rn_t = -\sigma\psi_{ya}(1-\rho_a)a_t$ | natural rate of interest |
| 3 | $y^n_t = \psi_{ya}a_t$ | natural output |
| 4 | $x_t = y_t - y^n_t$ | the output gap, by definition |
| 5 | $mc_t = \big(\sigma + \frac{\varphi+\alpha}{1-\alpha}\big)x_t$ | marginal cost under flexible wages |
| 6 | $\pi_t = \beta E_t\pi_{t+1} + \lambda_p mc_t$ | Phillips curve |
| 7 | $i_t = \phi_\pi \pi_t + \phi_y y_t + v_t$ | policy rule |
| 8–9 | $a_t = \rho_a a_{t-1} + \varepsilon^a_t$, $v_t = \rho_v v_{t-1} + \varepsilon^v_t$ | the two processes |

**The three-equation reduction.** Substituting 5 into 6 and 3–4 into 1 gives the familiar system in $x_t$, $\pi_t$ and $i_t$ with the Phillips curve's slope $\kappa = \lambda_p(\sigma + \frac{\varphi+\alpha}{1-\alpha})$. The library does **not** write it that way, and the reason is compositional rather than aesthetic: a Phillips curve written in the output gap has the flexible-wage substitution folded into its slope, and such a block cannot be composed with a wage friction. Exposing $mc$ as a variable of the core is what makes `ehl-2000` the same model plus one component rather than a rewrite. See `docs/theory/wage-setting.md` §5.

**One accounting identity**, equation 4, and no others: with no capital and no government, goods market clearing is $y_t = c_t$ and consumption is not carried as a separate variable. That is why this entry reports no `consumption` common variable: doing so would assert a distinction the model does not make.

**The policy rule responds to output, not to the output gap.** Equation 7 carries $y_t$. The distinction matters under technology disturbances, when natural output varies. The model carries technology-shock targets as well as monetary-shock targets.

## 4. Steady state

Zero inflation, zero output gap, $i = rn = -\log\beta$. The model is written directly in log deviations about that point, so no steady state is computed: there is nothing to solve. The approximation is valid only about a **zero-inflation** steady state — at trend inflation the Phillips curve acquires further terms and $\lambda_p$ is no longer its slope (`docs/theory/price-setting.md` §7).

## 5. Parameters

Declared in `core-nk-classical`, `calvo-prices` and `taylor-rule`, each with a `source`. Four are derived rather than set: $\psi_{ya}$, $\Theta$, $\lambda_p$ and $\kappa$, built from the deep parameters by the assembler in dependency order. $\kappa$ enters no equation and is retained because the entry's closed forms and the component's nesting rate are stated in terms of it; its own description says so.

$\varepsilon$, the elasticity of substitution across goods, affects the model only through $\Theta$ and so is weakly identified; the library records the textbook value with its source rather than treating it as free.

## 6. Theoretical properties

**Determinacy.** The solution is unique when the rule satisfies the Taylor principle. The library does not derive the condition; it reports a Blanchard–Kahn failure, and distinguishes its two kinds — no bounded solution, and indeterminacy — when the solver encounters one.

**Monetary non-neutrality**, and its disappearance. As $\theta_p \to 0$ the Phillips curve becomes vertical, the output gap returns to zero at every date, and the model reproduces the classical one: real neutrality, with inflation still determined by the rule. The convergence is linear in $\theta_p$ with an analytically implied constant, and `calvo-prices` declares both the limit and the rate, so a sign error that happens to vanish in the limit cannot pass.

**What the model cannot say.** Nothing about welfare: the second-order terms a welfare statement needs are not available while the equations are supplied log-linearised. The entry's tier is `composed` and makes no welfare claim.

## 7. The library's representation, and what it simplifies

| | |
|---|---|
| **not** written as one file | the model is a composition of three components; `nk-gali-2015-ch3` is the simplest case the machinery is tested on, and if the assembler cannot reproduce this model's closed form, nothing larger is worth attempting |
| verified by closed forms, not table cells | the impact responses of the gap and of inflation to a monetary shock hold at **every** calibration, so they are stronger than any transcribed figure; the entry's targets are those forms, at two calibrations |
| marginal cost exposed, slope not folded | §3 |
| source equations | Galí (2015), chapter 3, eqs. (17), (20) and (22)–(24), checked against the supplied chapter |
| no indexation block for this family | `price-indexation` exists but was written for the medium-scale family, whose curve carries trend growth and a Kimball slope. An indexation block in Galí's parameterisation does not exist |
