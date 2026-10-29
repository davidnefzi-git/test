# Primary-source comparison — 29 October 2026

This is an **interim scientific review**, not certification of the full library.
Source PDFs were supplied privately and are not redistributed in this repository.

## Source editions consulted

- Galí, *Monetary Policy, Inflation, and the Business Cycle* (2015), chapters **3** and **6**. The uploaded chapter-3 PDF is misleadingly named "Chapter 4"; the chapter heading clearly reads "Chapter 3 — The Basic New Keynesian Model". These PDFs are image-only.
- Erceg, Henderson and Levin (2000), *Journal of Monetary Economics* 46, 281–313.
- Galí and Monacelli (2005), *Review of Economic Studies* 72, 707–734.
- Smets and Wouters (2007), **ECB Working Paper No. 722**, February 2007, including its model appendix. This supplied PDF is not the final *American Economic Review* pagination. The AER edition requires a separate check before its individual statements are certified.

## Findings established from the supplied originals

| Library location | Primary reference | Finding and action |
| --- | --- | --- |
| `core-nk-classical.euler` | Galí (2015), ch. 3, eq. (23), chapter PDF p. 13 | Confirmed the dynamic IS curve in output-gap form. The source's preference disturbance is not included in this library's composition. Corrected provenance text. |
| `core-nk-classical.natural-rate` | Galí (2015), ch. 3, eq. (24), chapter PDF p. 13 | Confirmed the **negative** technology-shock contribution under stationary AR(1) productivity. Its sign is not a modelling error. |
| `core-nk-classical.natural-output` | Galí (2015), ch. 3, eq. (20), chapter PDF p. 12 | Confirmed natural output's coefficient; corrected second-hand equation-number provenance. |
| `calvo-prices.nkpc` | Galí (2015), ch. 3, eqs. (17), (21)–(22), and ch. 6, eq. (18) | Chapter 3's eq. (22) is the **output-gap** Phillips curve; the library instead uses the intermediate **marginal-cost** form, a valid representation for wage-friction composition. The source description now distinguishes these. |
| `calvo-wages.wage-pc` | Galí (2015), ch. 6, eqs. (15), (19)–(20), chapter PDF pp. 9, 12 | The previous citation to **eq. (22)** was wrong: eq. (22) is the IS curve, not the wage Phillips curve. Corrected the source. |
| `calvo-wages.real-wage-gap` | Galí (2015), ch. 6, eq. (21), chapter PDF p. 12 | Corrected citation against supplied chapter. |
| `docs/theory/wage-setting.md` | Galí (2015), ch. 6, eqs. (19)–(20) | Corrected an impossible self-referential definition of wage-markup gap. With `omega_tilde` meaning **real-wage gap** and `mu_w` the wage-markup deviation, the correct relation is `mu_w = omega_tilde - (sigma + varphi/(1-alpha))*x`. |
| `models/ehl-2000` | EHL (2000), §2, especially production eq. (4) and §3 welfare; Galí (2015), ch. 6 | The library entry describes the **Galí chapter-6 teaching-model specialisation of EHL-style staggered wages and prices**, not the complete EHL (2000) model. The EHL original has an aggregate fixed capital stock, Cobb–Douglas capital/labour production, subsidies and a welfare criterion. Corrected the entry's name, overview and source attribution without changing its stable ID. |
| `core-soe-gm.sigma_a` | Galí and Monacelli (2005), eqs. (27)–(30), pp. 716–717 | The coefficient `sigma_a` is the **inverse** effective intertemporal elasticity, not the elasticity itself. Clarified the parameter description; its formula is unchanged. |
| `models/smets-wouters-2007/spec/model.md` | ECB Working Paper No. 722 (2007), title page and model appendix | Identified the version boundary. This edition cannot by itself validate claims specific to the final AER publication. Added an edition notice. |

## Documentary cleanup undertaken

- Removed obsolete statements that Galí chapter-3 and chapter-6 equation numbers were known only from third-party annotations where the corresponding original chapters had now been checked.
- Removed historical mutation-test anecdotes and one recorded solver runtime from model documentation.
- Kept the numerical test infrastructure, the `golden` targets and economic assumptions intact.
- Kept the legacy `ehl-2000` folder ID to avoid breaking entry references while disclosing that its actual economic specification is Galí chapter 6.

## Boundaries and remaining work

1. The source-edition comparison is **not exhaustive**. The 78 component equations and all parameter defaults have **not** each been audited against the supplied originals. Do not infer primary-source certification from `status: original`.
2. The EHL (2000) entry cannot honestly claim a full model replication unless an additional entry implements the omitted capital, subsidies and welfare analysis; that development is **outside this cleanup task**.
3. The Smets–Wouters final AER version has not been supplied. Equations and coefficients of the ECB working-paper version can be examined, but claims of verbatim final-publication conformity remain pending.
4. The complete Kimball aggregator derivation and the primary Calvo (1983) and Rotemberg (1982) checks require their own sources where not established in the supplied papers.
5. Automated tests and numerical IRFs were **not independently executed** during this connector-based edit. The changes made here to canonical equations and parameter formulas are zero; numeric solutions should be unchanged, but that is **not** a verified non-regression result until tests run.
6. The historical audit `docs/audit-2026-10.md` remains in the repository. It should be treated as a prior-commit record rather than a statement that no source text has been checked as of this branch. Additional cleanup should preserve the permanent scientific content while removing transient execution anecdotes.

## Status

This branch contains a **verified first set of corrections and a partial documentary cleanup**. Its existence does not indicate completion of a full primary-source audit or successful numerical validation.
