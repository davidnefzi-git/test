# A library of canonical DSGE models and reusable structural components

## What this is for

This library exists so that the specification of a structural macroeconomic model can be
**recovered, understood and reused** — not merely run.

Three uses, in increasing order of difficulty:

1. **Recover a canonical model.** Its environment, the agents' problems, its equilibrium
   conditions, its complete equation system, its parameters with their sources, its steady
   state, and the theoretical properties that hold in it.
2. **Understand a mechanism.** What economic primitives a friction rests on, which
   first-order conditions produce its equations, which approximations were taken, and what
   the resulting coefficients mean.
3. **Reuse a mechanism somewhere else.** Which assumptions must hold for its equations to
   remain valid, which other mechanisms contradict it, and which steps of its derivation
   have to be redone when the surrounding economy differs from the one it came from.

The third is the hard one and it is the reason the library is organised the way it is. A
linearised equation is not a portable object. Having the Euler equation with habit
formation does not let you reintroduce it into an economy whose budget constraint, assets
or household structure differ. Having a Phillips curve does not let you reconstruct the
pricing problem without the aggregation technology, the competitive structure and the
firm's optimality conditions. A library that stores only equations supports the first use
and quietly fails the third.

## What this is not

Not an estimation environment, not a DSGE solver intended to compete with Dynare, not a
replication harness.

There is a numerical engine, and its purpose is narrow: to establish that the equations
written down are the equations intended, that the models close, and that the components
compose. It is a verification instrument, not the product.

There is no likelihood, no Kalman filter, no sampler, no data download. Information about
calibrations, estimated values and priors **is** kept, because those are properties of the
canonical models, but their presence is not a reason to build econometric machinery around
them.

---

## Organisation

Two artefact types, and four layers of knowledge about them.

### The two artefact types

| | **model entry** | **component** |
|---|---|---|
| folder | `models/<id>/` | `components/<id>/` |
| what it is | a published model, assembled | a reusable piece of one: a core, a friction, a maintained assumption, a policy rule |
| runs on its own | yes | no |
| has an equilibrium, a tier | yes | no |
| verified by | closed forms, cross-checks against independent implementations, published values | a nesting test, plus the entries that compose it |

A model entry holds no equations. It names the components it is assembled from, and the
assembler refuses a composition that is not closed. That is what makes a second model
sharing a mechanism **one more component**, not a second copy of the equations: there is
one Calvo Phillips curve in this library, not one per model that uses it.

### The four layers

**1. Equations, structured.** Each component carries its equations in a form the engine
can read and differentiate, each with the variables it uses, the parameters it needs and
the equations of other components it replaces. `schema/component.schema.json` is the
contract.

**2. Derivations, in prose.** `docs/theory/` holds the algebra: primitives, the agents'
problems, the first-order conditions, the aggregation, the approximation. Organised **by
mechanism, not by component**, because the derivations are shared — one Calvo derivation
serves every pricing block. Each document ends with a table headed *what a transplant
requires*, which lists the steps that fail when the environment changes. That table is the
part written for the third use above.

**3. Contracts, declared.** Three things a reader must not have to infer:

- every equation declares its **status** with respect to its source — attested in the
  publication, derived from it, deliberately adapted, a standard relation, or unverified —
  and a derived or adapted equation must point at where the steps are written out;
- every component declares the economic **assumptions it maintains**, the equations in
  which each is operative, and what replacing one would require;
- `taxonomy/` pins the shared vocabulary: variables with their timing and units, families
  with the variables their members report for comparison, mechanisms, and the parameter
  symbols more than one component may declare.

The `timing` field in `taxonomy/variables.yaml` is the one to read first. Two components
can be internally correct, agree on every variable name, and produce a model whose
dynamics are wrong because one treats the capital stock as chosen last period and the
other as chosen this period. No closure check catches that; only a stated convention does.

**4. Verification, mechanical where it can be.** Described below.

### The directory layout

```
components/<id>/component.yaml    one component: equations, interface, parameters,
                                  assumptions, nesting target, provenance
models/<id>/manifest.yaml         what the entry is assembled from, and what is verified
models/<id>/golden/targets.yaml   the numbers it must reproduce
models/<id>/spec/model.md         the model: environment, problems, system, properties
docs/theory/                      the derivations, by mechanism
docs/composition/README.md        why the composition layer is built this way
docs/audit-2026-10.md             what was wrong, what changed, what is still open
taxonomy/                         variables, families, mechanisms, shared parameters
schema/                           the component contract, as JSON Schema
modellib/                         the assembler, the solver, the golden runner
tests/                            what is checked, and what is deliberately not
```

---

## Content

Described by kind rather than enumerated, since the library grows.

**Cores** are the skeletons other components mount on. Each owns a family's endogenous
variables and is deliberately **not** closed on its own: a core plus nothing does not
solve, because the equation that closes the nominal or real side is whichever component
supplies it. Each also carries one **closure equation per friction it expects**, so that a
model without the friction is still complete and so that the friction's frictionless limit
is an equation rather than a numerical coincidence.

**Frictions** introduce a mechanism, normally by replacing a core equation. Each declares
a **nesting target**: the parameter that switches it off, the limit, the composition that
must be recovered, and — where a closed form exists — the rate of convergence. A limit
alone is satisfied by a block with a sign error whose effect happens to vanish; the rate
is not.

**Maintained assumptions** are components with no friction parameter: a relation the model
takes as given and that another component might replace. They exist as components when
their replacement is a live possibility, and as declared assumptions on a core when it is
not.

**Policy rules** close the nominal or fiscal side. Where a published comparison turns on
the rule — several regimes for the same economy — each regime is a component, so the
comparison is a matter of exchanging one block rather than maintaining several models that
differ in one equation.

**Model entries** are published models assembled from the above, spanning the closed
economy, the open economy, real business cycle models and the medium-scale estimated
family. Each carries a specification document, a manifest recording what is verified and
at what tier, and numerical targets.

Scale, at the time of this writing: 24 components across 4 cores, 4 model entries, 78
equations each with a declared status, 52 declared assumptions, 4 theory documents, and
471 tests. The point of recording it is the ratio, not the totals: the library is small
enough that every equation can be accounted for individually, and it is organised so that
it stays that way as it grows.

---

## Verification, and what it does not establish

Four layers, each catching what the one before it cannot.

**Closed forms.** Where an analytic solution exists it is the target, because it holds at
*every* calibration rather than at one. These are stronger than transcribed table cells.

**Independent implementations.** Each entry is compared against a separate transcription
of the same published equation list, in its own notation, solved separately. Agreement is
at machine precision throughout. This is the layer that catches an equation that solves
correctly but says something other than the article does.

**Nesting.** Drive a friction's parameter to its limit; the composition must reproduce the
one without it, at the analytically implied rate where one exists.

**Mutation.** Perturb each equation in turn and require at least one test to fail. An
equation whose perturbation survives is an equation nothing verifies, whatever a review
concluded. Running this over the library found half of one branch's equations unverified,
and the recurring cause was always the same: a term alive under only one shock, or at only
one calibration.

### Three things verification here cannot do

**It cannot certify economics.** No test establishes that a Phillips curve is Galí's, that
two components are theoretically compatible, or that a derivation is correct. Those
require mathematics and reading. The library's answers to them are the `status` field, the
theory documents and the open questions — not a green tick.

**A cross-check that fits a normalisation verifies structure, not orientation.** When two
implementations differ in a shock's convention, the comparison must fit a scale factor for
that shock — and a fitted factor absorbs a **sign**. One wedge in this library was
implemented with the wrong sign and the cross-check agreed to 1e-13 before the correction
and after it. The closed form did not catch it either, because the relevant one is a
cancellation between two coefficients and holds whichever sign the pair carries. What
caught it was reading the impulse response against the article's own sentence. Every
shock now carries a target whose sign is meaningful, sourced to the publication's prose
rather than to its equations.

**A nesting test removes one component**, so it never reaches a composition two blocks
away from an entry. Five equations of one core were perturbable with no test failing,
because every composition the suite built in which they were live had marginal cost pinned
at zero. The composition that exposed them was an ordinary model that had simply never
been assembled.

Both of those are recorded in `docs/composition/README.md`, in the sections on what
verification cannot see.

---

## Honesty rules

These are binding on anything added to the library.

- A tier is never set above what the tests demonstrate.
- A field that cannot be determined from the source is `null`, and the question goes in
  `verification.open_questions`. It is not guessed.
- An adaptation is never presented as an original equation. That is what the `status`
  field exists for.
- An equation number, a reference or a result that has not been consulted is not
  reconstructed. Where a correspondence is second-hand, the component says so.
- A parameter's `source` points at where the number actually came from.
- `open_questions` holds questions that are open. Resolved items go to `notes`, where they
  read as history.
- A documentary reorganisation does not change a number. When one is changed, the change
  is a separate, justified act.

---

## Running it

```bash
pip install -e ".[dev]"
python -m pytest -q
python -m modellib describe <core> <block> ...     # the assembled system
python -m modellib golden <model-id>               # its targets
python -m modellib irf <core> <block> ...          # impulse responses
```

Dependencies: `numpy`, `scipy`, `sympy`, `pyyaml`, and `pytest`. No MATLAB, no Dynare, no
network access.

## Where to start reading

| if you want | read |
|---|---|
| what a model is and what holds in it | `models/<id>/spec/model.md` |
| where an equation comes from | the component's `status` and `derivation` fields, then `docs/theory/` |
| whether a mechanism fits your model | the component's `assumptions`, then the *what a transplant requires* table in its theory document |
| why the library is built this way | `docs/composition/README.md` |
| what is wrong with it today | `docs/audit-2026-10.md` §6 |
