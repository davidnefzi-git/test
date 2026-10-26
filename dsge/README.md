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
167 passed in 36s

$ python -m modellib golden nk-gali-2015-ch3     #  9 targets
$ python -m modellib golden ehl-2000             #  5 targets
$ python -m modellib golden gali-monacelli-2005  #  5 targets
$ python -m modellib golden smets-wouters-2007   # 35 targets
```

Four composed entries and twenty-four components, across three model families: the
three-equation New Keynesian benchmark, the same model with sticky wages as well as
sticky prices, the canonical small open economy with the four policy regimes of its
article as swappable components, and **Smets and Wouters (2007)** -- thirty-seven
equations from twelve components, the workhorse estimated medium-scale model. Plus a
real business cycle core written in **levels** rather than log-linearised, which the
`tests/test_levels.py` suite exercises.

Smets-Wouters is the entry that forced the last mechanism into the assembler, and it is
worth reading for that reason. Its policy rule responds to output less output under
FLEXIBLE PRICES, and the second term is the output of a parallel economy. The reference
implementation writes that economy out a second time: eleven more equations, every
coefficient repeated, nothing linking the two copies. Correct the sticky Euler equation
and not its twin, and the model still assembles, still solves, and now measures its
output gap against the wrong benchmark -- invisibly, because the twin has no observable
of its own.

So the twin is not written. It is **composed**, from a subset of the entry's own
components, and the assembler enforces that subset condition: that is what makes the
twin provably the same model with its nominal blocks removed, rather than a second model
free to drift. Every equation the two economies share is stored exactly once.
`models/smets-wouters-2007/spec/model.md` is the full account.

Every entry is also cross-checked against an independent transcription of the same
published equation list, solved separately. Agreement is at machine precision
throughout: 3.3e-16 and 1.4e-16 for the one-friction model under its two shocks,
4.4e-16 and 3.3e-16 for the two-friction model, 2.0e-15 at worst for the open economy
across twelve variables, four regimes and two calibrations, 1.6e-13 for the real
business cycle model, and 2.8e-13 for Smets-Wouters across seven shocks, thirty-three
variables and eight periods.

A cross-check is the strongest check here and it has one blind spot, which cost a defect
to find. Where the two implementations adopt different conventions for a shock, the
comparison has to fit a SCALE FACTOR for it -- and a fitted factor absorbs a SIGN. The
risk-premium wedge of Smets-Wouters was implemented with the wrong sign, so that a wider
premium raised consumption, and the cross-check agreed to 1e-13 both before and after
the correction. The closed forms did not catch it either: the sharpest of them is that
the wedge is exactly neutral in the flexible-price twin, and that is a cancellation
between two coefficients, which holds whichever sign the pair carries so long as they
carry the same one. What caught it was reading the impulse response against the
article's own sentence.

So: where a cross-check fits a normalisation it verifies structure, not orientation --
and that is exactly where the risk of misreading the article is highest, since a factor
has to be fitted only when the two sources disagree about it. Every shock now carries a
target whose sign is meaningful, sourced to the article's prose rather than to its
equations.

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

- ~~**Log-linear equations only.**~~ Closed. A component may declare
  `equation_form: levels`, carry the model's own non-linear equations and a steady state,
  and the assembler solves that steady state, verifies it against every equation, and
  evaluates the Jacobians there. A composition may not mix the two forms.
- ~~**A toy solver.**~~ Closed, twice over. Iteration on the policy function returned a
  root with spectral radius 1.07 for a model with capital and called it a solution; the
  solver is now a generalized Schur decomposition on the companion pencil with a Newton
  polish, and it carries a thirty-seven-equation model with its own flexible-price twin.
- ~~**One core, three blocks.**~~ Closed: four cores and twenty-four components, and the
  representation did need the work this item anticipated -- a component that introduces
  variables and equations together, and one that supplies a whole parallel economy.
- **No estimation.** The `prior` fields are declared and validated but nothing samples
  from them. This is now the most visible gap: `smets-wouters-2007` reproduces the
  model's dynamics and declares its seven observables, their transformations and its
  sample, and its tier stays at `composed` for want of a sampler.
- **No unconditional moments.** The headline result of `smets-wouters-2007` is a variance
  decomposition and this computes impulse responses only. The first order already
  provides what a moments tier needs; what is missing besides the code is a detrending
  convention for the entries carrying a unit root.
- **The assembler substitutes parameter values BEFORE differentiating**, so every
  parameter sweep re-differentiates the whole system. A nesting target drives a friction
  through four values and pays for four symbolic differentiations of a twenty- to
  thirty-seven-equation system; that is why the medium-scale entry's thirty-five targets
  take twenty-four of the suite's thirty-six seconds. Differentiating once with the
  parameters kept symbolic, and substituting numbers afterwards, would make a sweep
  almost free. Not done here: it is on the numerical path and belongs with its own
  verification rather than in an entry's commit.

  The suite reached eight minutes before this was looked at, and the cause was not that.
  The golden driver called `run_golden` once per TARGET, so an entry with n targets
  evaluated n-squared of them -- invisible at nine targets, and 455 of 460 seconds at
  thirty-five. Worth recording how that was found: the first version of this note
  asserted, without measuring, that the time was elsewhere and that the medium-scale
  entry accounted for about thirty seconds of it. A profile said the opposite, and every
  one of that entry's targets was taking twelve seconds or more. The lesson is the same
  one section 2.2c makes about shock signs: a plausible account of where a number comes
  from is not a measurement of it.

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
