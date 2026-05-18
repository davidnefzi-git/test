# Feuille de Route v8 — Design Empirique

## Who Supplies Synthetic Dollars? Bilateral Microstructure of Demand and Supply in FX Swap Markets

---

## 1. Positionnement

### 1.1 Ce qui existe

Khetan (2025) : MMF/wholesale funding → FX swaps → basis, avec IV et transactions. Price impact ~7 bps pour +10% de demande bancaire. Kloks-Mattille-Ranaldo (2024) : substitution repo/MMF → FX swaps au quarter-end, GIV, prix de transactions. Ben Zeev et al. : GIV demande institutionnelle → CIP basis. Aldasoro et al. : frictions MMF, régulation, pricing dans les marchés MMF. Du-Tepper-Verdelhan : CIP deviations, régulation bancaire. Rime-Schrimpf-Syrstad : funding costs des arbitrageurs et CIP.

### 1.2 Ce que ce papier fait de différent

L'avantage est la donnée bilatérale réglementaire : les DEUX contreparties de chaque transaction FX swap sont identifiées. Cela permet d'observer simultanément la demande et l'offre de dollars synthétiques par secteur, juridiction et tenor.

### 1.3 Contribution

> To our knowledge, this is among the first papers to jointly observe both sides of FX swap transactions and use this bilateral structure to map synthetic-dollar demand and supply by sector. We identify sector-specific price sensitivities by exploiting prime-MMF funding shocks and EPFR portfolio outflows as sector-specific demand shifters, and decompose the aggregate price impact into a demand-shift component and a state-dependent market intermediation capacity component.

### 1.4 Structure du papier

| Partie | Contenu | Robustesse |
|--------|---------|-----------|
| **1. Cadre conceptuel** | FX swaps comme technologie de conversion en dollars synthétiques ; inside/outside dollar liquidity | Théorique |
| **2. Microstructure bilatérale** | Cartographie descriptive : qui demande, qui fournit, par secteur/juridiction/tenor | La plus robuste |
| **3. IV simple** | Chocs MMF → Q_{FB} → Price impact | Bloc causal transparent |
| **4. Qui absorbe les chocs ?** | Dealers, hedge funds, autres banques — et comment la structure change en stress/QE | Semi-causal |
| **5. Demand system** | Sensibilités-prix sectorielles, décomposition, contrefactuels | Extension structurelle (plus hypothétique) |
| **6. Extensions** | Spot FX, cross-tenor substitution, dispersion sectorielle des prix | Complémentaire |

---

## 2. Cadre conceptuel : FX swaps et liquidité dollar synthétique

### 2.1 Inside vs outside dollar liquidity

**Outside safe dollar liquidity (O_t) :** créances dollar connectées au cœur institutionnel américain — réserves Fed, Treasuries, passifs bancaires domestiques backstoppés (FDIC, discount window), swap lines.

**Inside synthetic dollar liquidity (I_t) :** liquidité dollar produite hors du système bancaire domestique américain, notamment via les FX swaps, le repo offshore, les dépôts eurodollars et les bilans des banques globales.

En temps normal, I ≈ O. En stress, I ≠ O.

### 2.2 FX swaps comme technologie de conversion

Les FX swaps sont le principal marché où les agents non-US convertissent de la liquidité en devise locale en dollars synthétiques. La near leg fournit les USD, la far leg les rend.

Le **prix de cette conversion** est le Transaction-Implied Basis (TIB), ou son inverse PriceUSD = -TIB.

### 2.3 Le marché à plusieurs acteurs

```
Demande de dollars synthétiques (Q_s > 0) :
  Banques étrangères (funding) — shifter : MMF exposure
  Asset managers (hedging) — shifter : EPFR flows
  Corporates (hedging commercial)

Offre de dollars synthétiques (Q_s < 0) :
  Dealers / banques US (intermédiation) — capacité : bilan, accès Fed
  Hedge funds (basis trade) — shifter : rentabilité × risk capacity
  Reserve managers (gestion de réserves)
```

### 2.4 Condition d'équilibre et price impact

```
Σ_s Q_{s,m,t} = 0
```

**Équation de prix d'équilibre :**
```
PriceUSD_{m,t} = -(1/B) × Σ_s [α_{s,m} + γ_s X_{s,m,t} + ε_{s,m,t}]
```

où B = Σ_s β_s < 0 est la pente agrégée de la net-demand.

**Price impact d'un choc MMF :**
```
ΔPriceUSD^{MMF} = -(γ_{FB} / B) × ΔZ^{MMF}
```

### 2.5 Correspondance théorie-données

| Objet théorique | Objet empirique |
|-----------------|-----------------|
| I_t (inside synthetic dollar liquidity) | Dollars synthétiques produits par FX swaps |
| O_t (outside safe dollar liquidity) | Funding dollar onshore (MMF, repo, fed funds) |
| B_t (capacité de conversion) | Capacité des dealers, FBO branches, bilans bancaires |
| q_t (qualité de l'eurodollar) | Facilité de conversion : TIB, dispersion des prix, taker/maker ratio |
| U_t/B_t (tension du marché) | Ratio demande/capacité |
| μ_t (spread de funding) | PriceUSD = -TIB |

---

## 3. Les données

### 3.1 Transactions FX OTC — reporting réglementaire bilatéral

Reporting exhaustif. Les deux contreparties identifiées par nom, secteur, pays. Taker/maker observé. Jambe forward observée. Stocks et flux disponibles.

**Baseline :** FX swaps uniquement. Forwards et CCS en robustesse.

### 3.2 Conventions

**Signe USD :** `SignedUSDFlow > 0` = obtient des USD.

**Prix :**
```
PriceUSD_{m,t} = -TIB_{m,t}
```

PriceUSD > 0 = dollar synthétique cher.

**Validation :** banques étrangères majoritairement SignedUSDFlow > 0 ; banques US / dealers majoritairement < 0.

### 3.3 Agrégation en cellules

```
c = sector × country × currency_pair × tenor_bucket × date
```

Buckets : ON, 1W, 1M, 3M, 6M, 1Y+.

### 3.4 Quantités sectorielles

```
Q_{s,m,t} = Σ_{c ∈ m, sector=s} SignedUSDFlow_{c,t}
```

**Market-clearing residual :**
```
r_{m,t} = Σ_s Q_{s,m,t}  (≈ 0 empiriquement)
```

**Groupe cible pour l'IV simple :**
```
Q_{FB,m,t} = NetUSDTaking des banques étrangères dans m
```

### 3.5 Taker/maker

```
Q_{s,m,t} = Q^{taker}_{s,m,t} + Q^{maker}_{s,m,t}
```

Prédiction : π^{taker} >> π^{maker} dans le premier étage.

### 3.6 Prix par marché et prix sectoriels

```
TIB_{m,t} = médiane pondérée par volume des forward points dans m
PriceUSD_{m,t} = -TIB_{m,t}
PricePaid_{s,m,t} = -TIB_{s,m,t}
Spread_s = PricePaid_{s} - PricePaid_{interdealer}
```

Filtres de liquidité : seuils min transactions et volume ; winsorisation 1er-99ème percentile.

---

## 4. Construction des instruments

### 4.1 Instrument MMF (canal funding bancaire)

**Baseline (Option B — shift-share) :**
```
Z^{MMF}_{m,t} = Exposure^{MMF}_{m,m-1} × FundingShock_t
Exposure^{MMF}_{m,m-1} = Σ_i w_{i,m}^{pre} × MMFShare_{i,m-1}
```

**Identification :** variation cross-marché de l'exposition prédéterminée (pas le choc commun, absorbé par τ_t).

**Robustesse (Option A — mensuel) :**
```
Z^{MMF}_{m,m} = Σ_i w_{i,m}^{pre} × MMFLoss_{i,m}
```

### 4.2 Poids prédéterminés

```
w_{i,m}^{pre} = GrossVolume_{i,m,[t-12m,t-1m]} / Σ_j GrossVolume_{j,m,[t-12m,t-1m]}
```

Rolling 12m laggé. Robustesse : 6m, 24m, fixes.

### 4.3 Instrument EPFR (canal hedging)

```
Z^{EPFR}_{m,t} = EPFRBondFlow_{j(k),w(t)}
```

### 4.4 Variables d'état conditionnelles

```
DealerCapacity_t = f(Primary Dealer repo, H.8 Borrowings, leverage)
CDSAgg_{m,t} = Σ_i w_{i,m}^{pre} × CDS_{i,t}
Z^{HF}_{m,t} = (-TIB_{m,t-1}) × RiskCapacity_t  (pas un instrument strict)
```

---

## 5. Approche A — IV simple

### 5.1 Premier étage

```
Q_{FB,m,t} = α_m + τ_t + π Z^{MMF}_{m,t} + γ CDSAgg_{m,t}
           + δ Z^{EPFR}_{m,t} + u_{m,t}
```

F-stat Kleibergen-Paap > 10 requis.

**Diagnostic taker/maker :** π^{taker} >> π^{maker} attendu.

### 5.2 Deuxième étage

```
ΔPriceUSD_{m,t} = α_m + τ_t + β Q̂_{FB,m,t} + γ CDSAgg_{m,t} + ε_{m,t}
```

**β > 0 attendu.** β = price impact coefficient (bps/Mds USD). Ce n'est PAS une élasticité.

### 5.3 Interactions (deux endogènes, deux instruments)

**Par DealerConstraint (P6) :**
```
ΔPriceUSD = α_m + τ_t + β₁ Q̂ + β₂ [Q × DealerConstraint]̂ + ε
```
β₂ > 0 attendu.

**Par QuarterEnd (P7) :** idem. β₂ > 0.

**Par tenor (P5) :**

| Tenor | β attendu |
|-------|-----------|
| ON, 1W | Fort positif |
| 1M | Positif |
| 3M | Modérément positif |
| 6M+ | Faible |

### 5.4 Forme réduite

```
ΔPriceUSD_{m,t} = α_m + τ_t + β_RF Z^{MMF}_{m,t} + ε
```

β_RF > 0. Wald : β_IV = β_RF / π.

---

## 6. Approche B — Demand system (extension structurelle)

### 6.1 Philosophie

β_IV ≈ -γ_{FB} / B. Le demand system décompose ce price impact en taille du choc (γ_{FB}) et capacité d'absorption (B).

### 6.2 Versions progressives

| Version | Secteurs | Usage |
|---------|---------|-------|
| **DS1** | FB, NBFI, Dealers (résidu) | Baseline structurelle |
| **DS2** | FB, USBanks/Dealers, HedgeFunds, AM, Corp/Other | Si premiers étages sectoriels forts |
| **DS3** | Bilatéral sector-to-sector | Microstructure descriptive |

### 6.3 DS1 — Trois secteurs

```
q_{s,m,t} = α_{s,m} + (β_s + β_s^C C_{s,t}) × PriceUSD_{m,t}
           + γ_s X_{s,m,t} + ε_{s,m,t}
q_{s,m,t} = Q_{s,m,t} / GrossVolume^{pre}_{s,m}
```

**Signes attendus :**

| Secteur | β_s attendu | Interprétation |
|---------|------------|----------------|
| FB | β_{FB} < 0 | Relativement inélastiques |
| NBFI | Signe ambigu | AM : β < 0 ; HF : β > 0 (basis traders) |

**Prédiction P3 :** |β_{FB}| < |β_{HF}|.

**Dealers en résidu :**
```
Q_D = -(Q_{FB} + Q_{NBFI} + Q_{Other})
```

**Instruments cross-sectoriels :**

| Équation | Shifter propre | Instrument pour PriceUSD |
|----------|----------------|--------------------------|
| FB | Z^{MMF} | Z^{EPFR} |
| NBFI | Z^{EPFR} | Z^{MMF} |

### 6.4 Équation de prix d'équilibre

```
PriceUSD_{m,t} = -(1/B) × Σ_s [α_{s,m} + γ_s X_{s,m,t} + ε_{s,m,t}]
B = Σ_s β_s < 0
```

### 6.5 Contrefactuels (model-based)

**CF1 — Choc MMF 10% sur banques JP :**
```
ΔPriceUSD_{USD/JPY,1M} = -(γ_{FB}/B) × 0.10 × MMFExposure_{JP}
```

**CF2 — Absence de basis trade (β_{HF} = 0) :** |B| diminue → price impact augmente.

**CF3 — Quarter-end dealers contraints :** |B| diminue → price impact augmente.

Présenter comme « model-based simulations », pas comme « quasi-experimental estimates ».

---

## 7. Partie 4 du papier — Qui absorbe les chocs ?

### 7.1 Matrice d'intermédiation

Pour chaque juridiction demandeuse de USD, distribution sectorielle des contreparties fournissant les USD.

### 7.2 Dynamique événementielle

- Quarter-end (dealers se retirent → HF prennent le relais ?)
- COVID mars 2020 (tous se retirent sauf Fed swap lines ?)
- Post-réforme MMF 2016 (reconfiguration structurelle ?)

### 7.3 Taker/maker par contrepartie

Quand les FB obtiennent des USD : ratio taker/total augmente-t-il en stress ?

---

## 8. Identification

### 8.1 Piliers

| Pilier | Absorbe |
|--------|---------|
| τ_t (effets fixes date) | Tous les chocs communs |
| α_m (effets fixes marché) | Différences permanentes entre paires/tenors |
| CDSAgg_{m,t} | Composante crédit bancaire |
| Z^{EPFR} en contrôle | Composante hedging portefeuille |
| w^{pre}, MMFShare_{m-1} | Prédétermination |

**Précision cruciale :** identification par interaction Exposure^{MMF}_{m,m-1} × FundingShock_t, pas du choc commun seul.

### 8.2 Menaces principales

| Menace | Canal | Réponse |
|--------|-------|---------|
| Dollar shortage global | Commun | τ_t ; variation cross-marché via w^{pre} |
| Crédit bancaire | Spécifique | CDSAgg (mêmes poids que Z) |
| MMFs fournisseurs FX | Offre | Vérifier que MMFs ∉ contreparties FX |
| Rotation prime→gov | Commun | w^{pre} crée variation cross-marché |
| Exclusion cross-sectorielle (DS) | Structurel | Plus hypothétique ; CDSAgg ; présenter comme tel |

### 8.3 Conditions de crédibilité

| Condition | Test |
|-----------|------|
| Premier étage fort | F-stat > 10 |
| Taker > Maker | π^{taker} >> π^{maker} |
| Pas de pre-trends | Z pré-période → ΔPriceUSD non significatif |
| Convention de signe | FB > 0, US banks < 0 en moyenne |
| Market clearing | r_{m,t} ≈ 0 |
| Suridentification | Hansen J |

---

## 9. Prédictions

| # | Prédiction | Partie | Signe attendu |
|---|-----------|--------|---------------|
| P1 | Les FB qui perdent du MMF augmentent leur net USD-taking | 3 | π > 0 ; π^{taker} >> π^{maker} |
| P2 | Cette demande instrumentée rend le dollar synthétique plus cher | 3 | **β > 0** |
| P3 | Les FB sont plus price-inelastic que les HF | 5 | \|β_{FB}\| < \|β_{HF}\| |
| P4 | Les dealers US absorbent la majorité de la demande excédentaire | 4 | Part dealers > 40% |
| P5 | Le price impact est concentré sur les tenors courts | 3, 5 | β plus fort sur tenors courts |
| P6 | Le price impact est amplifié quand les dealers sont contraints | 3, 5 | β₂ > 0 (interaction DealerConstraint) |
| P7 | Le price impact est amplifié en quarter-end | 3, 5 | β₂ > 0 (interaction QE) |
| P8 | Le canal banking (MMF) et hedging (EPFR) ont des price impacts distincts | 5 | γ_{FB}/B ≠ γ_{NBFI}/B |
| P9 | La pression se transmet au spot via tenors courts | 6 | β_S > 0 |

---

## 10. Extensions

### 10.1 Dispersion sectorielle des prix

```
Spread_{s,m,t} = PricePaid_{s,m,t} - PricePaid_{interdealer,m,t}
```

### 10.2 Cross-tenor substitution (DS2)

```
q_{s,k,h,t} = α + Σ_{h'} β_{s,h,h'} PriceUSD_{k,h',t} + γ X + ε
```

### 10.3 Spot FX

```
Δlog S_{k,t} = α_k + τ_t + β_S Q̂^{short}_{FB,k,t} + δ Z^{EPFR}_{k,t} + ε
```

---

## 11. Inférence

| Aspect | Méthode |
|--------|---------|
| SE IV | Two-way clustered (marché × semaine). ~36 marchés → wild cluster bootstrap |
| SE demand system | GMM robust SE ou bootstrap |
| Instrument faible | Kleibergen-Paap > 10 ; Anderson-Rubin si < 10 |
| Suridentification | Hansen J |
| Shift-share | Adão-Kolesár-Morales (2019) en robustesse |

---

## 12. Données

### Disponibles
N-MFP, BankFocus, BIS LBS, FED H.8, EFFR/OBFR, Primary Dealers.

### À obtenir
Transactions FX swaps (réglementaire), CDS bancaires, EPFR, CCBS Bloomberg (validation), Spot FX, Prime/Gov MMF AUM, Fed ON RRP, VIX/MOVE.

---

## 13. Étapes de travail

### Phase A — Données FX
A1–A9 : Convention signe, baseline FX swaps, taker/maker, agrégation cellules, Q_{s,m,t}, r_{m,t}, TIB/PriceUSD, validation vs Bloomberg, matrice d'intermédiation.

### Phase B — Instruments
B1–B9 : poids, MMFShare, FundingShock, Z^{MMF}, Z^{EPFR}, CDSAgg, DealerCapacity.

### Phase C — Diagnostics
C1–C10 : descriptives, contrepartie, dispersion, corrélations, F-stat, pre-trends, validation TIB.

### Phase D — Estimation
D1–D13 : Forme réduite, IV, taker/maker, β > 0, OLS vs IV, hétérogénéités, DS1, décomposition, contrefactuels, extensions.

### Phase E — Robustesse
E1–E15 : Option A, fréquences alternatives, AKM inference, wild bootstrap, Anderson-Rubin, etc.
