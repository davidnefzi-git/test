# Canonical DSGE models and structural mechanisms

This repository contains a structured **economic knowledge base**. The equations and
source-derived theoretical descriptions are intended to be inspected and reused;
the numerical solver is maintained only as a consistency check.

The repository is **not** an estimation package, a replication harness, or an instruction
system for a language model.

## Scientific contents

| Canonical entry | Primary theoretical reference | Scope |
| --- | --- | --- |
| `models/nk-gali-2015-ch3` | Galí (2015), chapter 3 | Basic New Keynesian closed economy |
| `models/nk-gali-2015-ch6` | Galí (2015), chapter 6 | New Keynesian model with staggered price and wage setting |
| `models/gali-monacelli-2005` | Galí and Monacelli (2005) | Small open economy and monetary regimes |
| `models/smets-wouters-2007` | Smets and Wouters (2007) | First-order medium-scale dynamics |

The library also includes a Hansen (1985) indivisible-labour core, for which the original
article was not supplied in the current primary-source review.

The individual canonical entries document which assumptions and equations their
representations retain and which they omit.

## Directory organisation

- `components/`: the equations, variables, parameters, structural assumptions and
  economic dependencies of each reusable mechanism.
- `models/`: manifests specifying complete models, theory specifications and
  mathematical reference targets.
- `docs/theory/`: source-based derivations, from primitives and first-order conditions
  to equilibrium equations and approximations.
- `taxonomy/`: controlled economic vocabulary for variables, parameters, families
  and mechanisms.
- `schema/`: declaration contracts and validation rules.
- `modellib/` and `tests/`: **maintenance and verification infrastructure**, not a
  body of scientific claims.
- `docs/composition/README.md`: technical data-format and algebraic-interface reference.
- `docs/model-documentation-policy.md`: rules for theoretical versus estimated model entries.
- `CONTRIBUTING.md`: contribution workflow, scientific-source rules and formatting conventions.

The canonical equation is recorded in its component YAML. Mathematical demonstrations
are held in the shared theory documents; derivation pointers connect the two without
maintaining competing copies.

## Scientific provenance

Two distinct fields apply to an equation:

- `status` characterises the equation's **relation to the attributed work**:
  `original`, `derived`, `adapted`, `standard`, or `unverified`.
- `source_check` describes what has actually been **checked against an independent
  source**: `verified_primary`, `verified_working_paper`, `pending`, or
  `standard_identity`.

The fields must not be conflated. `verified_working_paper` refers specifically to
the supplied ECB Working Paper No. 722 version of Smets and Wouters (2007); it is
not a claim of verbatim conformity with the final AER edition. See
`docs/theory/source-editions.md`.

Theoretical equivalence and numerical verification are different from provenance
verification. A successful matrix solution or impulse-response test does not establish
that the corresponding equation was transcribed faithfully.

## Limitations

The library contains mostly first-order approximations. Second-order welfare evaluations
are not implemented. Bayesian estimation is documented only for canonical models whose
published contribution relies on an explicit estimation procedure; the library does not
run those estimations. Some primary sources (including Hansen 1985 and the original Kimball,
Calvo and Rotemberg papers) are not included in the supplied review; claims depending
on those publications remain explicitly qualified in the component metadata.

## Local verification

From `dsge/`, after installing the dependencies declared by the project:

```bash
python -m pytest -q
python -m modellib golden nk-gali-2015-ch3
python -m modellib golden gali-monacelli-2005
python -m modellib golden smets-wouters-2007
```

Execution outputs and historical test counts belong to CI, pull requests or Git
history, not in the economic definitions.
