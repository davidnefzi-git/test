# DSGE composition-layer prototype

A working test of a composition design for a structural-model library. It assembles the basic New Keynesian model of
Galí (2015, ch. 3) from a classical core plus two blocks, rather than writing it as one
file, and verifies the result against closed-form solutions.

Written from the textbook equations. No third-party replication file is reproduced, so
nothing here carries another project's licence.

## Why this model

The simplest canonical case. Its solution for a monetary policy shock is known in closed
form, so the assembler can be checked exactly instead of to a transcribed decimal; and it
nests the classical model, so the nesting test has a known target. If the design fails
here, nothing larger is worth attempting.

## Result

```
$ python -m pytest -q
27 passed

$ python -m modellib golden nk-gali-2015-ch3     # 8 targets
$ python -m modellib golden ehl-2000             # 5 targets
$ python -m modellib golden gali-monacelli-2005  # 5 targets
```

Three composed entries and twelve components, across three model families: the
three-equation New Keynesian benchmark, the same model with sticky wages as well as
sticky prices, and the canonical small open economy with the four policy regimes of its
article as swappable components. Plus a real business cycle core written in **levels**
rather than log-linearised, which the `tests/test_levels.py` suite exercises.

Every entry is also cross-checked against an independent transcription of the same
published equation list, solved separately. Agreement is at machine precision
throughout: 3.3e-16 and 1.4e-16 for the one-friction model under its two shocks,
4.4e-16 and 3.3e-16 for the two-friction model, 2.0e-15 at worst for the open economy
across twelve variables, four regimes and two calibrations, and 1.6e-13 for the real
business cycle model.

## The solver, twice replaced

Worth recording, because each version was forced by a failure rather than chosen.

A fixed-point iteration on the policy function stalled at a residual of 2e-9 on a
calibration it had previously solved, once two definitional equations were added.
Newton's method on the matrix quadratic fixed that — and then returned a root of
spectral radius 1.07 for the real business cycle model and reported it as a solution,
because iteration converges to whichever root its starting point falls towards and a
model with endogenous capital is a saddle-path problem. Selecting the root is now a
generalized Schur decomposition, which also makes the Blanchard-Kahn condition
checkable and separates its two failures; Newton is kept to polish the selected root.

## Two defects the closed forms did not catch

Worth stating prominently, because it is the most useful thing this prototype has
produced.

Both were in the core, both survived every passing target, and both were found only by
comparing against an independent implementation:

- **the sign of the natural rate.** A positive persistent technology shock lowers the
  natural rate; the file had it rising. The model therefore answered that such a shock
  opens a *positive* output gap, +0.0855 where the truth is -0.0855. Right magnitude,
  wrong direction.
- **the policy rule.** It responded to the output gap where the article writes it in
  output. The two coincide exactly when natural output does not move.

What they have in common: both are identically masked under a monetary shock, and every
target then in the library used one. Hence the rule now recorded in the design document
— every shock a component declares must be exercised by at least one golden target —
and the stronger one it implies: closed forms verify that a model solves what it says,
and only an independent implementation verifies that it says what the article says.

## What each file contains, and what it is for

| File | Contents | Use |
|---|---|---|
| `schema/component.schema.json` | JSON Schema for a component (friction block) manifest: `provides`, `requires`, `replaces`, `depends_on`, `incompatible_with`, `nesting_target`, `minimum_perturbation_order`, and per-parameter `prior`. | The proposed new artefact type. A block has no equilibrium, no welfare and no verification tier, so `manifest.schema.json` cannot describe it honestly. |
| `taxonomy/variables.yaml` | The canonical variable namespace: symbol, definition, units, and `timing`. | Composition presupposes that blocks written by different hands connect. `timing` is the decisive field: a block that disagrees on whether a stock is predetermined assembles without error and produces wrong dynamics. |
| `components/core-nk-classical/` | The core: Euler equation, natural rate, two exogenous processes, and the flexible-price pricing condition. Five equations for six variables. | Deliberately not closed on its own. The sixth equation is whatever policy block closes the nominal side, which is why `Composition("core-nk-classical")` raises. |
| `components/calvo-prices/` | Calvo (1983) price setting. Introduces no variable; replaces the core's pricing equation by the Phillips curve. Carries priors and a `nesting_target`. | The worked example of the `provides` / `requires` / `replaces` pattern. |
| `components/rotemberg-prices/` | Rotemberg (1982) pricing, declared `incompatible_with: [calvo-prices]`. | Present only to exercise the incompatibility check. Equivalent to Calvo at first order, not beyond, hence a mutually exclusive variant and never an alias. |
| `components/taylor-rule/` | Interest rate rule, with priors on `phi_pi` and `phi_x`. | The policy block that closes the core. |
| `modellib/compose.py` | The assembler: loads components, runs the four composition checks, resolves derived parameters in dependency order, and builds the coefficient matrices from the declarative equations. | The core of the design. Its job is to refuse to assemble a model that is not well posed. |
| `modellib/lre.py` | First-order solution of `A2 E y(+1) + A0 y + A1 y(-1) + B eps = 0` by iteration on the policy function, with explicit failure on non-convergence or instability. | Deliberately small. A silently wrong solution is the worst outcome for a library whose purpose is verified numbers. |
| `modellib/golden.py` | Golden-target runner for two new target kinds: `analytic` (expected value as a closed form in the model's parameters) and `nesting`. | Both kinds are absent from the current repository format and both are required. |
| `models/nk-gali-2015-ch3/manifest.yaml` | The model entry. Replaces `model.py` by a `composition` block, and carries `common_variable_map`, structured `solver` settings, a declared `shocks` list, and `verification.tier: composed`. | Shows the five model-manifest changes in use rather than in prose. |
| `models/nk-gali-2015-ch3/golden/targets.yaml` | Six targets: five analytic, one nesting. | What verification looks like for a model you assembled, which has no paper of its own. |
| `tests/test_composition.py` | Ten tests, most of them negative controls. | The checks that must fail: unclosed composition, missing policy block, two pricing blocks, a friction block used as a core, an unknown parameter, a violated Taylor principle. |
| `tests/test_golden.py` | One test per golden target. | Mirrors the existing repository's `tests/test_golden.py`. |

## The four composition checks

A composition that is not closed, or that is doubly determined, otherwise solves without
complaint and yields dynamics that mean nothing. That silent failure is the whole reason
the interface fields exist. The assembler refuses when:

1. a required variable is provided by no included component;
2. two components provide the same variable;
3. two components replace the same equation;
4. the number of equations differs from the number of endogenous variables.

Each refusal names what is wrong:

```
Composition("core-nk-classical", ["calvo-prices"])
  -> composition is not closed: 5 equations for 6 endogenous variables (a, i, pi, rn, v, x)

Composition("core-nk-classical", ["calvo-prices", "rotemberg-prices", "taylor-rule"])
  -> components 'calvo-prices' and 'rotemberg-prices' are declared incompatible
```

## The nesting test

A model you assembled has no article, so `reproduces_paper` is unavailable. The honest
substitute: drive the friction parameter to its limit and require the composed model to
return to the core's own solution.

`calvo-prices` declares `theta_p -> 0`. Two things are checked, not one. That the output
gap response converges to the classical value of zero, and that it does so at the rate
implied analytically,

```
lim (x / theta_p) = -(1 - beta*rho_v) / (Theta * (sigma + (varphi+alpha)/(1-alpha)) * (phi_pi - rho_v))
```

which the prototype matches to four significant figures at `theta_p = 1e-4`
(`-0.2525463` against `-0.2525`). Convergence alone would let a sign error or a
mis-stated timing convention through; the rate check will not.

## What this prototype does not do

Stated plainly, because the gap between it and a usable library is the real question.

- **Log-linear equations only.** Blocks carry already-linearised equations. A real
  library needs the nonlinear equations plus a steady-state solver, otherwise second
  order, welfare and `minimum_perturbation_order` are unreachable. This is the largest
  remaining decision, and it is where Dynare or a symbolic steady state must be chosen.
- **No estimation.** The `prior` fields are declared and validated but nothing samples
  from them. The data contract (observables, transformations, sample, hashes) is not
  implemented.
- **One core, three blocks.** The checks generalise; the equation representation will
  need more work for blocks that introduce variables and equations together, such as
  the financial accelerator.
- **A toy solver.** Iteration on the policy function is adequate for six equations and
  is validated against the closed form here. It is not a substitute for a QZ-based
  solver on a medium-scale model.

## Running it

```bash
pip install -e ".[dev]"
python -m pytest -q
python -m modellib golden nk-gali-2015-ch3
python -m modellib describe core-nk-classical calvo-prices taylor-rule
python -m modellib describe core-nk-classical taylor-rule          # the classical limit
python -m modellib irf core-nk-classical calvo-prices taylor-rule
```

Dependencies: `numpy`, `sympy`, `pyyaml`, and `pytest` for the tests. No MATLAB, no
Dynare, no network access.
