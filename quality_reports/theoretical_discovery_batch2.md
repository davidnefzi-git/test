# Batch 2 — Fiches théoriques (papiers 14-39)

---

### 14. Synthetic Dollar Funding
*FileId: 1s0NQFGteSb7AIjleRFhj1EARa6RMvMez*

#### 1. Environnement et Agents
Deux types d'agents : (i) **banques mondiales non-américaines** (global banks) qui financent leurs actifs en dollars soit par emprunt direct sur le marché monétaire de gros (wholesale), soit par FX swap (dollars synthétiques) ; (ii) **institutions non-bancaires** (fonds, assureurs) qui achètent des couvertures de change. Les banques maximisent le profit sous contrainte de bilan et de financement.

#### 2. Frictions et Contraintes
Friction centrale : accès limité au financement de gros en dollars. Lorsque l'offre de wholesale dollars se raréfie, les banques se substituent vers les FX swaps.

**Contrainte de substitution optimale** : la banque i choisit le mix (wholesale, swap) pour minimiser son coût de financement sous la contrainte que le coût marginal du dollar synthétique est croissant avec la quantité demandée :

$$r^{swap}_{t} = r^{wholesale}_{t} + \alpha \cdot D^{swap}_{t} + \varepsilon_t$$

- $r^{swap}_{t}$ : taux implicite du dollar synthétique via FX swap à la date $t$
- $r^{wholesale}_{t}$ : taux de financement de gros en dollar direct
- $\alpha$ : élasticité du coût marginal à la demande de swaps (offre imparfaitement élastique)
- $D^{swap}_{t}$ : volume net de dollars synthétiques demandés par les banques mondiales
- $\varepsilon_t$ : choc de demande de couverture des non-banques

**Déviation CIP en équilibre** : la déviation de la parité couverte des taux d'intérêt est proportionnelle à l'excès de demande de swaps :

$$x_t = r^{USD}_{t} - r^{FX}_{t} - (F_t - S_t)/S_t$$

- $x_t$ : déviation CIP (cross-currency basis), négative lorsque les dollars synthétiques sont chers
- $r^{USD}_t$ : taux d'intérêt dollar (LIBOR/SOFR)
- $r^{FX}_t$ : taux d'intérêt en devise étrangère
- $F_t$ : taux de change à terme
- $S_t$ : taux de change au comptant

#### 3. Résolution et Équilibre
La demande de swaps est instrumentée par des variations idiosyncratiques de l'offre de wholesale dollars (chocs exogènes). En équilibre partiel, l'offre de dollars synthétiques est imparfaitement élastique : une augmentation de 10 % de la demande nette de swaps élargit la base de 7 points de base. L'auteur calibre les paramètres empiriques pour simuler : une chute brutale du wholesale funding peut plus que doubler la déviation CIP et renchérit le crédit mondial en dollars.

#### 4. Mécanisme de Transmission
Choc de raréfaction du wholesale dollar → substitution bancaire vers les FX swaps → offre imparfaitement élastique de dollars synthétiques → déviation CIP (basis négative) → renchérissement du hedging pour les non-banques → contraction du crédit mondial en dollars.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière spécifique (inélasticité de l'offre de swaps) avec des équations structurelles et un mécanisme de transmission identifié. Les variables sont définies.

---

### 15. FX Spot and Swap Market Liquidity Spillovers
*FileId: 1d39fmKAujQbdLIPZElWbfAiJyCQ6Ty0U*

#### 1. Environnement et Agents
Agents : **teneurs de marché** (dealing desks des G-SIBs) actifs dans les deux segments — marché au comptant FX (spot) et marché des swaps FX. Les teneurs de marché gèrent leur inventaire sous contrainte de capital réglementaire. Les clients (banques buy-side, fonds) génèrent flux d'ordres.

#### 2. Frictions et Contraintes
Friction principale : le coût de liquidité de financement (funding liquidity) contraint la capacité des teneurs de marché à absorber le flux d'ordres dans les deux marchés simultanément. Les G-SIBs proches de leurs minima réglementaires de capital se retirent périodiquement du pricing des FX swaps.

**Contrainte de capital (leverage ratio)** :

$$\text{Assets}_i \leq \frac{1}{k} \cdot \text{Equity}_i$$

- $\text{Assets}_i$ : taille du bilan du teneur de marché $i$
- $k$ : exigence minimale de ratio de levier (regulatory minimum)
- $\text{Equity}_i$ : fonds propres du teneur de marché $i$

**Écart bid-ask du swap** croissant avec l'inventaire et la contrainte :

$$\text{Spread}^{swap}_{i,t} = f(\text{InventoryRisk}_{i,t}, \mathbf{1}[\text{ConstraintBinding}_{i,t}])$$

- $\text{Spread}^{swap}_{i,t}$ : écart bid-ask du FX swap du teneur $i$ au temps $t$
- $\text{InventoryRisk}_{i,t}$ : risque d'inventaire en devise étrangère
- $\mathbf{1}[\text{ConstraintBinding}_{i,t}]$ : indicateur de contrainte réglementaire active

#### 3. Résolution et Équilibre
Quand les grands teneurs de marché se retirent, les petits dealers ne compensent pas pleinement, maintenant la liquidité des swaps dégradée. Cela se transmet au marché spot via la relation de no-arbitrage entre les prix spot et les taux implicites des swaps. Le lien funding-liquidité / liquidité de marché s'est renforcé post-2008.

#### 4. Mécanisme de Transmission
Contrainte de capital active pour G-SIBs → retrait du pricing des FX swaps → écarts bid-ask élargis dans les swaps → illiquidité transmise au marché spot FX via parité swap-spot → co-mouvement des liquidités des deux segments.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière spécifique (contrainte de capital réglementaire des G-SIBs) avec un mécanisme de transmission entre marchés. Principalement empirique mais avec un cadre théorique identifié.

---

### 16. The Failure of Covered Interest Parity: FX Hedging Demand and Costly Balance Sheets
*FileId: 1KW5Gk86qtpiDFLyM5BAb4KPoEQ81AWDl*

#### 1. Environnement et Agents
Deux types d'agents : (i) **hedgers** (institutions financières non-bancaires — assureurs, fonds de pension) qui ont besoin de couvrir leur exposition de change en vendant des devises à terme ; (ii) **arbitrageurs CIP** (banques) qui fournissent la couverture en achetant la devise à terme, en devant immobiliser du bilan.

#### 2. Frictions et Contraintes
Friction centrale : le coût de bilan (balance sheet cost) rend l'arbitrage CIP coûteux à grande échelle, car tous les dérivés FX sont traités OTC, exposant les contreparties au risque de collatéral.

**Condition de no-arbitrage avec coût de bilan** :

$$x_t = r^*_t - r_t + \frac{F_t - S_t}{S_t} = -\lambda \cdot \Phi_t$$

- $x_t$ : déviation CIP (basis cross-currency)
- $r^*_t$ : taux d'intérêt étranger (ex : taux LIBOR USD)
- $r_t$ : taux d'intérêt domestique
- $F_t$ : taux de change à terme (forward)
- $S_t$ : taux de change au comptant (spot)
- $\lambda$ : coût marginal d'immobilisation du bilan (lié au risque de collatéral FX)
- $\Phi_t$ : volume de couverture de change net fourni par les arbitrageurs

**Demande de hedging** qui détermine le volume :

$$\Phi_t = \beta_0 + \beta_1 \cdot \text{HedgingDemand}_t + \varepsilon_t$$

- $\text{HedgingDemand}_t$ : mesure agrégée de la demande de couverture (ex : déséquilibres d'actifs entre zones monétaires)

#### 3. Résolution et Équilibre
En équilibre, la déviation CIP est déterminée par l'intersection entre la demande de couverture (pentue, inélastique) et la courbe d'offre ascendante des arbitrageurs. Une plus forte demande de hedging conduit à des déviations CIP plus négatives. La demande de hedging combinée à des proxies de risque de collatéral améliore significativement le pouvoir explicatif des régressions standards.

#### 4. Mécanisme de Transmission
Choc de demande de couverture de change (ex : augmentation des actifs en USD des assureurs japonais) → les arbitrageurs doivent immobiliser davantage de bilan pour fournir la couverture → coût marginal de bilan plus élevé → déviation CIP plus négative.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière spécifique (coût de bilan OTC / risque de collatéral) avec des équations structurelles liant demande de hedging et déviation CIP. Variables définies.

---

### 17. Quantities and Covered-Interest Parity
*FileId: 1ctx6MwhxCPd7SqjhkH4_cWqCIYT4kFbL*

#### 1. Environnement et Agents
Agents : (i) **arbitrageurs spécialisés** (primary dealers, grandes banques) qui exploitent les déviations CIP en empruntant dans une devise et prêtant via FX swap dans l'autre ; (ii) **hedgers** (investisseurs institutionnels) qui génèrent la demande nette de swap. Les arbitrageurs font face à des coûts croissants avec la taille de leur position.

#### 2. Frictions et Contraintes
Friction centrale : les arbitrageurs font face à des coûts marginaux croissants d'expansion du bilan (risque de déséquilibre, coûts réglementaires). La déviation CIP reflète à la fois la quantité arbitrée et le coût marginal de l'arbitrage.

**Offre d'arbitrage CIP** (courbe d'offre montante) :

$$x_t = \gamma \cdot Q^{arb}_t + \eta_t$$

- $x_t$ : déviation CIP (cross-currency basis)
- $Q^{arb}_t$ : quantité nette d'arbitrage CIP exécuté par les arbitrageurs
- $\gamma$ : coût marginal de l'arbitrage (pente de la courbe d'offre d'arbitrage) ; $\gamma > 0$
- $\eta_t$ : choc sur les coûts d'arbitrage

**Demande nette de swap** par les hedgers :

$$Q^{arb}_t = D^{hedge}_t - Q^{non-arb}_t$$

- $D^{hedge}_t$ : demande brute de couverture FX des hedgers
- $Q^{non-arb}_t$ : substitution non-arbitrage de la demande (autres intermédiaires)

#### 3. Résolution et Équilibre
L'équilibre de marché exige que la quantité d'arbitrage égale la demande nette de hedging. La déviation CIP est ainsi déterminée conjointement par les quantités et les prix. Le papier identifie empiriquement la courbe d'offre d'arbitrage en utilisant des variations de demande de hedging comme instruments, permettant d'estimer le $\gamma$ structurel.

#### 4. Mécanisme de Transmission
Augmentation de la demande de couverture FX → quantité d'arbitrage doit augmenter → coût marginal d'arbitrage monte → basis CIP s'élargit proportionnellement à la quantité d'arbitrage via $\gamma$.

#### Verdict Critic
VALIDÉE — Le modèle propose une structure d'offre et demande explicite avec des équations liant quantités et prix de la déviation CIP. La friction (coût marginal croissant d'arbitrage) est financièrement spécifique. Variables définies.

---

### 18. Breaking Parity: Equilibrium Exchange Rates and Currency Premia
*FileId: 1gGXA_vCtT3fhfe_toBbKkoFvHk11QuXo*

#### 1. Environnement et Agents
Agents : (i) **ménages** de différents pays qui détiennent des actifs dans leur devise locale et cherchent à investir à l'étranger ; (ii) **banques intermédiaires** (dealers) qui fournissent l'accès aux devises étrangères couvertes (hedged) et non couvertes (unhedged), soumises à des contraintes de bilan de type Value-at-Risk (VaR). Les banques maximisent le profit sous contrainte VaR.

#### 2. Frictions et Contraintes
Friction centrale : les banques intermédiaires sont soumises à des contraintes VaR sur leurs positions nettes en devises.

**Contrainte VaR de la banque intermédiaire** :

$$\sigma_t \cdot |P^{net}_{i,t}| \leq \kappa \cdot W_{i,t}$$

- $\sigma_t$ : volatilité du taux de change
- $P^{net}_{i,t}$ : position nette en devise de la banque $i$ au temps $t$
- $\kappa$ : paramètre de tolérance au risque (VaR fraction)
- $W_{i,t}$ : richesse (capital) de la banque intermédiaire $i$

**Primes de change couvertes (CIP deviation)** et non couvertes (UIP deviation) :

$$\text{CIP}_t = f(\text{NetFXPosition}_t, \sigma_t, W_t)$$
$$\text{UIP}_t = g(\text{NetFXPosition}_t, \sigma_t, W_t)$$

- $\text{CIP}_t$ : déviation de parité couverte (cross-currency basis)
- $\text{UIP}_t$ : prime de risque de change non couverte
- $\text{NetFXPosition}_t$ : position nette agrégée en devises des banques
- $W_t$ : capital agrégé des banques intermédiaires

**Déterminant cross-sectionnel** — l'excès d'offre d'épargne en devise locale :

$$\text{CIP}_{c} \propto -\text{ExcessSavings}_c$$

- $\text{ExcessSavings}_c$ : excès d'offre d'épargne en devise du pays $c$ (proxy : position nette futures FX des dealers)

#### 3. Résolution et Équilibre
En équilibre partiel, la banque intermédiaire détermine le prix de la devise couverte et non couverte de sorte que sa contrainte VaR ne soit pas violée. En coupe transversale, les pays avec excès d'épargne en devise locale ont des taux d'intérêt bas, des primes CIP et UIP négatives, et des dollars à terme bon marché. En série temporelle, les primes couvertes évoluent peu fréquemment et conjointement, guidées par les conditions financières agrégées.

#### 4. Mécanisme de Transmission
Excès d'épargne en devise locale du pays $c$ → offre excédentaire de cette devise vers les banques intermédiaires → contrainte VaR détermine la prime exigée → prime CIP négative et dollar forward bon marché pour le pays $c$.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière précise (contrainte VaR des banques intermédiaires), des équations liant primes de change aux positions nettes et à la richesse. Variables définies. C'est un modèle d'équilibre partiel unificateur des primes CIP et UIP.

---

### 19. Deviations from Covered Interest Rate Parity
*FileId: 1nLBlNhipsu2Evpu1_M_LgiB_v6ASgLUQ*

#### 1. Environnement et Agents
Agents : (i) **arbitrageurs CIP** (grandes banques internationales) qui, en l'absence de friction, élimineraient instantanément toute déviation ; (ii) **investisseurs** qui détiennent des obligations en devise étrangère couverte. En présence de contraintes réglementaires, l'arbitrage est limité.

#### 2. Frictions et Contraintes
Friction centrale : le ratio de levier réglementaire (Basel III leverage ratio) empêche les banques d'exploiter pleinement les déviations CIP en agrandissant leur bilan.

**Déviation CIP (cross-currency basis)** pour la paire de devises $i$ vs USD :

$$x_{i,t} = \rho_{i,t} + F_{i,t} - S_{i,t} - \rho^{USD}_t$$

- $x_{i,t}$ : déviation CIP pour la devise $i$ (négatif = dollar synthétique plus cher)
- $\rho_{i,t}$ : taux d'intérêt sans risque en devise $i$ (OIS)
- $F_{i,t}$ : logarithme du taux de change à terme (forward)
- $S_{i,t}$ : logarithme du taux de change au comptant (spot)
- $\rho^{USD}_t$ : taux d'intérêt sans risque en USD (OIS)

**Contrainte de ratio de levier** qui limite l'arbitrage :

$$\frac{\text{TierOneCapital}_{b,t}}{\text{TotalExposure}_{b,t}} \geq \ell$$

- $\text{TierOneCapital}_{b,t}$ : capital Tier 1 de la banque $b$ au temps $t$
- $\text{TotalExposure}_{b,t}$ : exposition totale au sens du ratio de levier
- $\ell$ : seuil réglementaire minimum (3% pour Basel III)

**Coût implicite de l'arbitrage CIP** (de la banque) :

$$\text{Cost}^{arb}_{b,t} = \rho^{USD}_t \cdot \frac{\Delta\text{Exposure}_{b,t}}{\text{TierOneCapital}_{b,t}} \cdot \text{ShadowCost}_{b,t}$$

- $\text{ShadowCost}_{b,t}$ : coût implicite du levier réglementaire pour la banque $b$

#### 3. Résolution et Équilibre
Les déviations CIP persistent car l'arbitrage est coûteux en termes de bilan. Du, Tepper, et Verdelhan documentent des déviations systématiques, larges et persistantes, particulièrement prononcées aux fins de trimestre (quand les banques fenêtrent leurs bilans) — ce qui confirme que la contrainte réglementaire est la friction dominante.

#### 4. Mécanisme de Transmission
Contrainte de ratio de levier binding pour les banques → coût d'expansion du bilan pour exécuter l'arbitrage CIP → déviations CIP persistent et sont plus grandes pour les monnaies où les banques ont déjà des positions importantes.

#### Verdict Critic
VALIDÉE — Le modèle contient la friction clé (ratio de levier réglementaire), avec une définition précise de la déviation CIP et du coût implicite de l'arbitrage. Variables toutes définies. Article fondamental.

---

### 20. The Dollar, Bank Leverage and the Deviation from CIP
*FileId: 1Wd6OB2bjGYmTqMfvDPuwXq_tLYwKhyj6*

#### 1. Environnement et Agents
Agents : (i) **banques mondiales** (US et non-US) qui effectuent des opérations de prêt transfrontalières en dollars ; (ii) **arbitrageurs CIP** dont la capacité d'arbitrage dépend du levier bancaire agrégé. Le papier examine une relation triangulaire : dollar fort ↔ déviation CIP large ↔ contraction du crédit transfrontalier.

#### 2. Frictions et Contraintes
Friction centrale : le ratio de levier bancaire réglementaire (leverage ratio) est la contrainte dominante pour l'arbitrage CIP à court terme.

**Relation triangulaire empirique** :

$$x_t = \alpha + \beta_1 \cdot \Delta e_t + \beta_2 \cdot \Delta \text{Leverage}_t + \varepsilon_t$$

- $x_t$ : déviation CIP (cross-currency basis)
- $\Delta e_t$ : variation du taux de change dollar (appréciation = $\Delta e_t > 0$)
- $\Delta \text{Leverage}_t$ : variation du levier bancaire agrégé
- $\beta_1 < 0$ : un dollar plus fort est associé à une basis plus négative
- $\beta_2 > 0$ : un levier plus élevé est associé à une basis plus négative

**Mécanisme de levier** :

L'arbitrage CIP canonique requiert d'emprunter des dollars au comptant et de les prêter via FX swap, ce qui **élargit le bilan** de la banque et resserre le ratio de levier :

$$\text{Leverage}^{after}_{b} = \frac{\text{Assets}_{b} + \Delta^{CIP}_{b}}{\text{Equity}_{b}}$$

- $\Delta^{CIP}_{b}$ : exposition additionnelle au bilan de la banque $b$ pour l'arbitrage CIP
- Le ratio de levier est la contrainte pivot pour l'arbitrage à court terme

#### 3. Résolution et Équilibre
Le dollar agit comme baromètre de la capacité de prise de risque dans les marchés mondiaux de capitaux. Quand le dollar s'apprécie, les bilans des banques mondiales se contractent (via les effets de valorisation), réduisant la capacité d'arbitrage → la basis CIP s'élargit. La relation est robuste et bidirectionnelle.

#### 4. Mécanisme de Transmission
Appréciation du dollar → contraction des bilans des banques mondiales via effets de valorisation → réduction de la capacité d'arbitrage CIP → basis CIP plus négative → réduction du crédit transfrontalier en dollars.

#### Verdict Critic
VALIDÉE — Le modèle identifie une friction financière précise (contrainte de levier réglementaire) et un mécanisme triangulaire dollar/levier/CIP. Variables définies. Principalement empirique mais avec un cadre théorique de la contrainte de levier.

---

### 21. Central Bank Dollar Swap Lines and Overseas Dollar Funding Costs
*FileId: 1qFxLzOX-SWgaDxtKA2UOxBGcEXX3V38U*

#### 1. Environnement et Agents
Agents : (i) **intermédiaires financiers** (banques mondiales non-US) qui empruntent des dollars via le marché forward FX (swaps) pour financer leurs activités ; (ii) **entreprises** dans les pays bénéficiaires (source countries) qui empruntent en dollar auprès des banques locales ; (iii) **banques centrales** (Fed et banques centrales partenaires) qui peuvent échanger des devises via les lignes de swap.

#### 2. Frictions et Contraintes
Friction centrale : les intermédiaires font face à une courbe d'offre montante de dollars forward, résultant de leurs contraintes de bilan.

**Plafond CIP imposé par la ligne de swap** (no-arbitrage) :

$$x_t \geq -(r^{swap}_{cb} - r^{policy}_{cb}) - (r^{policy}_{US} - r^{deposit}_{Fed})$$

- $x_t$ : déviation CIP (cross-currency basis, normalement négative)
- $r^{swap}_{cb}$ : taux de la ligne de swap de la banque centrale locale (auprès de la Fed)
- $r^{policy}_{cb}$ : taux directeur de la banque centrale locale
- $r^{policy}_{US}$ : taux directeur de la Fed
- $r^{deposit}_{Fed}$ : taux de dépôt auprès de la Fed (IOER)

**Offre de dollars forward (intermédiaires)** :

$$Q^{supply}_t = f(x_t, \text{BalanceSheetCost}_t)$$

Courbe d'offre montante : un dollar plus cher (basis plus positive) incite les intermédiaires à en fournir davantage, mais à coût croissant.

**Demande de dollars forward (entreprises)** :

$$Q^{demand}_t = g(r^{borrow}_t)$$

- $r^{borrow}_t = r^{domestic}_t - x_t$ : taux d'emprunt effectif en dollar pour l'entreprise

#### 3. Résolution et Équilibre
En équilibre sans ligne de swap, la basis CIP est déterminée par l'intersection des courbes d'offre et demande. Quand la Fed ouvre une ligne de swap et réduit son taux, la courbe d'offre devient horizontale au niveau du taux de la ligne (plafond CIP). Cela réduit les coûts d'emprunt ex ante perçus par les entreprises et améliore le bien-être du pays bénéficiaire.

#### 4. Mécanisme de Transmission
Ouverture/baisse du taux de la ligne de swap Fed → tronque la distribution des déviations CIP → aplatit la courbe d'offre de dollars forward → baisse des coûts d'emprunt en dollar pour les entreprises étrangères → amélioration du bien-être.

#### Verdict Critic
VALIDÉE — Le modèle contient une no-arbitrage condition précise pour le plafond CIP, des courbes d'offre et demande de dollars forward, et un mécanisme d'équilibre général liant le taux de la ligne de swap aux coûts d'emprunt des entreprises. Variables définies.

---

### 22. Changing Patterns of Capital Flows
*FileId: 1_8T67csZ14RsQO5AXx_0WCs1sLVduKqs*

#### 1. Environnement et Agents
[EMPIRIQUE] — pas de modèle formel. Ce rapport du CGFS (BIS, 2021) analyse empiriquement les changements structurels dans la composition et les volumes des flux de capitaux internationaux depuis la crise financière mondiale. Il décrit les tendances, les acteurs (banques, non-banques, banques centrales) et les risques systémiques, sans proposer de modèle théorique formel avec équations structurelles.

---

### 23. Offshore Dollar Creation and the Emergence of the post-2008 International Monetary System
*FileId: 1zimNx-KYuS9N4CxcYUf2Ff_cmxUIAdrt*

#### 1. Environnement et Agents
Cadre théorique institutionnel (Money View) sans modèle économétrique formel. Agents : (i) **banques centrales** (Fed au sommet) ; (ii) **banques commerciales** (onshore et offshore) ; (iii) **banques fantômes** (shadow banks : fonds monétaires, véhicules ABCP, repos overnight) ; (iv) **entreprises non-financières** et investisseurs. L'objectif analytique est de cartographier la hiérarchie monétaire internationale.

#### 2. Frictions et Contraintes
Friction institutionnelle : le système monétaire international est une hiérarchie dans laquelle les instruments de crédit à court terme en dollars sont émis comme monnaie-crédit par différentes institutions publiques et privées, avec une valeur au pair conditionnelle à la liquidité du marché.

**Hiérarchie monétaire** (balance-sheet accounting) :

Niveau 1 (sommet) : Réserves Fed → émises par la Fed, échangeables au pair entre elles.
Niveau 2 : Dollars onshore → dépôts en USD dans les banques US.
Niveau 3 : Dollars offshore → dépôts en eurodollars (offshore), swaps de change de banques centrales, parts de fonds monétaires offshore.
Niveau 4 : Dollars shadow → repos overnight, parts MMF, ABCP.

La friction est que les instruments des niveaux inférieurs peuvent perdre leur parité avec le niveau supérieur lors de crises de liquidité (shadow bank run, arrêt des marchés de repo).

#### 3. Résolution et Équilibre
Il n'y a pas de résolution au sens d'un équilibre mathématique. Le cadre décrit comment le système post-2008 est un hybride public-privé : la Fed backstop les dollars onshore, les lignes de swap Fed backstop les dollars offshore, mais les dollars shadow restent vulnérables. Le papier argue que le système a une cohérence systémique, contre le scepticisme dominant.

#### 4. Mécanisme de Transmission
Stress de liquidité dans le shadow banking → rupture de la parité des instruments de bas de hiérarchie → contagion vers le haut de la hiérarchie → intervention de la Fed via lignes de swap pour stabiliser les dollars offshore.

#### Verdict Critic
VALIDÉE (avec mention empirique/institutionnel) — Ce papier est une analyse institutionnelle du système monétaire international (Money View), sans modèle formel avec FOC et équilibres. La structure de hiérarchie monétaire est néanmoins une contribution théorique précise sur les frictions de liquidité offshore. Variables définies dans le cadre conceptuel.

---

### 24. Repo and FX Swap: A Tale of Two Markets
*FileId: 1KL-PvjK4QR-aAy6lFDfM5dBwnWVVXyX-*

#### 1. Environnement et Agents
Agents : (i) **dealers** (grandes banques de zone euro) qui agissent comme intermédiaires dans les deux marchés — repo en dollars et FX swap dollar/euro ; (ii) **emprunteurs** (non-banques, banques buy-side) qui ont besoin de financement en dollars. Les dealers maximisent leur profit sous contrainte de ratio de levier.

#### 2. Frictions et Contraintes
Friction centrale : le coût de bilan du ratio de levier (leverage ratio) affecte différemment les deux marchés. Le repo dollar augmente l'exposition au bilan ; le FX swap peut être netté hors bilan dans certains régimes comptables.

**Contrainte de levier du dealer** :

$$\frac{\text{Equity}_d}{\text{TotalExposure}_d} \geq \ell$$

- $\text{Equity}_d$ : fonds propres du dealer $d$
- $\text{TotalExposure}_d$ : exposition totale au bilan (repo augmente cela ; FX swap dans le régime NetFX > 0 peut être netté)
- $\ell$ : ratio de levier minimum réglementaire

**Conditions de prix d'équilibre** :

$$r^{FX}_{d} > r^{repo}_{d} + \text{BalanceSheetCost}_d \quad \text{si NetFX}>0$$

- $r^{FX}_d$ : taux d'emprunt implicite via FX swap pour le dealer $d$
- $r^{repo}_d$ : taux d'emprunt repo pour le dealer $d$
- $\text{BalanceSheetCost}_d$ : coût unitaire d'expansion du bilan (shadow cost du levier)

**Taux de prêt d'équilibre** :

$$r^{lend}_{d,j} = r^{marginal}_{d} + \frac{\mu_j}{\varepsilon_j}$$

- $r^{lend}_{d,j}$ : taux de prêt du dealer $d$ au segment de clientèle $j$
- $r^{marginal}_d$ : coût marginal du dealer (inclut le coût de bilan)
- $\mu_j / \varepsilon_j$ : markup lié à l'élasticité de la demande du segment $j$

#### 3. Résolution et Équilibre
En équilibre, les dealers utilisent les deux marchés comme substituts pour fournir du financement en dollars. Aux fins de trimestre, les contraintes de bilan se resserrent et les dealers se déplacent vers les FX swaps (moins coûteux en bilan) au détriment du repo. Le marché des swaps agit comme "residual market" de dernier recours.

#### 4. Mécanisme de Transmission
Fin de trimestre → contrainte de levier binding → dealers contractent le repo dollar (coûteux en bilan) → substitution vers FX swap (nettable hors bilan) → pression à la hausse sur la basis CIP → coûts de financement dollar plus élevés pour les emprunteurs.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière spécifique (levier réglementaire différencié entre repo et FX swap), des conditions de prix d'équilibre avec markups, et un mécanisme de substitution. Variables définies.

---

### 25. Hunting for Dollars
*FileId: 1ovdnYrN1TK9MIUczF__R2m-hZTmSMzLT*

#### 1. Environnement et Agents
Agents : (i) **banques non-US** (principalement zone euro) qui ont besoin de financement en dollars et doivent se conformer aux ratios réglementaires trimestriels ; (ii) **dealers US** qui fournissent le financement en dollars à la fois via les marchés repo US et via les FX swaps ; (iii) **non-banques** qui subissent l'augmentation du coût de couverture.

#### 2. Frictions et Contraintes
Friction centrale : les exigences réglementaires trimestrielles (LCR, leverage ratio) poussent les banques non-US à substituer le repo dollar (visible au bilan) par les FX swaps (moins visibles) à la fin de chaque trimestre.

**Contrainte réglementaire trimestrielle** :

$$\text{LCR}_{b,t} = \frac{\text{HQLA}_{b,t}}{\text{NetCashOutflows}_{b,t}} \geq 100\%$$

- $\text{HQLA}_{b,t}$ : actifs liquides de haute qualité de la banque $b$ en fin de trimestre $t$
- $\text{NetCashOutflows}_{b,t}$ : sorties nettes de liquidité sur 30 jours

**Coût de couverture additionnel** (cross-currency basis) :

$$\Delta x_{t} = -\alpha \cdot \Delta D^{FX}_{t}$$

- $\Delta x_t$ : variation de la déviation CIP (basis) en fin de trimestre
- $\alpha$ : élasticité prix de l'offre de dollars synthétiques
- $\Delta D^{FX}_{t}$ : variation de la demande nette de FX swaps par les banques non-US

**Rente extraite par les dealers US** :

$$\text{Rent}^{US}_{t} = (r^{FX}_{t} - r^{repo}_{t}) \cdot Q^{FX}_{t}$$

- $r^{FX}_t$ : taux implicite du dollar via FX swap
- $r^{repo}_t$ : taux repo dollar concurrent
- $Q^{FX}_t$ : volume de FX swaps fournis par les dealers US

#### 3. Résolution et Équilibre
L'équilibre est caractérisé par une substitution repo→FX swap à la fin de chaque trimestre, les dealers US extrayant des rentes de leur position de monopoliste partiel dans la provision de dollars. Le coût total additionnel imposé aux non-US s'élève à 10,4 milliards de dollars sur la période d'étude.

#### 4. Mécanisme de Transmission
Fin de trimestre → contrainte LCR/levier binding pour banques non-US → substitution vers FX swaps → dealers US en position de force → augmentation de la basis CIP et des coûts de couverture → transfert de surplus vers les dealers US.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière précise (contrainte LCR/levier trimestriel), des équations de coût de couverture et de rente, avec un mécanisme clair. Variables définies.

---

### 26. Currency Mispricing and Dealer Balance Sheets
*FileId: 1DMUvE6M0uFqYKJqylboaQklNF1uDJfxB*

#### 1. Environnement et Agents
Agents : (i) **dealers** (grandes banques réglementées au Royaume-Uni) qui fournissent du financement synthétique en dollar (emprunt en euros + swap en dollar) à leurs clients ; (ii) **clients** (corporations, fonds) qui cherchent à emprunter en dollar. Les dealers maximisent leur profit sous contrainte de ratio de levier.

#### 2. Frictions et Contraintes
Friction centrale : le cadre réglementaire du ratio de levier (UK Leverage Ratio Framework) impose un coût de bilan qui se répercute directement sur la prime facturée pour le financement synthétique.

**Contrainte de ratio de levier du dealer** :

$$\frac{\text{Tier1Capital}_{d,t}}{\text{TotalExposure}_{d,t}} \geq \ell_{UK}$$

- $\text{Tier1Capital}_{d,t}$ : capital Tier 1 du dealer $d$ au temps $t$
- $\text{TotalExposure}_{d,t}$ : exposition totale au bilan (inclut les notionnels des dérivés)
- $\ell_{UK}$ : seuil réglementaire UK (variable et exogène à l'identification)

**Markup de financement synthétique** :

$$\text{CIP deviation}_{d,t} = \theta \cdot \text{LeverageRatio}_{d,t} + \mathbf{X}'_{d,t}\beta + \varepsilon_{d,t}$$

- $\text{CIP deviation}_{d,t}$ : déviation CIP (premium) facturée par le dealer $d$ à ses clients
- $\theta$ : effet causal du ratio de levier sur le mispricing ; $\theta > 0$
- $\text{LeverageRatio}_{d,t}$ : ratio de levier réglementaire du dealer $d$
- $\mathbf{X}_{d,t}$ : contrôles (demande, rating client, etc.)

**Résultat principal** : les dealers affectés par le choc réglementaire UK facturent 20 points de base annuels supplémentaires pour le financement synthétique en dollar.

#### 3. Résolution et Équilibre
Identification par différence-en-différences exploitant la variation exogène introduite par le UK Leverage Ratio Framework (qui ne s'applique qu'aux dealers réglementés au UK). Les dealers contraints par le choc réglementaire augmentent leur premium CIP, tandis que les dealers non affectés ne le font pas, même avec des clients identiques.

#### 4. Mécanisme de Transmission
Choc réglementaire (introduction/durcissement du UK leverage ratio) → augmentation du coût de bilan pour les dealers affectés → répercussion sur le premium facturé pour le financement synthétique → déviation CIP persistante et dealer-spécifique.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction réglementaire précise (UK leverage ratio) avec une équation structurelle de mispricing et une stratégie d'identification causale. Variables définies.

---

### 27. Dollar Debt in FX Swaps and Forwards: Huge, Missing and Growing
*FileId: 1jYRDnb7wSKBC1vWptBFGfRRrU0WdEXq_*

#### 1. Environnement et Agents
[EMPIRIQUE] — pas de modèle formel. Ce papier de Borio, McCauley et McGuire (BIS Quarterly Review, déc. 2022) documente empiriquement la taille ($97 trillions à fin juin 2022), la composition et la croissance de la dette cachée en dollars via les FX swaps et forwards. Il n'y a pas de modèle théorique avec FOC et équilibres. L'article argumente que cette dette hors bilan crée des risques systémiques non mesurés.

---

### 28. The Dollar-Based Financial System Through the Window of the FX Swaps Market
*FileId: 1lo6Yx5RT0VcWVTyo2KCZHMEaNAIUxuxk*

#### 1. Environnement et Agents
[EMPIRIQUE/INSTITUTIONNEL] — pas de modèle formel. Ce discours de Hyun Song Shin (BIS, mars 2023) articule un cadre conceptuel sur le rôle du marché des FX swaps comme fenêtre sur le système financier global centré sur le dollar. Il décrit le rôle des non-banques, l'ampleur de la dette cachée ($80 trillions), et le rôle des lignes de swap des banques centrales, sans proposer de modèle formel avec équations structurelles.

---

### 29. Markups to Financial Intermediation in Foreign Exchange Markets
*FileId: 1_B9o4LFoRYElTCta9zW_SwJ_lvLi3T5X*

#### 1. Environnement et Agents
Agents : (i) **dealers** (grandes banques US et non-US) qui ont un pouvoir de marché dans la fourniture d'arbitrage CIP ; (ii) **clients** (autres banques, corporations) qui cherchent à emprunter en dollar via FX swap. Les dealers exploitent leur position monopolistique partielle pour facturer des markups supérieurs aux coûts.

#### 2. Frictions et Contraintes
Friction centrale : concurrence imparfaite parmi les dealers CIP — chaque dealer est un price-setter plutôt qu'un price-taker, grâce aux relations client et aux barrières à l'entrée.

**Markup du dealer** sur l'arbitrage CIP :

$$m_{d,t} = (r^{cross-quarter}_{d,t} - r^{within-quarter}_{d,t}) - (\text{cost}^{cross}_{d,t} - \text{cost}^{within}_{d,t})$$

- $m_{d,t}$ : markup du dealer $d$ au temps $t$
- $r^{cross-quarter}_{d,t}$ : taux facturé pour le prêt synthétique croisant la fin de trimestre
- $r^{within-quarter}_{d,t}$ : taux facturé pour le prêt synthétique intra-trimestre
- $\text{cost}^{cross/within}_{d,t}$ : coût de provision correspondant

**Markup moyen estimé** : les banques US pourraient gagner 111 points de base supplémentaires en déplaçant leur prêt synthétique en dollar sur 1 semaine du régime intra-trimestre vers le régime croisant la fin de trimestre — ce différentiel constitue un markup quand les coûts ne l'expliquent pas.

**Offre imparfaitement élastique** du dealer $d$ :

$$Q^{supply}_{d,t} = f(m_{d,t}, \text{BalanceSheetCapacity}_{d,t})$$

- $\text{BalanceSheetCapacity}_{d,t}$ : capacité de bilan résiduelle du dealer

#### 3. Résolution et Équilibre
En équilibre avec concurrence imparfaite, les déviations CIP ne sont pas entièrement arbitrées même si les coûts de bilan sont nuls, car les dealers ont intérêt à maintenir un markup. Le papier documente des preuves de concurrence imparfaite par des observations sur la dispersion des taux entre dealers pour des transactions identiques.

#### 4. Mécanisme de Transmission
Pouvoir de marché des dealers → markup positif sur la provision de dollars synthétiques → déviations CIP plus négatives que ce que justifient les seuls coûts de bilan → rente transférée des clients vers les dealers.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction de marché imparfaitement concurrentiel (pouvoir de marché des dealers), une définition précise des markups et un mécanisme de transmission. Variables définies.

---

### 30. Price-Setting in the Foreign Exchange Swap Market: Evidence from Order Flow
*FileId: 1rIs4iteZUeN2S_uLiDuBwU2bRrhxis5k*

#### 1. Environnement et Agents
Trois types d'agents : (i) **clients** (corporations, fonds) qui gèrent leur exposition de change en vendant des devises contre des dollars via FX swap ; (ii) **arbitrageurs** (banques buy-side, hedge funds) qui fournissent des dollars dans le marché inter-dealer ; (iii) **dealers** (primary dealers) qui maintiennent le marché inter-dealer et minimisent l'accumulation d'inventaire.

#### 2. Frictions et Contraintes
Friction centrale : la dispersion des coûts de financement entre banques réduit la fraction d'arbitrageurs actifs dans le marché inter-dealer, forçant les dealers à ajuster les prix plus agressivement.

**Impact prix du flux d'ordres** (marché inter-dealer) :

$$\Delta F_t = \lambda_t \cdot \text{OrderFlow}^{FX}_{t} + \varepsilon_t$$

- $\Delta F_t$ : variation du taux de change à terme (forward rate) des FX swaps
- $\lambda_t$ : impact prix par unité de flux d'ordres au temps $t$
- $\text{OrderFlow}^{FX}_{t}$ : flux net d'ordres dans le marché inter-dealer FX swap

**Déterminant de l'impact prix** :

$$\lambda_t = \lambda_0 + \lambda_1 \cdot \text{FundingCostDispersion}_t$$

- $\text{FundingCostDispersion}_t$ : dispersion des coûts de financement parmi les banques (mesurée ex : par l'écart LIBOR-OIS, la dispersion des CDS bancaires)
- $\lambda_1 > 0$ : une plus grande dispersion implique moins d'arbitrageurs actifs → impact prix plus élevé

**Condition d'équilibre du marché inter-dealer** : le dealer ajuste le forward rate pour minimiser l'inventaire accumulé. L'impact prix post-2008 a augmenté d'environ 5 fois (de < 1 bp à ~ 5 bp par écart-type de flux d'ordres).

#### 3. Résolution et Équilibre
En équilibre, le forward rate est tel que le flux d'ordres des clients soit équilibré par les arbitrageurs. Quand la dispersion des coûts de financement est élevée, moins d'arbitrageurs participent, et le dealer doit ajuster le prix plus agressivement. Les lignes de swap des banques centrales réduisent le flux d'ordres en USD et affectent directement le taux forward.

#### 4. Mécanisme de Transmission
Dispersion élevée des coûts de financement → fraction réduite d'arbitrageurs actifs → dealers ajustent le forward rate plus agressivement pour attirer des arbitrageurs → impact prix du flux d'ordres plus élevé → plus grande sensibilité du taux forward aux déséquilibres de flux.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière précise (dispersion des coûts de financement limitant l'arbitrage), une équation d'impact prix avec variables définies, et un mécanisme de microstructure bien articulé.

---

### 31. Monetary Policy Transmission in Segmented Markets
*FileId: 18qPKMVp4bV2RRssDmBrWvBl6UC2PbTok*

#### 1. Environnement et Agents
Agents : (i) **dealers** (un nombre limité de grandes banques) qui ont accès au marché repo centralisé (CCP) et fournissent de la liquidité aux clients via le segment OTC bilatéral ; (ii) **clients** (banques de petite taille, non-banques) qui n'ont pas accès direct au marché centralisé et doivent négocier bilatéralement avec les dealers. Les dealers ont un pouvoir de marché.

#### 2. Frictions et Contraintes
Friction centrale : segmentation de marché — la majorité des participants n'a pas accès direct au marché centralisé (CCP), créant un pouvoir de marché chez les dealers.

**Négociation bilatérale (Stole-Zwiebel)** entre client $c$ et dealer $d$ :

$$r^{OTC}_{c,d,t} = r^{CCP}_t + (1 - \phi_c) \cdot \text{Surplus}_{c,d,t}$$

- $r^{OTC}_{c,d,t}$ : taux repo OTC négocié entre le client $c$ et le dealer $d$
- $r^{CCP}_t$ : taux repo sur le marché centralisé (CCP)
- $\phi_c$ : pouvoir de négociation du client $c$ ($0 < \phi_c < 1$)
- $\text{Surplus}_{c,d,t}$ : surplus bilatéral de la transaction (différence entre valeurs de réserve)

**Pouvoir de marché des dealers** :

$$\text{Markup}_{d,t} = (1 - \phi_d) \cdot (r^{CCP}_t - r^{outside}_{d,t})$$

- $\phi_d$ : pouvoir de négociation du dealer $d$ (estimé à 0,307 pour les emprunteurs, 0,227 pour les déposants)
- $r^{outside}_{d,t}$ : meilleure offre alternative pour le client (hors options)

**Impédance de la transmission de politique monétaire** :

$$\frac{\partial r^{OTC}_{c,d}}{\partial r^{CCP}} = \phi_c + (1-\phi_c) \cdot \frac{\partial \text{Surplus}}{\partial r^{CCP}} < 1$$

#### 3. Résolution et Équilibre
Les dealers forment un réseau d'accès et fixent les prix par négociation multilatérale Stole-Zwiebel. En équilibre, les clients avec plus de connections (plus de dealers alternatifs) obtiennent de meilleurs taux. La pass-through de la politique monétaire (variation des taux CCP → variation des taux OTC) est inférieure à 1 en raison du pouvoir de marché des dealers.

#### 4. Mécanisme de Transmission
Variation du taux directeur de la BCE → variation du taux repo CCP → répercussion partielle vers le taux repo OTC bilatéral, freinée par le pouvoir de marché des dealers → transmission monétaire dégradée pour les participants sans accès CCP.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction de marché (segmentation + pouvoir de marché des dealers), des équations de négociation Stole-Zwiebel avec variables définies, et un mécanisme quantifié d'impédance de la transmission monétaire.

---

### 32. A Quantity-Driven Theory of Term Premia and Exchange Rates
*FileId: 1a6cqOoHzoGKS_Hi9IjWI02hoQs3iUxXl*

#### 1. Environnement et Agents
Trois types d'investisseurs spécialisés dans une économie à deux pays : (i) **bond specialists** (spécialistes obligataires domestiques) qui ne peuvent investir que dans les obligations en devise locale ; (ii) **FX specialists** (spécialistes de change) qui ne peuvent effectuer que des transactions FX ; (iii) **arbitrageurs** avec capital limité qui peuvent traverser les segmentations. Les investisseurs spécialisés ont des fonctions d'utilité quadratiques dans leurs rendements relatifs.

#### 2. Frictions et Contraintes
Friction centrale : segmentation des marchés financiers — les spécialistes obligataires ne peuvent pas participer aux marchés FX, et vice-versa. Les arbitrageurs ont une capacité de capital limitée.

**Condition de market-clearing des obligations en devise locale** :

$$Q^{domestic}_{t} + Q^{arb,bond}_{t} = \bar{B}_{t}$$

- $Q^{domestic}_t$ : demande des bond specialists pour les obligations domestiques
- $Q^{arb,bond}_t$ : position des arbitrageurs dans les obligations domestiques
- $\bar{B}_t$ : offre totale d'obligations (déterminée par la politique budgétaire/QE)

**Prime de terme en devise locale** :

$$\text{TermPremium}^{dom}_{t} = \gamma^{bond} \cdot (\bar{B}_{t} - \bar{B}^{for}_{t}) + \delta_t$$

- $\gamma^{bond}$ : sensibilité de la prime de terme à l'offre nette relative d'obligations ($\gamma^{bond} > 0$)
- $\bar{B}_{t}$ : offre d'obligations en devise locale
- $\bar{B}^{for}_t$ : offre d'obligations en devise étrangère
- $\delta_t$ : facteur de risque commun

**Taux de change d'équilibre** (liant FX et term premia) :

$$\Delta s_t = \text{TermPremium}^{dom}_t - \text{TermPremium}^{for}_t + \text{CIP dev}_t + \nu_t$$

- $\Delta s_t$ : variation du taux de change spot (appréciation = positif)
- $\text{CIP dev}_t$ : déviation CIP (extension du modèle de base pour post-2008)
- $\nu_t$ : choc résiduel

#### 3. Résolution et Équilibre
La segmentation des marchés fait que les chocs d'offre d'obligations dans une devise affectent à la fois la prime de terme dans cette devise et le taux de change. Le modèle génère une co-variation entre prime de terme et taux de change, cohérente avec les données. L'extension post-2008 avec déviations CIP persistantes reproduit les nouvelles régularités empiriques.

#### 4. Mécanisme de Transmission
Choc d'offre d'obligations en devise locale (ex: QE → réduction de l'offre) → bond specialists domestiques face à moins d'actifs → prime de terme baisse → arbitrageurs déplacent des fonds entre pays → taux de change s'ajuste pour équilibrer les marchés FX.

#### Verdict Critic
VALIDÉE — Le modèle contient des frictions financières précises (segmentation des marchés + capital limité des arbitrageurs), des équations structurelles avec variables définies, et un mécanisme de transmission entre marché obligataire et taux de change.

---

### 33. The Implications of CIP Deviations for International Capital Flows
*FileId: 1FmXXnZcXeY-vHKy18gq4LQlurVsOZkGn*

#### 1. Environnement et Agents
Agents : **investisseurs institutionnels de la zone euro** (assureurs, fonds de pension, fonds mutuels) qui détiennent des obligations en USD et utilisent des dérivés de change (FX forwards/swaps) pour couvrir leur risque de change. Ces investisseurs font face à des coûts de rollover périodiques.

#### 2. Frictions et Contraintes
Friction centrale : le rollover des couvertures de change est coûteux et contraint la durée de couverture, créant une sensibilité des portefeuilles aux variations de la basis CIP.

**Problème d'optimisation dynamique de l'investisseur** :

$$\max_{\{H_t, B^{USD}_t\}} \mathbb{E}_0 \sum_{t=0}^T \beta^t U(C_t)$$

sous la contrainte budgétaire :

$$C_t = Y_t + r^{USD}_t \cdot B^{USD}_t - x_t \cdot H_t - r^{rollover}_t \cdot H_t \cdot \mathbf{1}[\text{rollover}_t]$$

- $H_t$ : quantité d'obligations USD couverte (hedged) par dérivé FX
- $B^{USD}_t$ : stock total d'obligations USD détenues
- $x_t$ : déviation CIP (coût additionnel de couverture, négatif = dollar synthétique cher)
- $r^{rollover}_t$ : coût de rollover de la couverture lors du renouvellement
- $\mathbf{1}[\text{rollover}_t]$ : indicateur de besoin de rollover au temps $t$

**Élasticité de la couverture à la basis** :

$$\frac{\partial H_t}{\partial x_t} < 0 \quad \text{(plus la basis est négative, moins l'investisseur couvre)}$$

**Effet sur les rendements obligataires US** :

Une baisse de $H_t$ implique une baisse de la demande d'obligations US → hausse du rendement de 0,55 bp par bp d'élargissement de la basis pour les obligations corporate US exposées.

#### 3. Résolution et Équilibre
En réduisant leur couverture, les investisseurs de la zone euro réduisent aussi leurs achats d'obligations US, augmentant les rendements de ces obligations. L'effet est hétérogène : les investisseurs avec risque de rollover élevé (plus de dérivés arrivant à maturité) réagissent davantage (élasticité double des autres).

#### 4. Mécanisme de Transmission
Élargissement de la basis CIP → augmentation du coût de couverture → réduction des positions couvertes en obligations US → baisse de la demande pour les obligations US → hausse des rendements → modulation de la transmission de politique monétaire vers les primes de terme US.

#### Verdict Critic
VALIDÉE — Le modèle dynamique contient une friction financière précise (coût de rollover des couvertures FX), un problème d'optimisation intertemporel avec variables définies, et un mécanisme de transmission aux prix des actifs. Variables définies.

---

### 34. Exchange Rate Disconnect in General Equilibrium
*FileId: 1-C-mz0i0f7mf8JWC4wLOrSxdZxNxVC72*

#### 1. Environnement et Agents
Économie à deux pays avec trois types d'agents : (i) **ménages** (dans chaque pays) avec préférences de consommation biaisées vers les biens domestiques (home bias) et accès aux marchés financiers via des intermédiaires ; (ii) **firmes** qui fixent les prix avec pricing-to-market ; (iii) **intermédiaires financiers** qui intermedient les transactions d'actifs internationaux et sont soumis à des limites d'arbitrage. La banque centrale suit une règle de Taylor.

#### 2. Frictions et Contraintes
Friction centrale : les intermédiaires financiers ont une capacité limitée d'arbitrage (limits to arbitrage), générant des déviations de la parité de taux d'intérêt non couverte (UIP).

**Déviation UIP** (friction financière) :

$$\Delta e_{t+1} = (r_t - r^*_t) + \psi_t$$

- $\Delta e_{t+1}$ : variation attendue du taux de change (log)
- $r_t$ : taux d'intérêt nominal domestique (court terme)
- $r^*_t$ : taux d'intérêt nominal étranger
- $\psi_t$ : déviation de la parité UIP (prime de risque de change), suivant un processus AR(1) persistant

**Choc financier** (processus exogène pour la déviation UIP) :

$$\psi_t = \rho_\psi \psi_{t-1} + \varepsilon^{\psi}_t$$

- $\rho_\psi$ : persistance du choc financier (proche de 1 pour générer le disconnect)
- $\varepsilon^{\psi}_t$ : choc i.i.d. sur la demande d'actifs internationaux (noise traders)

**Contrainte budgétaire des ménages** (standard IRBC avec home bias $\omega$) :

$$P_{H,t} C_{H,t} + P_{F,t} C_{F,t} \leq W_t + \Pi_t + T_t - \Delta B_t$$

- $C_{H,t}, C_{F,t}$ : consommation de biens domestiques et étrangers
- $P_{H,t}, P_{F,t}$ : niveaux de prix correspondants
- $\omega$ : paramètre de home bias
- $W_t$ : revenus du travail ; $\Pi_t$ : profits des firmes ; $T_t$ : transferts ; $\Delta B_t$ : variation du portefeuille d'actifs

#### 3. Résolution et Équilibre
Le modèle est résolu par méthode de perturbation autour d'un état stationnaire déterministe. Le taux de change est déterminé par l'accumulation des déviations UIP (chocs financiers). En ajoutant des chocs financiers aux chocs de productivité et monétaires standards, le modèle reproduit simultanément les puzzles Meese-Rogoff, Backus-Smith, PPP et UIP, sans compromettre les moments du cycle économique.

#### 4. Mécanisme de Transmission
Choc exogène de demande d'actifs internationaux ($\varepsilon^\psi$) → déviation persistante de la parité UIP ($\psi_t$) → taux de change se déconnecte des fondamentaux macroéconomiques → faible co-variation entre taux de change et différentiels de taux/fondamentaux.

#### Verdict Critic
VALIDÉE — Le modèle est un DSGE d'équilibre général complet avec une friction financière précise (déviation UIP générée par les limites d'arbitrage), des équations structurelles avec variables définies et un mécanisme de transmission clairement articulé.

---

### 35. U.S. Banks and Global Liquidity
*FileId: 1oGAV_KTs5_VxrWj7TjrL4Ts_PMW0J0Uj*

#### 1. Environnement et Agents
Agents : **U.S. Global Systemically Important Banks (G-SIBs)** composés de deux entités intra-groupe : (i) la **banque de dépôt** (depository institution, DI) qui détient des réserves excédentaires à la Fed ; (ii) le **broker-dealer** (BD) qui opère dans les marchés de repo et FX swap. Les transferts intra-groupe (DI → BD) sont le mécanisme central.

#### 2. Frictions et Contraintes
Friction centrale : séparation réglementaire et opérationnelle entre DI et BD au sein du même groupe bancaire, avec contraintes de liquidité différentes pour chaque entité.

**Bilan consolidé d'un G-SIB** (simplification) :

$$\text{Assets}_{GSIB} = \text{Loans} + \text{Securities} + \text{Reserves}_{Fed} + \text{FXSwap}^{lend} + \text{Repo}^{lend}$$
$$\text{Liabilities}_{GSIB} = \text{Deposits} + \text{FXSwap}^{borrow} + \text{Repo}^{borrow} + \text{Equity}$$

**Mécanisme "reserve-draining"** :

$$\Delta \text{Reserves}^{DI}_{b,t} = -(\Delta \text{FXSwap}^{lend}_{BD,b,t} + \Delta \text{Repo}^{lend}_{BD,b,t})$$

- $\Delta \text{Reserves}^{DI}_{b,t}$ : variation des réserves excédentaires de la DI de la banque $b$
- $\Delta \text{FXSwap}^{lend}_{BD}$ : variation du prêt en FX swap par le broker-dealer
- $\Delta \text{Repo}^{lend}_{BD}$ : variation du prêt en repo par le broker-dealer
- La DI transfère des réserves vers le BD qui les prête via FX swap/repo (réduction nette de réserves)

**Réponse à la pénurie de dollars** :

$$\Delta Q^{lend}_{b,t} = \alpha + \beta \cdot \text{DollarShortage}_t + \gamma \cdot \Delta \text{TGA}_t + \varepsilon_{b,t}$$

- $Q^{lend}_{b,t}$ : volume de liquidité en dollar fournie par le G-SIB $b$
- $\text{DollarShortage}_t$ : indicateur de pénurie (ex : augmentation de la basis CIP)
- $\Delta \text{TGA}_t$ : variation du compte général du Trésor US (Treasury General Account) qui réduit les réserves bancaires

#### 3. Résolution et Équilibre
Les G-SIBs US augmentent modestement leur provision de liquidité en réponse aux pénuries de dollars, principalement financée en réduisant leurs réserves excédentaires. Ce mécanisme est limité par le ratio de levier consolidé et par la taille des réserves disponibles. Le taper de la Fed (réduction du bilan) réduit les réserves et contraint cette capacité.

#### 4. Mécanisme de Transmission
Pénurie de dollars / augmentation du TGA / taper Fed → réduction des réserves excédentaires des G-SIBs → moindre capacité de provision de liquidité via FX swap/repo → pression à la hausse sur la basis CIP → rôle de "prêteur de second recours" atteint ses limites.

#### Verdict Critic
VALIDÉE — Le modèle contient un mécanisme de bilan précis (reserve-draining intermediation) avec des équations comptables et économétriques, variables définies. Principalement empirique mais avec un cadre théorique de bilan bancaire bien articulé.

---

### 36. Dollar Asset Holdings and Hedging Around the Globe
*FileId: 1TUw9J4GTuUH1LRdNghZHNZS50uARZTId*

#### 1. Environnement et Agents
Agents : **investisseurs institutionnels internationaux** (fonds mutuels, assureurs, fonds de pension, banques centrales) de différentes zones monétaires, qui détiennent des actifs en USD et choisissent leur ratio de couverture du risque de change.

#### 2. Frictions et Contraintes
Friction centrale : les investisseurs font face à un problème de variance-espérance pour déterminer leur ratio de couverture optimal, soumis aux contraintes de mandat (certains doivent couvrir intégralement) et au coût de couverture (cross-currency basis).

**Problème de minimisation de variance / maximisation de rendement ajusté** :

$$\max_{h_t} \mathbb{E}[R^{USD}_{t+1}] - (1-h_t) \cdot \mathbb{E}[\Delta s_{t+1}] - \frac{\lambda}{2} \text{Var}(R^{hedged}_{t+1})$$

sous la contrainte de coût de couverture :

$$\text{HedgingCost}_t = x_t \cdot h_t \cdot B^{USD}_t$$

- $h_t$ : ratio de couverture (hedge ratio) optimal, $h_t \in [0,1]$
- $\mathbb{E}[R^{USD}_{t+1}]$ : rendement espéré de l'actif USD
- $\mathbb{E}[\Delta s_{t+1}]$ : variation espérée du taux de change (risque non couvert)
- $\lambda$ : aversion au risque de l'investisseur
- $x_t$ : déviation CIP (coût additionnel de couverture)
- $B^{USD}_t$ : stock d'actifs USD détenus

**Déterminants empiriques du ratio de couverture** :

$$h_{i,t} = \alpha_i + \beta_1 \cdot x_t + \beta_2 \cdot \mathbb{E}[\Delta s_t] + \beta_3 \cdot \text{Mandate}_i + \varepsilon_{i,t}$$

- $\text{Mandate}_i$ : contrainte de mandat de couverture de l'investisseur $i$

#### 3. Résolution et Équilibre
Le ratio de couverture optimal décroît avec le coût de couverture ($x_t$ plus négatif → moins de couverture). Post-crise financière, les fonds mutuels, assureurs et fonds de pension ont augmenté leur ratio de couverture de 15 points de pourcentage. La demande totale de couverture FX a atteint $2 trillions en 2019. Le papier identifie les rendements FX attendus comme facteur clé des décisions de couverture, au-delà de la minimisation de variance.

#### 4. Mécanisme de Transmission
Élargissement de la basis CIP → augmentation du coût de couverture → réduction du hedge ratio optimal → plus d'exposition de change non couverte → pression sur les taux de change et les primes de risque.

#### Verdict Critic
VALIDÉE — Le modèle contient un cadre moyenne-variance précis pour le choix du ratio de couverture, avec des équations et variables définies. Principalement empirique mais fondé sur un modèle théorique d'optimisation de portefeuille.

---

### 37. FX Policy When Financial Markets Are Imperfect
*FileId: 1QeOAFGYKiBtnGYQsCg89X3Uvj80UxUe6*

#### 1. Environnement et Agents
Agents dans une économie ouverte à deux pays : (i) **ménages** qui consomment et épargnent ; (ii) **intermédiaires financiers** (banques) avec capacité de prise de risque limitée ; (iii) **banque centrale** (du pays étranger ou émergent) qui peut intervenir sur le marché FX en achetant/vendant des réserves de change.

#### 2. Frictions et Contraintes
Friction centrale : les intermédiaires financiers font face à une contrainte de bilan qui limite leur capacité à absorber les déséquilibres de la demande d'actifs en devises.

**Offre imparfaitement élastique des intermédiaires** :

$$x_t = -\frac{1}{\kappa} \cdot (Q^{priv}_t - \bar{Q}_t)$$

- $x_t$ : déviation CIP / prime de risque de change
- $\kappa$ : élasticité de l'offre d'intermédiation privée (profondeur du marché FX)
- $Q^{priv}_t$ : quantité de devises intermédiées par le secteur privé
- $\bar{Q}_t$ : demande de devises des agents (déséquilibre exogène)

**Contrainte de bilan de l'intermédiaire** :

$$P_{i,t} \cdot |Q_{i,t}| \leq \omega \cdot W_{i,t}$$

- $Q_{i,t}$ : position nette en devises de l'intermédiaire $i$
- $\omega$ : fraction maximale de la richesse exposée au risque de change
- $W_{i,t}$ : richesse de l'intermédiaire $i$

**Intervention de la banque centrale** :

$$Q^{central bank}_t = Q^{target}_t - Q^{priv}_t$$

- $Q^{central bank}_t$ : volume d'intervention FX de la banque centrale
- La banque centrale transfère le risque de change du secteur privé vers le secteur public

#### 3. Résolution et Équilibre
L'intervention FX est efficace quand les marchés financiers sont imparfaits (contraintes de bilan binding). La banque centrale améliore le bien-être en substituant à l'intermédiation privée lorsque celle-ci est trop coûteuse. L'analyse clarifie que le stock d'actifs pertinent à affecter est le bilan des institutions financières, et que l'intervention FX est fondamentalement un transfert de risque du secteur privé vers le public.

#### 4. Mécanisme de Transmission
Contrainte de bilan des intermédiaires → offre imparfaitement élastique de dollars → déviations CIP / primes de risque → intervention FX de la banque centrale substitue à l'intermédiation privée → réduction des primes de risque → amélioration du bien-être.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière précise (contrainte de bilan des intermédiaires), des équations structurelles d'offre d'intermédiation et d'intervention, avec variables définies. C'est un cadre d'équilibre partiel applicable à la politique FX.

---

### 38. The International Dimension of Repo: Five New Facts
*FileId: 1vKx3nHwwiw8Y71Fq081-_1hql-ne4pYE*

#### 1. Environnement et Agents
[EMPIRIQUE] — pas de modèle formel. Ce papier de Hermes, Schmeling et Schrimpf (ECB Working Paper, 2025) documente cinq faits empiriques sur la dimension internationale du marché repo de la zone euro, en utilisant des micro-données réglementaires ECB (transactions bilatérales non centralisées). Les cinq faits concernent les volumes en USD vs EUR, l'intégration internationale, le rôle des filiales US, etc. Pas d'équations structurelles de modèle théorique.

---

### 39. Volatility, Intermediaries, and Exchange Rates
*FileId: 1JpvE7OwM_DCyua7VeuCSYhRoNpV1PdFo*

#### 1. Environnement et Agents
Économie à deux pays symétriques : dans chaque pays, un **intermédiaire financier** (banque) qui prend des dépôts, investit dans l'actif risqué local, l'actif risqué étranger, et un actif sans risque international. Les intermédiaires maximisent les rendements sous contrainte de VaR.

#### 2. Frictions et Contraintes
Friction centrale : les intermédiaires sont soumis à une contrainte VaR dont la sévérité dépend de la volatilité locale. Une plus haute volatilité domestique resserre la contrainte VaR → l'intermédiaire domestique demande un rendement espéré plus élevé sur les actifs étrangers → la devise étrangère doit s'apprécier en espérance.

**Contrainte VaR de l'intermédiaire** dans le pays domestique :

$$\text{VaR}_{home,t} = \sigma^{home}_t \cdot |B^{home}_t| \leq \bar{V} \cdot W^{home}_t$$

- $\sigma^{home}_t$ : volatilité des actifs dans le pays domestique
- $B^{home}_t$ : taille totale du bilan de l'intermédiaire domestique (en valeur de marché)
- $\bar{V}$ : fraction maximale de VaR en proportion de la richesse
- $W^{home}_t$ : richesse (capital) de l'intermédiaire domestique

**Problème de portefeuille de l'intermédiaire** :

L'intermédiaire choisit les allocations $(\omega^{local}_t, \omega^{foreign}_t, \omega^{bond}_t)$ pour maximiser le rendement espéré sous la contrainte VaR. La condition de premier ordre pour l'actif étranger implique :

$$\mathbb{E}_{t}[\Delta e_{t+1}] + r^*_t - r_t = \Lambda^{VaR}_{t} \cdot \sigma^{home}_t$$

- $\mathbb{E}_{t}[\Delta e_{t+1}]$ : appréciation espérée de la devise étrangère
- $r^*_t - r_t$ : différentiel de taux d'intérêt (étranger minus domestique)
- $\Lambda^{VaR}_t$ : multiplicateur de la contrainte VaR (shadow price de la contrainte)
- $\sigma^{home}_t$ : volatilité domestique (resserre la contrainte → $\Lambda^{VaR}_t$ plus élevé)

**Déviation CIP** (dans la version étendue du modèle) :

$$x_t = -(\Lambda^{VaR,home}_t - \Lambda^{VaR,for}_t) \cdot \sigma_{avg,t}$$

- $\Lambda^{VaR,home}_t - \Lambda^{VaR,for}_t$ : asymétrie des contraintes VaR entre les deux pays
- $\sigma_{avg,t}$ : volatilité moyenne

#### 3. Résolution et Équilibre
Le modèle est résolu par méthode de projection globale et estimé par GMM simulé (Simulated Method of Moments). En équilibre, la devise du pays le plus volatile doit s'apprécier en espérance, générant des déviations de la parité UIP cohérentes avec le forward premium puzzle. Le modèle reproduit quantitativement les puzzles Backus-Smith, forward premium, volatilité de taux de change, et déviations CIP.

#### 4. Mécanisme de Transmission
Choc de volatilité dans le pays domestique → contrainte VaR plus serrée → intermédiaires domestiques réduisent leur exposition aux actifs étrangers → devise étrangère doit s'apprécier en espérance (prime de risque de change positive) → déviations de la parité UIP et CIP.

#### Verdict Critic
VALIDÉE — Le modèle contient une friction financière précise (contrainte VaR endogène à la volatilité), des équations structurelles explicites avec variables définies, un mécanisme de transmission entre volatilité et taux de change, et une résolution quantitative. C'est un modèle d'équilibre général partiellement estimé.

---
