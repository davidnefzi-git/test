# DSGE component representation and validation

This document describes the **information format and technical consistency checks**
used by the structural-model library. It is not an LLM workflow, a model-design skill,
or an estimation protocol.

## Model entries and components

A model entry in `models/<id>/` describes a complete theoretical specification.
A component in `components/<id>/component.yaml` describes a structural mechanism,
assumption or policy equation that may enter a model; a component alone does not
claim to be a closed model.

`models/<id>/manifest.yaml` records the core, included blocks, relevant
flexible-price economy, shocks and model-level economic metadata. The component YAML
records the equations and their direct economic prerequisites.

## Component contract

| Field | Economic or structural meaning |
| --- | --- |
| `variables.provides` | Endogenous variables introduced by the component |
| `variables.requires` | Variables supplied by other included components |
| `variables.requires_shadow` | Variables needed from a separate flexible-price economy |
| `depends_on` | Required component dependencies |
| `incompatible_with` | Mechanisms that must not coexist |
| `compatible_cores` | Cores whose parameter and variable conventions are supported |
| `replaces` | Equations displaced by the component |
| `assumptions` | Economic primitives and maintained restrictions affecting equations |
| `equations[].status` | Relation of each equation to its attributed publication |
| `equations[].source_check` | Distinct independent source-verification status |
| `equations[].derivation` | Pointer to the theoretical mathematical demonstration |
| `parameters` and `shocks` | Definitions, normalisations, calibration and source metadata |

All equation expressions equal zero. The DSL uses `x(+1)` and `x(-1)`
for leads and lags. These are mathematical contracts, not free-text suggestions.

## Economic compatibility versus algebraic closure

Mechanical checks can establish that an expression uses declared variables, that a
replacement points to an existing equation, that there is no duplicated provider,
and that an assembled equation system is square. They cannot establish that two
sets of preferences, technologies, trading arrangements or assets describe one
coherent economy.

That limitation is why `assumptions` and the derivation documents exist.
In particular, identical variable names do not prove agreement on a natural
allocation, timing of capital, inflation definition or household asset structure.

`taxonomy/variables.yaml` defines units and timing. `taxonomy/parameters.yaml`
documents legitimately shared symbols. If parameters denote distinct economic
objects, they must not silently share one name.

## Flexible-price counterparts

Some medium-scale models define the policy output gap relative to a parallel
economy with nominal frictions removed.

Such a model may declare a `shadow` in its manifest:
- `components`: real-side components used by the counterpart;
- `suffix`: variable namespace suffix for the counterpart;
- `shared`: exogenous objects common to both economies;
- `drop`: duplicate shock-process equations removed from the counterpart.

A component such as `taylor-rule-sw` then declares
`variables.requires_shadow` rather than treating its counterpart as an
unidentified exogenous series.

## Scientific verification

A correct source status is not proof of empirical replication or of economic
validity. Three questions must remain separate:

1. **Source fidelity:** do the equation and its economic interpretation follow the
   cited primary reference, including its edition and conventions?
2. **Algebraic integrity:** are the transforms, dependencies and identities correct?
3. **Numerical behaviour:** does the specified model solve with the expected
   properties under the chosen parameters and shocks?

`status` identifies an equation as original, derived, adapted, standard or
unverified. `source_check` specifies whether it has actually been checked against
an original, against the supplied ECB working-paper version, remains pending, or
is a generic identity. The latter is not a proxy for the first.

The tests in `tests/` cover only those properties that are mechanisable:
valid declarations, internal references, consistent interfaces, limits and
the algebra of models. They do **not** certify the fidelity of a Phillips curve
or the applicability of an economic assumption without reading its source.

The `golden/targets.yaml` files contain enduring analytical reference
properties and numerical test criteria, not logs of particular test executions.

## Reuse and source limits

Reusable equations are conditional on the underlying primitives. Replacing
complete international markets by incomplete markets, Calvo by Rotemberg
pricing, or external by internal habits can affect several equilibrium equations
at once. The consequences are set out by the component's `assumptions`
and by `docs/theory/`.

See `docs/theory/source-editions.md` for the verified primary-source scope of each
canonical model and `docs/model-documentation-policy.md` for the documentation required
for theoretical, calibrated and estimated entries.

Unresolved scientific limitations remain in the component and model files.
Transient test counts, build timings, mutation anecdotes and historical
development notes are retained in Git history or associated pull requests,
not as model-theoretic properties.
