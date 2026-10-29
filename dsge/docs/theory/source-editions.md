# Primary reference editions and evidentiary limits

The original publications were consulted from privately supplied PDF copies. The PDFs
are not redistributed by this repository. Equation numbers and page references refer to
the editions identified here, not to third-party replication code.

| Reference | Edition actually available | Primary-source scope |
| --- | --- | --- |
| Galí (2015), ch. 3 | Scanned chapter headed **The Basic New Keynesian Model** (the uploaded filename incorrectly says “Chapter 4”) | Dynamic IS eq. (23), natural-rate eq. (24), natural output eq. (20), pricing eqs. (17), (21)–(22) |
| Galí (2015), ch. 6 | Scanned chapter headed **A Model with Sticky Wages and Prices** | Wage pricing eqs. (15), (19)–(20); wage-gap eq. (21); dynamic IS eq. (22) |
| Erceg, Henderson and Levin (2000) | Journal of Monetary Economics 46, 281–313 | Original fixed-capital and subsidy environment and second-order welfare analysis; **not** the complete composition stored as `ehl-2000` |
| Galí and Monacelli (2005) | Review of Economic Studies 72, 707–734 | Complete-markets small-open-economy equilibrium; eqs. (27), (29)–(31), (35)–(37) |
| Smets and Wouters (2007) | **ECB Working Paper No. 722**, February 2007, including the model appendix | The working paper's linearised relations (1)–(14); **not** a page-for-page verification of the final American Economic Review text |

## Formula and version conventions

**Galí chapter 3.** Eq. (22) is the output-gap Phillips curve, obtained from the
marginal-cost price equation and the flexible-wage supply relation. The reusable
`calvo-prices` component uses the intermediate marginal-cost formulation so that it
can coexist with the Galí chapter-6 wage friction.

**Galí chapter 6.** The wage Phillips curve is eq. (20), following the markup identity
in eq. (19). Eq. (21) governs the real-wage gap. Eq. (22) is the *dynamic IS curve*:
attributing the wage Phillips curve to eq. (22) is incorrect.

**EHL 2000 versus the teaching benchmark.** The entry named `ehl-2000` retains a
legacy identifier, but it is a Galí chapter-6 specialisation with no aggregate fixed
capital input, market-power-offsetting subsidies or second-order welfare criterion.
Those are features of the original article that cannot be inferred from the
teaching-model composition.

**Smets–Wouters working-paper numbering.** In the supplied ECB edition:
resource constraint (1); consumption (2); investment (3); value of installed capital
(4); production (5); capital services (6); utilisation (7); accumulation (8);
marginal cost (9); pricing (10); factor demand (11); wage markup / MRS (12);
wage setting (13); monetary rule (14). Component citations to the supplied PDF should
use this numbering, not numbering inherited from an unverified edition or annotations.

**Theoretical limitation.** The ECB working-paper text does not independently certify
every statement of the published AER article. `source_check: verified_working_paper`
is deliberately different from `verified_primary`.

## Remaining source boundaries

The standalone primary papers Calvo (1983), Rotemberg (1982), Kimball (1995) and Hansen
(1985) were not supplied. Where the provided canonical texts do not give a full proof
of these original contributions, source checking is still pending. The independent
source-check status is recorded at the individual equation rather than being inferred
from whether its algebraic or numerical tests succeed.
