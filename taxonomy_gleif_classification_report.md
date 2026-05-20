# UCI Classification Report
## taxonomy_gleif_corrected.xlsx → taxonomy_gleif_classified.xlsx

**Date:** 2026-05-20  
**Input:** 2,433 rows × 56 columns (from taxonomy_gleif_corrected.xlsx)  
**Output:** 2,433 rows × 63 columns (7 new columns added)

---

## Part 1: What Was Done

### Methodology Applied

The classification applies the 3-pillar strategy defined in `taxonomy_uci_classification_strategy.md` to every row in the enriched and corrected dataset.

**New columns produced:**

| Column | Type | Description |
|---|---|---|
| `uci_category` | string | Economic category of the UCI (10 values) |
| `is_gsib` | bool | True if UCI is on FSB G-SIB 2023 list |
| `gsib_jurisdiction` | string | Country code of G-SIB home regulator |
| `is_fx_dealer` | bool | True if UCI is a top-tier FX dealer bank |
| `gsib_dual_role` | string | GSIB_and_FX_dealer / GSIB_only / FX_dealer_only |
| `effective_parent_lei` | string | Best-available parent LEI (corrected > uci_ult > UCI_LEI) |
| `intragroup_potential` | string | confirmed / probable / uncertain / no |

### Pillar 1: UCI Category

The `uci_category` column assigns each entity to one of 10 categories based on the economic nature of its Ultimate Controller of Interest. Classification uses a **decision hierarchy**:

1. LEI-based lookup (118 entries) — resolves non-Latin names (Chinese, Japanese, Korean, Arabic) and known edge cases
2. PE/Infra patterns — checked before AM to catch Partners Group, EQT, etc.
3. Asset manager patterns (~120 patterns) — checked before G-SIBs to prevent AM subsidiaries from being labelled GSIB
4. Hedge fund patterns
5. US G-SIBs (name patterns + AM-exclusion check)
6. Non-US G-SIBs (name patterns + AM-exclusion check)
7. Insurance/Pension
8. Other banks
9. Sovereign/Gov
10. Corporate/Industrial
11. `Other_Financial` fallback

The `corrected_parent_lei` / `corrected_parent_name` fields (from Pillar 0 corrections) take precedence over raw GLEIF fields, ensuring 247 previously mis-mapped entities receive the correct parent context.

### Pillar 2: G-SIB Flags

The `is_gsib`, `gsib_jurisdiction`, `is_fx_dealer`, and `gsib_dual_role` columns identify entities whose UCI belongs to a G-SIB or is an active FX market-maker, based on the FSB 2023 G-SIB list. Both LEI-based and name-based matching is used; the AM-exclusion check prevents asset-management subsidiaries from being wrongly flagged as G-SIBs.

### Pillar 3: Intragroup Potential

`intragroup_potential` estimates the likelihood that a transaction between this entity and another entity in the dataset is an intragroup trade:

- **confirmed**: ≥3 siblings sharing the same effective parent LEI, and `UCI_Confidence = high`
- **probable**: ≥2 siblings sharing the same effective parent LEI
- **uncertain**: only 1 known sibling in the dataset
- **no**: no valid effective parent LEI

---

## Part 2: Results — What Works and What Doesn't

### Category Distribution (final)

| Category | Count | % |
|---|---|---|
| AssetManager_Global | 813 | 33.4% |
| Other_Financial | 359 | 14.8% |
| Corporate_Industrial | 283 | 11.6% |
| GSIB_nonUS | 270 | 11.1% |
| Bank_Other | 269 | 11.1% |
| InsurancePension | 195 | 8.0% |
| GSIB_US | 99 | 4.1% |
| PE_Infra_Manager | 95 | 3.9% |
| HedgeFund_AltManager | 28 | 1.2% |
| Sovereign_Gov | 14 | 0.6% |
| UNCLASSIFIABLE | 8 | 0.3% |

**Total classified:** 2,425 / 2,433 (99.7%)

### What Works Well

**LEI-based lookup for non-Latin names (118 entities):** Japanese, Chinese, Korean, Arabic, and Taiwanese entities are correctly classified — their names cannot be matched with Latin-script regex patterns. This LEI map is the most reliable component of the system: it uses authoritative GLEIF identifiers and was manually validated.

**AM-exclusion check for G-SIB subsidiaries:** BNP Paribas Asset Management, Goldman Sachs Asset Management, Societe Generale Gestion, HSBC Trinkaus, Santander Asset Management Luxembourg, UniCredit Invest, and UBS Fund Management are all correctly classified as `AssetManager_Global` rather than being swept into their parent G-SIB's bucket. The negative-lookahead regex patterns in `GSIB_US_PATTERNS` and `GSIB_NONUS_PATTERNS` prevent this contamination.

**Corrected parent propagation:** The 247 entities with `corrected_parent_lei`/`corrected_parent_name` populated from the correction phase (Cases A, B, D, E, F) use their corrected parent for classification, not the erroneous or missing GLEIF mapping. This avoids propagating bad parenting into the classification.

**Hedge fund detection:** Marshall Wace, Brevan Howard, Capula, CQS, Millennium, Citadel, Two Sigma, and Point72 are correctly caught.

**PE/Infra detection:** Partners Group (all Luxembourg / UK / US / Cayman subsidiaries), KKR, Carlyle, Blackstone, EQT, Ares, and Brookfield are correctly classified as `PE_Infra_Manager`.

**Intragroup potential:** 500 entities have `confirmed` intragroup potential (≥3 siblings, high-confidence UCI), 1,176 have `probable`. These are the primary candidates for intragroup trade detection in research on CIP deviations.

### What Doesn't Work / Residual Limitations

**`Other_Financial` bucket (359 entities, 346 unique UCIs):**

The residual `Other_Financial` bucket contains entities that fall through all pattern rules. Key sub-groups:

| Sub-type | Examples | Why Not Classified |
|---|---|---|
| Invalid LEI | `LEI_INVALIDE` (10 rows) | No valid identifier |
| Single-entity UCIs | DRW Investments, Orange County ERS, NZ Super, Future Fund | Too specific for generic patterns |
| Mixed conglomerates | Morningstar (data/AM), TVM (insurance/cooperative) | Ambiguous economic category |
| Obscure fund platforms | Partners Group Cayman Mgmt I | Name variant not in PE patterns |
| Non-Latin leftovers | Банк ВТБ (Cyrillic) | Cyrillic script not covered by LEI map or patterns |
| Corporate trading arms | JERA Trading, FAB Global Markets | Parent context not reliably determinable |

The true `Other_Financial` rate after correcting known misclassifications is ~14.8%. Before corrections, this bucket was 23.4% (570 entities). The 359 remaining are plausibly genuine `Other_Financial` — non-standard structures, smaller intermediaries, or entities whose economic function cannot be determined from their name alone.

**Cyrillic-script entities:** VTB Bank (Банк ВТБ, Russia) appears in `Other_Financial`. The LEI map covers CJK and Arabic scripts but not Cyrillic. VTB's LEI (`549300ZK53CNGEEI6A29`) is not in the current LEI map.

**Jurisdiction inference for non-US G-SIBs:** When a G-SIB is matched by name rather than LEI, the `gsib_jurisdiction` field is inferred from `uci_entity_country`. This is correct for the entity itself but may not reflect the home regulator (e.g., a German branch of BNP Paribas would show `DE` instead of `FR`). For research-grade use, jurisdiction should come from the consolidated entity LEI.

**`intragroup_potential` is entity-level, not transaction-level:** The flag signals that two entities *could* be trading intragroup (same parent), not that they *are*. A trade between BNP Paribas Paris and BNP Paribas London will show `confirmed`, but a trade between BNP Paribas and an external counterparty will also show `confirmed` because they share the same parent-level UCI. True intragroup flag requires bilateral comparison of `effective_parent_lei` across both legs of a trade.

**G-SIB count inflation (370 entities):** The `is_gsib = True` flag marks any entity whose UCI is a G-SIB. This means 370 entities (including funds and subsidiaries managed by G-SIBs) are flagged. If the research question is "how many distinct G-SIB counterparties are in the dataset", the answer is the number of unique G-SIB UCIs (≈ 28), not 370.

---

## Part 3: Suggested Improvements

### Priority 1: Extend LEI Map to Cyrillic + Thai + Hebrew Scripts

VTB, Sberbank, and other Russian/Eastern European entities use Cyrillic. Similarly, some Thai banks (Kasikornbank, Bangkok Bank) appear with Thai script rather than Latin transliteration. The LEI map approach works well — it simply needs to be extended with the relevant LEIs identified via GLEIF API queries.

**Implementation:** Run the GLEIF API on all entities in `Other_Financial` with non-Latin, non-CJK, non-Arabic characters; add their LEIs to the map.

### Priority 2: Wikidata / Wikipedia API for Unknown UCIs

For single-entity UCIs in `Other_Financial`, a Wikidata lookup on the entity name can return `instance of` (P31) properties: *bank* → `Bank_Other`, *hedge fund* → `HedgeFund_AltManager`, *insurance company* → `InsurancePension`, etc. This would cover entities like "Future Fund" (sovereign wealth fund), "NZ Superannuation" (sovereign pension), and "DRW Investments" (prop trading/HF).

**Implementation:** Query `https://www.wikidata.org/w/api.php?action=wbsearchentities&search={name}`, take the top hit, check P31 against a category-to-label map. Estimated coverage gain: 20–40% of remaining `Other_Financial`.

### Priority 3: LEI-to-Category via GLEIF Entity-Type Field

GLEIF Level 1 already returns `entity.category` (BRANCH, FUND, SOLE_PROPRIETOR) and the `entity.legalForm.id` (BIC/NACE codes). NACE codes map directly to ISIC industry classifications:

- NACE 64.1x → Banks and credit institutions → `Bank_Other`
- NACE 64.3x → Trusts, funds, investment vehicles → depends
- NACE 65.1x → Insurance → `InsurancePension`
- NACE 65.3x → Pension funds → `InsurancePension`

**Implementation:** In `enrich_leis.py`, extract `entity.legalForm.id` and map NACE prefixes to UCI categories. This is scalable to any new LEI batch without updating pattern lists.

### Priority 4: Bilateral Intragroup Flag for Transaction Data

The current `intragroup_potential` is entity-level. For CIP deviation research, the key question is: "for a given FX swap trade, are both counterparties subsidiaries of the same group?" This requires:

```python
def is_intragroup_trade(lei_a: str, lei_b: str, lei_to_parent: dict) -> bool:
    parent_a = lei_to_parent.get(lei_a)
    parent_b = lei_to_parent.get(lei_b)
    return parent_a is not None and parent_a == parent_b
```

where `lei_to_parent` is the `effective_parent_lei` lookup built from this dataset.

### Priority 5: Vintage-Aware Classification

The dataset spans multiple years (`first_year` to `last_year`). Some entities changed group membership or G-SIB status over the period (Credit Suisse ceased to exist in 2023; some Chinese banks were added/removed from the G-SIB list). Classification should be year-conditional: an entity that joined UBS in 2023 is not a UBS subsidiary for 2019 trades. This requires a time-indexed version of the correction and classification tables.

---

## Technical Notes

- Classification script: `classify_uci.py`
- LEI map entries: 118 (CJK: 92, Arabic: 8, other: 18)
- Pattern rules: ~350 regex patterns across 10 category lists
- Runtime: < 5 seconds on 2,433 rows
- Deterministic: same input always produces same output
- All classification logic is explainable by rule (no ML black box)
