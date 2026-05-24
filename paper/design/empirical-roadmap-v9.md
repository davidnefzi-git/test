# Feuille de Route v9 — Design Empirique

## Inside Synthetic Dollar Liquidity and the Microstructure of FX Swap Markets

**Version :** v9 (2026-05-24) — instrument d'offre + décomposition bilatérale  
**Version précédente :** v8 (2026-05-18) — IV shift-share MMF, demand system  
**Branche :** `claude/ecstatic-turing-uNl56`

---

## 1. Positionnement et contribution (inchangé de v8)

Contribution centrale : les **deux contreparties** de chaque transaction FX swap sont observées simultanément. Le papier est le premier à combiner :

1. Instruments de demande et d'offre séparés
2. Décomposition bilatérale complète (qui demande / qui fournit / par quel dealer / à quel prix)
3. Reconstruction des positions ouvertes des dealers (UnmatchedLoad, NettingEfficiency)

---

## 2. Structure du papier (inchangée de v8)

| Partie | Contenu | Statut |
|--------|---------|--------|
| **1. Cadre conceptuel** | Inside/outside dollar liquidity ; search-and-matching | ✅ Rédigé |
| **2. Microstructure bilatérale** | Cartographie descriptive : matrice d'intermédiation | ✅ Rédigé |
| **3. IV simple (demande)** | MMF → Q_FB → Price impact | ✅ Codé |
| **4. Instrument d'offre (NEW v9)** | CrossQE × dealer composition → DealerSupply | 🔵 Nouveau |
| **5. Système simultané (NEW v9)** | Demande + offre dans un seul système | 🔵 Nouveau |
| **6. Décomposition bilatérale (NEW v9)** | Spreads sectoriels, taker/maker, absorption | 🔵 Nouveau |
| **7. Demand system** | Extension structurelle, contrefactuels | ✅ Codé |

---

## 3. Unité d'observation et notation

```
ℓ = transaction individuelle
m = currency_pair × tenor_bucket  (marché)
t = date
τ = tenor exact (en jours)

P_{m,t} = -TIB_{m,t}          (prix du dollar synthétique, > 0 = cher)
Q_{FB,m,t} = demande nette de dollars synthétiques des banques étrangères
DealerSupply_{m,t} = offre nette de dollars synthétiques des dealers

SignedUSDFlow_{a,ℓ} > 0  ⟺  entité a obtient des dollars synthétiques
```

**Conventions de nommage dans le code R :**

| Code | Objet théorique | Description |
|------|----------------|-------------|
| `mu_t` | μ_t | Spread de funding = PriceUSD = -TIB |
| `U_t` | Q_{FB,m,t} | Demande nette USD des banques étrangères |
| `B_cap` | B_t | Capacité d'intermédiation des dealers |
| `Z_MMF` | Z^D_{m,t} | Instrument de demande (shift-share MMF) |
| `Z_S_QE` | Z^{S,QE}_{m,τ,t} | Instrument d'offre (CrossQE × dealer comp.) |
| `DealerSupply` | DealerSupply_{m,t} | Outcome premier étage offre |
| `cross_qe` | CrossQE_{m,τ,t} | = 1 si le contrat traverse un quarter-end |
| `unmatched_load` | UnmatchedLoad_{d,t} | Charge non appariée du dealer |
| `netting_eff` | NettingEfficiency_{d,t} | Efficacité de netting du dealer |

---

## 4. Premier bloc — Instrument de demande MMF (inchangé de v8)

### 4.1 Construction

```
Z^D_{m,t} = Exposure^MMF_{m,m-1} × FundingShock_t
Exposure^MMF_{m,m-1} = Σ_i w^pre_{i,m} × MMFShare_{i,m-1}
w^pre_{i,m} = GrossVolume_{i,m,[t-12m,t-1m]} / Σ_j GrossVolume_{j,m,...}
```

### 4.2 Premier étage demande

```
Q^{FB}_{m,t} = α_m + δ_t + π_D Z^D_{m,t} + Γ X_{m,t} + u_{m,t}
```

Signe attendu : π_D > 0.

### 4.3 Deuxième étage

```
P_{m,t} = α_m + δ_t + β_D Q̂^{FB}_{m,t} + Γ X_{m,t} + ε_{m,t}
```

Signe attendu : β_D > 0 (demande ↑ → prix ↑).

---

## 5. Deuxième bloc — Instrument d'offre quarter-end × dealer (NEW v9)

### 5.1 Intuition économique

Les contrats FX swap qui traversent une date de reporting trimestriel consomment du bilan réglementaire. La variation pertinente pour l'identification provient de l'interaction entre :
- le fait que le contrat traverse ou non le quarter-end (CrossQE)
- la dépendance prédéterminée du marché à des dealers ex ante contraints (composition dealer)

### 5.2 Définition de CrossQE

Au niveau transactionnel :
```
CrossQE_ℓ = 1{near_ℓ ≤ QE_q < far_ℓ}
```

Au niveau marché-tenor-date :
```
CrossQE_{m,τ,t} = 1{un contrat de tenor τ initié à t traverse QE_q}
```

Cette variation est plus informative qu'une dummy de fin de trimestre car elle dépend du tenor du contrat.

### 5.3 Instrument d'offre principal

```
Z^{S,QE}_{m,τ,t} = CrossQE_{m,τ,t} × Σ_d s^pre_{d,m,τ} × RegIntensity_d
```

Composantes :
- `s^pre_{d,m,τ}` : part de marché prédéterminée du dealer d dans (m,τ)
- `RegIntensity_d` : intensité réglementaire du dealer (snapshot vs. moyenne ; G-SIB ; etc.)
- `CrossQE_{m,τ,t}` : le contrat traverse la date de reporting

**Baseline :** `RegIntensity_d = SnapshotDealer_d` (variable binaire).

### 5.4 Premier étage offre

```
DealerSupply_{m,τ,t} = α_{m,τ} + δ_t + π_S Z^{S,QE}_{m,τ,t} + Γ X_{m,τ,t} + u_{m,τ,t}
```

Signe attendu : π_S < 0 (CrossQE ↑ → offre dealer ↓).

Outcomes alternatifs du premier étage :
- `DealerSupply_{m,t}` (volume net USD fourni par dealers)
- `DealerGrossVolume_{m,t}` (volume brut)
- `DealerShare_{m,t}` (part de marché des dealers)
- `InterdealerShare_{m,t}` (proportion interdealer)

### 5.5 Deuxième étage offre

```
P_{m,τ,t} = α_{m,τ} + δ_t + β_S DealerSupplŷ_{m,τ,t} + Γ X_{m,τ,t} + ε_{m,τ,t}
```

Signe attendu : β_S < 0 (offre ↓ → prix ↑).

Ou en termes de rareté (`Scarcity = -DealerSupply`) : β_S > 0.

---

## 6. Troisième bloc — Instrument enrichi par les positions ouvertes (NEW v9)

### 6.1 Reconstruction des positions ouvertes

Pour chaque dealer d à chaque date t :

```
USDObtained_{d,t} = Σ_{ℓ active} max(SignedUSDFlow_{d,ℓ}, 0)
USDSupplied_{d,t} = Σ_{ℓ active} max(-SignedUSDFlow_{d,ℓ}, 0)

MatchedIntermediation_{d,t} = min(USDObtained_{d,t}, USDSupplied_{d,t})
UnmatchedLoad_{d,t} = |USDSupplied_{d,t} - USDObtained_{d,t}|
NettingEfficiency_{d,t} = 1 - UnmatchedLoad_{d,t} / (USDSupplied_{d,t} + USDObtained_{d,t})
```

Une transaction est active à la date t si `eff_dt ≤ t < exp_dt` (requiert la Table 3 du pipeline Python).

### 6.2 Instrument enrichi

```
Z^{S,LoadQE}_{m,τ,t} = CrossQE_{m,τ,t} × Σ_d s^pre_{d,m,τ} × UnmatchedLoad^pre_{d,-m}
```

où `UnmatchedLoad^pre_{d,-m}` est la charge non appariée prédéterminée du dealer, calculée hors-marché m (leave-one-market-out).

**Statut :** extension mécanistique / robustesse avancée (pas l'instrument principal).

---

## 7. Système simultané demande-offre (NEW v9)

### 7.1 Forme réduite (deux équations)

```
Q^{FB}_{m,t} = α_m + δ_t + π_D Z^D_{m,t} + π_S Z^S_{m,t} + Γ X_{m,t} + u^Q_{m,t}
DealerSupply_{m,t} = α_m + δ_t + ρ_D Z^D_{m,t} + ρ_S Z^S_{m,t} + Γ X_{m,t} + u^S_{m,t}
```

Signes attendus : π_D > 0, ρ_S < 0.

Test de validité mécanique :
- Z^D doit principalement déplacer Q^FB (pas DealerSupply)
- Z^S doit principalement déplacer DealerSupply (pas Q^FB)

### 7.2 Deuxième étage structurel

```
P_{m,t} = α_m + δ_t + β_D Q̂^{FB}_{m,t} + β_S Scarcitŷ^{Dealer}_{m,t} + Γ X_{m,t} + ε_{m,t}
```

Signes attendus : β_D > 0, β_S > 0.

### 7.3 Interaction demande × capacité (hypothèse centrale)

Forme structurelle :
```
P_{m,t} = α_m + δ_t + β_D Q̂^{FB}_{m,t} + β_C (Q̂^{FB}_{m,t} × Scarcity^{Dealer}_{m,t}) + Γ X_{m,t} + ε_{m,t}
```

Forme réduite :
```
P_{m,t} = α_m + δ_t + θ_1 Z^D_{m,t} + θ_2 Z^S_{m,t} + θ_3 (Z^D_{m,t} × Z^S_{m,t}) + Γ X_{m,t} + ε_{m,t}
```

Hypothèse centrale : **θ_3 > 0** — un choc de demande bancaire a un effet de prix plus fort quand la capacité dealer est contrainte.

---

## 8. Décomposition bilatérale de l'ajustement (NEW v9)

### 8.1 Prix sectoriels et spreads

```
P_{s,m,t} = prix moyen payé par le secteur s dans le marché m à la date t
Spread_{s,m,t} = P_{s,m,t} - P_{ID,m,t}
```

Spécification :
```
Spread_{s,m,t} = α_{s,m} + δ_t + β_s Q̂^{FB}_{m,t} + γ_s Scarcitŷ^{Dealer}_{m,t} + ε_{s,m,t}
```

Questions : qui paie le coût de l'ajustement ? Les banques ? Les hedge funds ? Les asset managers ?

### 8.2 Matrice de flux bilatéraux

```
Flow_{s→r,m,t} = flux de dollars synthétiques du secteur s (fournisseur) vers r (demandeur)
```

Spécification :
```
Share_{s→r,m,t} = α_{s,r,m} + δ_t + β_{s,r} Z^D_{m,t} + γ_{s,r} Z^S_{m,t} + ε_{s,r,m,t}
```

Questions : qui absorbe physiquement le choc ? Les dealers réduisent-ils leur part ? Les hedge funds prennent-ils le relais ?

### 8.3 Taker / Maker

```
Q^{Taker}_{FB,m,t} = α_m + δ_t + π_T Z^D_{m,t} + Γ X_{m,t} + u_{m,t}
```

Une hausse de Q^{Taker}_FB en réponse à Z^D indique une demande urgente (pas seulement structurelle).

---

## 9. Identification : hypothèses et réponses

### 9.1 Instrument MMF (demande)

**Hypothèse d'exclusion :**
```
Z^D_{m,t} ⊥ ε_{m,t}  conditionnellement aux FE et contrôles, sauf via Q^FB
```

**Menaces et réponses :**

| Menace | Réponse |
|--------|---------|
| Stress global de dollar funding | Effets fixes date ; variation cross-market via w^pre |
| Crédit bancaire | CDSAgg (mêmes poids que Z) |
| Anticipation par les marchés | Pré-tendances Z_{t-k} → P_{m,t} non significatif |
| Concentration des poids | Leave-one-bank-out, leave-one-country-out |

### 9.2 Instrument quarter-end (offre)

**Formulation correcte de l'exogénéité :**
> "The timing of quarter-end reporting dates is predetermined, but identification comes from differential exposure of currency-tenor markets to contracts crossing reporting dates and to dealers with high predetermined regulatory intensity."

**Menaces et réponses :**

| Menace | Réponse |
|--------|---------|
| Demande client autour du QE | Comparer tenors traités vs. non traités à la même date |
| Absorption par effets fixes date | Variation cross-tenor à la même date |
| Anticipation du QE | Pas besoin de surprise — l'identification vient de la composition prédéterminée |
| Demande dealer endogène | Contrôler la demande sectorielle observée |

### 9.3 Instruments faibles

- Kleibergen-Paap rk Wald F-stat (pas seulement F > 10)
- Anderson-Rubin confidence sets si F < 10
- Wild cluster bootstrap
- Clustering double (marché × semaine)
- Leave-one-market-out

---

## 10. Tests de validation (NEW v9)

### 10.1 Pertinence du premier étage

| Instrument | Outcome testé |
|-----------|--------------|
| Z^D | Q^{FB} (attendu +) |
| Z^S | DealerSupply, DealerShare, InterdealerShare (attendu -) |
| Z^S | UnmatchedLoad, NettingEfficiency |

Un bon instrument d'offre doit déplacer les variables de capacité dealer, pas seulement le prix.

### 10.2 Placebos sectoriels (instrument MMF)

Effets de Z^D plus forts sur les banques exposées aux MMFs que sur :
- Corporates
- Insurers / pension funds
- Souverains
- Secteurs sans exposition MMF

### 10.3 Placebos tenor (instrument QE)

Effets de Z^S plus forts pour les tenors qui traversent le quarter-end que pour les tenors voisins qui ne le traversent pas.

### 10.4 Placebos dates

Tester de fausses dates de quarter-end : QE_q + 10 jours ou QE_q - 10 jours.

### 10.5 Hétérogénéité dealer

Effet de Z^S plus fort pour :
- Les dealers snapshot vs. moyenne quotidienne
- Les G-SIBs
- Les dealers avec forte charge prédéterminée (UnmatchedLoad élevé)
- Les dealers avec faible NettingEfficiency

---

## 11. Tableaux et figures à produire

### Résultats principaux

| Tableau | Script | Contenu |
|---------|--------|---------|
| `iv_first_stage.tex` | `04_iv_estimation.R` | Premier étage demande (taker/maker) |
| `iv_second_stage.tex` | `04_iv_estimation.R` | Deuxième étage demande |
| `iv_supply_first_stage.tex` | `04_iv_estimation.R` | Premier étage offre (Z^S → DealerSupply) |
| `iv_simultaneous_system.tex` | `04_iv_estimation.R` | Système simultané demande-offre |
| `iv_demand_capacity_interaction.tex` | `04_iv_estimation.R` | Interaction θ_3 |
| `bilateral_sector_spreads.tex` | `07_bilateral_decomposition.R` | Spreads sectoriels |
| `bilateral_flow_matrix.tex` | `07_bilateral_decomposition.R` | Matrice d'absorption |
| `bilateral_taker_maker.tex` | `07_bilateral_decomposition.R` | Taker/maker par secteur |

### Figures

| Figure | Script | Contenu |
|--------|--------|---------|
| `intermediation_matrix.pdf` | `03_descriptives.R` | Matrice d'intermédiation bilatérale |
| `cross_qe_variation.pdf` | `07_bilateral_decomposition.R` | CrossQE par tenor et date |
| `dealer_unmatched_load.pdf` | `07_bilateral_decomposition.R` | UnmatchedLoad des dealers |
| `sector_spread_dynamics.pdf` | `07_bilateral_decomposition.R` | Spreads sectoriels dans le temps |

---

## 12. Données nécessaires (mise à jour v9)

Cinq tables du pipeline Python :

| Table | Niveau | Usage |
|-------|--------|-------|
| **T1** : Agrégat cellule enrichi | Cellule-jour | Q^FB, mu_t, taker_ratio, VWAP |
| **T2** : Matrice bilatérale | Secteur×Secteur×cellule-jour | Flow_{s→r,m,t}, spreads sectoriels |
| **T3** : Transactions légères | Transaction | CrossQE_ℓ (exp_dt exact), TIB transactionnel |
| **T4** : Positions ouvertes | Dealer×jour | UnmatchedLoad_{d,t}, NettingEfficiency |
| **T5** : Flux par LEI | Banque×cellule-jour | DomShare_{i,m} (poids IV) |

**Point critique :** T3 et T4 sont impossibles à construire depuis l'agrégat journalier actuel car il perd `exp_dt` exact. Stocker T3 en Parquet partitionné par `eff_dt`.

---

## 13. Robustesse et extensions

### 13.1 Instruments alternatifs d'offre

```
Z^{Repo}_{m,t} = RepoStress_t × Σ_d s^pre_{d,m} RepoExposure_d
Z^{TGA}_{m,t} = TGAShock_t × Σ_d s^pre_{d,m} USTIntensity_d
```

Ces instruments servent de validation du canal de coût d'opportunité du bilan.

### 13.2 Spillovers vers le spot

```
ΔS_{c,t} = α_c + δ^global_t + β DerivativePressurê_{c,t} + Γ X_{c,t} + ε_{c,t}
```

Extension secondaire — identifier l'identification principale sur le marché des FX swaps.

### 13.3 Matrice d'absorption dynamique

```
A_{s,r,m,t} = Flow_{s→r,m,t} / Σ_s Flow_{s→r,m,t}

A_{s,r,m,t} = α_{s,r,m} + δ_t + β_{s,r} Z^D_{m,t} + γ_{s,r} Z^S_{m,t} + ε_{s,r,m,t}
```

Forme la plus directe de la contribution microstructurelle : montre qui absorbe le choc de demande et ce qui se passe quand les dealers sont contraints.

---

## 14. Prédictions (mise à jour v9)

| # | Prédiction | Partie | Signe | Instrument |
|---|-----------|--------|-------|------------|
| P1 | Les FB exposés aux MMFs augmentent leur net USD-taking | 3 | π_D > 0 | Z^D |
| P2 | Cette demande rend le dollar synthétique plus cher | 3 | β_D > 0 | Z^D |
| P3 | Les FB sont plus price-inelastic que les HF | 7 | |β_FB| < |β_HF| | DS1 |
| P4 | Les dealers réduisent leur offre quand les contrats traversent le QE | 4 | π_S < 0 | Z^S |
| P5 | Cette contraction d'offre augmente le prix | 4 | β_S > 0 | Z^S |
| P6 | L'effet prix est amplifié quand la capacité dealer est contrainte | 5 | θ_3 > 0 | Z^D × Z^S |
| P7 | Les banques étrangères absorbent le coût (spreads sectoriels > 0) | 6 | β_FB > 0 | Z^D |
| P8 | Les HF agissent comme absorbeurs partiels du choc | 6 | γ_HF ambigu | Z^S |
| P9 | La demande urgente (taker) augmente plus que la demande routinière (maker) | 6 | π_taker >> π_maker | Z^D |
| P10 | La pression se transmet au spot FX via les tenors courts | Extension | β_S > 0 | Z^D |

---

## 15. Étapes de travail (mise à jour v9)

### Phase A — Données (prérequis)
- A1 : Construire T1 (agrégat enrichi + VWAP)
- A2 : Construire T2 (matrice bilatérale directionnelle)
- A3 : Construire T3 (transactions légères avec exp_dt)
- A4 : Construire T4 (positions ouvertes dealers)
- A5 : Enrichir taxonomie avec pays (GLEIF)
- A6 : Joindre taux spot (Bloomberg/BCE) pour TIB

### Phase B — Instrument d'offre
- B1 : Construire CrossQE_{m,τ,t} depuis T3
- B2 : Construire s^pre_{d,m,τ} depuis T5
- B3 : Construire RegIntensity_d (baseline = SnapshotDealer)
- B4 : Construire Z^{S,QE}
- B5 : Construire UnmatchedLoad^pre_{d,-m} depuis T4

### Phase C — Estimation système simultané
- C1 : Forme réduite (deux équations)
- C2 : Deuxième étage structurel (β_D, β_S)
- C3 : Interaction θ_3

### Phase D — Décomposition bilatérale
- D1 : Spreads sectoriels P_{s,m,t}
- D2 : Matrice de flux Flow_{s→r,m,t}
- D3 : Taker/maker par secteur
- D4 : Dealer heterogeneity (RegIntensity, UnmatchedLoad)

### Phase E — Validations
- E1 : Placebos sectoriels (Z^D sur corporates, insurers)
- E2 : Placebos tenor (CrossQE vs. non-CrossQE à même date)
- E3 : Placebos dates (QE_q ± 10 jours)
- E4 : Hétérogénéité dealer (snapshot vs. average, G-SIB)
