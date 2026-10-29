# Smets and Wouters (2007), as composed here

## What the entry is and is not

It is the model's **dynamics**, at the posterior means of Tables 1A and 1B, assembled
from twelve components and verified three ways.

It is **not** the estimation. There is no Bayesian estimator in the harness and the
authors' data cannot be redistributed from this repository, so the entry's tier is
`composed` and not `estimation_replicated`. What the estimation would need is written
down rather than left implicit: the seven observables, their transformations, the sample
and the frequency are declared in the manifest's `data` block, so that adding an
estimator later is a matter of writing one and not of rediscovering what it should be
fitted to.

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

## Verification

### Layer 1: closed forms

The sharpest is a neutrality result. **In the twin, a risk-premium shock moves nothing.**
The wedge raises the return households require; with no nominal rigidity the equilibrium
risk-free real rate falls by exactly as much, and no quantity moves at all.

That holds only if the wedge enters the Euler equation at `−c_3` and the arbitrage
equation at `−1`. Either coefficient wrong, in magnitude or in sign, and the twin's
output stops being zero. One target, two coefficients.

The others are the twin's closures (`mc_f = 0`, `w_f = mrs_f`), the utilisation slope,
capital services against the stock carried into the period, and the resource constraint
and production function along the whole impulse response rather than at one horizon.

### Layer 2: an independent implementation

Both economies were compared against a separate transcription of a third-party Dynare
replication of the same article: its own notation, its own parameterisation path, its own
equation forms — unscaled Phillips curves, the household first-order condition
substituted into the wage equation, the rescaled risk-premium wedge, no real-rate
variable at all — solved separately.

Agreement is at machine precision, the worst residual being **2.8e-13** over seven
shocks, thirty-three variables and eight periods, once two differences are accounted for.
Both are differences between the **article** and that replication, not errors in either,
and this entry follows the article in both:

1. **The risk-premium wedge.** The article carries it at `−c_3` in the Euler equation and
   `−1` in the arbitrage equation. The replication rescales it and flips its sign. The
   replication's convention makes the arbitrage equation depend on the habit parameter,
   which would deny the core its habit-free closure.
2. **The investment shock in capital accumulation.** The article's equation (8) carries
   the factor `(1 + β̄γ)`, about 1.997 at the posterior mean; the replication omits it, a
   discrepancy pointed out by Del Negro and Schorfheide (2012).

### Layer 3: mutation

Every equation of the twelve components was perturbed in turn — a parameter scaled, a
variable added, a sign flipped — and the suite re-run. A perturbation that survives names
an equation nothing verifies.

### What layer 2 cannot see, and the defect that proved it

The cross-check fixes the scale at one for six of the seven shocks, so for those six the
normalisation is verified rather than fitted. The seventh needs a factor, because the
article and the replication genuinely differ on the wedge's convention -- and a fitted
factor absorbs a **sign**.

The risk-premium wedge was first implemented with the wrong sign, so that a wider premium
*raised* consumption. The cross-check agreed to 1e-13 before the correction and to 1e-13
after it. Neither the closure tests nor the nesting tests saw it either: the twin's
neutrality result is a *cancellation*, and it holds whichever sign both coefficients
carry, as long as they carry the same one.

What caught it was reading the impulse response against the article's own sentence: *"a
positive shock to this wedge increases the required return on assets and reduces current
consumption."*

The lesson is recorded in the targets file and generalised in `docs/audit-2026-10.md`: where
a cross-check fits a normalisation it verifies **structure**, not **orientation** -- and
that is exactly where the risk of misreading the article is highest, since a convention
has to be fitted only when the two sources disagree about it. Every shock in this entry
therefore carries a target whose sign is meaningful, stating what direction the economy
moves in and sourced to the article's text rather than to its equations.

## Known limits

- The variance decomposition that is the article's headline result needs unconditional
  moments, which the harness does not compute.
- Welfare comparisons across the frictions need a second order, out of reach while
  equations are supplied log-linearised.
- The seven measurement equations are declared but not implemented, because no estimator
  reads them.
- Chib and Ramamurthy (2010) show the mode the article reports is not the mode. The
  posterior **means** are used here, which are unaffected by that point, but anyone
  reproducing the estimation should know it.
