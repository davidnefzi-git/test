# Master Database — Macrofinance Internationale

**Projet :** Macrofinance Internationale
**Source :** 39 articles de recherche extraits au format JSON depuis Google Drive
**Date de compilation :** 2026-05-07
**Thèmes couverts :** CIP deviations, FX swaps, dollar funding, exchange rate determination, international liquidity

---

## 1. International Liquidity and Exchange Rate Dynamics

**Auteurs :** Xavier Gabaix, Matteo Maggiori
**Hypothèse Centrale :** Les taux de change sont déterminés par les flux de capitaux dans des marchés financiers imparfaits, où les intermédiaires financiers (financiers) absorbent les déséquilibres internationaux en échange d'une compensation pour le risque de change.
**Modèle / Équations Clés :** `C_t = (C_{NT,t})^α_t (C_{H,t})^{a_t} (C_{F,t})^{1-α_t}` ; utilité des ménages `U = ln C_0 + E[ln C_1]` ; le taux de change d'équilibre dépend de la capacité bilancielle des financiers (paramètre Γ).
**Stratégie Empirique :** Modèle théorique général d'équilibre ; les prédictions sont confrontées aux faits stylisés de la déconnexion taux de change–fondamentaux, de la prime de terme et des rendements du carry trade.
**Conclusion Principale :** Les chocs sur les bilans des intermédiaires financiers modifient leur compensation exigée pour le risque de change, affectant à la fois le niveau et la volatilité des taux de change, ce qui permet de rationaliser l'énigme de la déconnexion et d'autres régularités empiriques.

---

## 2. The Spillover of Money Market Turbulence to FX Swap and Cross-Currency Swap Markets

**Auteurs :** Information non détectée
**Hypothèse Centrale :** La turbulence des marchés monétaires de la seconde moitié de 2007 s'est propagée aux marchés des swaps FX et des swaps de devises croisées, provoquant des déviations marquées de la parité couverte des taux d'intérêt (CIP).
**Modèle / Équations Clés :** Taux dollar synthétique via FX swap : `r_{USD}^{FX-implied} = (F/S)(1 + r_{EUR}) - 1` ; condition CIP : `(1 + r_{EUR}) × (F/S) = 1 + r_{USD}`.
**Stratégie Empirique :** Analyse descriptive des spreads entre taux implicites FX swap et LIBOR dollar (EUR/USD, GBP/USD, JPY/USD), données Bloomberg 2007–2008 ; tests de causalité de Granger entre FX swaps et swaps de devises croisées.
**Conclusion Principale :** Les institutions financières non américaines ont massivement utilisé le marché des swaps FX pour pallier la pénurie de dollars, entraînant des violations de la CIP allant jusqu'à 35 pb et une détérioration de la liquidité mesurée par l'élargissement des spreads bid-ask.

---

## 3. Global Portfolio Investments and FX Derivatives

**Auteurs :** Information non détectée (BIS Working Paper)
**Hypothèse Centrale :** Les volumes d'encours en swaps FX et dérivés de change constituent un proxy de l'activité de couverture des investisseurs institutionnels des économies avancées sur les marchés obligataires internationaux.
**Modèle / Équations Clés :** `rx_{t+1}^{$,H} ≈ r_{t+1}^$ + (f_t^l - s_t^l) - rf_t^l = T_{t+1}^$ + x_t^l` ; rendement excédentaire lié à la couverture via forward ; modèle de portefeuille obligataire avec couverture de change optimale.
**Stratégie Empirique :** Données BIS OTC sur les dérivés FX et flux obligataires transfrontaliers ; régressions OLS et en variables instrumentales (VI) sur les déterminants des volumes de swaps FX, avec surprises de politique monétaire comme instrument.
**Conclusion Principale :** Les fonds, assureurs et fonds de pension qui investissent à l'international et couvrent leur risque de change génèrent une relation symbiotique entre les flux obligataires et l'activité sur les dérivés FX, faisant de ces derniers un baromètre de premier plan des conditions financières mondiales.

---

## 4. Constrained Liquidity Provision in Currency Markets

**Auteurs :** Information non détectée (BIS Working Paper No 1073 ; mention d'Angelo Ranaldo, BIS)
**Hypothèse Centrale :** Les contraintes de bilan des banques teneurs de marché réduisent simultanément l'offre de liquidité (hausse des coûts) et génèrent une demande atypique de liquidité à court terme, notamment autour des dates de reporting trimestriel.
**Modèle / Équations Clés :** Contrainte de bilan : `σ × q ≤ T` ; coût de liquidité via véhicule : `VLOOP = (m_x - m_y) / m_z` ; coût total : `TCOST = (s_x + s_y + s_z) / 2`.
**Stratégie Empirique :** Données de trading FX spot de CLS Group (settlement system mondial) et données de cotations ; identification des chocs d'offre de liquidité via les ratios de levier des dealers ; régressions avec effets fixes sur paires de devises et dates.
**Conclusion Principale :** Les contraintes des dealers expliquent à la fois la hausse des coûts de liquidité et un pic paradoxal des volumes en fin de trimestre, ce dernier étant lié à une demande de financement à court terme par des agents contraints.

---

## 5. Segmented Money Markets and CIP Arbitrage

**Auteurs :** Information non détectée (BIS Working Paper)
**Hypothèse Centrale :** La violation persistante de la CIP post-crise s'explique par la segmentation des marchés monétaires et l'hétérogénéité des coûts de financement entre banques, rendant impossible la loi du prix unique dans les marchés internationaux.
**Modèle / Équations Clés :** CIP : `(1 + r^$) = (F/S)(1 + r)` ; base CIP : `Basis_t = (F_t/S_t)(1 + r_{t,€}) - (1 + r_{t,$})` ; arbitrage LOOP vs CIP distingués explicitement.
**Stratégie Empirique :** Construction d'un jeu de données sur les taux du marché monétaire (LIBOR, OIS, repo) pour plusieurs devises G10 ; analyse de la base CIP avec taux OIS pour isoler les primes de liquidité de financement ; panel multi-devises.
**Conclusion Principale :** Dans un environnement post-crise de marchés segmentés et de coûts de financement hétérogènes, les arbitragistes CIP ne peuvent éliminer les écarts, car leurs propres contraintes de bilan leur imposent des coûts de financement supérieurs aux gains potentiels de l'arbitrage.

---

## 6. Foreign Exchange Swap Liquidity

**Auteurs :** Information non détectée
**Hypothèse Centrale :** La liquidité du marché mondial des swaps FX est hautement fragmentée et instable par rapport au marché spot, et les contraintes des dealers créent une dynamique paradoxale (hausse des volumes avec dégradation de la liquidité) en fin de trimestre.
**Modèle / Équations Clés :** Price impact : `PI_{t}^{(x|y)} = RPV_t^{(x|y)} / V_t^{(x|y)}` ; swap point (base de swap) : `SP_t^{(x|y),m} = F_t^{(x|y),m} - S_t^{(x|y)}`.
**Stratégie Empirique :** Première étude systématique mondiale de la liquidité des swaps FX à partir des données de CLS Group ; mesures de tightness et de depth ; analyse des effets de fin de trimestre et lien avec la base CIP.
**Conclusion Principale :** La liquidité des swaps FX est fragile et liée aux contraintes des intermédiaires ; un nouveau canal de demande de financement à court terme explique la hausse simultanée des volumes et la détérioration de la liquidité en fin de trimestre ; forte corrélation avec la base cross-currency.

---

## 7. Can Time-Varying Currency Risk Hedging Explain Exchange Rates?

**Auteurs :** Leonie Bräuer, Harald Hau
**Hypothèse Centrale :** La hausse des positions obligataires nettes internationales des investisseurs non américains au cours de la dernière décennie explique l'augmentation de la demande nette de couverture en dollars via les dérivés FX, lesquels influencent les taux de change spot via l'arbitrage CIP.
**Modèle / Équations Clés :** Hedging pressure : `HP_{c,t} = 100 × (Dollar Short - Dollar Long) / (Outstanding Interest Market)_{c,t}` ; lien avec les taux spot via l'arbitrage CIP entre marchés spot et swap.
**Stratégie Empirique :** Données CLS sur les positions en dérivés FX (forwards et swaps encours) pour 7 grandes devises contre USD, 2012–2022 ; ratio de capital des intermédiaires comme variable instrumentale pour l'offre de couverture ; IV pour identifier la demande inélastique.
**Conclusion Principale :** Les variations des positions nettes de couverture des investisseurs institutionnels expliquent environ 30 % de la variation mensuelle des sept principaux taux de change contre dollar sur 2012–2022, confirmant un canal de détermination des taux de change par la demande de couverture.

---

## 8. FX Swaps and Forwards: Missing Global Debt

**Auteurs :** Claudio Borio, Robert McCauley, Patrick McGuire (BIS)
**Hypothèse Centrale :** Les engagements en dollars contractés via les swaps et forwards FX constituent une dette mondiale cachée hors bilan, fonctionnellement équivalente à des repos, d'un montant comparable (voire supérieur) aux $10,7 billions de dette dollar inscrite au bilan.
**Modèle / Équations Clés :** Comparaison bilancielle entre repo (on-balance sheet) et FX swap (off-balance sheet) pour une même position économique ; décomposition des $58 billions d'encours en swaps/forwards FX par contrepartie et devise.
**Stratégie Empirique :** Combinaison de sources de données BIS (statistiques OTC sur les dérivés, enquête triennale), données de la Fed et sources nationales pour estimer la taille et la distribution de la dette cachée ; analyse descriptive et comptable.
**Conclusion Principale :** Les non-résidents (en particulier les non-banques hors États-Unis) détiennent des montants massifs de dette dollar hors bilan via swaps/forwards FX, créant des risques de refinancement systémiques invisibles aux régulateurs et aux analystes de stabilité financière.

---

## 9. Global Bank Lending and Exchange Rates

**Auteurs :** Information non détectée (BIS Working Paper)
**Hypothèse Centrale :** Les flux transfrontaliers de prêts syndiqués en devises étrangères par les banques globales influencent significativement les taux de change, avec une élasticité accrue lorsque les intermédiaires sont contraints en capital ou que les conditions de financement en dollars se tendent.
**Modèle / Équations Clés :** Taux de change d'équilibre : `e_0 = (1+Γ)ι_0 + E[ι_1] - Γf*/(2+Γ)` (modèle Gabaix-Maggiori adapté) ; flux nets de prêts cross-currency : `NCCL_{c,t} = log(loans USD_{c,t}) - log(loans^c_{US,t})`.
**Stratégie Empirique :** Données granulaires sur les prêts syndiqués (DealScan) pour plusieurs devises et pays emprunteurs ; régressions de panel des variations de taux de change sur les flux nets de prêts cross-currency ; tests sur le rôle du levier des broker-dealers et des conditions de financement USD.
**Conclusion Principale :** Un accroissement net des prêts en dollars par les banques étrangères apprécie le dollar ; l'effet est amplifié quand les intermédiaires sont contraints, confirmant que les flux de prêts bancaires cross-currency constituent un canal de transmission vers les taux de change.

---

## 10. Exchange Rate Determination Under Limits to CIP Arbitrage

**Auteurs :** Information non détectée
**Hypothèse Centrale :** Sous des limites à l'arbitrage CIP, le taux de change et la déviation CIP sont conjointement déterminés par l'équilibre simultané des marchés FX spot et swap, permettant à de nouveaux chocs financiers transitant par le marché des swaps d'affecter le taux de change.
**Modèle / Équations Clés :** Taux synthétique : `1 + i_{$}^{syn} = (F_t/S_t)(1 + i_e)` ; déviation CIP (base) : `(1 + i_e)(F_t/S_t) = 1 + i_$` ; modèle à deux pays avec ménages, banque centrale et intermédiaires contraints.
**Stratégie Empirique :** Modèle théorique calibré ; analyse comparative statique de chocs financiers divers (lignes de swap des banques centrales, demande de couverture, chocs de politique monétaire) ; confrontation aux faits stylisés post-2008.
**Conclusion Principale :** Les déviations CIP persistent en équilibre sous contraintes d'arbitrage limitées et les chocs transitant par le marché des swaps (couverture, lignes de swap banques centrales) ont des effets sur le taux de change absents dans les modèles à CIP parfaite.

---

## 11. The Hedging Channel of Exchange Rate Determination

**Auteurs :** Information non détectée
**Hypothèse Centrale :** Les déséquilibres extérieurs nets des pays génèrent une demande de couverture de change qui, combinée à des contraintes d'intermédiation financière, explique à la fois le niveau et la volatilité des taux de change spot et forward.
**Modèle / Équations Clés :** Utilité de l'investisseur : `U_n = E[W_n^2] - (γ/2)Var[W_n^2]` ; richesse : `W_n^2 = h_n X_n R_D F_n (hedged) + (1-h_n) X_n R_D S_n^2 (unhedged)` ; équilibre des marchés forward et spot déterminant la base et les taux.
**Stratégie Empirique :** Données sur les positions nettes extérieures et les taux de couverture pour les devises G10 (AUD, CAD, CHF, EUR, GBP, JPY, NOK, NZD, SEK) ; tests des moments conditionnels et inconditionnels des taux de change, prix d'options et bases cross-currency.
**Conclusion Principale :** Le canal de couverture relie les déséquilibres extérieurs à la dynamique des taux de change : les pays avec de grandes positions nettes en actifs étrangers présentent une appréciation de leur monnaie lors des périodes de stress financier, confirmé empiriquement sur les G10.

---

## 12. Risk and Resilience in the Global FX Market

**Auteurs :** Information non détectée (Chapitre du Global Financial Stability Report, FMI)
**Hypothèse Centrale :** La montée des institutions financières non bancaires (IFNB) et l'expansion des dérivés FX rendent le marché des changes mondial plus vulnérable aux chocs macrofinanciers, amplifiant les coûts de financement, la volatilité et les tensions de liquidité.
**Modèle / Équations Clés :** Information non détectée (étude empirique/descriptive sans formule centrale publiée dans le JSON).
**Stratégie Empirique :** Données de turnover BIS (triennial survey, $9,6 trillions/jour) ; mesures de stress FX (base CIP, volatilité excess spot-return, coûts de transaction) ; régressions VAR et panel sur l'effet des chocs d'incertitude macrofinancière sur les conditions de marché FX.
**Conclusion Principale :** Une hausse de l'incertitude macrofinancière élève significativement les coûts de financement FX, détériore la liquidité et amplifie la volatilité des taux de change ; les vulnérabilités structurelles (IFNB, fragmentation) exacerbent ces effets et appellent à un renforcement de la surveillance et des coussins de liquidité.

---

## 13. Covered Interest Parity Lost: Understanding the Cross-Currency Basis

**Auteurs :** Claudio Borio, Robert McCauley, Patrick McGuire, Vladyslav Sushko (BIS)
**Hypothèse Centrale :** Les violations persistantes de la CIP depuis la Grande Crise Financière reflètent la combinaison d'une demande inélastique de couverture de change et de limites à l'arbitrage plus strictes résultant de contraintes de bilan post-crise et d'une gestion des risques plus rigoureuse.
**Modèle / Équations Clés :** CIP : `F/S = (1 + i*)/(1 + i)` ; base cross-currency (déviation CIP) : `basis = F/S × (1+i*) - (1+i)` → `-(i - i* - (F-S)/S)` ; coûts d'arbitrage transmis via contraintes de bilan.
**Stratégie Empirique :** Données de marché sur les bases cross-currency pour plusieurs devises G10 (principalement USD/JPY, USD/EUR) ; indicateurs quantitatifs de la demande de couverture et des contraintes d'arbitrage ; régressions de panel transversales (devises) et temporelles sur les déterminants de la base.
**Conclusion Principale :** La base cross-currency persistante et négative depuis 2014 reflète une demande de couverture inélastique (assureurs, fonds de pension japonais et européens couvrant leurs positions en bons du Trésor US) confrontée à une capacité d'arbitrage limitée des banques, validé empiriquement en coupe transversale et en série temporelle.

---

## 14. Synthetic Dollar Funding

**Auteurs :** Umang Khetan
**Hypothèse Centrale :** Lorsque les banques mondiales font face à des contraintes sur leur accès au financement en gros en dollars (wholesale), elles substituent ce financement par des swaps de change (FX swaps) comme source "synthétique" de dollars, ce qui cause des déviations par rapport à la parité des taux d'intérêt couverte (CIP).
**Modèle / Équations Clés :** `∆Synthetic Dollars_c,t = β∆MMF Holdings_c,t + Controls + α_c + α_t + ε_c,t` ; `Net Synthetic Dollars_s,c,t = βTreated × Post + Controls + α_c + α_t + ε_s,c,t` ; `L^D = L^W + L^S` (offre totale de dollars = wholesale + synthétique).
**Stratégie Empirique :** Données journalières de flux d'ordres FX (CLS MarketData, janv. 2013–déc. 2023) et données mensuelles N-MFP (SEC) sur les money market funds (MMFs) ; stratégie de variables instrumentales exploitant la variation idiosyncratique de la disponibilité du dollar en gros pour identifier l'effet causal.
**Conclusion Principale :** Une augmentation de la demande de swaps par les banques (due aux contraintes en gros) cause des déviations de la CIP et augmente les coûts de couverture des institutions non-bancaires ; une baisse sévère du financement en gros peut perturber le crédit mondial en dollars, mais un relâchement des contraintes pourrait réduire de moitié les déviations CIP.

---

## 15. FX Spot and Swap Market Liquidity Spillovers

**Auteurs :** Andreas Schrimpf, Vladyslav Sushko (BIS)
**Hypothèse Centrale :** La liquidité du marché FX au comptant et la liquidité du marché FX des swaps sont intimement liées, et leurs co-mouvements ont été renforcés depuis 2014, avec des épisodes de sécheresse de liquidité de financement qui se propagent vers la liquidité de marché.
**Modèle / Équations Clés :** `Spread_S^h = (S^ask_h − S^bid_h) / S^mid_h` (spread de liquidité spot) ; `Spread_F^h = (F^ask_h − F^bid_h) / F^mid_h` (spread de liquidité swap) ; `F discount_h = (F^mid_h − S^mid_h) / S^mid_h`.
**Stratégie Empirique :** Données tick-level (Refinitiv Tick History) pour JPY/USD et EUR/USD sur 1er février 2010 – 31 mai 2017 à fréquence horaire ; analyse des co-mouvements entre liquidité de marché (spreads bid-ask) et liquidité de financement (cross-currency basis), avec sous-périodes pré- et post-2014.
**Conclusion Principale :** La co-évolution entre liquidité de marché FX spot et liquidité de financement FX (swaps) s'est intensifiée après 2014, et les sécheresses de liquidité de financement se propagent désormais vers la liquidité de marché ; la concurrence entre dealers joue un rôle clé dans ce mécanisme.

---

## 16. The Failure of Covered Interest Parity: FX Hedging Demand and Costly Balance Sheets

**Auteurs :** Information non détectée (BIS Working Paper)
**Hypothèse Centrale :** La demande nette de couvertures en FX par des agents à « habitat préféré » (assureurs, fonds de pension) est le principal facteur expliquant le niveau persistant des déviations de CIP, tandis que les bilans coûteux des banques constituent la friction qui les rend durables.
**Modèle / Équations Clés :** `F_{t,τ}/S_t × (1 + R*_{t,τ}) = 1 + R_{t,τ}` (CIP standard) ; `F_{t,1} − S_t = S_t × (1 + R_{t,τ} + b_{t,1})/(1 + R*_{t,τ}) − S_t` (définition du basis).
**Stratégie Empirique :** Analyse en composantes principales (PCA) de la structure par termes des déviations CIP pour EUR/USD, USD/JPY, AUD/USD ; modèle à correction d'erreur (ECM) avec mesures de la demande de couverture FX (positions nettes à terme des agents non-bancaires) et proxies de liquidité ; données de 2008 à 2016.
**Conclusion Principale :** La demande de couverture FX est le facteur de premier ordre des déviations persistantes de CIP au niveau long terme, et cette relation est robuste à travers les paires de devises ; les frictions de bilan bancaire (coûts de provisions pour risques de marché et de contrepartie sur les dérivés OTC) renforcent l'effet.

---

## 17. Quantities and Covered-Interest Parity

**Auteurs :** Nathan Foley-Fisher, Rodney Garratt, Stefan Gissler, Borghan Narajabad (Federal Reserve Board)
**Hypothèse Centrale :** Les positions réelles des banques dans les marchés de CIP arbitrage révèlent trois frictions nouvelles qui expliquent les déviations CIP : la rareté des actifs étrangers sûrs, le pouvoir de marché et la segmentation des intermédiaires spécialisés, et la concentration de la demande.
**Modèle / Équations Clés :** `Basis_k ≡ P_{f,k} − r_k` (définition du basis) ; chaque intermédiaire i maximise `E(W_{i,2}) − (γ_i/2) V(W_{i,2})` (objectif moyenne-variance).
**Stratégie Empirique :** Données de supervision confidentielles FR 2052a (Complex Institution Liquidity Monitoring Report) couvrant 25 000 milliards USD de positions notionnelles journalières ; exploitation de la variation croisée entre devises et maturités des bases CIP pour identifier les frictions.
**Conclusion Principale :** Les banques prêtent le plus de dollars dans les marchés (devise/maturité) où les déviations CIP sont les plus larges ; la rareté d'actifs étrangers sûrs, la segmentation des intermédiaires et la concentration de la demande sont les trois forces principales qui engendrent et maintiennent les bases CIP.

---

## 18. Breaking Parity: Equilibrium Exchange Rates and Currency Premia

**Auteurs :** Gino Cenedese, Pasquale Della Corte, Tianyu Wang (IMF Working Paper)
**Hypothèse Centrale :** Les primes de devises (CIP et UIP) et les taux de change d'équilibre sont déterminés conjointement par l'offre et la demande de couverture des banques intermédiaires soumises à des contraintes de bilan de type VaR, ce qui relie la dynamique des taux de change aux frictions d'intermédiation.
**Modèle / Équations Clés :** `B*_t + H*_t + A*_t = W*_t + D*_t` (bilan de la banque globale) ; prime UIP `= R*_t − R_t E_t/S_t × S*_t`.
**Stratégie Empirique :** Panel de devises G7+ et 4 marchés émergents à fréquence mensuelle (horizon 3 mois) ; utilisation de positions futures des dealers bancaires comme proxy de l'offre nette de devises ; panel dynamique avec estimateurs GMM et régressions en coupe transversale sur les primes CIP et UIP.
**Conclusion Principale :** Les primes de devises et la dynamique des taux de change sont rationalisées par un modèle d'intermédiation où les banques soumises à des contraintes VaR déterminent conjointement les primes CIP et UIP ; les déviations de parité reflètent des primes d'équilibre frictionnelles plutôt que de pures opportunités d'arbitrage.

---

## 19. Deviations from Covered Interest Rate Parity

**Auteurs :** Wenxin Du, Alexander Tepper, Adrien Verdelhan (NBER Working Paper No. 23170, 2017)
**Hypothèse Centrale :** Les déviations de la CIP post-crise constituent de larges opportunités d'arbitrage persistantes et systématiques qui ne peuvent s'expliquer par le risque de crédit ou les coûts de transaction, et sont causalement liées aux réglementations bancaires pesant sur les bilans en fin de trimestre.
**Modèle / Équations Clés :** `(1 + y$_{t,t+n})^n = (1 + y_{t,t+n})^n × S_t/F_{t,t+n}` (CIP) ; `ρ_{t,t+n} ≡ (1/n)(f_{t,t+n} − s_t) = y_{t,t+n} − y$_{t,t+n}` (basis).
**Stratégie Empirique :** Données sur les taux forward et les obligations KfW émises en plusieurs devises pour les G10 ; analyse de la structure par termes des bases CIP ; exploitation des effets de fin de trimestre comme variation quasi-expérimentale pour identifier l'effet causal de la réglementation bancaire.
**Conclusion Principale :** Les déviations de CIP sont grandes, persistantes et systématiques pour les principales devises du G10, particulièrement prononcées en fin de trimestre (effet des bilans bancaires) ; l'interaction entre l'intermédiation financière coûteuse et les déséquilibres internationaux d'offre et de demande de financement explique ces déviations.

---

## 20. The Dollar, Bank Leverage and the Deviation from CIP

**Auteurs :** Stefan Avdjiev, Wenxin Du, Catherine Koch, Hyun Song Shin (BIS Working Paper)
**Hypothèse Centrale :** Il existe une relation triangulaire entre la force du dollar américain, les déviations de CIP et le crédit bancaire transfrontalier libellé en dollars : un dollar plus fort est associé à des bases CIP plus larges et à une croissance plus faible du crédit transfrontalier en dollars.
**Modèle / Équations Clés :** `(1 + y$_{t,t+n})^n = (1 + y^i_{t,t+n} + x_{it,t+n})^n × S_{it}/F_{it,t+n}` (CIP) ; `∆x_{it} = α_i + β∆Dollar_t + γ∆BER_{it} + δ CONTR_{it} + ε_{it}`.
**Stratégie Empirique :** Panel de devises G10 et données de prêts transfrontaliers BIS à fréquence journalière et trimestrielle ; régressions de panel avec effets fixes et SVARs structurels (SPVARs) ; étude d'événement autour de l'élection présidentielle américaine de novembre 2016.
**Conclusion Principale :** Un dollar plus fort comprime le levier bancaire, ce qui élargit les bases CIP et réduit le crédit transfrontalier en dollars ; le mécanisme opère via l'effet du taux de change sur le coût d'ombre du levier bancaire.

---

## 21. Central Bank Dollar Swap Lines and Overseas Dollar Funding Costs

**Auteurs :** Linda S. Goldberg, Craig Kennedy, Jason Miu (Federal Reserve Bank of New York)
**Hypothèse Centrale :** Les lignes de swap en dollars de la Fed avec les banques centrales étrangères ont été un outil efficace pour réduire les coûts de financement en dollars pour les banques étrangères lors de la crise financière de 2007–2009.
**Modèle / Équations Clés :** `Basis_t = (F_{t,t+s}/S_t) × (1 + r^{eurLibor}_t) / (1 + r^{Libor}_t) − 1` (basis FX swap) ; condition d'efficacité comparative des facilités TAF vs swaps BCE.
**Stratégie Empirique :** Analyse descriptive et économétrique de l'évolution des encours et des prix des facilités CB swap (2007–2010) ; comparaison des coûts directs et indirects (collatéral) des TAF auctions versus dollar swap lines ; discussions avec participants de marché.
**Conclusion Principale :** Les facilités de swap en dollars de la Fed ont efficacement réduit les coûts de financement en dollars à l'étranger et constituent un outil important pour gérer les perturbations systémiques de liquidité ; leur performance est liée aux enchères TAF qui fournissaient également de la liquidité dollar.

---

## 22. Changing Patterns of Capital Flows

**Auteurs :** Comité sur le Système Financier Global (CGFS), Banque des Règlements Internationaux — présidé par Philip Lowe (Gouverneur, Reserve Bank of Australia)
**Hypothèse Centrale :** La décennie post-GFC a vu des changements significatifs dans la composition des flux de capitaux (passage des banques aux non-banques), qui ont réorienté plutôt que réduit les risques liés aux flux de capitaux volatils, notamment pour les économies de marché émergentes (EMEs).
**Modèle / Équations Clés :** Information non détectée (rapport institutionnel sans modèle formel central).
**Stratégie Empirique :** Analyse des flux de capitaux internationaux à fréquence trimestrielle pour les EMEs et les économies avancées sur la période post-GFC ; enquête auprès de 34 banques centrales (août 2020) ; panel de régressions sur les déterminants des flux entrants par type ; analyse des arrêts soudains (sudden stops).
**Conclusion Principale :** La montée en puissance des investisseurs non-bancaires (gestionnaires d'actifs) et le passage au financement de marché ont diversifié les sources de financement pour les EMEs mais n'ont pas réduit la fréquence des chocs extrêmes ; des outils macro-prudentiels et de gestion des flux de capitaux restent nécessaires pour la stabilité financière.

---

## 23. Offshore Dollar Creation and the Emergence of the Post-2008 International Monetary System

**Auteurs :** Steffen Murau
**Hypothèse Centrale :** Le système monétaire international (SMI) post-2008 se structure autour d'une « sphère offshore du dollar » où des institutions financières non-américaines créent de la monnaie de crédit libellée en dollars hors du territoire américain, constituant le véritable cœur de la liquidité internationale contemporaine.
**Modèle / Équations Clés :** Information non détectée (article théorique utilisant le cadre « Money View » sans équations formelles).
**Stratégie Empirique :** Analyse conceptuelle et institutionnelle basée sur le cadre « Money View » de Perry Mehrling ; cartographie des trois composantes de la sphère offshore du dollar : dépôts eurodollars, shadow money offshore, et monnaie de banque centrale du réseau C6 de swaps ; entretiens avec des praticiens.
**Conclusion Principale :** Le SMI a une qualité systémique fondée sur la création de crédit-monnaie en dollars offshore par des banques commerciales, des banques shadow et des banques centrales ; cette sphère offshore du dollar est la principale source de liquidité internationale, mais sa fragilité structurelle a été révélée par la crise de 2007–2009.

---

## 24. Repo and FX Swap: A Tale of Two Markets

**Auteurs :** Information non détectée (BCE / Eurosystème)
**Hypothèse Centrale :** Pour les grandes banques de la zone euro, les marchés repo et FX swap sont des substituts proches pour l'obtention de financement en dollars, mais les coûts de bilan plus élevés des repos conduisent les dealers à exercer un pouvoir de marché dans les deux marchés.
**Modèle / Équations Clés :** `ρ_{t_0,t_m} = (360/ACT(t_s, t_m)) × Φ_{t,t_m}/S_t` (taux implicite FX swap) ; `y_{it} = α_t + α^R_r × 1_{rcpg(i)=r} + α^M_m × 1_{mat(i)=m} + γ_{1s} × 1_{cps(i)=s} + γ_{2s} × 1_{cps(i)=s} × q(t) + ε_{it}`.
**Stratégie Empirique :** Données de transactions effectives des grandes banques de la zone euro dans les marchés repo (SFTR) et FX swap (MMSR) de la BCE ; période août 2017 – août 2024 (FX swap) et mai 2021 – août 2024 (combiné) ; régressions de panel avec effets fixes par date, catégorie de contrepartie et maturité.
**Conclusion Principale :** Les marchés repo et FX swap sont des substituts proches pour les banques euro-zone, avec un spread repo significativement plus large que celui des FX swaps (reflet des coûts de bilan) ; les dealers exercent un pouvoir de marché dans les deux marchés malgré une utilisation similaire du bilan.

---

## 25. Hunting for Dollars

**Auteurs :** Information non détectée (BIS / Federal Reserve)
**Hypothèse Centrale :** Les banques non-américaines contraintes substituent en fin de trimestre leur emprunt en dollars sur les marchés repo américains (financement wholesale) par des FX swaps (financement synthétique), ce qui explique les hausses observées du basis CIP en fin de trimestre.
**Modèle / Équations Clés :** Leverage Ratio : `Tier 1 Capital / Total Exposure ≥ θ` ; CIP : `(1 + i^y_{t,t+n}) = (1 + i^x_{t,t+n}) × F^{x|y}_{t,t+n}/S^{x|y}_t` ; basis : `χ^{x|y}_{t,t+n} = (F^{x|y}_{t,t+n}/S^{x|y}_t) × (1 + i^x_{t,t+n}) − (1 + i^y_{t,t+n})`.
**Stratégie Empirique :** Données granulaires mondiales sur les flux de financement wholesale (repo BrokerTec Europe) et synthétique (FX swaps CLS) ; identification par l'hétérogénéité des règles de reporting réglementaires (fin de trimestre pour les banques de la zone euro vs fin d'année pour d'autres) ; analyse des prix et des quantités à un niveau bancaire individuel.
**Conclusion Principale :** Les banques de la zone euro en particulier substituent le financement repo en dollars par des FX swaps en fin de trimestre, payant une prime élevée (basis CIP plus large) pour obtenir des dollars synthétiques ; les bénéfices de cette substitution reviennent principalement aux dealers américains.

---

## 26. Currency Mispricing and Dealer Balance Sheets

**Auteurs :** Gino Cenedese, Pasquale Della Corte, Tianyu Wang (Bank of England Staff Working Paper No. 779)
**Hypothèse Centrale :** La déviation de la CIP (mispricing des devises) est directement liée aux contraintes de bilan des dealers résultant de la réglementation post-crise : les dealers avec un ratio de levier plus élevé exigent une prime supplémentaire de leurs clients pour le financement synthétique en dollars.
**Modèle / Équations Clés :** `1 + r_{$,t} = (F_{i,t}/S_{i,t}) × (1 + r_{i,t})` (CIP) ; `∂π/∂x_i = (1 + r_i) × F_i/S_i + (1 + r_i) × x_i × dF_i/dx_i − (1 + r) = 0` (condition du premier ordre du dealer).
**Stratégie Empirique :** Données de référentiel de transactions OTC (trade repository) sur les dérivés de change avec identités des contreparties divulguées ; données de levier trimestriel de 11 banques dealers (UK COREP) ; stratégie de double différence exploitant (i) la divulgation publique du ratio de levier et (ii) l'introduction du cadre de ratio de levier UK.
**Conclusion Principale :** Les dealers soumis à un ratio de levier plus élevé imposent une prime significativement plus importante pour le financement synthétique en dollars ; la causalité est établie par deux variations exogènes liées à la réglementation du ratio de levier, confirmant que les contraintes de bilan post-crise sont la source directe du mispricing des devises.

---

## 27. Dollar Debt in FX Swaps and Forwards: Huge, Missing and Growing

**Auteurs :** Claudio Borio, Robert McCauley, Patrick McGuire (BIS)
**Hypothèse Centrale :** Les swaps de change, contrats à terme et swaps de devises croisées génèrent des obligations de paiement en dollars qui n'apparaissent pas dans les bilans et sont absentes des statistiques standard de la dette, créant une dette cachée massive et en croissance rapide.
**Modèle / Équations Clés :** Information non détectée (pas de formules dans le JSON).
**Stratégie Empirique :** Données de l'enquête triennale BIS 2022 et des statistiques OTC BIS ; estimation de la dette hors bilan en supposant que les non-banques hors États-Unis sont emprunteurs nets de dollars via les swaps FX.
**Conclusion Principale :** Les non-banques hors États-Unis doivent jusqu'à 26 000 milliards de dollars en dette dollar hors bilan (double leur dette on-bilan), et les banques non-américaines environ 39 000 milliards, rendant les politiques de crise (lignes de swap de banques centrales) aveugles à la distribution géographique réelle de ces obligations.

---

## 28. The Dollar-Based Financial System Through the Window of the FX Swaps Market

**Auteurs :** Hyun Song Shin (BIS)
**Hypothèse Centrale :** Le rôle international dominant du dollar tient moins aux déséquilibres de compte courant qu'à sa fonction de monnaie de financement de choix pour les banques et les intermédiaires financiers non bancaires (NBFI) dans les marchés de capitaux mondiaux.
**Modèle / Équations Clés :** Information non détectée (pas de formules dans le JSON).
**Stratégie Empirique :** Analyse descriptive des données de l'enquête triennale BIS (flux quotidiens et encours) sur les swaps/forwards FX, ventilés par instrument, devise, échéance, secteur et localisation.
**Conclusion Principale :** Les obligations de paiement en dollars associées aux swaps/forwards FX dépassent 80 000 milliards de dollars, les NBFI sont devenus les principaux utilisateurs, et les lignes de swap des banques centrales représentent le filet de sécurité essentiel du système financier mondial en dollar.

---

## 29. Markups to Financial Intermediation in Foreign Exchange Markets

**Auteurs :** Information non détectée
**Hypothèse Centrale :** Les banques exercent un pouvoir de marché dans la tarification des contrats à terme en dollars, capturant des markups qui s'ajoutent aux déviations de la parité des taux d'intérêt couverts (CIP).
**Modèle / Équations Clés :** CIP : `e^(τ i_c,t,τ) × (F_c,t,τ / S_c,t) = e^(τ i_$,t,τ)` ; déviation : `(1/τ)(f_c,t,τ − s_c,t) = i_$,t,τ − i_c,t,τ`.
**Stratégie Empirique :** Données Bloomberg sur les taux de change spot et à terme (2013–2020) pour plusieurs paires de devises ; analyse des asymétries de prix et des effets de la concurrence sur les spreads d'arbitrage CIP.
**Conclusion Principale :** En moyenne de 2013 à 2020, les gérants d'actifs étrangers ont vendu à terme 1 100 milliards USD net ; les banques exercent un pouvoir de marché asymétrique : les spreads d'arbitrage augmentent de 6,6 pb lors d'une baisse de 25 pb des spreads de taux d'intérêt et se réduisent quand la concurrence diminue de manière prévisible.

---

## 30. Price-Setting in the Foreign Exchange Swap Market: Evidence from Order Flow

**Auteurs :** Information non détectée (Norges Bank Working Paper)
**Hypothèse Centrale :** Le flux d'ordres est le signal fondamental utilisé par les dealers pour mettre à jour le prix des swaps FX, constituant un canal de découverte des prix qui n'existait pas avant 2008.
**Modèle / Équations Clés :** CIP : `Δ = (1 + r^f_$ )^direct − (F/S)(1 + r^f_d)^synthetic` ; déviation CIP : `Δ = (1 + r^f_$ )^direct − (F/S)(1 + r^f_d)`.
**Stratégie Empirique :** Données tick Thomson Reuters sur taux spot et à terme EUR/USD, CHF/USD, JPY/USD ; données de flux d'ordres pour 1 semaine de maturité ; analyse pré/post-2008.
**Conclusion Principale :** Le flux d'ordres a un impact significatif sur le prix dans le marché des swaps FX après 2008 (effet inexistant avant), confirmant que les frictions d'arbitrage post-GFC ont transformé la structure de découverte des prix.

---

## 31. Monetary Policy Transmission in Segmented Markets

**Auteurs :** Information non détectée (ECB Working Paper Series)
**Hypothèse Centrale :** Le pouvoir de marché des banques dealers dans les marchés repo OTC européens entrave la transmission efficace de la politique monétaire de la BCE à la majorité des participants du marché.
**Modèle / Équations Clés :** Régression : `r_it = β_t X_it + ε_it` ; taux de prêt résiduel : `Loan Rate^resid_cdkns = α + β₁ BilateralVol_cdk + β₂ TotalVol_ck + β₃ RANum_c + η_n + δ_s + ω_d + ε_cdkns`.
**Stratégie Empirique :** Données réglementaires microéconomiques sur le marché repo de la zone euro (MMSR/EMIR) ; analyse des spreads entre dealers et non-dealers, et des marges d'intérêt nettes des dealers ; expériences naturelles autour de changements de politique.
**Conclusion Principale :** Les banques dealers obtiennent de meilleurs prix grâce à leur pouvoir de marché dans les marchés repo OTC, ce qui freine la transmission de la politique monétaire ; permettre aux non-banques d'accéder directement à la facilité de dépôt de la BCE pourrait améliorer cette transmission.

---

## 32. A Quantity-Driven Theory of Term Premia and Exchange Rates

**Auteurs :** Information non détectée
**Hypothèse Centrale :** La capacité de prise de risque limitée des investisseurs obligataires spécialisés, confrontés à des chocs d'offre et de demande sur les obligations longues en deux devises, détermine simultanément les taux de change et les primes de terme.
**Modèle / Équations Clés :** `H q_c,t = A_c + B · H i*_c,t − i_t + D · H y*_c,t − y_t + H ε_c,t` (régression des flux d'achat nets sur les écarts de taux courts et longs).
**Stratégie Empirique :** Modèle calibré sur données internationales d'obligations et de taux de change ; validation sur les corrélations entre rendements excédentaires sur devises et obligations longues, et les effets de QE sur les taux de change.
**Conclusion Principale :** Le modèle reproduit plusieurs faits empiriques importants, notamment la co-variation entre taux de change et primes de terme, et le fait que le QE des banques centrales affecte les taux de change ; une extension relie les taux de change spot aux déviations persistantes de la CIP.

---

## 33. The Implications of CIP Deviations for International Capital Flows

**Auteurs :** Information non détectée (ECB Working Paper Series)
**Hypothèse Centrale :** Les déviations de la CIP (cross-currency basis) depuis 2008 alourdissent le coût de couverture du risque de change et conduisent les investisseurs internationaux à réduire leurs positions FX et leurs investissements en actifs USD.
**Modèle / Équations Clés :** `CCB_t,τ = r^USD_t,τ − r^EUR_t,τ − (12/τ) log(F_t,τ / S_t)` (Synthetic USD rate) ; dynamique de la base : `df_t = (θ_t − µ_x) dt − σ_x dZ^x_t`.
**Stratégie Empirique :** Panel inédit combinant les déclarations réglementaires EMIR (transactions sur dérivés USD-EUR) et les données de détention d'obligations (SHS-S) pour les investisseurs de la zone euro, décembre 2018 – mars 2024 ; méthode OLS avec effets fixes.
**Conclusion Principale :** Des déviations CIP plus larges conduisent les investisseurs de la zone euro à réduire significativement leurs positions FX et leurs investissements en actifs USD, générant des flux de capitaux internationaux substantiels et amplifiant la volatilité financière.

---

## 34. Exchange Rate Disconnect in General Equilibrium

**Auteurs :** Information non détectée (NBER Working Paper)
**Hypothèse Centrale :** Un modèle d'équilibre général dynamique fondé sur des complémentarités stratégiques dans la fixation des prix, une faible substituabilité entre biens domestiques et étrangers, et un biais domestique dans la consommation, peut simultanément expliquer l'ensemble des grandes énigmes des taux de change (Meese-Rogoff, PPP, termes de l'échange, Backus-Smith, UIP).
**Modèle / Équations Clés :** Utilité : `E_0 Σ β^t [e^(χt)/(1−σ)] C^(1−σ)_t − e^(κt)/(1+1/ν) L^(1+1/ν)_t` ; contrainte budgétaire : `P_t C_t + B_t+1/R_t + B*_t+1/(E_t e^(ψt) R*_t) ≤ B_t + B*_t E_t + W_t L_t + Π_t − T_t + Ω_t`.
**Stratégie Empirique :** Modèle calibré sur données macroéconomiques internationales (moments Meese-Rogoff 1983, Rogoff 1996, Atkeson-Burstein 2008) ; solution analytique en forme close testée sur l'ensemble des puzzles de taux de change.
**Conclusion Principale :** Le modèle fournit une résolution unifiée et analytiquement traçable des principales énigmes des taux de change via deux blocs : un processus de chocs exogènes et un mécanisme de transmission reposant sur des complémentarités stratégiques de prix.

---

## 35. U.S. Banks and Global Liquidity

**Auteurs :** Information non détectée (Federal Reserve Board, International Finance Discussion Papers)
**Hypothèse Centrale :** Les grandes banques américaines (GSIBs) jouent un rôle central d'intermédiaires dans le financement dollar mondial en puisant dans leurs réserves excédentaires pour substituer les emprunts repo et prêter davantage sur le marché des swaps FX en période de pénurie de liquidité dollar.
**Modèle / Équations Clés :** `FX Swap Lend court terme = FC Reverse Repo − FC Repo + FC Excess Reserve` ; `ΔTGAt = ΔTSYIssue_t + ΔTGAOther_t`.
**Stratégie Empirique :** Données de bilans bancaires américains (Y-9C/FR2644), données repo et swaps FX, étude d'événements autour des fins de trimestre, variations TGA et SOMA ; régressions avec indicateurs de pénurie de liquidité.
**Conclusion Principale :** Les GSIBs américaines réduisent leurs réserves à la Fed pour substituer les emprunts repo et prêter sur le marché des swaps FX lors des pénuries de dollars ; les entités non-broker-dealer au sein des BHC fournissent des fonds internes aux bras broker-dealer qui les prêtent ensuite.

---

## 36. Dollar Asset Holdings and Hedging Around the Globe

**Auteurs :** Information non détectée
**Hypothèse Centrale :** Les investisseurs institutionnels étrangers détiennent des quantités massives d'actifs en dollars et couvrent une part significative de leur exposition au risque de change malgré des coûts de couverture élevés, et cette demande de couverture agrégée affecte les coûts de hedging en présence d'intermédiaires contraints.
**Modèle / Équations Clés :** `X^(c,$)_(t,ω) = (R^$_(t,ω)/R^c_(t,ω)) × (F_(t,ω)/S_t)^(12/ω) → 1` ; `x^(c,$)_(t,ω) = ln(1 + X^(c,$)_(t,ω))`.
**Stratégie Empirique :** Compilation de déclarations détaillées (sector statistics et company filings) de fonds mutuels, fonds de pension et assurances dans plusieurs pays ; données sur 20 ans jusqu'en 2019 ; régression de la demande de couverture sur les rendements FX attendus et la variance.
**Conclusion Principale :** Les avoirs étrangers en USD ont été multipliés par six sur deux décennies ; les ratios de couverture ont augmenté de 15 points de pourcentage après 2008-09 ; la couverture atteint 2 000 milliards en 2019 ; les rendements FX attendus (au-delà de la minimisation de variance) déterminent l'exposition aux devises.

---

## 37. FX Policy When Financial Markets Are Imperfect

**Auteurs :** Matteo Maggiori (Stanford University Graduate School of Business, NBER, CEPR)
**Hypothèse Centrale :** Lorsque les marchés financiers sont imparfaits (capacité de prise de risque limitée des intermédiaires), les taux de change sont déterminés par les déséquilibres d'offre et de demande d'actifs en différentes devises, rendant l'intervention FX efficace et potentiellement amélioratrice du bien-être.
**Modèle / Équations Clés :** Modèle Gabaix-Maggiori (2015) : contrainte de crédit `V_0 e_0 ≤ Γ q²_0 e_0` ; demande agrégée des financiers `Q_0 = (1/Γ) E[(e_0 − e_1 R*/R)]` ; taux de change : `e_0 = (1+Γ)ξ_0 + E[ξ_1]/2 + Γ`.
**Stratégie Empirique :** Modèle théorique à deux pays (US-Japon) avec financiers contraints ; calibration sur données internationales ; analyse comparative des interventions FX au Brésil, Israël et Suisse.
**Conclusion Principale :** L'intervention FX est inefficace en marchés parfaits (neutralité Modigliani-Miller/équivalence ricardienne) mais efficace et optimale sous frictions financières ; son efficacité est croissante avec la sévérité des contraintes et plus forte dans les marchés peu profonds comme les économies émergentes.

---

## 38. The International Dimension of Repo: Five New Facts

**Auteurs :** Information non détectée (ECB / BIS Working Paper)
**Hypothèse Centrale :** Le marché repo international, successeur du marché eurodollar non sécurisé, est dominé par le dollar américain et joue un rôle critique dans le financement transfrontalier, notamment pour les entités de la zone euro.
**Modèle / Équations Clés :** Régression : `i_t = α + β · USD_it + δ′ X_it + µ_t + ε_it` (impact de la dénomination en USD sur les taux repo).
**Stratégie Empirique :** Securities and Financing Transactions Datastore (SFTDS) – microdata réglementaires granulaires de la zone euro couvrant les repos multi-devises ; analyse de panel avec effets fixes temporels.
**Conclusion Principale :** Cinq faits nouveaux : les repos en USD impliquant des entités de la zone euro représentent environ 40 % des encours ; le dollar domine le marché repo international comme il dominait le marché eurodollar ; ces marchés sont hautement intégrés à l'échelle internationale et les acteurs américains jouent un rôle pivot.

---

## 39. Volatility, Intermediaries, and Exchange Rates

**Auteurs :** Information non détectée
**Hypothèse Centrale :** La volatilité variable dans le temps entraîne les taux de change via la gestion du risque des intermédiaires financiers à effet de levier soumis à des contraintes de Value-at-Risk : une volatilité plus élevée resserre les contraintes financières et oblige les intermédiaires à exiger des rendements plus élevés sur les actifs étrangers.
**Modèle / Équations Clés :** `log X_t+1 − log X_t = µ + τ(log Y_t − log X_t) + σ_X,t ε_X,t+1` ; `log(σ_X,t+1) = (1−ρ_σ) log σ + ρ_σ log(σ_X,t) + σ_σ η_X,t+1`.
**Stratégie Empirique :** Estimation par méthode des moments simulés (SMM) à fréquence trimestrielle ; paramètres calibrés sur des valeurs standard (taux d'actualisation 0,995, aversion au risque 2) et estimés pour reproduire les moments empiriques des taux de change.
**Conclusion Principale :** Le modèle résout quantitativement le puzzle de Backus-Smith, le forward premium puzzle, le puzzle de volatilité des taux de change, et génère des déviations de la CIP ; la volatilité est le canal principal par lequel les contraintes des intermédiaires affectent les prix d'actifs internationaux.
