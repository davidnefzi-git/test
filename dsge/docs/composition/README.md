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
- the assembler with its four checks, incompatibility and dependency handling, and
  resolution of derived parameters in dependency order;
- a first-order solution of the assembled system, explicit on non-convergence or
  instability rather than returning a plausible wrong answer;
- closed-form golden targets and the nesting test, exercised on `nk-gali-2015-ch3`.

Not implemented, in the order the gaps bite:

- **Non-linear equations and a steady state.** Components carry equations that are
  already log-linearised. This is the one substantial decision left: without the
  non-linear equations and a steady-state solver, second order, welfare and
  `minimum_perturbation_order` are all out of reach, which rules out the recursive-preference
  and stochastic-volatility components the catalogue calls for. The two serious options are
  a Dynare `.mod` back end — the canonical literature is already written in it and
  Bayesian estimation is solved there, at the cost of a MATLAB or Octave dependency that
  the current `solver.implementation` enumeration does not admit — and a sequence-space
  Jacobian back end, whose block abstraction is the closest existing precedent to this
  design and which covers heterogeneous agents as well.
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
- **A production solver.** Iteration on the policy function is adequate for six
  equations and is validated here against a closed form. It is not a substitute for a
  QZ-based solver on a medium-scale model.

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
