# Smets and Wouters (2007), as composed here

**Primary source.** Smets and Wouters (2007), *American Economic Review* 97(3),
586–606, has been supplied and is the authoritative source for the Bayesian
empirical reference. The earlier ECB Working Paper No. 722 remains relevant when
comparing equation conventions. See [`estimation.md`](estimation.md) and
[`../estimation.yaml`](../estimation.yaml) for the seven observables, estimation
procedure, priors, posterior results and associated evidence.


## What the entry is and is not

It is the model's **dynamics**, at the posterior means of Tables 1A and 1B, assembled
from twelve components and verified three ways.

**The estimated model is more than its dynamics.** The AER's Section II reports a
Bayesian likelihood on seven observables, 36 inferred parameters, explicit priors,
a posterior-mode optimisation and Metropolis–Hastings inference. Those elements are
now part of this model's reference resources in `estimation.yaml` and
`spec/estimation.md`. They are source-based published facts, **not an estimation
performed by the library**, whose numerical tier remains `composed`.

## The structure, and why it is cut this way

The model has twenty-four equations in the sticky economy and thirteen in its
flexible-price twin. The cut into components follows one rule: **a component owns the
margin it changes, and nothing else.**

| component | kind | what it owns | what it replaces |
|---|---|---|---|
| `core-nk-medium` | core | the real block: production, factor demand, capital, the value of installed capital, the intertemporal margin in terms of a REAL rate | — |
| `capital-utilisation` | friction | the utilisation decision | the core's fixed-utilisation closure |
| `fiscal-block-simple` | policy | exogenous spending and its process | — |
| `habit-consumption` | friction | nothing; it changes two margins | the Euler equation and the marginal rate of substitution |
| `investment-adjustment-cost` | friction | the investment-specific shock | the no-adjustment-cost closure and capital accumulation |
| `calvo-prices-kimball` | friction | inflation and the price-markup process | the core's flexible-price closure |
| `price-indexation` | friction | nothing | the price Phillips curve |
| `calvo-wages-kimball` | friction | the wage-markup process | the core's flexible-wage closure |
| `wage-indexation` | friction | nothing | the wage Phillips curve |
| `fisher-equation` | assumption | nothing; one identity | — |
| `taylor-rule-sw` | policy | the policy rate and its shock | — |
| `rule-inflation-only` | policy | a simpler closure, used by the nesting tests | — |

Three choices in that table are worth defending.

### The core prices a real rate, not a nominal one less inflation

Every equation of the real block that involves an intertemporal margin — the Euler
equation and the arbitrage equation for installed capital — is written in terms of `rr`,
and a separate component supplies `rr = i − E π(+1)`.

Writing `i − pi(+1)` inline would be shorter and is what the reference implementation
does. It also makes a flexible-price twin inexpressible, because that economy has no
nominal rate and no inflation. One identity, factored out, is the whole price of being
able to form the twin at all.

### The marginal rate of substitution is a variable

The wage Phillips curve needs the gap between the real wage and the household's marginal
rate of substitution. Under habit formation that rate involves lagged consumption, so
writing it out inside the wage equation — again, what the reference does — makes the wage
block depend on the consumption block.

Exposing `mrs` as a variable with its own defining equation, which the habit component
replaces, costs one equation and one variable and buys independence: the wage friction
can be composed with any consumption specification, and the habit friction's entire
footprint is two replaced equations.

### Capital accumulation is in the core, utilisation is not

Accumulation is an identity: a model with capital has it whether or not anything is
costly. Utilisation is a decision, with a parameter that can be driven to a limit where
the decision disappears. The first belongs to the skeleton; the second is a friction.

The investment-adjustment-cost component nonetheless **replaces** the accumulation
identity, with a version carrying the investment-specific shock. That is not an
inconsistency: the shock's coefficient in that equation is proportional to the adjustment
cost, so at zero adjustment cost the term is not small, it is absent. A shock that exists
only through a friction belongs to that friction.

## The flexible-price twin

The policy rule responds to output less its flexible-price counterpart. That counterpart
is not a variable of the model: it is the output of a parallel economy.

The reference implementation writes that economy out a second time — eleven equations,
every coefficient repeated. Nothing links the two copies. An author who corrects the
sticky Euler equation and not its twin gets a model that still assembles, still solves,
and whose output gap is now measured against the wrong benchmark; and because the twin
has no observable of its own, the error shows up only as a shifted gap.

So the twin is not written. It is **composed**, from a subset of this entry's own
components:

```yaml
shadow:
  components: [core-nk-medium, capital-utilisation, fiscal-block-simple,
               habit-consumption, investment-adjustment-cost]
  suffix: _f
  shared: [a, b, g, zi]
  drop: [core-nk-medium.technology, core-nk-medium.risk-premium,
         fiscal-block-simple.spending, investment-adjustment-cost.investment-shock]
```

Read as economics: the flexible-price economy is this model with its four nominal blocks
removed. Remove them and the core's own flexible-price and flexible-wage closures bind,
which is what makes the twin the flexible-price economy rather than a differently
calibrated copy. Every equation the two economies share is stored exactly once, so
correcting one corrects both — necessarily, not by discipline.

Two fields carry the content:

- **`shared`** names the objects the two economies hold in common. The exogenous
  processes: both economies are driven by the same realised technology, not by two
  independent draws. Their laws of motion are therefore **dropped** from the twin.
- **`drop`** names those equations explicitly, by id, rather than having the assembler
  infer them. The inference would be guesswork; the declaration is checked, and omitting
  one shows up as a closure failure instead of as a second technology process quietly
  fighting the first.

The assembler enforces that `components` is a **subset** of the host's. That restriction
is the mechanism's whole content: it is what makes the twin provably the same model with
blocks removed.

A component that needs the twin says so, with `requires_shadow`, so that composing the
rule without a twin fails at the closure check with a message naming what is missing.

## Theoretical and numerical checks

The first-order equations are supplied in their structurally reduced form,
with the flexible-price counterpart built from common real-side components.
This representation must be distinguished from direct primary-source verification.

In the flexible-price counterpart, the risk-premium disturbance is absorbed by
the real interest rate and does not change real quantities under the maintained
model assumptions. This equilibrium restriction is included among the algebraic
reference targets, but alone it cannot determine the economic sign of a shock.

Two economically relevant **normalisation conventions** must remain visible:

1. **Risk-premium orientation.** A positive risk-premium shock increases the
   required return on households' assets and reduces consumption. The Euler
   and capital-value equations contain its negative contributions. This
   convention is described explicitly in ECB WP 722, §2, eqs. (2) and (4).
2. **Investment disturbance in accumulation.** ECB WP 722, eq. (8), has an
   investment-efficiency coefficient including the factor
   `(1 + beta_bar*gamma_g)`. Alternative implementations may omit that factor; the library follows the published source. The library retains the equation of the supplied paper.

These are scientific normalisation distinctions, not statistics from a
particular test run. The source-version limitations are recorded in
`docs/theory/source-editions.md`.

## Bayesian evidence and limits

The paper's Table 1A reports nineteen structural/steady-state posterior distributions
and Table 1B seventeen shock-process posterior distributions. Their full priors,
posterior modes, means and quantiles are available in
[`estimation.yaml`](../estimation.yaml). Equation (15), the Metropolis–Hastings
procedure, comparisons against VAR and BVAR models, and counterfactual importance of
frictions are explained in [`estimation.md`](estimation.md). The reference also
identifies the steady-state inflation and hours intercepts absent from the dynamic
component composition.

The library does not estimate the model, compute posterior uncertainty bands,
integrate a marginal likelihood, or reproduce variance decompositions from data.
Welfare analyses beyond first order are likewise outside its current solver.
These are limitations of executable verification, **not omissions from the
scientific description of the canonical estimated model**.
