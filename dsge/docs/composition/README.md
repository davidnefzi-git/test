# The composition layer

How this repository represents a model that is *assembled* from reusable pieces rather
than ported from one replication package, why it is built this way, and what a
contributor has to do to add a piece.

Scope. This document covers the second of the two objectives set for the DSGE extension:
not only cataloguing canonical models so that an estimation can be replicated, but
combining modular pieces into a model built for a specific research question. The first
objective needs the model manifest extended; the second needs a second artefact type,
and that is what is described here.

---

## 1. Rationale

### 1.1 A block is not a model, and must not be filed as one

A friction — Calvo pricing, a financial accelerator, search and matching in the labour
market, local-currency pricing — is not a model. It has no equilibrium of its own, no
welfare, nothing to run, and no published table it reproduces. `manifest.schema.json`
requires `economics.equilibrium`, at least one `interface.tiers` entry, a
`verification.tier`, and the repository requires `golden/targets.yaml`. A block
satisfies none of these honestly, and filling those fields with placeholders would be
exactly the kind of overstatement the honesty rules in `CLAUDE.md` exist to prevent.

Hence `schema/component.schema.json`: a separate artefact type, with a separate folder
(`components/`), separate validation, and a separate notion of what it means to be
verified.

### 1.2 What composition requires that a model manifest cannot express

Assembling a model from pieces is not a matter of concatenating equations. The question
that has to be answerable mechanically is whether a given combination is a model at all.
Three declarations make it answerable:

- `variables.provides` — the endogenous variables the component *introduces*.
- `variables.requires` — the variables it uses but does not introduce.
- `replaces` — the equations it removes, by fully qualified id.

With these, four failures are caught before any number is produced:

0. components written in different equation forms, checked first because a mixed
   composition's other symptoms point the author in the wrong direction;
1. a required variable that no included component provides;
2. two components providing the same variable;
3. two components replacing the same equation;
4. a mismatch between the number of equations and the number of endogenous variables.

Without them, a composition that is under-determined or doubly determined solves without
complaint and yields dynamics that mean nothing. That silent failure, not the extra
typing, is the reason the three fields are mandatory.

A consequence worth stating, because it is counter-intuitive on first reading: a
component that *replaces* an equation `provides` nothing. `calvo-prices` introduces no
new variable. It supplies a different equation for a slot the core already owns. The
core therefore owns every endogenous variable and is deliberately **not closed on its
own** — five equations for six variables in the New Keynesian case, the sixth being
whatever policy component closes the nominal side. `Composition("core-nk-classical")`
raises, and that is the intended behaviour rather than an oversight.

### 1.3 Why a variable namespace, and why `timing` is the field that matters

Components are written by different people at different times and must still connect.
`taxonomy/variables.yaml` is the namespace their equations are written in. It is not the
same thing as a family's `common_variables` in `taxonomy/families.yaml`, which are
outputs declared for cross-model comparison; conflating the two is a mistake that only
shows up much later, so the two files say so explicitly.

The decisive field is `timing`. Two components can each be internally correct, agree on
every variable name, and still produce a model whose dynamics are wrong, because one
treats the capital stock as chosen last period and the other as chosen this period. No
closure check catches that: the equation count is right and every variable is provided.
Only a stated convention catches it, which is why `timing` is mandatory and why the
entry for `k` spells out that a component needing the stock available for production in
period *t* must write `k(-1)`.

`modellib.compose` refuses a component that uses a variable absent from
`taxonomy/variables.yaml`. Adding one therefore requires a `taxonomy/` pull request,
which is the intent: the namespace is a shared commitment, not a convenience.

### 1.4 Why the nesting test replaces `reproduces_paper`

A model you assembled yourself has no article, so `reproduces_paper` is unavailable and
`runs` understates what has been shown. The honest substitute is to exploit the fact
that a friction block, by construction, has a limit in which it disappears:

> Drive the friction parameter to its limit, and the composed model must reproduce the
> solution of the composition **without** that block.

Each component declares this in `nesting_target`. Two things are checked, not one: that
the response converges to the limiting value, and that it converges at the rate the
theory implies, where a closed form for the rate exists. The second check is the one
that earns its place. Convergence alone is satisfied by a block with a sign error
whose effect merely happens to vanish in the limit; the rate is not.

Worth recording as a caution: not every limit is a valid nesting test. `soe-closure` is
the counter-example. Removing the device that makes net foreign assets stationary does
not recover a simpler well-behaved model, it reintroduces a unit root. Its
`nesting_target` is therefore flagged `pathological: true` and documented rather than
tested. A block whose limit is degenerate must say so instead of being quietly skipped.

### 1.5 Why notation is mapped rather than imposed

The obvious design is to force every model into one set of variable names. It is the
wrong one, and the Macroeconomic Model Data Base established the better pattern on more
than a hundred models: each model keeps the notation of its own author, and adds a block
of definitional equations mapping its variables onto a small set of common ones, with
its own policy rule commented out and replaced by a common rule written in those common
variables.

This repository follows that pattern through `common_variable_map` in the model manifest.
A model stays readable against the article it came from — which is what makes review
possible — while comparison across models stays mechanical. Rewriting every entry into
a house notation would have bought the second at the cost of the first.

Note that the MMB's own model files carry no stated licence, so they are a reference to
read and a convention to adopt, never files to copy in. See section 3.6.

---

## 2. Organisation

### 2.1 Layout

```
schema/component.schema.json     The component artefact type
taxonomy/variables.yaml          The namespace component equations are written in
components/<component-id>/
    component.yaml               The component manifest; the only required file
modellib/compose.py              The assembler: the four checks, parameters, matrices
modellib/lre.py                  First-order solution of the assembled linear system
models/<model-id>/
    manifest.yaml                With a `composition` block instead of parameters of its own
    model.py                     Thin adapter: exposes the composition through modellib.Model
    golden/targets.yaml          Targets, including closed-form ones
    tests/test_properties.py     The nesting test and any model-specific property
tests/test_components.py         Every component validates against its schema
tests/test_composition.py        The assembler's checks, mostly negative controls
docs/composition/README.md       This file
```

A composed entry keeps a `model.py`. It is a thin adapter over `modellib.compose`, and it
exists so that `registry.load_model`, `golden.run_golden`, `python -m modellib golden`
and `tests/test_golden.py` all work on a composed entry exactly as on a ported one. The
composition layer is an addition to the harness, not a parallel one.

### 2.2 The two artefact types, and how they relate

| | Model entry | Component |
|---|---|---|
| Folder | `models/<id>/` | `components/<id>/` |
| Schema | `manifest.schema.json` | `component.schema.json` |
| Runs on its own | Yes | No |
| Has an equilibrium, welfare, tiers | Yes | No |
| Verified by | Published tables, or closed forms | A nesting test, plus its source paper inside its own core |
| Listed by | `python -m modellib list` | `python -m modellib components` |

A model entry may be implemented either way: as a port with a hand-written `model.py`
(`eaton-kortum-2002`), or as a composition (`nk-gali-2015-ch3`). Both are first-class.

### 2.2b Establishing that an equation is verified

Inspection is not enough, and this is the most useful thing the project has learned.
Four equations passed review while nothing in the suite verified them, and the cause was
the same every time: a term that is alive under only one shock, or at only one
calibration.

| Equation | Hidden because |
|---|---|
| the natural rate's sign | every target used the monetary shock, under which technology is zero |
| the policy rule's argument | output and the output gap coincide when natural output does not move |
| `psi_wa` in the real wage gap | it multiplies the change in technology, and the entry's targets were all monetary |
| the open economy's foreign terms | `Theta_gm` is exactly zero at the article's own baseline |

The remedy is mutation testing, and it is cheap: perturb each equation — add a small
multiple of a variable it does not contain, or scale one of its parameters — and require
at least one test to fail. An equation whose mutation survives is an equation nothing
verifies, whatever the review said. Running it over this library found half the published
prototype's equations unverified, including every equation of the open-economy core,
because two entries lacked a manifest and the golden runner silently skipped them.

Three rules follow, and `tests/test_coverage.py` enforces them:

1. an entry carrying targets must carry a manifest, or it is never collected;
2. every shock an entry declares must be fired by that entry's own targets or tests;
3. the response fired must be non-degenerate at the calibration used — which is why the
   foreign-shock targets of `gali-monacelli-2005` sit at a calibration where the foreign
   terms are not identically zero, and why its identity tests are parametrised over both
   shocks.

Two refinements the Smets-Wouters sweep forced, both about reading the survivor list
rather than about producing it.

**A survivor may be unkillable.** Some mutations do not change the model, and then no
test could possibly fail. Two kinds showed up here. A sign flip on a single-term
homogeneous equation -- the core's closure `mc`, becoming `-mc` -- is the same equation,
since scaling an equation by a constant cannot change its solution. And the operator that
adds a small multiple of "a variable the equation does not contain" can pick a variable
that is identically zero wherever that equation is live. Such survivors are noise, and
noise in a survivor list is worse than useless: it trains the reader to discount the real
ones. The discriminator is the model, not the suite -- rebuild every composition in which
the equation is live, solve with and without the mutation, and compare the solution
matrices. Identical means equivalent; different means a gap.

**A gap can be a composition nobody built.** Three survivors here looked equivalent and
were not. Adding `0.05*mc` to the core's habit-free Euler equation, to its marginal rate
of substitution or to its capital accumulation identity failed nothing -- because every
composition the suite built in which those equations were live had marginal cost pinned
at zero, the price-setting closure being unreplaced there. But a determinate composition
exists in which they are live and marginal cost moves: sticky prices on a capital core,
with flexible wages and neither habit nor adjustment costs, which is an ordinary textbook
model. It was simply never assembled.

That is the general shape of the thing: a nesting test removes ONE component, so it never
reaches a composition that differs from the entry by two. The remedy is a test that
asserts the two routes to the same economy agree -- compose without a friction, versus
compose with it and drive its parameter to zero -- taken in a composition where the
equations under test are not degenerate.

A convenient corollary for review: an identity is best checked as the residual of its own
equation, period by period, rather than through a quantity it influences. The ordering of
output gaps across policy regimes is a true statement about the model and a weak check on
any coefficient; `i = phi_pi*pi` at every horizon is exact.

### 2.2c What verification cannot see when it fits a normalisation

Section 2.2b is about equations no test touches. This one is about an equation every
layer of verification touched and none of them read correctly, which is a different
failure and needs a different remedy.

A cross-check against an independent implementation is the strongest check the library
has: it is what found the natural-rate sign and the policy rule's argument. But where the
two implementations adopt different conventions for a shock -- one carrying a rescaled
wedge, the other the raw one -- the comparison has to allow a SCALE FACTOR for that shock,
and a scale factor absorbs a sign.

The distinction is worth keeping sharp, because it says exactly how far the weakness
reaches. In `smets-wouters-2007` six of the seven shocks were compared at a scale FIXED
at one, so for those six the normalisation is verified, not fitted. The seventh, the
risk-premium wedge, needed a factor because the article and the replication genuinely
differ there -- and that is the one that went wrong. It was implemented with the wrong
sign, so that a wider premium raised consumption, and the cross-check agreed to 1e-13
before the correction and to 1e-13 after it, because the fitted factor simply changed
sign too. The weakness is not general; it is precisely coextensive with the places a
convention had to be fitted, which is also where the risk of misreading the article is
highest.

Neither did the closed forms see it. The sharpest closed form in that entry is a
neutrality result: in the flexible-price twin the wedge moves nothing, because the real
rate falls by exactly its width. That is a CANCELLATION between two coefficients, and it
holds whichever sign the pair carries so long as they carry the same one. Nor did the
nesting tests, which drive a friction to zero and say nothing about a shock's direction.

What caught it was reading the impulse response against the article's own sentence: "a
positive shock to this wedge increases the required return on assets and reduces current
consumption."

Two rules follow.

1. **A cross-check that fits a normalisation verifies structure, not orientation.** It
   establishes that the equations are the article's up to the normalisation of each
   shock, which is most of what one wants and not all of it.
2. **Every shock carries a sign target**, stating the direction the economy moves in,
   sourced to the article's PROSE rather than to its equations -- because the prose is
   what states the direction, and a transcribed equation can be transcribed with its sign
   inverted and still look right.

The second rule is cheap: a sign target is a transcribed number that already exists, with
a description saying which way it points and why.

### 2.2d A model that refers to its own flexible-price allocation

Some models contain an equation about an allocation they do not themselves have.
Smets-Wouters's policy rule is the standard case: it responds to output less output under
flexible prices, and the second term is the output of a parallel economy.

The ordinary way to supply it is to write that economy out a second time. For
Smets-Wouters that is eleven more equations with every coefficient repeated and nothing
linking the copies. The failure mode is specific and nasty: correct the sticky Euler
equation and not its twin, and the model still assembles, still solves, and now measures
its output gap against the wrong benchmark -- invisibly, because the twin has no
observable of its own.

A composition therefore declares a **shadow** instead:

```yaml
shadow:
  components: [core-nk-medium, capital-utilisation, fiscal-block-simple,
               habit-consumption, investment-adjustment-cost]
  suffix: _f
  shared: [a, b, g, zi]
  drop: [core-nk-medium.technology, core-nk-medium.risk-premium,
         fiscal-block-simple.spending, investment-adjustment-cost.investment-shock]
```

The twin is composed from the host's OWN components, and the assembler enforces that the
list is a subset of the host's. That restriction is the mechanism's whole content: it is
what makes the twin provably the same model with blocks removed, rather than a second
model free to drift. Every equation the two economies share is stored exactly once, so
correcting one corrects both -- necessarily, not by discipline.

`shared` names the objects the two economies hold in common, which are the exogenous
processes: both economies are driven by the same realised technology, not by two
independent draws. Their laws of motion are consequently dropped from the twin, and
`drop` names them explicitly rather than having the assembler infer them -- an inference
would be guesswork, while a declaration is checked, and omitting one surfaces as a
closure failure instead of as a second technology process quietly fighting the first.

Two things this requires of the core, and both are worth stating because they are what
makes a twin expressible at all:

- **The intertemporal margin is written in terms of a real rate**, with a separate
  one-line component supplying `rr = i - E pi(+1)`. Writing `i - pi(+1)` inline is
  shorter and makes a twin inexpressible, because the flexible-price economy has no
  nominal rate and no inflation to subtract.
- **The core carries a closure for each friction to replace.** Remove the nominal blocks
  and the flexible-price and flexible-wage closures bind, which is what makes the twin
  the flexible-price economy and not a recalibrated copy.

A component needing the twin declares `variables.requires_shadow`, so that composing it
without one fails at the closure check with a message naming what is missing, rather than
later on an unresolved symbol.

### 2.3 Definition of done for a component

Mirrors the model checklist in `CLAUDE.md`, and is additional to it.

1. `components/<id>/component.yaml` validates against `schema/component.schema.json`
   (`python -m modellib validate-components`).
2. Every variable in `variables.provides` and `variables.requires` is declared in
   `taxonomy/variables.yaml`. New variables go in a separate `taxonomy/` pull request
   first.
3. Every `replaces` entry names an equation that exists, written
   `<component-id>.<equation-id>`.
4. Every parameter has a `default`, a `source`, and — when `method` is `estimated` — a
   `prior`. No unsourced numbers.
5. A `nesting_target`, or `pathological: true` with an explanation of why the limit is
   not a valid test.
6. The component appears in at least one composition that is exercised by a test.
7. `minimum_perturbation_order` is set whenever the component has no effect at first
   order.
8. `provenance.license` is filled in, including `"None stated"` where that is the truth.

### 2.4 Branches and review

Following `CLAUDE.md`: one concern per branch, and taxonomy before everything that
references it.

| Branch | Contents |
|---|---|
| `taxonomy/<topic>` | `taxonomy/variables.yaml`, `taxonomy/families.yaml` |
| `schema/<topic>` | `schema/*.json`, this document, `docs/decisions.md` |
| `harness/<topic>` | `modellib/*`, `tests/test_composition.py`, `tests/test_components.py` |
| `component/<component-id>` | One component, and nothing else |
| `model/<model-id>` | One model entry, and nothing else |

A component pull request is reviewed on four things, in this order: the
`provides`/`requires`/`replaces` triplet, the parameter sources and priors, the
`nesting_target` and whether its rate is right, and only then the equations. The first
is where composition errors live; the last is where a reviewer's attention naturally
goes, which is why the order is written down.

### 2.5 Golden targets: the closed-form kind

`golden/targets.yaml` accepts, in addition to a numeric `expected`, a closed-form
`expected_expr` evaluated in the model's own resolved parameters, with named
intermediates under `where`. Three reasons:

- Some canonical results are propositions, not table cells. Obstfeld-Rogoff (1995),
  Eggertsson-Woodford (2003) and Golosov et al. (2014) state closed forms, and a
  numeric-only target format cannot verify them at all.
- Where a closed form exists it is a *stronger* target than a published number, because
  it holds at every calibration rather than at the one the article happens to print. A
  composed entry can therefore be checked at two calibrations and the agreement is not a
  coincidence of rounding.
- It keeps a transcribed number auditable as `source: "Paper Table IX, row AUS, column 1"`
  where that is what the target is, which the existing format already does well.

`expected_expr` and `expected` are mutually exclusive, and the tolerance rules in
`CLAUDE.md` apply unchanged to both.

### 2.6 Third-party model files and licences

`.mod` files are the natural source for canonical DSGE models, and their licences differ
in a way that matters here.

- The largest documented collection of Dynare replications is distributed under
  **GPL-3.0**, a reciprocal licence. Keeping such files in this private repository
  triggers no obligation, because nothing is distributed. Publishing the repository with
  them inside would place the derived work under GPL-3.0.
- The Macroeconomic Model Data Base states no licence for its model files. Treat it as
  link-only.
- Journal and author replication packages vary, and frequently state nothing. An
  unstated licence is not a permissive licence.

The practice already established for `eaton-kortum-2002` resolves this and should be
followed without exception: the third-party file goes in `original/` with
`provenance.license` and `provenance.redistributable` recorded truthfully, and **the
implementation in this repository is written from the article**, not translated from the
file. The library's own code is then not a derived work, and the question of making the
repository public stays open instead of being foreclosed by a copy made for convenience.

The same reasoning rules out committing article PDFs. What a reader or an agent needs is
the structured extraction — the equations in `spec/model.md`, the transcribed numbers in
`golden/`, the estimation details in the manifest's `data` block — which is auditable in
a way a two-column PDF is not, and which does not raise the question at all. Keep
personal copies in a git-ignored `papers/` folder and use institutional access.

---

## 3. What is implemented, and what is not

Stated plainly, because the distance between this layer and a usable one is the real
question.

Implemented:

- the component artefact type, its schema, and validation in `python -m modellib validate-components`;
- the assembler with its checks — equation form first, then dependencies,
  incompatibilities, the namespace, double provision, double replacement, unprovided
  variables, the twin's subset condition, and closure — incompatibility and dependency
  handling, and resolution of derived parameters in dependency order;
- a first-order solution of the assembled system, explicit on non-convergence or
  instability rather than returning a plausible wrong answer;
- closed-form golden targets and the nesting test, exercised on every composed entry;
- a flexible-price twin as a `shadow` composition (section 2.2d), for models whose
  equations refer to an allocation they do not themselves contain;
- mutation testing as the standard of equation coverage (section 2.2b), and sign targets
  as the standard of shock orientation (section 2.2c).

Not implemented, in the order the gaps bite:

- ~~**Non-linear equations and a steady state.**~~ Implemented, and the correction is
  worth recording because the obstacle was misdiagnosed for several days. A component
  now declares `equation_form: levels`, carries the model's own non-linear equations and
  a steady state, and the assembler solves that steady state, verifies it against every
  equation, and evaluates the Jacobians there. A composition may not mix forms, which is
  the fifth composition check.

  What made this look like a large architectural decision — a Dynare back end against a
  sequence-space one — was a confusion between the *representation* and the *solver*.
  Writing non-linear equations was never the difficulty: the assembler already
  differentiated symbolically, so evaluating those derivatives at a steady state rather
  than treating them as constants was a modest change. The real obstacle appeared only
  when the first such model was run. A model with endogenous capital is a saddle-path
  problem, and selecting the stable root is not something root-finding by iteration
  does reliably: Newton's method returned a root with spectral radius 1.07 for
  Hansen (1985) and called it a solution. That required a generalized Schur
  decomposition, which is thirty lines and also makes the Blanchard-Kahn condition
  checkable, reporting its two failures — no bounded solution, and indeterminacy —
  separately.

  The lesson generalises past this repository: the question "why can we not do X" is
  worth re-asking against the code rather than answered from the shape of the problem.

- **Second order, and everything that needs it.** Still out of reach, and now the only
  thing the representation does not already permit: welfare comparisons, recursive
  preferences and stochastic volatility all have no first-order effect. The equations are
  in levels, so what is missing is the second-order perturbation itself — the
  Schmitt-Grohe-Uribe recursion — and not a different way of writing models. That is a
  bounded piece of work on a known algorithm, not an architectural choice.
- **Estimation.** The `prior` and `data` fields are declared and validated, and nothing
  yet samples from them. The `estimate` tier remains unimplemented for every entry.
- ~~**Components that add variables and equations together.**~~ Closed by
  `calvo-wages`, which introduces wage inflation and the real wage gap together with
  their laws of motion and a new definition of marginal cost. Two lessons came out of
  it. First, a reduced-form coefficient blocks composition: `calvo-prices` originally
  wrote its curve in the output gap with the flexible-wage substitution folded into
  `kappa`, which silently assumed flexible wages, and the fix was to expose `mc` as a
  variable of the core so the pricing block never changes. Second, a component that
  introduces an endogenous STATE — `omega_tilde` enters its own law of motion with a
  lag — must say so in `taxonomy/variables.yaml`, because a contributor who treats it
  as forward-looking gets a model that assembles cleanly and has no wage dynamics at
  all.
- ~~**A production solver.**~~ Closed. Iteration on the policy function was adequate for
  six equations and not for a model with endogenous capital; the solver is now a
  generalized Schur decomposition on the companion pencil with a Newton polish, and it
  carries a thirty-seven-equation model with its own flexible-price twin.
- ~~**A medium-scale model.**~~ Closed by `smets-wouters-2007`: twelve components,
  thirty-seven equations, seven shocks, verified against an independent implementation to
  2.8e-13. The mechanism it needed — a flexible-price twin, composed rather than
  duplicated — is section 2.2d, and it is the first piece of the layer that is about a
  model referring to an allocation it does not itself contain.
- **Unconditional moments.** The headline result of `smets-wouters-2007` is a variance
  decomposition, and the harness computes impulse responses only. This is now the gap
  that bites first: a moments tier needs the solution's autocovariances, which the first
  order already provides, plus a detrending convention for the entries that carry a unit
  root. That convention belongs in `taxonomy/families.yaml` beside the family's common
  variables.

## 4. Sequencing

The change sets are ordered so that the test suite passes after each one.

1. `taxonomy/` — the namespace and the family common variables. Referenced by everything
   that follows; no behaviour change.
2. `schema/` — the extended model manifest, the component schema, this document, the
   decision log entry. Existing manifests keep validating; no behaviour change.
3. `harness/` + `components/` — the assembler, the solver, the golden extension, the
   four components, and their tests.
4. `model/nk-gali-2015-ch3` — the first composed model entry, with closed-form targets
   and the nesting test.
