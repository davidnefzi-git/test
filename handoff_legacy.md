# Handoff Legacy — Inside Synthetic Dollar Liquidity and the Microstructure of FX Swap Markets

**Date de rédaction :** 2026-05-24  
**Branche active :** `claude/fx-swap-research-phase-NpiZS`  
**Phases complétées :** 1 (Discovery), 2 (Strategy & Theory), 3 (Execution), 4 (Presentation)  
**Statut global :** Pipeline académique opérationnel sur données synthétiques. Données réelles à intégrer.

---

## 1. Stratégie empirique et logique métier

### 1.1 Question de recherche

Quels déterminants structurels fixent le premium sur la liquidité dollar synthétique dans les marchés de FX swaps ? Le papier fait la distinction entre *inside* (FX swaps, repo offshore, eurodollars) et *outside* (réserves Fed, Treasuries, FDIC) dollar liquidity. En période de stress, la liquidité *inside* se dégrade — le papier en modélise et mesure le mécanisme.

### 1.2 Contribution principale

Avantage de données unique : les **deux contreparties** de chaque transaction FX swap sont observées (reporting réglementaire bilatéral). Cela permet de cartographier simultanément la demande et l'offre de dollars synthétiques par secteur, juridiction et tenor — ce que les papiers existants (Khetan 2025, Du-Tepper-Verdelhan, Rime-Schrimpf-Syrstad) ne peuvent pas faire.

### 1.3 Modèle théorique (Phases 1–2)

Cadre search-and-matching avec agrégateur CES de qualité. Trois objets centraux :

| Objet théorique | Proxy empirique | Nom variable |
|-----------------|-----------------|--------------|
| `U_t` — demande nette de dollars des banques étrangères | `Q_{FB,m,t}` | `U_t` |
| `B_t` — capacité des intermédiaires (dealers, FBOs) | Composite dealer + FBO | `B_cap` |
| `μ_t` — spread de funding | `PriceUSD_{m,t} = -TIB_{m,t}` | `mu_t` |
| `q_t` — qualité du marché | Taker ratio, dispersion des prix | `q_t` |
| `θ_t = U_t / B_t` — tension du marché | Ratio construit | `theta_t` |
| `𝓑 = Σ β_s` — pente agrégée de la net-demand | Paramètre demand system | `B_agg` |

**Collision de notation critique (résolue) :** `B_t` (capacité) ≠ `𝓑` (pente agrégée). Dans le `.tex`, utiliser `\mathcal{B}` pour la pente. Dans le code R, utiliser `B_cap` (capacité) et `B_agg` (pente). Ne jamais utiliser un `B` nu.

### 1.4 Quatre propositions testables

| Proposition | Résultat | Statut de testabilité |
|-------------|----------|----------------------|
| **P1 :** `∂μ*/∂U_t > 0` — choc demande → premium ↑ | Testable via IV shift-share | ✅ Jaune (LATE + atténuation FB-only) |
| **P2 :** `∂μ*/∂B_t < 0` — contrainte capacité → amplification | Testable via hétérogénéité (DealerConstraint) | ✅ Jaune (effet hétérogénéité, pas causal B_t) |
| **P3 :** Convexité du price impact en θ_t | **Théorique uniquement** — pas de test empirique direct | 🔴 Non testable sans spécification de seuil |
| **P4 :** Quarter-end → B_t ↓ → μ_t ↑ | Testable en réduit (QuarterEnd interaction) | ✅ Jaune (attribution supply vs demand non séparée) |

**Décision éditoriale ferme (Proposition 3) :** aucun test empirique de la convexité. Aucune spécification de seuil (Hansen 1999). Le résultat est présenté comme théorique.

### 1.5 Stratégie d'identification : Shift-share IV

```
Premier étage :
  Q_{FB,m,t} = α_m + τ_t + π·Z^MMF_{m,t} + γ·CDSAgg_{m,t} + u_{m,t}

Deuxième étage :
  ΔPriceUSD_{m,t} = α_m + τ_t + β·Q̂_{FB,m,t} + γ·CDSAgg_{m,t} + ε_{m,t}

Instrument :
  Z^MMF_{m,t} = Exposure^MMF_{m,t-1} × MMFOutflow_t
  Exposure^MMF_{m,t-1} = Σ_i w_{i,m}^pre × MMFShare_{i,m-1}
  w_{i,m}^pre = GrossVolume_{i,m,[t-12m,t-1m]} / Σ_j GrossVolume_{j,m,...}
```

- **Inférence baseline :** AKM (Adão-Kolesár-Morales 2019) shift-share SEs
- **Inférence secondaire :** Two-way clustered SE (marché × semaine) + wild cluster bootstrap (~36 marchés)
- **Prérequis validité :** balance tests sur les banques dominant-share AVANT toute estimation

### 1.6 Positionnement du demand system

Le demand system est l'**extension structurelle (Partie 4/Section 6)**, pas un résultat principal co-égal. Les résultats principaux sont les Parties 2–3 (microstructure descriptive + IV simple). Le demand system fournit l'interprétation structurelle : `β_IV ≈ -γ_{FB}/𝓑`, et les contrefactuels (CF1–CF4).

---

## 2. Structure des données

### 2.1 Données de transaction brutes (source DTCC/réglementaire)

Chaque ligne = une transaction FX swap individuelle. Champs pertinents confirmés dans les données brutes :

| Champ brut | Rôle | Disponibilité |
|-----------|------|--------------|
| `counterparty_1`, `counterparty_2` | LEI des deux contreparties | ✅ |
| `direction_of_leg_1/2` | TAKE / MAKE (taker = demandeur de USD) | ✅ |
| `notional_amount_of_contract_or_leg_1/2` | Montants notionnels | ✅ |
| `notional_currency_of_contract_or_leg_1/2` | Devises | ✅ |
| `exchange_rate` | **Taux forward** de la jambe far (≠ taux spot) | ✅ |
| `effective_date` / `expiration_date` | Dates near/far leg | ✅ |
| `booking_location` | Pays de réservation de la contrepartie déclarante | ✅ (proxy pays cpty1) |
| `trader_location` | Localisation du trader | ✅ |
| `trading_capacity_of_specified_person` | PRIN / AGNT (proxy dealer) | ✅ |
| `contract_type` | SWAP / FORW | ✅ |

**Important :** `exchange_rate` = taux forward (jambe far), pas le taux spot. Pour construire le TIB (variable dépendante μ_t), il faut également le taux spot contemporain — source externe obligatoire (Bloomberg/BCE).

### 2.2 Données agrégées (sortie du pipeline Python)

Fichier : `daily_flows_by_sector_tenor_resolved_YYYYMMDD_YYYYMMDD.csv`

| Colonne | Type | Description |
|---------|------|-------------|
| `eff_dt` | date | Date de transaction |
| `instrument` | str | SWAP / FORW / FX_LINEAR |
| `pair` | str | Ex: SGD/USD, EUR/USD |
| `tenor_bucket` | str | overnight, 1D-7D, 7D-1M, 1M-3M, 3M-6M, >6M |
| `categorie_cpty1` | str | Secteur contrepartie A (Bank, Insurer...) |
| `categorie_cpty2` | str | Secteur contrepartie B |
| `net_flow_M` | float | Flux net USD en millions (positif = obtient USD) |
| `gross_volume_M` | float | Volume brut USD en millions |
| `nb_transactions` | int | Nombre de transactions dans la cellule |

**Dimensions manquantes dans l'agrégat actuel** (à ajouter — voir Section 5) :
- `booking_location_cpty1` — pays proxy de la contrepartie déclarante
- `taker_ratio` — proportion de transactions TAKE (proxy q_t)
- `vwap_fx_forward` — taux forward moyen pondéré (pour TIB)
- `prin_ratio` — proportion PRIN (proxy dealer capacity)
- Table séparée par LEI pour calculer `DomShare_{i,m}`

### 2.3 Taxonomie des contreparties

Fichier : `common_taxonomy.xlsx`

| Colonne | Description | Statut |
|---------|-------------|--------|
| `LEI` | Identifiant legal entity | ✅ présent |
| `categorie` | Secteur (Bank, Insurer, ...) | ✅ présent |
| `country` | Pays de l'entité | ❌ **à ajouter** via GLEIF |

**Action requise :** enrichir via bulk download GLEIF (`Entity.LegalAddress.Country`). Jointure sur `LEI`.

### 2.4 Cellule empirique cible (design v8)

```
c = secteur × pays × paire_devise × tenor × date
```

La cellule actuelle (agrégat Python) est `secteur × paire × tenor × date` — il manque le **pays**.

### 2.5 Données de prix (TIB / PriceUSD) — non encore dans le pipeline

`PriceUSD_{m,t} = -TIB_{m,t}` doit être construit à partir de :
- **Taux forward** : `exchange_rate` dans les données brutes (disponible) = F_t
- **Taux spot** : source externe Bloomberg/BCE = S_t
- `TIB ≈ (F_t - S_t)/S_t × 360/tenor_days - (r_USD - r_nonUSD)`

Option alternative : utiliser Bloomberg CCBS directement comme validation externe.

---

## 3. Code : points d'entrée et structure

### 3.1 Pipeline Python (extraction et déduplication)

**Fichier principal :** (non versité dans ce repo — à versionner séparément)

Langage : Python/PySpark. Entrée : table Spark `cln_zone.tcln_otc_cde_dtcc_tsr_fx`. Exécution via notebook Databricks ou spark-submit.

**Points d'entrée :**

| Fonction | Description |
|----------|-------------|
| `process_day(date_str)` | Traitement d'une journée : filtre, déduplication, agrégation |
| Boucle principale (Section 5) | Itère sur `[start_date, end_date]`, écrit les CSV de façon incrémentale |

**Paramètres clés :**
```python
start_date = "2024-10-01"
end_date   = "2026-04-30"
SAVE_FULL_AUDIT = False   # True = audit complet (lourd)
OVERWRITE_OUTPUTS = True
```

**Sorties :**
- `daily_flows_by_sector_tenor_resolved_*.csv` — agrégat principal (input du pipeline R)
- `audit_unresolved_conflicts_*.csv` — transactions non déduplicables
- `audit_resolution_status_summary_*.csv` — statistiques de résolution
- `daily_processing_log_*.csv` — journal quotidien

### 3.2 Pipeline R (estimation)

**Entrée unique :** `Rscript scripts/R/00_master.R` (depuis la racine du projet)

```
scripts/R/
  00_master.R              # Point d'entrée unique — source 01–06 dans l'ordre
  01_simulate_data.R       # Génération données synthétiques (→ remplacer par vraies données)
  02_balance_tests.R       # Balance tests (prérequis IV) — à exécuter EN PREMIER
  03_descriptives.R        # Statistiques descriptives + figures
  04_iv_estimation.R       # IV principal + AKM SE + wild bootstrap + robustesse
  05_demand_system.R       # Extension structurelle (Partie 4 du papier)
  06_quality_checks.R      # Validation market clearing, TIB vs Bloomberg, filtres
  functions/helpers.R      # Fonctions partagées (stars, fmt_coef_se, get_iv_beta, etc.)
```

**Outputs attendus :**

| Script | Tables (`paper/tables/`) | Figures (`paper/figures/`) |
|--------|--------------------------|---------------------------|
| 02 | `balance_tests.tex` | `balance_tests_share_distribution.pdf` |
| 03 | `summary_stats.tex` | `intermediation_matrix.pdf`, `theta_mu_timeseries.pdf`, `q_distribution.pdf` |
| 04 | `iv_first_stage.tex`, `iv_second_stage.tex`, `iv_interactions.tex`, `pretrend_diagnostic.tex`, `iv_bootstrap.tex` | — |
| 05 | `demand_system.tex` | — |
| 06 | `quality_checks.tex` | `tib_ccbs_validation.pdf` |

**Conventions de nommage obligatoires (ne pas modifier) :**
- `B_cap` = capacité des intermédiaires (théorie : B_t)
- `B_agg` = pente agrégée du demand system (théorie : 𝓑 = Σβ_s)
- `SignedUSDFlow > 0` = l'entité obtient des USD
- `U_t`, `mu_t`, `q_t`, `theta_t` = objets théoriques dans le code

### 3.3 Données synthétiques (état actuel)

`01_simulate_data.R` génère un panel synthétique (~182 000 lignes cellules, ~5.5M lignes banques) avec des propriétés distributionnelles cohérentes avec les données réelles estimées (pic de μ_t de 15 bps en mars 2020, élévation de θ_t aux quarter-ends, dégradation de q_t en stress).

**Pour substituer les vraies données :** remplacer le bloc de simulation dans `01_simulate_data.R` par une lecture des fichiers CSV issus du pipeline Python. Tous les scripts downstream lisent depuis `Output/fx_swap/*.rds` via `here::here()` — aucun autre changement n'est nécessaire.

### 3.4 Paper LaTeX

```
paper/
  main.tex                          # Shell à compléter (sections via \input{})
  sections/
    theoretical_framework.tex       # Section 3 — modèle (Propositions 1–4, Theorem 1)
    empirical_results.tex           # Sections 4–6 — données, IV, demand system
    introduction.tex                # Section 1 — placeholder
    model.tex                       # Section 2 — placeholder
  theory/sections/
    inside-synthetic-dollar-v2.tex  # Framework théorique formel complet (source de vérité)
  talks/
    fx_swap_seminar_talk.tex        # Beamer 34 frames — séminaire 60 min
  design/
    empirical-roadmap-v8.md         # Design empirique de référence
```

**Compilation :**
```bash
cd paper && latexmk main.tex
```
(XeLaTeX + biber via `paper/latexmkrc`)

---

## 4. Limites et problèmes identifiés

### 4.1 Limites critiques — données (bloquantes pour les vrais résultats)

| Problème | Impact | Solution |
|----------|--------|----------|
| **Toutes les estimations R tournent sur données synthétiques** | Les coefficients (β ≈ 2.8 bps, F = 38.4) sont illustratifs, non empiriques | Substituer les vraies données dans `01_simulate_data.R` |
| **Variable dépendante μ_t absente du pipeline Python** | Impossible d'estimer l'IV sans PriceUSD = -TIB | Construire TIB = (F_t - S_t)/S_t × 360/k - OIS_spread. Requires: spot rate (Bloomberg/BCE) + taux OIS |
| **Pays des contreparties absent de la taxonomie** | Impossible d'identifier FBO vs banques domestiques ; cellule empirique incomplète | Enrichir `common_taxonomy.xlsx` avec GLEIF country |
| **Table par LEI pour DomShare_{i,m} non produite** | Premier étage de l'IV impossible sans poids de parts de marché | Ajouter agrégation par LEI dans le pipeline Python (Section 4.9) |
| **Taker ratio absent de l'agrégat** | Proxy q_t indisponible | Ajouter `nb_taker`, `gross_taker_volume_M`, `taker_ratio` dans le pipeline Python |

### 4.2 Limites du pipeline Python

| Problème | Localisation | Sévérité |
|----------|-------------|----------|
| `booking_location` non extrait | Section 4.1 | Haute — seul proxy pays cpty1 disponible |
| `trading_capacity_of_specified_person` non extrait | Section 4.1 | Haute — proxy PRIN/AGNT dealer |
| `exchange_rate` (F_t) non conservé dans l'agrégat | Section 4.9 | Haute — nécessaire pour TIB |
| Pas de table agrégée par LEI | Section 4.9 | Haute — prérequis DomShare_{i,m} |
| Performance : `toPandas()` jour par jour sur Spark | Boucle Section 5 | Moyenne — acceptable pour la période considérée |
| `AMOUNT_CANDIDATE_BIN_USD = 10_000` peut créer des faux positifs | Section 4.4 | Moyenne — vérifier sur données réelles |

### 4.3 Limites du pipeline R (données synthétiques)

| Problème | Localisation | Sévérité |
|----------|-------------|----------|
| AKM SE implémenté manuellement (approx. HC, pas strictement Adão-Kolesár-Morales) | `04_iv_estimation.R` lignes ~369–420 | Haute — utiliser le package `ShiftShareSE` sur vraies données |
| Wild cluster bootstrap regroupe sur `cell_id` (36 marchés synthétiques) — petit nombre de clusters | `04_iv_estimation.R` lignes ~424–493 | Moyenne — acceptable sur vraies données si ~36 marchés |
| Demand system : `B_agg = Σ β_s` obtenu via OLS + IV séparés, pas GMM joint | `05_demand_system.R` | Haute — utiliser GMM en vraies données pour l'inférence jointe |
| F-stat = 38.4 est illustratif (DGP construit pour produire un premier étage fort) | `04_iv_estimation.R` | Cosmétique — sera remplacé par la vraie valeur |

### 4.4 Limites du paper LaTeX

| Problème | Fichier | Sévérité |
|----------|---------|----------|
| `paper/main.tex` est un shell vide — sections non assemblées | `main.tex` | Haute — à connecter |
| Tous les chiffres clés (β = 2.8, F = 38.4) sont des placeholders synthétiques | `empirical_results.tex`, `talks/fx_swap_seminar_talk.tex` | Haute — à mettre à jour avec vraies données |
| Introduction et section Discussion non rédigées | `sections/introduction.tex`, `sections/model.tex` | Haute |
| Figures PDF inexistantes (`paper/figures/*.pdf`) — les scripts R ne tournent pas sans vraies données | `paper/figures/` | Haute |

### 4.5 Décisions de modèle en suspens (signalées dans le strategy memo)

| Décision | Contexte | Recommandation memo |
|----------|----------|---------------------|
| α_t (préférence outside liquidity) non identifiable | Paramètre libre dans P1–P6 | Restreindre paramétriquement : α_t = α_0 + α_1·VIX_t |
| η (efficacité matching) non identifiable | Pas dans les propositions | Paramètre de calibration uniquement |
| γ (élasticité matching) partiellement identifiable | Pas dans les propositions | Calibrer à 0.5, sensibilité {0.3, 0.5, 0.7} |
| φ (capacité hedge funds) endogène à μ_t | P6 structurel non identifiable | Résultat descriptif uniquement |
| Multiplicité d'équilibres | Non formalisée | Extension théorique haute valeur — formaliser en annexe |
| P4 (quarter-end) comme corollaire de P2 | Proposition trop faible standalone | Dégrader en corollaire illustratif |

---

## 5. Modifications du pipeline Python à implémenter

**Version v9 (2026-05-24) :** la stratégie empirique v9 requiert cinq tables. Les Sections 5.1–5.6 couvrent les modifications v8 (T1 + T5). Les Sections 5.7–5.10 sont **nouvelles en v9** (T2 = matrice bilatérale, T3 = transactions légères, T4 = positions ouvertes).

### Récapitulatif des cinq tables

| Table | Niveau | Produite par | Taille estimée | Nécessité |
|-------|--------|-------------|----------------|-----------|
| **T1 — Agrégat cellule enrichi** | Cellule-jour | Boucle Python (modifiée 5.1–5.6) | ~500K lignes/an | ✅ v8 + VWAP |
| **T2 — Matrice bilatérale directionnelle** | Secteur×Secteur×cellule-jour | Boucle Python (Section 5.7) | ~2M lignes/an | ✅ v9 critique |
| **T3 — Transactions légères avec exp_dt** | Transaction individuelle | Boucle Python (Section 5.8) | ~50–200M lignes/an | ✅ CrossQE + TIB |
| **T4 — Positions ouvertes dealer×date** | Dealer×jour | Job Spark séparé (Section 5.9) | ~10K lignes/an | ✅ UnmatchedLoad |
| **T5 — Flux par LEI** | Banque×cellule-jour | Boucle Python (Section 5.5) | ~5M lignes/an | ✅ DomShare |

**Réponse directe : faut-il travailler transaction par transaction ?**
- **Oui pour :** CrossQE (exp_dt exact → T3 obligatoire) ; TIB transactionnel ; UnmatchedLoad (T4, générée depuis T3)
- **Non pour :** Q^FB, DealerSupply, taker_ratio (T1 suffit) ; Flow_{s→r} (T2 suffit) ; DomShare (T5 suffit)

**Point critique :** stocker T3 en **Parquet partitionné par eff_dt** — avec 50–200M transactions/an, le CSV est ingérable.

---

Voici les modifications concrètes à apporter au script Python existant pour combler les lacunes de données :

### 5.1 Section 2 — Taxonomie : ajouter le pays

```python
pdf_tax = pd.read_excel(
    "common_taxonomy.xlsx",
    usecols=["LEI", "categorie", "country"]  # ajouter country après enrichissement GLEIF
)
# Joindre les pays cpty1 et cpty2
df_tax_1 = df_tax.select(F.col("LEI").alias("LEI_1"),
                          F.col("categorie").alias("categorie_1"),
                          F.col("country").alias("country_1"))  # NOUVEAU
df_tax_2 = df_tax.select(F.col("LEI").alias("LEI_2"),
                          F.col("categorie").alias("categorie_2"),
                          F.col("country").alias("country_2"))  # NOUVEAU
```

### 5.2 Section 4.1 — Extraire booking_location et trading_capacity

Ajouter dans le bloc `df_txn_clean` :
```python
.withColumn("booking_location",
    F.when(has_col(df_txn_day, "booking_location"),
           clean_text_col("booking_location"))
    .otherwise(F.lit(None).cast("string")))
.withColumn("trading_capacity",
    F.when(has_col(df_txn_day, "trading_capacity_of_specified_person"),
           clean_text_col("trading_capacity_of_specified_person"))
    .otherwise(F.lit(None).cast("string")))
```

### 5.3 Section 4.2 — Conserver le taux forward

Après le bloc `df_usd` existant :
```python
df_usd = df_usd.withColumn("fx_forward_rate", F.col("fx_canonical"))
# NOTE : fx_canonical = nonusd_notional / usd_notional = taux forward jambe far
# Ce n'est PAS le taux spot. TIB nécessite une jointure externe sur S_t.
```

### 5.4 Section 4.9 — Agrégation principale enrichie

Ajouter dans `.agg()` :
```python
F.sum(F.when(F.col("sign_cp_low_final") > 0, F.lit(1))
       .otherwise(F.lit(0))).alias("nb_taker"),
F.sum(F.when(F.col("sign_cp_low_final") > 0, F.col("usd_notional_M_final"))
       .otherwise(F.lit(0.0))).alias("gross_taker_volume_M"),
F.sum(F.col("fx_forward_rate") * F.col("usd_notional_M_final")).alias("sum_fx_fwd_x_vol"),
F.first("booking_location", ignorenulls=True).alias("booking_location_cpty1"),
F.sum(F.when(F.col("trading_capacity") == "PRIN", F.lit(1))
       .otherwise(F.lit(0))).alias("nb_prin"),
```

Puis après `.withColumn("eff_dt", ...)` :
```python
.withColumn("taker_ratio", F.col("nb_taker") / F.col("nb_transactions"))
.withColumn("vwap_fx_forward", F.col("sum_fx_fwd_x_vol") / F.col("gross_volume_M"))
.withColumn("prin_ratio", F.col("nb_prin") / F.col("nb_transactions"))
.drop("sum_fx_fwd_x_vol")
```

### 5.5 Section 4.9 — Nouvelle agrégation par LEI (prérequis DomShare)

Ajouter juste après `df_agg` :
```python
df_agg_by_lei = (
    df_usd_resolved
    .groupBy(
        F.lit(date_str).alias("eff_dt"),
        F.col("pair_final").alias("pair"),
        F.col("tenor_bucket_final").alias("tenor_bucket"),
        F.col("cp_low_final").alias("lei"),
        F.col("country_1").alias("country")  # si enrichi
    )
    .agg(
        F.sum(F.abs("usd_notional_M_final")).alias("gross_volume_M"),
        F.count("*").alias("nb_transactions"),
        F.first("booking_location", ignorenulls=True).alias("booking_location"),
        F.first("trading_capacity", ignorenulls=True).alias("trading_capacity"),
        F.first("categorie_1", ignorenulls=True).alias("categorie"),
    )
)
# Écriture incrémentale dans la boucle :
# OUT_BY_LEI = f"daily_flows_by_lei_{PERIOD_SUFFIX}.csv"
# append_csv(df_agg_by_lei.toPandas(), OUT_BY_LEI)
```

### 5.6 Colonnes finales de `OUT_FINAL` (T1)



```python
pdf_day = pdf_day[[
    "eff_dt", "instrument", "pair", "tenor_bucket",
    "booking_location_cpty1",   # NOUVEAU
    "categorie_cpty1", "categorie_cpty2",
    "net_flow_M", "gross_volume_M", "nb_transactions",
    "nb_taker", "gross_taker_volume_M", "taker_ratio",   # NOUVEAU
    "vwap_fx_forward",     # NOUVEAU — F_t pour TIB
    "nb_prin", "prin_ratio",   # NOUVEAU
]]
```

---

### 5.7 Table 2 — Matrice bilatérale directionnelle (NOUVELLE v9)

**Niveau :** `secteur_fournisseur × secteur_demandeur × paire × tenor_bucket × date`  
**Objet :** `Flow_{s→r,m,t}` pour la décomposition bilatérale (Sections 8.2 et 13.3 du roadmap v9)

Cette table requiert de ne **pas** symétriser la cellule `(cat_A, cat_B)`. Il faut conserver la direction : qui fournit les USD, qui les obtient.

```python
# Ajouter dans process_day(), après le bloc df_usd_resolved :
df_bilateral = (
    df_usd_resolved
    .withColumn(
        "sector_provider",
        F.when(F.col("sign_cp_low_final") < 0, F.col("categorie_1"))
         .otherwise(F.col("categorie_2"))
    )
    .withColumn(
        "sector_demander",
        F.when(F.col("sign_cp_low_final") > 0, F.col("categorie_1"))
         .otherwise(F.col("categorie_2"))
    )
    .withColumn(
        "country_provider",
        F.when(F.col("sign_cp_low_final") < 0, F.col("country_1"))
         .otherwise(F.col("country_2"))
    )
    .withColumn(
        "country_demander",
        F.when(F.col("sign_cp_low_final") > 0, F.col("country_1"))
         .otherwise(F.col("country_2"))
    )
    .groupBy(
        F.lit(date_str).alias("eff_dt"),
        "pair_final", "tenor_bucket_final",
        "sector_provider", "sector_demander",
        "country_provider", "country_demander"
    )
    .agg(
        F.sum(F.abs("usd_notional_M_final")).alias("flow_M"),
        F.count("*").alias("nb_transactions"),
        F.sum(F.col("fx_forward_rate") * F.abs("usd_notional_M_final")).alias("sum_fwd_x_vol"),
        F.sum(F.when(F.col("sign_cp_low_final") > 0, F.lit(1))
               .otherwise(F.lit(0))).alias("nb_taker")
    )
    .withColumn("vwap_forward", F.col("sum_fwd_x_vol") / F.col("flow_M"))
    .withColumn("taker_ratio",  F.col("nb_taker") / F.col("nb_transactions"))
    .drop("sum_fwd_x_vol")
)
# OUT_BILATERAL = f"daily_flows_bilateral_{PERIOD_SUFFIX}.csv"
# append_csv(df_bilateral.toPandas(), OUT_BILATERAL)
```

**Lecture R :** cette table alimente directement `bilateral_flows.rds` dans `07_bilateral_decomposition.R`.

---

### 5.8 Table 3 — Transactions légères avec dates exactes (NOUVELLE v9)

**Niveau :** transaction individuelle (après déduplication)  
**Objet :** `CrossQE_ℓ = 1{near_ℓ ≤ QE_q < far_ℓ}` et construction de `Z^{S,QE}`

**Point critique :** `exp_dt` exact est perdu dans l'agrégat journalier. Cette table est **indispensable** pour l'instrument d'offre.

```python
# Ajouter dans process_day(), extraire depuis df_usd_resolved :
df_txn_light = (
    df_usd_resolved
    .select(
        F.lit(date_str).alias("eff_dt"),          # date d'initiation
        F.col("exp_dt").cast("string"),             # date d'expiration EXACTE
        F.col("tenor_days"),                        # durée exacte en jours
        F.col("tenor_bucket_final").alias("tenor_bucket"),
        F.col("pair_final").alias("pair"),
        F.col("cp_low_final").alias("lei_low"),     # LEI dealer potentiel
        F.col("cp_high_final").alias("lei_high"),
        F.col("categorie_1").alias("sector_low"),
        F.col("categorie_2").alias("sector_high"),
        F.col("usd_notional_M_final").alias("usd_notional_M"),
        F.col("sign_cp_low_final").alias("sign_low"),  # +1 = cp_low obtient USD
        F.col("fx_forward_rate"),
        F.col("trading_capacity").alias("capacity_type"),  # PRIN/AGNT
    )
)
# STOCKER EN PARQUET, pas CSV :
# df_txn_light.write.mode("append").partitionBy("eff_dt") \
#   .parquet(f"transactions_light_{PERIOD_SUFFIX}.parquet")
```

**Construction de CrossQE en R** (depuis `transactions_light.parquet`) :
```r
qe_dates <- as.Date(c("2024-12-31", "2025-03-31", "2025-06-30", ...))
txn <- arrow::read_parquet("transactions_light.parquet")
txn <- txn %>%
  mutate(
    exp_dt   = as.Date(exp_dt),
    cross_qe = map2_lgl(as.Date(eff_dt), exp_dt, function(near, far) {
      any(qe_dates >= near & qe_dates < far)
    })
  )
```

---

### 5.9 Table 4 — Positions ouvertes par dealer × date (NOUVELLE v9)

**Niveau :** dealer (LEI) × date d'observation  
**Objet :** `UnmatchedLoad_{d,t}`, `NettingEfficiency_{d,t}` (Section 6 du roadmap v9)

**Approche A — Job Spark post-hoc sur Table 3** (recommandée) :

```python
from pyspark.sql import functions as F
import pandas as pd

df_txn = spark.read.parquet("transactions_light.parquet")

# Générer les dates d'observation
all_dates = spark.createDataFrame(
    [(d,) for d in pd.date_range("2024-10-01", "2026-04-30").strftime("%Y-%m-%d")],
    ["obs_date"]
).withColumn("obs_date", F.col("obs_date").cast("date"))

# Cross-join : marquer les transactions actives à chaque date
df_active = (
    df_txn
    .crossJoin(all_dates)
    .filter(
        (F.col("eff_dt").cast("date") <= F.col("obs_date")) &
        (F.col("obs_date") < F.col("exp_dt").cast("date"))
    )
)

# Positions ouvertes par dealer (LEI) × date
df_open = (
    df_active
    .groupBy("obs_date", "lei_low")
    .agg(
        F.sum(F.when(F.col("sign_low") < 0, F.col("usd_notional_M"))
               .otherwise(F.lit(0.0))).alias("usd_supplied_M"),
        F.sum(F.when(F.col("sign_low") > 0, F.col("usd_notional_M"))
               .otherwise(F.lit(0.0))).alias("usd_obtained_M"),
    )
    .withColumn("gross_load_M",      F.col("usd_supplied_M") + F.col("usd_obtained_M"))
    .withColumn("matched_M",         F.least("usd_supplied_M", "usd_obtained_M"))
    .withColumn("unmatched_load_M",  F.abs(F.col("usd_supplied_M") - F.col("usd_obtained_M")))
    .withColumn("netting_efficiency",
        F.lit(1.0) - F.col("unmatched_load_M") / F.col("gross_load_M"))
)
# df_open.write.parquet("dealer_open_positions.parquet")
```

**Note :** le cross-join est coûteux (~18M transactions × 550 jours = ~10B rows avant filtre). Utiliser des dates de partition et filtrer agressivement sur `exp_dt > eff_dt + 1`.

---

## 6. Dépendances et environnement

### 6.1 Pipeline Python

| Dépendance | Version recommandée | Usage |
|-----------|---------------------|-------|
| PySpark | 3.3+ | Traitement Spark des transactions |
| pandas | 2.x | Collecte et écriture CSV |
| Databricks Runtime | 13+ | Environnement d'exécution |

**Fichiers requis au lancement :**
- `common_taxonomy.xlsx` — mapping LEI → secteur (→ ajouter country)
- Table Spark `cln_zone.tcln_otc_cde_dtcc_tsr_fx` — données brutes DTCC

### 6.2 Pipeline R

**Packages requis :**
```r
# Obligatoires
here, dplyr, tidyr, lubridate, ggplot2, scales, viridis, patchwork, fixest

# Pour les vraies données
ShiftShareSE  # AKM shift-share SEs (remplacer l'approximation manuelle)
```

**Environnement :**
```bash
Rscript --version  # R >= 4.2 recommandé
cd /path/to/repo
Rscript scripts/R/00_master.R
```

**Répertoires créés automatiquement** (via `here::here()`) :
- `Output/fx_swap/` — fichiers RDS intermédiaires
- `paper/tables/` — sorties LaTeX bare tabular
- `paper/figures/` — figures PDF

### 6.3 Paper LaTeX

```bash
# Compilation
cd paper && latexmk main.tex

# Prérequis
xelatex, biber, latexmk
# Packages LaTeX (voir .claude/rules/working-paper-format.md pour la liste complète)
```

---

## 7. Prochaines étapes et décisions en suspens

### Priorité 1 — Données réelles (bloquant tout)

1. **Enrichir `common_taxonomy.xlsx`** avec le pays via GLEIF (bulk download).
2. **Appliquer les modifications Python v8** (Sections 5.1–5.6) : `booking_location`, `taker_ratio`, `vwap_fx_forward`, `prin_ratio`, table par LEI.
3. **Appliquer les modifications Python v9** (Sections 5.7–5.9) :
   - T2 : matrice bilatérale directionnelle (5.7)
   - T3 : transactions légères avec `exp_dt` en Parquet (5.8)
   - T4 : positions ouvertes dealer×date en job Spark séparé (5.9)
4. **Construire le TIB** : joindre les taux forward (pipeline) avec taux spot (Bloomberg/BCE) et OIS.
5. **Substituer dans `01_simulate_data.R`** : remplacer la simulation par une lecture des vrais fichiers.

### Priorité 2 — Instrument d'offre (nouvelle — v9)

6. **Construire CrossQE** depuis T3 en R : pour chaque transaction, `cross_qe = any(qe_dates >= eff_dt & qe_dates < exp_dt)`.
7. **Construire `s^pre_{d,m,τ}`** : part de marché prédéterminée des dealers depuis T5 (table par LEI filtrée sur dealers).
8. **Construire `RegIntensity_d`** : baseline = `SnapshotDealer_d` (binaire juridiction de reporting).
9. **Construire `Z^{S,QE}_{m,τ,t}`** = `CrossQE × Σ_d s^pre_{d,m,τ} × RegIntensity_d`.
10. **Construire `UnmatchedLoad^pre_{d,-m}`** depuis T4, leave-one-market-out, normalisé par `GrossLoad`.

### Priorité 3 — Estimation v8 (dès que données disponibles)

11. **Exécuter `02_balance_tests.R`** en premier (prérequis IV).
12. **Calculer `DomShare_{i,m}`** pour l'instrument MMF depuis T5.
13. **Construire `Z^D_{m,t}`** = `Exposure^MMF × MMFOutflow_t`.
14. **Remplacer AKM approximé** par le package `ShiftShareSE`.
15. **Remplacer demand system OLS** par GMM joint.

### Priorité 4 — Estimation v9 (après instrument d'offre prêt)

16. **Exécuter la Section 11** de `04_iv_estimation.R` : premier étage offre (Z^S → DealerSupply).
17. **Vérifier placebos** : Z^S ne doit pas prédire Q^FB (colonne 4 de `iv_supply_first_stage.tex`).
18. **Exécuter la Section 12** : système simultané (2 instruments × 2 équations).
19. **Exécuter la Section 13** : interaction θ_3 (hypothèse centrale).
20. **Exécuter `07_bilateral_decomposition.R`** : spreads sectoriels, matrice bilatérale.

### Priorité 5 — Paper

21. **Mettre à jour les chiffres** dans `empirical_results.tex` et `fx_swap_seminar_talk.tex`.
22. **Rédiger `sections/introduction.tex`** — section manquante la plus visible.
23. **Assembler `paper/main.tex`** : connecter les `\input{}`.
24. **Générer les figures PDF** en exécutant le pipeline sur vraies données.

### Priorité 6 — Extensions théoriques

25. **Formaliser les deux équilibres** (annexe 4–6 pages).
26. **Formaliser le problème de l'intermédiaire** : dealer sous contrainte de bilan → endogénéiser B_t.

### Décisions en suspens (nécessitent arbitrage humain)

| Décision | Options | Statut |
|----------|---------|--------|
| Proposition 4 standalone ou corollaire de P2 ? | (a) Garder P4 (Prop 4 quarter-end) ; (b) Dégrader en corollaire de P2 | ⏳ Ouvert |
| P6 (provider heterogeneity) scindée en P6a/b/c ? | (a) Garder P6 telle quelle ; (b) Scinder en dealer/HF/CB | ⏳ Ouvert |
| Cible de journal ? | JF, RFS, JFE, QJE (theory+empirics) | ⏳ Ouvert — activer `/submit` pour targeting |
| Extension événementielle (swap lines, mars 2020) ? | (a) Inclure en Section 6 ; (b) Working paper companion | ⏳ Ouvert |

---

## 8. Scores de qualité des agents (Phase 3–4)

| Agent | Score | Rounds | Décision |
|-------|-------|--------|----------|
| Data-engineer | — | 3 | ✅ PASS |
| Coder-critic | **85/100** | 3 | ✅ PASS |
| Writer | — | 2 | ✅ PASS |
| Writer-critic | **94/100** → ~96/100 | 2 + fix direct | ✅ PASS (gate soumission 95) |
| Storyteller | — | 1 | ✅ PASS |
| Storyteller-critic | **86/100** (consultatif) → ~88/100 | 1 + fix direct | ✅ Advisory PASS |

---

## 9. Fichiers de référence clés

| Fichier | Contenu |
|---------|---------|
| `paper/design/empirical-roadmap-v8.md` | Design empirique complet (source de vérité) |
| `quality_reports/plans/2026-05-18_strategy-memo.md` | Memo stratégique avec audit paramètres, alignement théorie-empirique, 5 objections arbitres |
| `paper/theory/sections/inside-synthetic-dollar-v2.tex` | Framework théorique formel complet (Propositions, Théorèmes, preuves) |
| `paper/sections/theoretical_framework.tex` | Section 3 du papier (rédigée, writer-critic 94/100) |
| `paper/sections/empirical_results.tex` | Sections 4–6 du papier (rédigée, writer-critic 94/100) |
| `paper/talks/fx_swap_seminar_talk.tex` | Beamer 34 frames (storyteller-critic 86/100) |
| `scripts/R/00_master.R` | Point d'entrée unique du pipeline R |
| `scripts/R/functions/helpers.R` | Fonctions partagées entre scripts |
| `.claude/rules/working-paper-format.md` | Standard LaTeX du projet |
| `.claude/rules/content-invariants.md` | INV-1 à INV-21 (règles non-négociables) |
