# Batch 1 — Fiches théoriques (papiers 1-13)

---

### 1. International Liquidity and Exchange Rate Dynamics
*FileId: 1P-BseOPyff9GLqrzbpDbBwS8wmtTX74w*
*Gabaix & Maggiori, QJE 2015*

#### 1. Environnement et Agents

Deux types d'agents dans une économie à deux pays (Home = États-Unis, Foreign = Japon) :

- **Ménages** (households) dans chaque pays : disposent de dotations en biens et tiennent des portefeuilles d'actifs. Leurs préférences pour les actifs libellés dans leur propre devise génèrent des déséquilibres de flux de capitaux. La demande nette des ménages japonais pour des obligations en dollars constitue l'imbalance exogène $D$ à chaque période.

- **Financiers** (financiers / global intermediaries) : intermédiaires financiers internationaux qui prennent en charge les déséquilibres de portefeuille entre pays. Ils maximisent leur profit sous contrainte de bilan. Leur capacité à absorber le risque de change est limitée par une friction d'engagement limité (limited commitment).

#### 2. Frictions et Contraintes

**Friction centrale : engagement limité (limited commitment)**

La contrainte de bilan du financier est :

$$Q_t = \frac{D_t}{\Gamma}$$

où :
- $Q_t$ = position nette du financier en actifs étrangers (en dollar) ; la quantité d'imbalance que les financiers absorbent
- $D_t$ = demande nette excédentaire des ménages étrangers pour des actifs en dollars (l'imbalance de flux)
- $\Gamma$ = paramètre de capacité de prise de risque des financiers (inverse de l'aversion au risque agrégée des financiers) ; $\Gamma > 0$ : capacité limitée ; $\Gamma = 0$ : capacité illimitée (CIP/UIP tient)

La friction engendre une **courbe de demande de risque à pente négative** : plus l'imbalance $D_t$ est grande, plus le financier doit être compensé pour la prendre en charge, ce qui fait varier le taux de change.

**Demande de change du financier** (condition de premier ordre) :

$$E_t[\Delta e_{t+1}] + (i_t - i^*_t) = \Gamma \cdot Q_t$$

où :
- $E_t[\Delta e_{t+1}]$ = variation espérée du taux de change (dépréciation de la devise étrangère)
- $i_t$ = taux d'intérêt domestique (dollar)
- $i^*_t$ = taux d'intérêt étranger (yen)
- $\Gamma \cdot Q_t$ = prime de risque de change endogène requise par les financiers

Cette équation généralise l'UIP : quand $\Gamma = 0$, l'UIP standard tient ; quand $\Gamma > 0$, une déviation endogène apparaît.

#### 3. Résolution et Équilibre

**Condition de market-clearing** : l'offre nette d'actifs en dollars absorbée par les financiers équilibre la demande excédentaire des ménages :

$$Q_t = D_t / \Gamma$$

**Taux de change d'équilibre** :

$$e_t = \bar{e} - \frac{1}{\Gamma} \cdot D_t + \text{termes stochastiques}$$

où :
- $e_t$ = log du taux de change (prix d'une unité de devise étrangère en dollars)
- $\bar{e}$ = niveau d'équilibre de long terme
- $D_t$ = imbalance financière courante (demande nette de dollars par les agents étrangers)

Plus $D_t$ est élevé (plus les étrangers veulent d'actifs en dollars), plus le dollar s'apprécie ($e_t$ chute).

**Condition UIP généralisée** (déviation endogène) :

$$E_t[e_{t+1}] - e_t = (i^*_t - i_t) + \Gamma \cdot D_t / \text{Wealth}_t$$

#### 4. Mécanisme de Transmission

Un choc $D_t \uparrow$ (hausse de la demande d'actifs en dollars par les ménages étrangers) → les financiers doivent absorber une imbalance plus grande → via la contrainte d'engagement limité ($Q_t = D_t / \Gamma$), le bilan des financiers se dégrade → ils exigent une prime de risque plus élevée → le dollar s'apprécie immédiatement et la volatilité du taux de change augmente.

#### Verdict Critic

VALIDÉE. Les équations clés (demande du financier, contrainte de bilan, condition d'équilibre) sont présentes avec définitions des variables. La friction financière centrale (limited commitment, paramètre $\Gamma$) est bien spécifiée. Le modèle représente le cadre théorique de référence pour toute la littérature sur CIP/FX et sera cité par tous les papiers suivants.

---

### 2. The Spillover of Money Market Turbulence to FX Swap and Cross-Currency Swap Markets
*FileId: 1fgJ3-Vc1qKoW0g-tugWDD4J6LyMy3CGX*
*Baba, Packer & Nagano, BIS Quarterly Review, mars 2008*

#### 1. Environnement et Agents

[EMPIRIQUE — pas de modèle théorique formel]

Article descriptif/empirique analysant la transmission des tensions du marché monétaire américain (2007-2008) aux marchés des FX swaps et cross-currency swaps. Les agents impliqués sont :

- **Institutions financières européennes** : demandeuses nettes de dollars via les FX swaps (côté "dollar borrowing")
- **Contreparties américaines** : fournisseurs de liquidité en dollars via les swaps
- Pas de modèle d'optimisation formelle des agents

#### 2. Frictions et Contraintes

La friction centrale est documentée empiriquement, non dérivée d'un modèle formel :

**Condition CIP (définition de référence utilisée dans le papier)** :

$$\rho_{t,T}^{USD} = i_{t,T}^{USD} - \left(i_{t,T}^{FC} + \frac{F_{t,T} - S_t}{S_t} \cdot \frac{360}{T}\right)$$

où :
- $\rho_{t,T}^{USD}$ = déviation du taux FX swap implicite en dollars par rapport au LIBOR dollar (la "base" CIP)
- $i_{t,T}^{USD}$ = taux d'intérêt en dollars (LIBOR USD pour maturité $T$)
- $i_{t,T}^{FC}$ = taux d'intérêt en devise étrangère (LIBOR EUR ou JPY) pour maturité $T$
- $F_{t,T}$ = taux de change forward à terme $T$ (en USD par unité de devise étrangère)
- $S_t$ = taux de change spot (en USD par unité de devise étrangère)
- $T$ = maturité en jours

Avant août 2007, $\rho \approx 0$. Après août 2007 : $\rho$ atteint 40 pb en septembre 2007, puis des centaines de points de base après la faillite de Lehman.

**Friction identifiée** : flux à sens unique ("one-sided order flow") — les institutions européennes sont concentrées du côté "emprunteur de dollars" dans les FX swaps, ce qui entraîne une prime de liquidité.

#### 3. Résolution et Équilibre

Pas d'équilibre de modèle formel. L'article identifie empiriquement deux canaux de dislocation :

1. **Canal de risque de contrepartie** : $\rho_{t,T}^{USD}$ corrélé négativement avec la solidité financière des banques américaines (mesurée par les CDS spreads américains post-Lehman)
2. **Canal de liquidité de financement** : $\rho_{t,T}^{USD}$ corrélé positivement avec l'écart Libor-OIS (mesure de tension sur le marché monétaire interbancaire)

Régression estimée :
$$\rho_t = \alpha + \beta_1 \cdot \text{LiborOIS}_t + \beta_2 \cdot \text{CDS}_{US,t} + \beta_3 \cdot \text{CDS}_{EU,t} + \varepsilon_t$$

#### 4. Mécanisme de Transmission

Tensions sur le marché monétaire interbancaire américain (mesurées par la hausse du spread LIBOR-OIS) → flux à sens unique des banques européennes demandeuses de dollars via les FX swaps → prime de liquidité dans les FX swaps → déviation persistante de la parité CIP (la base s'élargit).

#### Verdict Critic

VALIDÉE avec mention [EMPIRIQUE]. Pas de modèle théorique formel ; la CIP est utilisée comme benchmark d'absence d'arbitrage. La formule de déviation CIP est bien définie. Article fondateur pour la documentation empirique des dislocations de marché en période de crise.

---

### 3. Global Portfolio Investments and FX Derivatives
*FileId: 1BAeqC4SFZ2eYbO2QXP0BlWIVxjMnhee2*
*Nenova, Schrimpf & Shin, BIS Working Paper No. 1273, juin 2025*

#### 1. Environnement et Agents

- **Investisseurs obligataires internationaux** (advanced economy bond investors) : agents représentatifs qui investissent dans des obligations d'État à 10 ans libellées en dollars ou en devises étrangères et couvrent leur risque de change via des FX swaps. Leur objectif est la maximisation du rendement ajusté du risque, sous contrainte de couverture de change.
- Pas de modélisation explicite de l'intermédiaire financier dans le cadre principal.

#### 2. Frictions et Contraintes

**Modèle de choix de portefeuille** — poids optimal de l'actif en dollars couvert dans le portefeuille global :

$$w^*_{USD,t} = f\left(E_t[r^{US}_{t,t+1}] - r^{US}_{f,t},\; E_t[r^{FC}_{t,t+1}] - r^{FC}_{f,t},\; \text{xcb}_{t},\; \Delta \text{FCI}_t,\; \Delta e_t\right)$$

où :
- $w^*_{USD,t}$ = poids optimal des obligations américaines couvertes dans le portefeuille international
- $E_t[r^{US}_{t,t+1}] - r^{US}_{f,t}$ = rendement excédentaire espéré des obligations US à 10 ans par rapport au taux court en dollars
- $E_t[r^{FC}_{t,t+1}] - r^{FC}_{f,t}$ = rendement excédentaire espéré des obligations en devise étrangère par rapport au taux court local
- $\text{xcb}_{t}$ = cross-currency basis (coût de couverture excédentaire par rapport au différentiel de taux monétaires, i.e., la déviation CIP)
- $\Delta \text{FCI}_t$ = variation des conditions financières globales (proxy de risque)
- $\Delta e_t$ = variations du taux de change en dollars (effets de valorisation)

**Friction** : le coût de couverture $\text{xcb}_t > 0$ réduit l'attractivité des actifs étrangers couverts pour les investisseurs américains (et vice versa pour les étrangers couvrant en dollars).

**Spécification empirique** (régression principale) :

$$\Delta \text{FXDerivatives}_{j,t} = \alpha_j + \beta_1 \cdot \Delta\text{slope}^{US}_{t} + \beta_2 \cdot \Delta\text{slope}^{j}_{t} + \beta_3 \cdot \Delta\text{xcb}_{j,t} + \beta_4 \cdot \Delta\text{FCI}_t + \varepsilon_{j,t}$$

où :
- $\Delta \text{FXDerivatives}_{j,t}$ = variation du volume notionnel des dérivés de change pour la devise $j$ (FX swaps + forwards)
- $\Delta\text{slope}^{US}_{t}$ = variation de la pente de la courbe des taux US (spread 10 ans - 3 mois) ; proxy du rendement excédentaire espéré des obligations US
- $\Delta\text{slope}^{j}_{t}$ = variation de la pente de la courbe des taux du pays $j$
- $j$ = devise (G10 + quelques émergents)
- $\alpha_j$ = effet fixe devise

#### 3. Résolution et Équilibre

Pas d'équilibre de modèle général. Le cadre relie les volumes de dérivés de change observés à l'activité de couverture de portefeuille via le modèle de choix de portefeuille. La condition de premier ordre donne :

$$\frac{\partial w^*}{\partial \text{xcb}} < 0 $$

Une hausse du coût de couverture (base plus négative) réduit la demande de couverture et donc les volumes de FX swaps/forwards.

#### 4. Mécanisme de Transmission

Une pentification de la courbe des taux US ($\Delta\text{slope}^{US} \uparrow$) → rendements obligataires US plus attractifs → entrées de capitaux étrangers dans les obligations US → hausse de la demande de couverture de change → augmentation des volumes de FX swaps/forwards.

#### Verdict Critic

VALIDÉE. Le modèle de choix de portefeuille est simple mais bien défini, avec chaque variable explicitement définie dans la spécification empirique. La friction CIP (cross-currency basis comme coût de couverture) est bien spécifiée. Article récent (2025) qui fournit un cadre empirique pour relier macro (courbe des taux) et micro (volumes de FX derivatives).

---

### 4. Constrained Liquidity Provision in Currency Markets
*FileId: 1MTX696V9u55InuEzDknQKWOsRCs5yPIO*
*Huang, Ranaldo, Schrimpf & Somogyi, Journal of Financial Economics, 2025 (BIS WP 1073, 2022)*

#### 1. Environnement et Agents

- **Dealers (teneurs de marché)** : fournisseurs de liquidité dans les marchés FX. Ils citent des prix bid/ask pour les paires de devises et absorbent les déséquilibres de flux d'ordres. Leur capacité d'intermédiation est contrainte par des limites VaR (Value-at-Risk) et des coûts de financement.
- **Investisseurs / clients** : demandeurs de liquidité FX (côté acheteur). Non modélisés explicitement en tant qu'optimisateurs.

#### 2. Frictions et Contraintes

**Décomposition du coût de liquidité via l'arbitrage triangulaire** :

La relation de no-arbitrage triangulaire entre trois devises (e.g., USD, AUD, JPY) donne :

$$S_{AUD/USD} \cdot S_{JPY/AUD} \cdot S_{USD/JPY} = 1$$

En log : $s_{AUD/USD} + s_{JPY/AUD} + s_{USD/JPY} = 0$

**VLOOP (Violation de la loi du prix unique)** — shadow cost des contraintes d'intermédiation :

$$\text{VLOOP}_t = s^{mid}_{AUD/USD,t} + s^{mid}_{JPY/AUD,t} + s^{mid}_{USD/JPY,t}$$

où :
- $s^{mid}_{i/j,t}$ = log du taux de change mid (moyenne bid-ask) de la paire $i/j$ au temps $t$
- $\text{VLOOP}_t > 0$ : déviation positive de la triangularité → prix incohérents → coût d'opportunité pour les arbitrageurs triangulaires
- Interprétation théorique : $\text{VLOOP}_t$ est une borne inférieure du coût d'ombre des contraintes d'intermédiation des dealers (selon la littérature sur l'asset pricing d'intermédiaires)

**TCOST (coût de transaction aller-retour)** :

$$\text{TCOST}_t = \frac{1}{2}\left(\text{ask}_{AUD/USD,t} - \text{bid}_{AUD/USD,t}\right) + \frac{1}{2}\left(\text{ask}_{JPY/AUD,t} - \text{bid}_{JPY/AUD,t}\right) + \frac{1}{2}\left(\text{ask}_{USD/JPY,t} - \text{bid}_{USD/JPY,t}\right)$$

où $\text{ask}_{i/j,t}$ et $\text{bid}_{i/j,t}$ sont les cotations ask et bid log du dealer pour la paire $i/j$.

**Contrainte d'intermédiation** (formalisation) :

Quand les contraintes sont resserrées (hausse du coût de financement $c_t$ ou des limites VaR $\nu_t$), le dealer réduit son élasticité d'offre de liquidité :

$$\frac{\partial Q^S_t}{\partial \text{TCOST}_t} \cdot \mathbf{1}[\text{constrained}] \ll \frac{\partial Q^S_t}{\partial \text{TCOST}_t} \cdot \mathbf{1}[\text{unconstrained}]$$

où $Q^S_t$ = volume d'intermédiation fourni par les dealers.

#### 3. Résolution et Équilibre

L'équilibre sur le marché de la liquidité FX détermine conjointement le coût de liquidité $\text{TCOST}_t + \text{VLOOP}_t$ et le volume $Q_t$ :

- En régime **non contraint** : forte élasticité de l'offre de liquidité ; relation positive volume-coût standard.
- En régime **contraint** : l'élasticité de l'offre chute d'au moins 80% → le coût de liquidité augmente de façon disproportionnée par rapport au volume.

**Résultat principal** : la non-linéarité vient d'une réduction de l'élasticité de l'offre (supply-side), pas de la demande.

#### 4. Mécanisme de Transmission

Resserrement des contraintes des dealers (hausse des coûts de financement $c_t \uparrow$ ou des limites VaR $\nu_t \uparrow$) → réduction de l'élasticité d'offre de liquidité → via la décomposition VLOOP/TCOST, le coût de liquidité augmente disproportionnellement par rapport au volume → déviations de la loi du prix unique (VLOOP augmente) même sans variation de la demande.

#### Verdict Critic

VALIDÉE. Les deux mesures clés (VLOOP, TCOST) sont dérivées d'une condition de no-arbitrage triangulaire et toutes les variables sont définies. La friction contrainte d'intermédiation est bien spécifiée. Seule limite : la contrainte des dealers est plus décrite fonctionnellement (réduction d'élasticité) que dérivée d'une maximisation explicite.

---

### 5. Segmented Money Markets and CIP Arbitrage
*FileId: 1MPP7cfcYeKq_blJk6yYi9y3JtAEu8CVa*
*Rime, Schrimpf & Syrstad, BIS Working Paper No. 651, 2017*

#### 1. Environnement et Agents

- **Banques tier-1 (top-tier global banks)** : accèdent aux taux de financement les plus bas (taux de la banque centrale, OIS) dans leur devise. Peuvent potentiellement réaliser des arbitrages CIP sans risque.
- **Banques tier-2 et autres institutions** : taux de financement plus élevés (Libor, taux repo, etc.). Pour elles, la déviation CIP apparente est inférieure ou nulle une fois leurs coûts marginaux pris en compte.
- **Dealers de FX swaps** : fixent les prix des FX swaps de façon à équilibrer les flux d'ordres. Leur contrainte de bilan limite leur capacité à fournir des FX swaps à prix arbitrable.

#### 2. Frictions et Contraintes

**Condition CIP généralisée avec coûts marginaux de financement hétérogènes** :

$$\rho^k_t = i^{USD,k}_t - \left(i^{FC,k}_t + \frac{F_t - S_t}{S_t}\right)$$

où :
- $\rho^k_t$ = profit d'arbitrage CIP net pour la banque $k$
- $i^{USD,k}_t$ = taux de financement marginal en dollars pour la banque $k$ (peut être taux OIS, Libor, ou taux repo, selon le segment)
- $i^{FC,k}_t$ = taux de financement marginal en devise étrangère pour la banque $k$
- $F_t$ = taux de change forward (cotation dealer)
- $S_t$ = taux de change spot

**Friction de segmentation** : les marchés monétaires sont segmentés — les taux de financement $i^{USD,k}_t$ varient selon :
1. Le **tier de la banque** (top-tier vs. autres)
2. La **devise** (USD vs. EUR vs. JPY vs. GBP, etc.)
3. L'**instrument** (OIS, Libor, repo, dépôt banque centrale)

**Condition de persistence de l'arbitrage** :

$$\rho^{\text{top-tier}}_t > 0 \quad \text{et} \quad \rho^{\text{tier-2}}_t \leq 0$$

Cela peut survenir en équilibre quand : (a) l'excès de réserves est abondant et rémunéré (e.g., BCE deposit facility), créant des asymétries dans les taux courts selon la devise ; (b) les banques top-tier ont accès à des taux plus bas que les Libor du panel.

**Contrainte de bilan du dealer** (limit-to-arbitrage) :

$$\text{Coût d'opportunité balance sheet} > \rho^k_t \quad \text{pour banques tier-2}$$

Les arbitrages CIP consomment davantage de bilan par dollar de profit espéré que les investissements risqués.

#### 3. Résolution et Équilibre

**Équilibre avec arbitrage persistant** : les dealers fixent les cotations FX swaps $F_t$ de façon à équilibrer leur flux d'ordres (minimiser leur position nette), non à éliminer tout arbitrage. Le résultat est :

$$F_t = S_t \cdot \frac{1 + i^{USD,\text{mid}}_t}{1 + i^{FC,\text{mid}}_t}$$

où $i^{\text{mid}}$ est le taux moyen pondéré des contreparties, non le taux de la banque top-tier.

Ceci implique que la base CIP apparente observée sur taux Libor ($\rho^{\text{Libor}}_t$) surestime les profits d'arbitrage réels pour la plupart des acteurs.

#### 4. Mécanisme de Transmission

Hausse de l'excès de réserves dans la zone euro (rémunéré au taux de dépôt BCE $< 0$) → divergence des taux courts entre zones monétaires → les taux Libor en euros divergent des taux OIS-euro → les dealers ne peuvent pas coter un $F_t$ qui annule la base CIP pour tous les segments simultanément → les banques top-tier bénéficient d'une base CIP positive persistante tandis que les tier-2 ne voient pas d'opportunité.

#### Verdict Critic

VALIDÉE. La condition CIP généralisée avec coûts hétérogènes est bien spécifiée et chaque variable définie. La friction de segmentation (heterogeneous marginal funding rates) est le coeur du modèle. Ce papier est fondamental pour comprendre pourquoi la base CIP mesurée sur Libor surestime l'opportunité d'arbitrage réelle.

---

### 6. Foreign Exchange Swap Liquidity
*FileId: 1I_ATcw2bSo_2nAUdDv0Im-j9qhaKanyT*
*Kloks, Mattille & Ranaldo, BIS Quarterly Review septembre 2023 / SFI Research Paper 23-22*

#### 1. Environnement et Agents

- **Dealers (G-SIBs et autres teneurs de marché)** : fournissent la liquidité dans le marché des FX swaps. Leurs contraintes de bilan (capital réglementaire, limites VaR) s'intensifient autour des dates de reporting trimestriel/annuel. Maximisent leur profit sous contraintes réglementaires.
- **Non-bank financial institutions (NBFIs) et entreprises** : demandeuses de liquidité FX swap pour des besoins de financement à court terme (hedging, financement en dollars).

#### 2. Frictions et Contraintes

**Tightness de la liquidité FX swap** (mesure principale) :

$$\text{Spread}^{\text{FX swap}}_{j,t} = \frac{F^{ask}_{j,t} - F^{bid}_{j,t}}{F^{mid}_{j,t}}$$

où :
- $F^{ask}_{j,t}$, $F^{bid}_{j,t}$, $F^{mid}_{j,t}$ = cotations ask, bid et mid du taux de change forward de la paire $j$ au temps $t$
- Ce spread mesure le coût aller-retour pour les utilisateurs finaux de FX swaps

**Depth de la liquidité** :

$$\text{Depth}_{j,t} = \text{Volume dealer-intermedié}_{j,t}$$

volume total de FX swaps intermédiés par les dealers de la paire $j$ au temps $t$.

**Friction principale — contrainte dealer en fin de trimestre** :

$$\text{Constraint}_{d,t} = \mathbf{1}[\text{G-SIB}_d] \cdot \mathbf{1}[\text{Quarter-end}_t]$$

Interaction entre statut G-SIB du dealer $d$ et date de fin de trimestre $t$ : à ces dates, les G-SIBs réduisent leurs positions FX swap pour alléger leur bilan déclaré (window dressing réglementaire).

**Nouveau canal de demande identifié** :

$$\text{Volume}_{j,t} \uparrow \quad \text{malgré} \quad \text{Liquidity}_{j,t} \downarrow \quad \text{quand} \quad \text{Constraint}_{d,t} = 1$$

Les NBFIs utilisent davantage les FX swaps pour lever des fonds à court terme précisément quand les conditions de liquidité se dégradent (canal de financement "funding channel").

**Lien avec déviation CIP** :

$$\rho_t \propto \text{Spread}^{\text{FX swap}}_t$$

La base cross-currency (déviation CIP) s'élargit quand les spreads FX swap augmentent.

#### 3. Résolution et Équilibre

L'article ne dérive pas d'équilibre de modèle formel. L'équilibre est documenté empiriquement : quand les dealers sont contraints ($\text{Constraint}_{d,t} = 1$), la relation volume-liquidité s'inverse (volume monte, liquidité chute). Cela est cohérent avec un modèle où la demande de financement d'urgence est inélastique au prix.

#### 4. Mécanisme de Transmission

Fin de trimestre → dealers G-SIBs réduisent leur activité FX swap (window dressing) pour abaisser leur bilan déclaré → offre de liquidité FX swap se contracte → spreads s'élargissent → mais la demande de financement des NBFIs est inélastique → volumes augmentent malgré la détérioration de la liquidité → déviations CIP s'amplifient temporairement.

#### Verdict Critic

VALIDÉE avec mention [PRINCIPALEMENT EMPIRIQUE]. Le cadre analytique est descriptif (tightness, depth, canal de financement) sans optimisation formelle. Cependant, les mesures sont bien définies et le mécanisme de transmission est clair. Contribution importante pour comprendre la fragmentation et l'instabilité de la liquidité dans les marchés FX swaps.

---

### 7. Can Time-Varying Currency Risk Hedging Explain Exchange Rates?
*FileId: 12MNGJZlEPOiUD_imIax0Fo-ulX4XKZxu*
*Bräuer & Hau, CESifo WP 10065, 2022*

#### 1. Environnement et Agents

- **Investisseurs institutionnels** (fonds obligataires, assureurs, fonds de pension) : détiennent des positions cross-border en obligations et couvrent leur risque de change via des FX forwards. Leur ratio de couverture $h_t \in [0,1]$ varie avec l'incertitude économique.
- **Intermédiaires financiers (currency traders)** : prennent l'autre côté des demandes de couverture. Leur capacité d'absorption est limitée.

#### 2. Frictions et Contraintes

**Pression de couverture nette (net hedging pressure)** :

$$\text{HP}_{j,t} = h_{j,t} \cdot \text{NFA}^{bond}_{j,t}$$

où :
- $\text{HP}_{j,t}$ = pression de couverture nette pour la devise $j$ au temps $t$ (en milliards USD)
- $h_{j,t}$ = ratio de couverture moyen des investisseurs institutionnels (fraction de la position cross-border couverte)
- $\text{NFA}^{bond}_{j,t}$ = position nette en obligations étrangères libellées en devise $j$ (actif financier net en devise $j$ détenus par résidents)

**Dynamique du ratio de couverture** :

$$h_{j,t} = h_0 + \alpha \cdot \text{VIX}_t + \varepsilon_{j,t}$$

où :
- $h_0$ = ratio de couverture de long terme (constante)
- $\alpha > 0$ = élasticité du ratio de couverture à l'incertitude (VIX)
- $\text{VIX}_t$ = indice de volatilité implicite (mesure d'incertitude / aversion au risque globale)

Quand l'incertitude monte ($\text{VIX} \uparrow$), les investisseurs augmentent leur couverture ($h \uparrow$), créant une pression de vente sur la devise $j$ dans le marché forward.

**Friction d'intermédiation** : la pression de couverture ne peut être absorbée instantanément → prime dans les marchés forward = déviation de la CIP/UIP :

$$f_{j,t} - s_{j,t} - (i_t - i^*_{j,t}) \propto -\text{HP}_{j,t} / \kappa_t$$

où :
- $f_{j,t}$ = log du taux de change forward
- $s_{j,t}$ = log du taux de change spot
- $i_t - i^*_{j,t}$ = différentiel de taux d'intérêt
- $\kappa_t$ = capacité d'absorption des intermédiaires (endogène)

#### 3. Résolution et Équilibre

**Spécification empirique principale (modèle VAR)** :

$$\Delta e_{j,t} = \alpha + \beta \cdot \Delta\text{HP}_{j,t} + \gamma \cdot \Delta\text{HP}_{j,t-1} + \delta \cdot \text{Controls}_{j,t} + \varepsilon_{j,t}$$

Résultat : $\beta < 0$ (une hausse de la pression de couverture de vente de dollars apprécie le dollar).

Les variations de $\text{HP}$ expliquent ~30% de la variation mensuelle des taux de change des 7 principales paires dollar sur 2012-2022.

**Propriété "Giffen"** identifiée : la demande de couverture est une "Giffen good" — quand le dollar s'apprécie, les investisseurs cherchent à vendre moins de dollars (moins de couverture), car la position devient relativement moins exposée.

#### 4. Mécanisme de Transmission

Hausse du VIX ($\text{VIX} \uparrow$) → investisseurs institutionnels augmentent leur ratio de couverture ($h \uparrow$) → pression de couverture nette $\text{HP}_{j,t} \uparrow$ (ventes de dollars forward) → via contrainte d'intermédiation des currency traders, prime dans les forwards → dépréciation des devises non-dollar vis-à-vis du dollar dans le marché spot via le lien forward-spot (arbitrage CIP contraint).

#### Verdict Critic

VALIDÉE. Les équations de HP et du ratio de couverture sont bien définies avec toutes les variables. La friction d'intermédiation (absorption capacity $\kappa_t$) est spécifiée de façon fonctionnelle. Le résultat "Giffen" est une contribution théorique importante. Ce papier lie directement les positions institutionnelles (NFA) à la dynamique du taux de change via le canal de couverture.

---

### 8. FX Swaps and Forwards: Missing Global Debt
*FileId: 14Hof1jFvZppXMQCn79uEOh7tBHtWsa4w*
*Borio, McCauley & McGuire, BIS Quarterly Review, septembre 2017*

#### 1. Environnement et Agents

[PRINCIPALEMENT DESCRIPTIF/ANALYTIQUE — pas de modèle d'optimisation formel]

- **Non-banks hors États-Unis** (compagnies d'assurance, fonds de pension, hedge funds, gestionnaires d'actifs) : s'endettent en dollars "hors bilan" via des FX swaps et forwards pour couvrir leurs positions obligataires en dollars.
- **Banques** : contreparties dans les FX swaps, inscrivent les engagements forward en hors-bilan.

#### 2. Frictions et Contraintes

**Identité comptable centrale** (le "missing debt") :

Un FX swap est **fonctionnellement équivalent à un emprunt sécurisé** (repo) mais n'apparaît pas dans les statistiques standards de dette. La décomposition est :

$$\underbrace{\text{Dollar debt total}_{t}}_{\text{vrai endettement}} = \underbrace{\text{On-balance sheet}_{t}}_{\text{visible dans stats}} + \underbrace{\text{Off-balance sheet FX swap/forward}_{t}}_{\text{"missing debt"}}$$

**Structure d'un FX swap** :

À la date $t=0$ : l'emprunteur reçoit $X$ dollars, livre $X/S_0$ euros (au spot $S_0$).
À la date $t=T$ : l'emprunteur rend $X \cdot (1 + r^{USD}_{T})$ dollars, récupère $X/S_0 \cdot (1 + r^{EUR}_{T})$ euros (au forward $F_T$).

Obligation en dollars implicite :

$$D^{implicit}_{t,T} = X \cdot (1 + r^{USD}_{T})$$

où :
- $X$ = montant en dollars échangé à l'initiation du swap
- $r^{USD}_{T}$ = taux implicite en dollars dans le FX swap
- $S_0$ = taux de change spot à l'initiation
- $F_T$ = taux de change forward à maturité $T$

**Problème de maturité** :

Les FX swaps/forwards ont en général des maturités courtes (< 1 an, souvent 3 mois), tandis que les actifs couverts (obligations) ont des maturités longues → **risque de rollover** systémique :

$$\text{Mismatch}_{t} = \text{Maturité actif}_{t} - \text{Maturité FX swap}_{t} > 0$$

#### 3. Résolution et Équilibre

Pas d'équilibre formel. L'article établit des estimations de l'ampleur :

- Non-banks hors US : ~$25 trillion de dette implicite hors bilan (2022)
- Dont banques non-américaines : ~$39 trillion (incluant positions intra-groupe)
- Le montant dépasse la dette en dollars on-balance sheet (~$10.7 trillion pour non-banks)

**Fragilité financière** :

$$\text{Risque de rollover}_{t} \propto \frac{\text{Off-balance sheet FX swap debt}}{\text{Réserves de change disponibles} + \text{Lignes de swap BC}}$$

#### 4. Mécanisme de Transmission

Stress financier global → non-capacité à renouveler les FX swaps à maturité ($rollover risk \uparrow$) → ventes d'actifs en dollars pour rembourser les obligations implicites en dollars → appréciation du dollar (fire-sale) → amplification pro-cyclique via le bilan des intermédiaires.

#### Verdict Critic

VALIDÉE avec mention [PRINCIPALEMENT DESCRIPTIF]. L'article est analytique/policy-oriented, pas un modèle théorique formel. Cependant, l'identité comptable et la structure du FX swap sont bien formalisées avec définitions des variables. Contribution fondamentale pour la mesure du risque systémique lié aux FX swaps hors bilan.

---

### 9. Global Bank Lending and Exchange Rates
*FileId: 1EZ6sGcoFdlvoL-UVBGkE-YGUNF3HQ2vz*
*Becker, Li, Schmeling & Schrimpf, BIS Working Paper No. 1161, 2024*

#### 1. Environnement et Agents

- **Banques non-américaines (foreign banks)** : accordent des prêts transfrontaliers libellés en dollars (cross-currency dollar loans). Pour financer ces prêts, elles doivent se procurer des dollars sur les marchés de financement (FX swaps, marché interbancaire, marché repo). Leur objectif est de maximiser la valeur de leurs fonds propres sous contrainte de bilan et de levier.
- **Banques américaines** : accordent des prêts en devises étrangères (symétrique mais de moindre ampleur).
- **Marché FX et marché des FX swaps** : transmettent les pressions de financement des banques vers le taux de change.

#### 2. Frictions et Contraintes

**Variable principale — flux de prêts cross-currency nets** :

$$\text{NetLending}^{USD}_{t} = \text{Loans}^{USD}_{\text{foreign banks},t} - \text{Loans}^{FC}_{\text{US banks},t}$$

où :
- $\text{Loans}^{USD}_{\text{foreign banks},t}$ = nouveaux prêts en dollars accordés par des banques non-américaines à l'international
- $\text{Loans}^{FC}_{\text{US banks},t}$ = nouveaux prêts en devises étrangères accordés par des banques américaines
- Quand $\text{NetLending}^{USD}_{t} > 0$ : pression nette d'achat de dollars sur les marchés de financement

**Contrainte de bilan bancaire** :

$$\text{Actifs}_{b,t} = \text{Fonds propres}_{b,t} + \text{Dettes}_{b,t}$$

avec contrainte de levier :
$$\text{Actifs}_{b,t} \leq \lambda_b \cdot \text{Fonds propres}_{b,t}$$

où $\lambda_b$ = ratio de levier maximum de la banque $b$.

Quand une banque étrangère octroie un prêt en dollars, elle doit se financer en dollars, mettant une pression à l'achat sur le dollar dans les marchés FX/FX swap.

**Effet sur le taux de change** (résultat empirique principal) :

$$\Delta e^{USD}_{t} = \alpha + \beta \cdot \Delta\text{NetLending}^{USD}_{t} + \gamma \cdot \text{CIP\_deviation}_{t} + \varepsilon_{t}$$

Magnitude estimée : +1 écart-type de $\text{NetLending}^{USD} \approx +36$ points de base d'appréciation du dollar.

**Lien avec les déviations CIP** :

$$\Delta\text{xcb}_{t} = \alpha + \beta \cdot \Delta\text{NetLending}^{USD}_{t} + \varepsilon_{t}$$

Les prêts cross-currency élargissent également la base CIP (dollar funding premium).

#### 3. Résolution et Équilibre

L'identification causale est obtenue via une **variable instrumentale granulaire (GIV)** :

- Instrument = choc de demande de prêts idiosyncratique à chaque banque (variation de la part de marché liée aux caractéristiques individuelles)
- Permet d'exclure la simultanéité entre taux de change et flux de prêts

L'effet s'est **intensifié après la crise financière mondiale** (GFC 2008), cohérent avec la montée en puissance de la réglementation bancaire et des frictions de bilan post-GFC.

#### 4. Mécanisme de Transmission

Choc de demande de prêts en dollars par une banque étrangère → cette banque achète des dollars (via FX swap ou marché spot) pour financer les prêts → pression à la hausse sur la demande de dollars → dollar s'apprécie (via market-clearing du marché FX) → simultanément, la base CIP (coût du dollar funding) s'élargit, confirmant la pression sur la liquidité dollar.

#### Verdict Critic

VALIDÉE. La variable principale est bien définie. La contrainte de bilan bancaire et son lien avec la demande de dollars sont explicites. L'identification GIV est décrite clairement. Papier central pour le lien banques → taux de change via canal de financement en dollars.

---

### 10. Exchange Rate Determination Under CIP Arbitrage
*FileId: 1fk22EsddXSoh-svZlqybFdyf5KGWsDUY*
*Bacchetta, Davis & van Wincoop, NBER WP 32876, 2024 (Dallas Fed WP 0425)*

#### 1. Environnement et Agents

Modèle à deux pays (Home, Foreign) avec trois types d'agents :

- **Ménages** : détiennent des portefeuilles en actifs domestiques et étrangers. Génèrent les flux de demande d'actifs.
- **Arbitrageurs CIP** (banques / intermédiaires financiers) : peuvent arbitrer les déviations CIP mais font face à des coûts de bilan (leverage constraints, capital requirements). Maximisent le profit sous contrainte.
- **Traders UIP** (hedge funds, investisseurs de portefeuille) : arbitrent les déviations de l'UIP. Aussi sujets à des limites d'arbitrage, mais différentes de celles des arbitrageurs CIP.

#### 2. Frictions et Contraintes

**Marché spot FX** — équilibre :

$$D^{spot}_t(e_t, \rho_t) = 0$$

où :
- $D^{spot}_t$ = demande nette d'actifs étrangers sur le marché spot
- $e_t$ = log du taux de change spot
- $\rho_t$ = déviation CIP (cross-currency basis)

**Marché swap FX** — équilibre :

$$D^{swap}_t(e_t, f_t, \rho_t) = 0$$

où :
- $f_t$ = log du taux de change forward
- $D^{swap}_t$ = demande nette dans le marché des FX swaps

**Déviation CIP** :

$$\rho_t = (i_t - i^*_t) - (f_t - e_t)$$

où :
- $i_t$ = taux d'intérêt en dollars (sans risque)
- $i^*_t$ = taux d'intérêt en devise étrangère (sans risque)
- $(f_t - e_t)$ = prime forward (forward premium)

**Contrainte de bilan des arbitrageurs CIP** :

$$|z^{CIP}_t| \leq \chi_t$$

où :
- $z^{CIP}_t$ = position nette d'arbitrage CIP (taille du portefeuille long-short)
- $\chi_t$ = capacité d'arbitrage (endogène ; dépend du capital réglementaire, de la liquidité, des coûts de financement)

Quand $\chi_t$ est faible (contrainte active) : $\rho_t \neq 0$ en équilibre.

#### 3. Résolution et Équilibre

**Détermination jointe** $(e_t, \rho_t)$ :

Le système de deux équations (marché spot + marché swap) détermine conjointement le taux de change spot et la déviation CIP. La nouveauté par rapport aux modèles antérieurs (Gabaix-Maggiori) :

$$e_t = \mathcal{E}(D^{spot}, D^{swap}, \chi_t, i_t - i^*_t)$$

**Deux résultats principaux** :

1. Les **chocs de marché swap** (variations de la demande de hedging) affectent le taux de change spot — ce canal n'existe pas sous CIP parfait.

2. Les **chocs traditionnels** (politique monétaire, flux de capitaux) ont un **effet amplifié** sur le taux de change grâce à la rétroaction spot → swap.

**Comparaison avec CIP parfait** : si $\chi_t \to \infty$ (capacité d'arbitrage illimitée), $\rho_t = 0$ et on retrouve les modèles standards. Si $\chi_t$ est fini et variable, le taux de change est affecté par une nouvelle classe de chocs financiers.

#### 4. Mécanisme de Transmission

Choc de demande de hedging (hausse de la demande de FX forward d'une devise) → sur le marché des FX swaps, pression à l'élargissement de la base CIP ($\rho_t \uparrow$) → via la contrainte $|z^{CIP}_t| \leq \chi_t$, les arbitrageurs ne peuvent pas éliminer complètement la base → la rétroaction swap → spot amplifie l'impact sur $e_t$ → taux de change spot se déplace en réponse à des chocs purement financiers (non fondamentaux).

#### Verdict Critic

VALIDÉE. La structure du modèle (deux marchés, trois types d'agents, contrainte d'arbitrage) est bien exposée. Les équations d'équilibre spot et swap et la formule de déviation CIP sont bien définies avec toutes les variables. C'est le modèle le plus complet disponible pour la détermination jointe du taux de change et de la base CIP.

---

### 11. The Hedging Channel of Exchange Rate Determination
*FileId: 19see67m68Tf4McqPsvUmSpm3YJZEoQ8M*
*Liao & Zhang, Review of Financial Studies 38(1), 2025 (IFDP 1283, Fed)*

#### 1. Environnement et Agents

Modèle à $N$ pays. Deux types d'agents :

- **Investisseurs** (représentatifs par pays $i$) : détiennent des positions nettes en actifs étrangers ("external imbalances" ou NFA). Quand l'incertitude de change augmente, ils augmentent leur couverture en proportion de leur imbalance. Ils maximisent l'utilité espérée d'une richesse finale :

$$U_i = E_0[W_{i,T}] - \frac{a}{2} \text{Var}_0[W_{i,T}]$$

où :
- $W_{i,T}$ = richesse terminale de l'investisseur du pays $i$
- $a$ = coefficient d'aversion au risque (identique entre investisseurs par hypothèse)

- **Currency traders** (teneur de marché/intermédiaire) : prennent l'autre côté des demandes de couverture. Contrainte de bilan limitant leur capacité d'absorption.

#### 2. Frictions et Contraintes

**Demande de couverture (hedging demand)** — l'investisseur avec imbalance nette $B_i$ en devise $j$ couvre en proportion de sa variance espérée :

$$H_{ij,t} = h_t \cdot B_{ij,t}$$

où :
- $H_{ij,t}$ = position de couverture nette vendue (forward) par l'investisseur $i$ sur la devise $j$
- $h_t = a \cdot \text{Var}_t[e_{j,t+1}]$ = ratio de couverture optimal (dépend de l'aversion au risque $a$ et de la variance conditionnelle du taux de change)
- $B_{ij,t}$ = imbalance nette en devise $j$ de l'investisseur du pays $i$ (NFA)

**Contrainte de bilan du currency trader** :

$$\sum_{j} |F_{j,t}| \leq \Phi_t$$

où :
- $F_{j,t}$ = position forward nette du trader sur la devise $j$
- $\Phi_t$ = capacité totale d'absorption du trader (contrainte endogène, se resserre en période de stress)

**Relation forward-spot avec friction d'intermédiation** :

$$f_{j,t} - s_{j,t} - (i_t - i^*_{j,t}) = \frac{1}{\Phi_t} \cdot \sum_i H_{ij,t}$$

où :
- $f_{j,t}$ = log du taux forward pour la devise $j$
- $s_{j,t}$ = log du taux spot pour la devise $j$
- $i_t - i^*_{j,t}$ = différentiel de taux d'intérêt
- Le terme de droite = déviation CIP endogène proportionnelle à la pression de couverture agrégée et à la contrainte du trader

#### 3. Résolution et Équilibre

**Condition de market-clearing** sur le marché forward de la devise $j$ :

$$\sum_i H_{ij,t} + F_{j,t} = 0$$

**Taux de change spot d'équilibre** :

$$s_{j,t} = \bar{s}_{j} - \frac{1}{\Phi_t} \cdot B^{net}_{j,t} \cdot h_t$$

où $B^{net}_{j,t} = \sum_i B_{ij,t}$ = imbalance globale nette en devise $j$.

**Deux propositions principales** :

1. Les pays avec imbalance positive ($B^{net} > 0$) voient leur devise **s'apprécier** quand la variance espérée $\text{Var}_t[e]$ augmente (donc $h_t \uparrow$) : les investisseurs couvrent leur exposition et achètent leur propre devise forward.

2. Les pays avec imbalance négative voient leur devise **se déprécier** dans le même contexte.

#### 4. Mécanisme de Transmission

Hausse de la volatilité espérée ($\text{Var}_t[e] \uparrow$, proxy : VIX) → investisseurs augmentent leur ratio de couverture ($h_t \uparrow$) → demande de couverture $H_{ij,t} \uparrow$ pour les devises avec imbalances significatives → pression sur les marchés forwards → via la contrainte du currency trader ($\Phi_t$ finie), prime sur les forwards → transmission au marché spot via arbitrage CIP contraint → le taux spot est déterminé conjointement par les imbalances externes ($B^{net}$) et la volatilité ($h_t$).

#### Verdict Critic

VALIDÉE. Toutes les équations sont définies avec précision : la fonction d'utilité des investisseurs, le ratio de couverture $h_t$, la contrainte du trader $\Phi_t$, la condition de market-clearing forward, et le taux spot d'équilibre. Ce modèle est théoriquement le plus rigoureux pour le "hedging channel" et directement comparable au modèle de Gabaix-Maggiori (dont il constitue une extension multi-pays avec canal de couverture explicite).

---

### 12. Risk and Resilience in the Global FX Market
*FileId: 1vYrkCeoxMxD4i4Q9dt2Bz55EaUKRxM3Q*
*IMF Global Financial Stability Report, Chapitre 2, octobre 2025*

#### 1. Environnement et Agents

[PRINCIPALEMENT ANALYTIQUE/POLICY — modèle formel limité]

- **Dealers FX** : teneurs de marché principaux, sujets à des contraintes de bilan. Leur retrait réduit la liquidité du marché.
- **Non-bank financial institutions (NBFIs)** : fonds, assureurs, gestionnaires d'actifs. Détiennent des positions FX importantes et utilisent des FX swaps pour la couverture.
- **Banques centrales** : fournissent des lignes de swap en dollars en dernier recours.

#### 2. Frictions et Contraintes

**Mesure de la pression de couverture (hedging pressure)** :

$$\text{HP}_{j,t} = \frac{\text{Net short FX swap position NBFIs}_{j,t}}{\text{Total outstanding FX swap market}_{j,t}}$$

où :
- $\text{HP}_{j,t}$ = pression de couverture nette des NBFIs pour la devise $j$ au temps $t$
- Au numérateur : position nette vendeuse de devises $j$ des NBFIs dans le marché des FX swaps (besoin de couverture)
- Au dénominateur : taille totale du marché des FX swaps pour la devise $j$

**Vulnérabilités structurelles identifiées** :

1. **Currency mismatch** :

$$\text{Mismatch}_{k,t} = \text{Assets}^{FC}_{k,t} - \text{Liabilities}^{FC}_{k,t}$$

déséquilibre entre actifs et passifs libellés en devises étrangères des intermédiaires $k$.

2. **Concentration des dealers** :

$$\text{HHI}_{j,t} = \sum_{d} \left(\frac{\text{Volume}_{d,j,t}}{\text{Total Volume}_{j,t}}\right)^2$$

indice Herfindahl-Hirschman de concentration des dealers pour la devise $j$.

3. **Participation des NBFIs** :

$$\text{NBFI Share}_{j,t} = \frac{\text{FX volume NBFIs}_{j,t}}{\text{Total FX volume}_{j,t}}$$

**Amplification** : les déséquilibres ci-dessus amplifient les effets d'un choc initial sur le marché FX.

#### 3. Résolution et Équilibre

Pas d'équilibre de modèle formel. Le chapitre fournit :

- Régressions de panel : impact de $\text{HP}_{j,t}$ sur la volatilité et les spreads FX
- Cohérence avec les résultats de Bräuer et Hau (2023) sur le canal de couverture
- Exercices de scénarios de stress pour évaluer la résilience

**Résultat empirique central** :

$$\Delta \sigma^{FX}_{j,t} = \alpha + \beta \cdot \Delta\text{HP}_{j,t} + \gamma \cdot \text{Constraint}_{d,t} + \delta \cdot \text{Structural vulnerability}_{j,t} + \varepsilon_{j,t}$$

où $\sigma^{FX}_{j,t}$ = volatilité du taux de change pour la devise $j$.

#### 4. Mécanisme de Transmission

Choc macro-financier (hausse de l'incertitude globale) → hausse de la demande de couverture des NBFIs ($\text{HP} \uparrow$) → dealers contraints ne peuvent absorber entièrement → via concentration élevée et currency mismatch des intermédiaires, la liquidité FX se dégrade → volatilité des taux de change augmente → risque de stress systémique si le dollar se renforce simultanément (aggravation des mismatch).

#### Verdict Critic

VALIDÉE avec mention [PRINCIPALEMENT EMPIRIQUE/POLICY]. Pas de modèle d'optimisation formel. Cependant, les mesures de vulnérabilités structurelles (HP, mismatch, HHI, NBFI share) sont bien définies. Le chapitre constitue une synthèse de politique utile intégrant plusieurs canaux de transmission documentés dans la littérature (Bräuer-Hau, Kloks-Ranaldo, etc.).

---

### 13. Covered Interest Parity Lost: Understanding the Cross-Currency Basis
*FileId: 118ONDm9_65pvflNN-SjBA2tCtYGCS9mc*
*Borio, McCauley, McGuire & Sushko, BIS Quarterly Review, septembre 2016*

#### 1. Environnement et Agents

- **Hedgers** (investisseurs cross-border, notamment japonais et européens) : détiennent des obligations en dollars et couvrent leur risque de change via des FX swaps/cross-currency swaps. Génèrent une demande structurelle de dollars forward.
- **Arbitrageurs (CIP traders)** : banques ou hedge funds qui tentent d'exploiter les déviations de la CIP. Contraints par leurs coûts de bilan.
- **Dealers** : fournissent la liquidité ; leur capacité est limitée par les coûts de bilan post-réglementation.

#### 2. Frictions et Contraintes

**Définition de la base cross-currency (CIP deviation)** :

$$b^{FC/USD}_{t,T} = i^{FC}_{t,T} - i^{USD}_{t,T} + \frac{F_{t,T} - S_t}{S_t}$$

Reformulation en termes de coût de couverture :

$$b^{FC/USD}_{t,T} = \rho^{FC}_{t,T} - \rho^{USD}_{t,T}$$

où :
- $b^{FC/USD}_{t,T}$ = base cross-currency (déviation CIP) pour la paire FC/USD à maturité $T$
- $i^{FC}_{t,T}$ = taux d'intérêt en devise étrangère (OIS, maturité $T$)
- $i^{USD}_{t,T}$ = taux d'intérêt en dollars (OIS, maturité $T$)
- $F_{t,T}$ = taux forward
- $S_t$ = taux spot
- Une base négative ($b < 0$) signifie que le financement en dollars via FX swap coûte plus que le taux dollar direct

**Demande de couverture (hedging demand)** :

$$\text{HD}^{FC/USD}_{t} = \text{Actifs en USD détenus par investisseurs FC} \times h_t$$

où :
- $h_t$ = ratio de couverture des investisseurs (fraction des actifs en dollars couverts)
- $\text{HD}$ = quantité de dollars forward achetés par les investisseurs étrangers (pression sur la base)

**Coût de bilan des arbitrageurs** (limits to arbitrage) :

$$\text{Coût d'arbitrage CIP}_t = \rho_t^{\text{RWA}} + \rho_t^{\text{leverage}} + \rho_t^{\text{funding}}$$

où :
- $\rho_t^{\text{RWA}}$ = coût lié aux exigences de fonds propres pondérés par le risque (Basel III)
- $\rho_t^{\text{leverage}}$ = coût lié au ratio de levier (Supplementary Leverage Ratio)
- $\rho_t^{\text{funding}}$ = coût de financement à court terme

Les banques n'arbitrent que si $|b_{t,T}| > \text{Coût d'arbitrage CIP}_t$.

#### 3. Résolution et Équilibre

**Condition d'équilibre** (proposée par les auteurs) :

$$b^{FC/USD}_{t,T} \approx -\gamma \cdot \frac{\text{HD}^{FC/USD}_{t}}{\text{Capacité d'arbitrage}_{t}}$$

où $\gamma$ = paramètre de sensibilité prix de la base à la demande de couverture.

Avec $\gamma > 0$ : plus la demande de couverture est élevée et plus la capacité d'arbitrage est réduite, plus la base est négative (dollar premium plus cher via FX swap).

**Spécification empirique** (régression centrale de l'article) :

$$b^{j/USD}_{t} = \alpha_j + \beta_1 \cdot \text{HD}^{j}_{t} + \beta_2 \cdot \text{BalanceSheetCost}_{t} + \varepsilon_{j,t}$$

Résultat : $\hat{\beta}_1 < 0$ et $\hat{\beta}_2 < 0$ (base plus négative quand HD est élevée et coûts de bilan élevés).

#### 4. Mécanisme de Transmission

Hausse de la demande de couverture de change des investisseurs étrangers ($\text{HD} \uparrow$, e.g., investisseurs japonais couvrant des positions en obligations US) → pression à l'achat de dollars forward → via les coûts de bilan élevés des arbitrageurs post-réforme réglementaire ($\text{Coût d'arbitrage CIP} \uparrow$), les banques n'arbitrent pas suffisamment → la base cross-currency devient plus négative (financement en dollars via FX swap plus coûteux) → persistance de la déviation CIP.

#### Verdict Critic

VALIDÉE. La formule de la base cross-currency est bien définie avec toutes les variables. La décomposition du coût d'arbitrage en composantes réglementaires est explicite. La condition d'équilibre reliant base, demande de couverture et capacité d'arbitrage est bien spécifiée. Article fondateur pour la compréhension post-crise des déviations CIP, cité par l'ensemble de la littérature sur la base cross-currency.

---
