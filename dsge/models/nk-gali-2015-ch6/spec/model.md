# Staggered prices and staggered wages

Galí (2015), chapter 6, assembled from `core-nk-classical` + `calvo-prices` +
`calvo-wages` + `taylor-rule`.

The derivations are in
[`docs/theory/wage-setting.md`](../../../docs/theory/wage-setting.md), which gives both
of this entry's derived identities in full. This document describes the model.

---

## 1. What this model adds, and why it is one component

This entry is `nk-gali-2015-ch3` plus `calvo-wages`. That is the whole difference, and it
is the point: the model is not a rewrite with a second friction built in but the same
composition with one more block, and the price-setting block is **not touched**.

That is only possible because the core exposes real marginal cost as a variable. A
Phillips curve written in the output gap carries the flexible-wage substitution inside
its slope and silently assumes flexible wages; the library's pricing block is written in
marginal cost, so adding a wage friction redefines marginal cost without redefining the
curve. `docs/theory/wage-setting.md` §5 derives the new definition.

## 2. Environment

As `nk-gali-2015-ch3`, with one change to the household.

**Differentiated labour.** The household supplies a continuum of labour types, each with
its own wage, aggregated by firms with elasticity $\varepsilon_w$. The household
therefore has market power in each type and sets a wage as a markup over its marginal
rate of substitution. Each period a wage can be reset with probability $1-\theta_w$.

**This is monopolistic wage setting, not unemployment.** The wage markup is a gap between
the real wage and a marginal rate of substitution; there is no search, no matching and no
one involuntarily out of work. A search block is not a substitute for `calvo-wages`: it
is a different theory of the same object, and `calvo-wages` says so in its `assumptions`.

## 3. The agents' problems

| agent | chooses | yields |
|---|---|---|
| household | consumption, bond holdings, and the wage for each labour type it may reset | Euler equation; reset wage as a markup over expected marginal rates of substitution |
| firm | the reset price | as in `nk-gali-2015-ch3` |
| central bank | the nominal rate | the rule |

## 4. Equilibrium and the complete system

Eleven equations in eleven variables. Relative to `nk-gali-2015-ch3`: two new variables,
wage inflation $\pi^w$ and the real wage gap $\tilde\omega$; three new equations; and one
of the core's closures replaced.

| | equation | what it is |
|---|---|---|
| 1–4 | IS curve, natural rate, natural output, output-gap definition | unchanged from the three-equation model |
| 5 | $\pi_t = \beta\mathbb{E}_t\pi_{t+1} + \lambda_p\, mc_t$ | price Phillips curve, **unchanged** |
| 6 | $\pi^w_t = \beta\mathbb{E}_t\pi^w_{t+1} + \lambda_w\big[\tilde\omega_t - (\sigma+\frac{\varphi}{1-\alpha})x_t\big]$ | wage Phillips curve |
| 7 | $\tilde\omega_t = \tilde\omega_{t-1} + \pi^w_t - \pi_t - \psi_{wa}\Delta a_t$ | real wage gap identity |
| 8 | $mc_t = \tilde\omega_t + \frac{\alpha}{1-\alpha}x_t$ | marginal cost, **replacing** the core's flexible-wage closure |
| 9 | $i_t = \phi_\pi\pi_t + \phi_y y_t + v_t$ | policy rule |
| 10–11 | the two processes | unchanged |

**Equation 7 is what makes the model's dynamics different in kind.** The real wage is a
ratio of two sticky nominal levels, so it carries history even though both inflation
rates are forward-looking, and the wage gap is therefore an endogenous **state**. The
three-equation model has no endogenous state at all. A contributor who declares
$\tilde\omega$ as purely contemporaneous gets a model that assembles cleanly and has no
wage dynamics; `taxonomy/variables.yaml` records the timing for that reason.

Equations 7 and 8 are derived identities, with their derivations in
`docs/theory/wage-setting.md` §§4–5.

## 5. Steady state

As `nk-gali-2015-ch3`: zero price and wage inflation, zero gaps, written directly in log
deviations. Nothing is solved.

## 6. Parameters

$\theta_w$ and $\varepsilon_w$ are declared by `calvo-wages`, with $\lambda_w$ and
$\psi_{wa}$ derived. Two cautions, both recorded in the component.

The specified value is $\varepsilon_w = 4.5$, distinct from the goods-market
elasticity. It is not innocuous:
$\varepsilon_w$ enters the slope through $(1+\varepsilon_w\varphi)$, and 4.5 against 9
changes $\lambda_w$ by about a factor of two.

$\varepsilon_w$ in `calvo-wages-kimball` is a different object — a Kimball **curvature**,
not an elasticity of substitution — and that component names it `curv_w` to keep them
apart. `taxonomy/parameters.yaml` registers which symbols are shared and which are not.

## 7. Theoretical properties

**Two limits, and the entry is verified at both.** As $\theta_w \to 0$ the wage markup gap
is held at zero, marginal cost collapses to the core's flexible-wage condition, and the
model must reproduce `nk-gali-2015-ch3` — a nesting limit whose target is another entry
whose own closed forms are already verified, rather than an abstract special case. As
$\theta_p \to 0$ prices become flexible while wages stay sticky, which is **not** the
classical model: the allocation is still distorted, by the wage friction.

**Why the entry's targets are closed forms at the two limits and not at a general
calibration.** No closed form exists for the two-friction model at a general calibration;
the article's own results are numerical. Closed forms at the limits are available and are
stronger than transcribed figures, because they hold at every calibration of the
remaining parameters.

**What the model cannot say.** The welfare losses the article reports require a
second-order or linear-quadratic treatment and are out of reach while the equations are
supplied log-linearised. The entry's tier reflects that: it reproduces the dynamics, not
the welfare ranking.

## 8. The library's representation, and what it simplifies

| | |
|---|---|
| wage inflation carried, the wage level not | the model has $\pi^w$ and the real wage **gap**, not the level of the real wage. The entry therefore reports no `real_wage` common variable: under that name it would be a different object |
| the equations are Galí's chapter 6 statement | two of the three wage equations are derived explicitly rather than quoted |
| source equations | Galí (2015), chapter 6, eqs. (15), (20) and (21) have been checked directly against the primary source |

