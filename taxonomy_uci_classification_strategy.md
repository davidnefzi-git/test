# UCI Classification and Intragroup Trade Detection Strategy

**Project:** CIP Deviations, FX Swaps, and Dollar Funding — Entity Taxonomy  
**Dataset:** 2,433 entities identified by LEI  
**Version:** 1.0 — May 2026

---

## Abstract

This document specifies three methodological pillars for extending the entity taxonomy of a dataset covering 2,433 legal entities identified by LEI, assembled in the context of research on covered interest parity (CIP) deviations, FX swap markets, and dollar funding intermediation. Pillar 1 defines a cross-jurisdictional UCI (Ultimate Controller of Interest) entity taxonomy grounded in economic function. Pillar 2 details how to identify G-SIBs, assign an FX dealer flag, and handle dual-role entities that combine market-making with asset management. Pillar 3 provides a replicable logic for flagging intragroup trades — transactions that are not arm's-length and must be excluded from market-pricing analysis. Throughout, the organizing principle is *economic function* rather than legal form, consistent with the fund-side taxonomy already embedded in the `categorie` column. The resulting new variables enable a demand-side / supply-side decomposition of FX swap activity relevant to the literature on CIP arbitrage, dollar funding, and preferred-habitat investing.

---

## 1. Background and Guiding Principles

The dataset covers entities active in FX swap and cross-currency basis swap markets, drawing on the BIS/Fed/ECB literature (39 papers). Each entity is identified by its LEI (Legal Entity Identifier, per GLEIF). The existing `categorie` column classifies *fund-side* entities (ETF, Hedge Fund, Mutual Fund/UCITS, Institutional/AIF, Private Equity/VC, Private Credit, Real Estate, Infrastructure, Other Investment Fund) by economic function, and a `Is_Fund_Like` flag isolates investment vehicle entities from operating entities.

The UCI entity — identified via `UCI_LEI` or `corrected_parent_lei` — represents the *controlling group* standing behind each legal entity. To study how institutional structure shapes FX hedging demand and dollar funding supply, it is necessary to characterize these UCI entities with the same economic-function discipline applied to the fund side.

Three operating principles govern this methodology:

1. **Economic function over legal form.** A société en commandite simple that is the general partner of an infrastructure fund is classified as *Private Equity / Infrastructure Manager*, not as a corporate holding company, because its economic function is GP-level fund management.
2. **Cross-jurisdictional applicability.** Categories must be resolvable using publicly available, internationally standardized sources (FSB, GLEIF, BIS, national supervisory registers) without relying on jurisdiction-specific legal labels.
3. **Research relevance for FX swap / CIP literature.** The taxonomy must separate entities whose FX hedging behavior is *demand-side* and persistent (insurers, pension operators, mutual funds) from entities that are *supply-side* intermediaries (G-SIBs, FX dealers) and from opportunistic arbitrageurs (hedge funds). This distinction maps directly onto the theoretical frameworks in Du, Tepper, and Verdelhan (2017), Bräuer and Hau (2022), Khetan (2023), and Borio, McCauley, and McGuire (2022).

---

## 2. Pillar 1 — UCI Entity Category Taxonomy

### 2.1 Category Definitions

The following ten categories are defined. Each UCI entity receives exactly one primary `uci_category` value.

| # | `uci_category` Value | Economic Function | FX Swap Role |
|---|---|---|---|
| 1 | `GSIB_US` | US Global Systemically Important Bank | FX dealer / market maker; dollar liquidity provider |
| 2 | `GSIB_nonUS` | Non-US GSIB | FX dealer / market maker; synthetic dollar borrower; cross-currency basis driver |
| 3 | `Bank_Other` | Non-GSIB bank or Domestic Systemically Important Bank (D-SIB) with significant international activity | Regional FX intermediation; dollar funding demand |
| 4 | `AssetManager_Global` | Large diversified asset manager (mutual funds, ETFs, multi-asset) | Primary source of inelastic, persistent FX hedging demand; key driver of non-US currency basis |
| 5 | `InsurancePension` | Insurance group or pension fund operator | Preferred-habitat investor; generates persistent long-dated CIP demand; studied in Kloks, Mattauch, and Schertler (2023) and related literature |
| 6 | `Sovereign_Gov` | Sovereign wealth fund, state-owned enterprise, central bank, government agency | Reserve management; official sector FX intervention; dollar swap line counterparty |
| 7 | `Corporate_Industrial` | Non-financial corporate (commodity trader, industrial, technology) | Operational FX hedging; trade finance; limited CIP sensitivity |
| 8 | `HedgeFund_AltManager` | Hedge fund manager or alternative investment manager | Opportunistic CIP arbitrageur when balance-sheet constraints are slack; studied in Du et al. (2017) |
| 9 | `PE_Infra_Manager` | Private equity or infrastructure GP / manager | Long-horizon FX exposure tied to portfolio company cash flows |
| 10 | `Other_Financial` | Residual financial entity (fintech, broker-dealer not covered above, exchange) | Heterogeneous; flag for manual review |

### 2.2 Decision Hierarchy

When a UCI entity could plausibly belong to multiple categories (e.g., a bank that also manages funds), the following strict hierarchy applies. Assign the *first matching* category from the ordered list:

```
DECISION HIERARCHY (top wins)
─────────────────────────────────────────────
1. Is UCI on FSB G-SIB list (current or prior vintage)?
   YES → GSIB_US  (if headquartered in US)
         GSIB_nonUS (otherwise)

2. Is UCI a licensed deposit-taking bank / credit institution
   with material international balance sheet?
   YES → Bank_Other

3. Is UCI primarily an insurance group or pension operator?
   YES → InsurancePension

4. Is UCI a sovereign entity, SWF, or state-owned enterprise?
   YES → Sovereign_Gov

5. Is UCI a non-financial corporate (SIC 0100–5999, 7000–8999
   excluding financial SICs)?
   YES → Corporate_Industrial

6. Is UCI a diversified asset manager (primary revenues from
   fund management, not proprietary trading)?
   YES → AssetManager_Global

7. Is UCI primarily a hedge fund manager or alternative manager?
   YES → HedgeFund_AltManager

8. Is UCI a PE / infrastructure GP?
   YES → PE_Infra_Manager

9. Otherwise:
   → Other_Financial
─────────────────────────────────────────────
```

The hierarchy places banks above asset managers because a banking group that owns an asset management arm is best characterized at the consolidated level by its systemic banking function — the source of its dollar funding relevance. Insurers and pension operators rank above corporates because their FX hedging behavior is structurally driven by liability duration matching, a mechanism studied extensively in the CIP literature (Borio et al., 2022; Liao and Zhang, 2020).

---

## 3. Pillar 2 — G-SIB Identification and Market-Maker Flag

### 3.1 Source and Vintages

The authoritative source for G-SIB identification is the **FSB Annual G-SIB List**, assessed each November using end-of-prior-year data. The 2023 assessment (published November 2023, applicable to 2024 transaction data) is the reference vintage for this dataset.

**Vintage handling.** Because the G-SIB list changes year-on-year (additions, deletions, bucket re-assignments), all flags must be keyed to the FSB assessment year that corresponds to the transaction or reporting date in the dataset. A entity that was a G-SIB in 2019 but removed in 2022 should carry `is_gsib = TRUE` for transactions dated before its removal. Implement this by storing a `gsib_vintage_year` lookup table mapping (LEI, FSB_year) → bucket.

### 3.2 2023 G-SIB Reference List

| Jurisdiction Group | Institution | Notes |
|---|---|---|
| **US G-SIBs** | JPMorgan Chase | Bucket 4 (highest surcharge) |
| | Bank of America | Bucket 3 |
| | Citigroup | Bucket 3 |
| | Goldman Sachs | Bucket 2; dual-role (see §3.4) |
| | Morgan Stanley | Bucket 2; dual-role (see §3.4) |
| | Wells Fargo | Bucket 2 |
| | Bank of New York Mellon | Bucket 1; custody-focused |
| | State Street | Bucket 1; custody/asset management |
| **Non-US G-SIBs** | HSBC | UK; major EM/Asia FX franchise |
| | BNP Paribas | France |
| | Barclays | UK |
| | Deutsche Bank | Germany; dual-role (see §3.4) |
| | Societe Generale | France |
| | Standard Chartered | UK; dominant Asia/Africa/ME franchise |
| | UBS | Switzerland; dual-role post-CS merger |
| | UniCredit | Italy |
| | ING Groep | Netherlands |
| | Santander | Spain |
| | BBVA | Spain |
| | Credit Agricole | France |
| | Groupe BPCE | France |
| | Nordea | Finland |
| | Mitsubishi UFJ Financial Group | Japan |
| | Mizuho Financial Group | Japan |
| | Sumitomo Mitsui Financial Group | Japan |
| | Agricultural Bank of China | China |
| | Bank of China | China; active offshore dollar market |
| | China Construction Bank | China |
| | ICBC | China |

LEIs for the above entities must be resolved against the GLEIF database using the `get_ultimate_parents` endpoint, matching on the group head entity. Where a group reorganization has occurred (e.g., UBS acquisition of Credit Suisse in 2023), the surviving entity's LEI is canonical post-merger.

### 3.3 FX Dealer Flag (`is_fx_dealer`)

`is_fx_dealer = TRUE` is assigned to:

1. All entities with `is_gsib = TRUE` (G-SIBs are, by definition, the core FX dealer network).
2. Non-G-SIB primary dealers in major FX markets identified via the **BIS Triennial Central Bank Survey** participant lists and recognized primary dealer registers of the Federal Reserve, ECB, Bank of England, and Bank of Japan.
3. Select regional banks with documented primary dealer status in Asian or emerging-market currency pairs (e.g., DBS Group, OCBC, and United Overseas Bank in SGD/USD; Kasikornbank and Bangkok Bank in THB/USD). These institutions intermediate FX swaps in markets where G-SIBs have limited local presence, and their omission would bias estimates of the effective FX dealer network in Asia/EM currency pairs studied in, for example, Bräuer and Hau (2022) and Du et al. (2017, §IV).

Non-G-SIB dealers are assigned `gsib_jurisdiction = NA` and `is_gsib = FALSE`, while retaining `is_fx_dealer = TRUE`. This allows the researcher to separately analyze G-SIB vs. non-G-SIB dealer behavior.

### 3.4 Dual-Role Entities

Several G-SIBs operate large, economically material asset management divisions:

| Institution | AM Division | Approximate AUM (2023) |
|---|---|---|
| Goldman Sachs | Goldman Sachs Asset Management | ~$2.8 tn |
| Morgan Stanley | Morgan Stanley Investment Management | ~$1.4 tn |
| Deutsche Bank | DWS Group (majority-owned) | ~$0.9 tn |
| UBS | UBS Asset Management | ~$1.1 tn |
| JPMorgan Chase | J.P. Morgan Asset Management | ~$3.0 tn |
| BNP Paribas | BNP Paribas Asset Management | ~$0.6 tn |

**Classification rule.** The UCI at the *consolidated group level* is classified by its primary banking function (`GSIB_US` or `GSIB_nonUS`). The dual-role nature is captured by a separate boolean flag `gsib_dual_role = TRUE`. This flag alerts researchers that FX swap activity attributed to such a UCI may originate from either the banking book (supply-side, market-making) or the asset management book (demand-side, hedging), and that trade-level disaggregation — where available — is necessary for precise attribution.

When the UCI is the *asset management subsidiary itself* (e.g., DWS Group GmbH with its own LEI, rather than Deutsche Bank AG), the entity is classified as `AssetManager_Global` with `gsib_dual_role = FALSE`, because the controlling UCI at that sub-consolidated level is an asset manager, not a bank.

---

## 4. Pillar 3 — Intragroup Trade Detection

### 4.1 Rationale

Intragroup FX swaps — transactions between two legal entities sharing the same ultimate economic owner — are not arm's-length. Their pricing reflects internal transfer pricing rather than market equilibrium, and their inclusion in CIP deviation analysis introduces measurement error. Identifying and excluding intragroup trades is therefore a prerequisite for cleanly estimating market-implied CIP deviations.

### 4.2 Effective Parent LEI Resolution

For each entity in the dataset, define:

```
effective_parent_lei =
    CASE
        WHEN corrected_parent_lei IS NOT NULL
            THEN corrected_parent_lei          -- researcher correction takes precedence
        WHEN gleif_category = 'BRANCH'
            THEN gleif_head_entity_lei         -- branch always resolved to head entity
        ELSE UCI_LEI                           -- GLEIF-derived ultimate parent
    END
```

The `corrected_parent_lei` field reflects manual or algorithmic corrections applied during dataset construction and takes precedence over the raw GLEIF-derived `UCI_LEI` when available.

### 4.3 Intragroup Flag Logic

For a bilateral transaction between counterparty A and counterparty B:

```
intragroup_flag =
    CASE
        -- Confirmed: both sides resolved via corrected_parent_lei to same entity
        WHEN effective_parent_lei_A = effective_parent_lei_B
         AND corrected_parent_lei_A IS NOT NULL
         AND corrected_parent_lei_B IS NOT NULL
            THEN 'confirmed'

        -- Probable: one side uses corrected_parent_lei, other uses UCI_LEI
        WHEN effective_parent_lei_A = effective_parent_lei_B
         AND (corrected_parent_lei_A IS NOT NULL OR corrected_parent_lei_B IS NOT NULL)
            THEN 'probable'

        -- Uncertain: parent match exists but data quality is low
        WHEN effective_parent_lei_A = effective_parent_lei_B
         AND (correction_cas_A = 'A_NON_RESOLU'
              OR correction_cas_B = 'A_NON_RESOLU'
              OR uci_confidence_A = 'very_low'
              OR uci_confidence_B = 'very_low')
            THEN 'uncertain'

        -- Stable block identity: same economic unit across time
        WHEN stable_block_id_A IS NOT NULL
         AND stable_block_id_A = stable_block_id_B
            THEN 'confirmed'

        ELSE 'no'
    END
```

### 4.4 Edge Cases

**Case 1 — Asymmetric correction availability.** When one counterparty has `corrected_parent_lei` and the other only has `UCI_LEI`, the `effective_parent_lei` values are still compared. A match yields `probable` (not `confirmed`) because the uncorrected side carries GLEIF lookup uncertainty.

**Case 2 — Self-parent entities.** When `UCI_LEI = entity_LEI` (the entity is its own ultimate parent in GLEIF), this typically indicates a standalone entity or an unresolved group. Two entities that are each their own GLEIF ultimate parent are *not* automatically classified as belonging to different groups; if supplementary group membership evidence exists (e.g., same `Stable_Block_ID`, same GLEIF Level 2 registration agent, known corporate relationship), the trade is flagged `uncertain` pending manual review.

**Case 3 — Unresolved entities (`correction_cas = A_NON_RESOLU`).** These entities carry no reliable group identifier. Any transaction involving at least one `A_NON_RESOLU` entity where the raw parent LEIs happen to match is flagged `uncertain`. These observations should be excluded from the primary analysis sample and examined separately as a robustness check.

**Case 4 — Branches.** GLEIF categorizes entities as `BRANCH` when they are a non-incorporated operating unit of a foreign legal entity. Per the GLEIF Level 2 data model, a branch's `HEAD_ENTITY_LEI` is the incorporated parent. For intragroup detection purposes, a transaction between a branch and its own head entity — or between two branches of the same head entity — is `confirmed` intragroup regardless of whether `corrected_parent_lei` is populated.

**Case 5 — Stable_Block_ID.** The `Stable_Block_ID` is a dataset-internal identifier assigned to groups of LEIs determined to represent the same economic unit across time (e.g., before and after a name change, re-registration, or jurisdiction transfer). Two entities sharing a `Stable_Block_ID` are treated as identical for intragroup purposes, yielding a `confirmed` flag. This identifier takes precedence over LEI-based matching.

---

## 5. Implementation — New Dataset Columns

The three pillars map to the following new columns, to be appended to the entity-level master table and joined to the transaction-level dataset via LEI:

| Column | Type | Source Pillar | Description |
|---|---|---|---|
| `uci_category` | string (enum) | Pillar 1 | Economic function of UCI entity; 10-value taxonomy |
| `is_gsib` | boolean | Pillar 2 | TRUE if UCI is on FSB G-SIB list for relevant vintage year |
| `gsib_jurisdiction` | string | Pillar 2 | `US`, `non-US`, or `NA` |
| `is_fx_dealer` | boolean | Pillar 2 | TRUE for G-SIBs and recognized non-G-SIB primary FX dealers |
| `gsib_dual_role` | boolean | Pillar 2 | TRUE if G-SIB UCI has material asset management division |
| `intragroup_flag` | string (enum) | Pillar 3 | `confirmed`, `probable`, `uncertain`, `no` |

The fund-side `categorie` column remains unchanged. Together, `categorie` (fund economic function) and `uci_category` (controlling group economic function) enable a two-dimensional characterization of each legal entity: what type of vehicle it is, and what type of institution controls it. This pairing supports the demand-side / supply-side decomposition central to Bräuer and Hau (2022), who distinguish between hedging demand from institutional investors and supply from dealer banks; to Du, Tepper, and Verdelhan (2017), who examine how G-SIB balance-sheet constraints generate CIP deviations; to Khetan (2023), who studies non-US banks' synthetic dollar borrowing; and to Borio, McCauley, and McGuire (2022), who examine the macrofinancial implications of FX swap-implied dollar funding gaps across institutional sectors.

---

## 6. Data Sources and Auditability

| Source | Use | Access |
|---|---|---|
| **GLEIF Level 1 & 2 data** | LEI-to-entity mapping; branch/head resolution | `https://www.gleif.org/en/lei-data/gleif-golden-copy` (daily snapshot) |
| **FSB G-SIB list** | G-SIB identification; annual vintages | `https://www.fsb.org/work-of-the-fsb/market-and-institutional-resilience/post-2008-financial-crisis-reforms/addressing-sifi/` |
| **BIS Triennial Survey** | Non-G-SIB FX dealer identification | `https://www.bis.org/statistics/rpfx23.htm` |
| **National primary dealer registers** | FRB, ECB, BoE, BoJ | Institution-specific public registers |
| **Dataset-internal fields** | `corrected_parent_lei`, `correction_cas`, `UCI_Confidence`, `Stable_Block_ID` | Project master entity table |

All classification decisions that cannot be resolved algorithmically from the above sources are documented in a companion `manual_overrides.csv` file with columns: `lei`, `field_overridden`, `assigned_value`, `rationale`, `analyst_id`, `date`. This ensures replicability and transparency for peer review.

---

## 7. Versioning and Maintenance

This taxonomy should be reviewed annually following publication of the updated FSB G-SIB list (typically November). The `gsib_vintage_year` lookup table must be extended with each new FSB assessment. When entities merge, demerge, or are acquired, the `Stable_Block_ID` logic and `corrected_parent_lei` fields take precedence over stale GLEIF records. A changelog entry is required in this document for any change to the category definitions or decision hierarchy, so that prior versions of the dataset remain reproducible.
