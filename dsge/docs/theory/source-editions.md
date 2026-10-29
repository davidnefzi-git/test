# Primary source verification

This document records the published references used to verify the canonical model entries
and the scope that has actually been checked. It intentionally excludes file-acquisition
details, upload history, local filenames and development notes.

| Reference | Edition | Verified scope |
| --- | --- | --- |
| Galí (2015), chapter 3 | *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed. | Dynamic IS equation (23), natural-rate equation (24), natural output (20), pricing equations (17), (21)–(22) |
| Galí (2015), chapter 6 | *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed. | Wage-setting equations (15), (19)–(20), real-wage-gap equation (21), dynamic IS equation (22) |
| Galí and Monacelli (2005) | *Review of Economic Studies* 72, 707–734 | Complete-markets small-open-economy equilibrium, relative-price identities, natural allocation and monetary-policy regimes |
| Smets and Wouters (2007) | *American Economic Review* 97(3), 586–606 | Structural equations (1)–(15), seven-observable measurement system, priors, posterior results, Bayesian estimation procedure and Tables 1A–1B |
| Smets and Wouters (2007) | ECB Working Paper No. 722 | Equation conventions used for comparison with the published AER specification |

## Formula and version conventions

**Galí chapter 3.** Equation (22) is the output-gap Phillips curve obtained from the
marginal-cost pricing equation and the flexible-wage supply relation. The reusable
`calvo-prices` component uses the intermediate marginal-cost formulation so that it
can be combined with alternative wage-setting blocks.

**Galí chapter 6.** The wage Phillips curve is equation (20), following the wage-markup
identity in equation (19). Equation (21) governs the real-wage gap. Equation (22) is the
dynamic IS curve.

**Smets–Wouters.** The AER publication is the controlling source for the canonical
empirical specification, including equation (15), Tables 1A–1B and the Bayesian
estimation procedure. The ECB working-paper version remains useful for checking equation
conventions. Component-level `source_check` values retain the edition against which
each equation was actually verified.

The AER estimation reference is stored in
`models/smets-wouters-2007/estimation.yaml` and explained in
`models/smets-wouters-2007/spec/estimation.md`.

## Remaining source boundaries

The standalone primary papers for Calvo pricing, Rotemberg pricing, the Kimball
aggregator and Hansen's indivisible-labour model have not all been independently checked
at equation level. Where a canonical source in this repository does not establish those
results directly, the corresponding component keeps an explicit pending source status.

A successful algebraic or numerical test does not change a source-verification status.
Source fidelity, algebraic validity and numerical behavior are separate checks.
