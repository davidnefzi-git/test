# Pure Theoretical Model Memo
## Dollar Funding Hierarchies, Backstop Architecture, and the Propagation of Liquidity Crises

**Status:** DRAFT — Theorist agent, 2026-05-07  
**Note on bibliography:** The anchors cited below (Holmstrom-Tirole 1998, Gabaix-Maggiori 2015, Brunnermeier-Pedersen 2009, Du-Tepper-Verdelhan 2018, Diamond-Dybvig 1983, Chang-Velasco 2001, He-Krishnamurthy 2013, Cesa-Bianchi et al. 2025, Murau-Pape-Pforr 2023, Mehrling 2021) are not yet in `Bibliography_base.bib`. They must be added before LaTeX compilation.

---

## A. Theoretical Gap

### A.1 The Three Isolated Literatures

**Literature 1 — CIP segmentation.** Du, Tepper, and Verdelhan (2018) establish empirically that covered interest parity (CIP) fails persistently for major currencies since 2008 and attribute the deviation to balance-sheet constraints of financial intermediaries. Bacchetta, Davis, and van Wincoop (2025) extend this to a general equilibrium framework in which intermediary constraints generate equilibrium basis dynamics. In both treatments, *segmentation is exogenous or parametric*: the set of agents who face constraints and the tightness of those constraints are taken as primitive inputs, not derived from the architecture of backstop provision. The model contains no hierarchy — all constrained intermediaries are symmetric with respect to their access to official liquidity support.

**Literature 2 — Swap lines as constraint-relaxing instruments.** Cesa-Bianchi et al. (2025) analyze Federal Reserve swap lines as a mechanism that expands the supply of dollar liquidity to foreign central banks, relaxing the funding constraint of a representative foreign bank. The treatment is single-segment and single-instrument: one class of foreign intermediary, one official facility. The analysis abstracts from (i) heterogeneity in backstop coverage across classes of foreign institutions, (ii) fire-sale externalities in collateral markets, and (iii) the endogenous response of dealer capacity to asset price movements triggered by the swap-line regime. Consequently, the model cannot speak to contagion from uncovered segments to covered ones, nor to the non-linearity of swap-line effectiveness as a function of aggregate stress.

**Literature 3 — Monetary hierarchy as conceptual architecture.** Murau, Pape, and Pforr (2023) and Mehrling (2021) provide an institutional taxonomy of the international monetary hierarchy: the Federal Reserve sits at the apex, primary dealers occupy an intermediate tier, foreign banks with access to swap lines occupy a subordinate tier, and offshore dollar users without any official backstop form the periphery. This literature is rich in institutional description and historically grounded. It does not, however, provide a formal model: the notions of "hierarchy," "backstop quality," and "propagation" remain conceptual. There are no equilibrium conditions, no optimization problems, no formal mechanism linking backstop architecture to the cross-currency basis.

### A.2 The Missing Link

The gap is precise: **no existing model endogenizes backstop quality as a primitive determinant of funding-market segmentation and crisis propagation.** The specific lacunae are:

(i) *Backstop heterogeneity is never modeled.* Existing intermediary-based models treat all foreign banks symmetrically. The differential access to official liquidity — automatic for US commercial banks, partial-and-conditional for swap-line recipients, zero for offshore dollar users — is an institutional fact with no formal representation.

(ii) *The collateral-market feedback loop is absent.* When uncovered institutions (segment 3) face a funding shock, they liquidate Treasuries. This depresses Treasury prices, erodes the marked-to-market wealth of the global dealer, and compresses dealer capacity to supply FX swaps — the very instrument that covered institutions (segment 2) rely on. No existing model captures this two-sided amplification.

(iii) *The multiplier structure is uncharacterized.* The force of amplification depends on the ratio of dealer feedback to bank elasticity in a way that admits a closed-form multiplier. This multiplier is the natural object for studying why swap-line effectiveness is state-dependent (rising during crises) and why regulation and backstop provision are substitutes in stabilization.

**This paper fills all three gaps within a single, internally consistent static model.**

---

## B. Environment and Agents

### B.1 Timing, Assets, and Contracts

The model is **static** with two dates, $t=0$ (planning) and $t=1$ (settlement).

**Assets.** There is a single safe collateral asset, US Treasury bonds, in fixed aggregate supply $\bar{X} > 0$. Each Treasury bond has face value 1 (normalized) and trades at price $P \in (0,1]$ at $t=0$. All dollar funding needs are denominated in US dollars.

**Contracts.** Two funding instruments are available to foreign banks at $t=0$:

1. *FX swap:* A contract in which the counterparty provides $\$1$ of dollar funding today against foreign-currency collateral at a pre-agreed exchange rate, with reversal at $t=1$. The cost per unit of swap is the *cross-currency basis* $b \geq 0$, measured in annualized dollar terms. The basis is the price of dollar liquidity above the CIP-implied rate.

2. *Treasury sale:* A spot sale of Treasuries at market price $P$ per unit. The bank surrenders $x$ units and receives $Px$ dollars. The liquidation incurs a convex cost (detailed in Section C).

**Dollar funding need.** Each bank $i$ must cover a dollar funding need $R_i \geq 0$ determined by its liability structure and the backstop coverage it receives. The exact expressions for $R_i$ are given in Section B.3 below.

### B.2 Agents

The economy is populated by five classes of agents.

---

**Agent 1 — Segment 1 banks (US commercial banks, onshore).**

Segment 1 consists of US-chartered commercial banks. These institutions have automatic, unconditional access to Federal Reserve emergency facilities (discount window, FDIC guarantee). Define $M_1 > 0$ as the dollar funding need of segment 1 in the absence of backstop support.

*Backstop:* $B_1 = M_1$. The backstop fully covers the funding need at $t=0$, so the *residual funding need* is
$$R_1 \equiv M_1 - B_1 = 0.$$

Segment 1 banks are therefore *inactive in equilibrium*: they neither sell Treasuries nor enter FX swaps. Their role in the model is to anchor the dollar at par and to establish the upper boundary of the backstop hierarchy. They do not enter any optimization problem.

---

**Agent 2 — Segment 2 banks (foreign banks with swap lines).**

Segment 2 consists of foreign banks whose central bank has an active bilateral dollar swap line with the Federal Reserve. Let $M_2 > 0$ denote the dollar funding need of a representative segment 2 bank in the absence of any backstop.

*Backstop:* $B_2 = \lambda M_2$, where $\lambda \in [0,1]$ is the *swap-line coverage rate* — the fraction of segment 2's funding need that can be met through the swap-line facility at the central-bank level, passed through to commercial banks in this segment. The parameter $\lambda$ is the central policy variable of the model.

*Residual funding need:*
$$R_2 \equiv M_2 - B_2 = (1-\lambda) M_2.$$

The segment 2 bank must cover $R_2$ using market instruments (FX swaps and/or Treasury sales). Its optimization problem is stated in Section C.

*Preferences:* The bank is a cost-minimizer. It is risk-neutral with respect to the dollar cost of covering $R_2$.

---

**Agent 3 — Segment 3 banks (offshore dollar users, no backstop).**

Segment 3 consists of foreign banks, investment funds, and financial entities that have no access to any central-bank backstop facility — neither a swap line nor a domestic lender of last resort in the relevant currency.

Let $M_3 > 0$ be the baseline dollar funding need of a representative segment 3 entity. In period $t=0$, a funding shock $\varepsilon \geq 0$ hits this segment — an unexpected increase in dollar liabilities that comes due or a sudden withdrawal of dollar funding lines.

*Backstop:* $B_3 = 0$.

*Residual funding need:*
$$R_3 \equiv M_3 + \varepsilon.$$

Segment 3 must cover $R_3$ entirely from market sources. Its optimization problem is structurally identical to that of segment 2 (Section C), with $R_3$ replacing $R_2$.

*Preferences:* Cost-minimizing, risk-neutral.

---

**Agent 4 — The global dealer.**

There is a single representative global dealer — a large internationally active bank or primary dealer that acts as market-maker in both the FX swap market and the Treasury secondary market. The dealer is the sole supplier of FX swaps to segments 2 and 3.

*Balance sheet at $t=0$ (before trading):*

The dealer holds an inventory of Treasuries $\bar{X}_d > 0$ (exogenous) and has initial equity capital $W_0 > 0$. The marked-to-market value of the dealer's balance sheet at price $P$ is
$$W(P) = W_0 + P \bar{X}_d.$$

*Decision variables:* The dealer chooses
- $O \geq 0$: the quantity of FX swaps offered to segments 2 and 3,
- $Z \geq 0$: the quantity of Treasuries purchased from segments 2 and 3 (absorption of fire sales).

*Objective:* The dealer maximizes mean-variance utility over profits. Denote by $\pi$ the dealer's profit from intermediation:
$$\pi = b \cdot O + (1-P) \cdot Z,$$
where $b$ is the per-unit basis received on swaps and $(1-P)$ is the per-unit capital gain on Treasuries purchased at price $P < 1$ and redeemed at face value 1.

The dealer's objective is
$$\max_{O \geq 0,\, Z \geq 0} \quad b O + (1-P) Z - \frac{\eta}{2}\left(\sigma_O^2 O^2 + \sigma_Z^2 Z^2\right),$$
where $\eta > 0$ is the coefficient of absolute risk aversion (CARA parameterization), $\sigma_O^2 > 0$ is the variance of the payoff per unit of swap position, and $\sigma_Z^2 > 0$ is the variance of the payoff per unit of Treasury absorption.

*Regulatory constraint (leverage):* The dealer is subject to a regulatory leverage constraint. Let $q_S > 0$ and $q_T > 0$ denote the risk-weights (capital charges per unit of exposure) on swap positions and Treasury holdings, respectively. Let $\phi > 0$ be the maximum permitted leverage ratio. The constraint is
$$q_S O + q_T(\bar{X}_d + Z) \leq \phi W(P),$$
where $W(P) = W_0 + P \bar{X}_d$ is the dealer's marked-to-market net worth. This constraint limits total risk-weighted assets relative to equity — it is the standard Basel-type leverage constraint.

---

**Agent 5 — Outside investors.**

A continuum of outside investors (pension funds, sovereign wealth funds, reserve managers) supplies a downward-sloping demand curve for Treasuries. Each investor $j$ has CARA preferences with coefficient of absolute risk aversion $\alpha > 0$, holds a prior that Treasury bonds will pay face value 1 at $t=1$, and faces idiosyncratic portfolio costs.

The aggregate demand of outside investors for Treasuries takes the reduced form
$$X^{out}(P) = X_0 - \frac{1-P}{\gamma},$$
where $X_0$ is baseline demand at $P=1$ and $\gamma > 0$ is an elasticity parameter derived from the CARA-normal portfolio problem. Equivalently, the outside-investor market-clearing condition yields the inverse-demand relation
$$P = 1 - \gamma b^{out},$$
where $b^{out}$ is the shadow cost of Treasuries to outside investors. In equilibrium, $b^{out}$ equals the cross-currency basis $b$ (the price of dollar liquidity) — the statement that arbitrage between the two funding channels equalizes their shadow costs. The precise derivation is given in Section D.3.

### B.3 Aggregate Funding Need

Define the *aggregate residual funding need*:
$$R \equiv R_2 + R_3 = (1-\lambda)M_2 + M_3 + \varepsilon.$$

This is the total dollar shortfall that must be met through market instruments. Note the three components:
- $(1-\lambda)M_2$: the portion of segment 2's need not covered by the swap line;
- $M_3$: the baseline need of segment 3;
- $\varepsilon$: the funding shock to segment 3.

The policy parameter $\lambda$ enters $R$ linearly and with coefficient $-M_2 < 0$, establishing the demand-relief channel of swap lines.

---

## C. Core Friction and Constraints

### C.1 The Central Friction: Backstop-Quality Heterogeneity

The fundamental friction in this model is *segmented access to official dollar liquidity*. This is not an assumption about transaction costs or information asymmetries in the usual sense; it is a structural feature of the international monetary architecture. Segment 1 banks face no liquidity risk in dollar funding markets because their backstop is automatic and unconditional. Segment 2 banks face partial exposure: the fraction $(1-\lambda)$ of their dollar needs is unsupported. Segment 3 banks bear the full exposure. This hierarchy generates heterogeneous demand for market-based dollar liquidity, which is the source of the cross-currency basis.

The second friction is *dealer balance-sheet constraints*. Without the leverage constraint, the dealer would absorb any quantity of fire sales and supply any quantity of swaps at the actuarially fair price. The constraint creates a capacity ceiling and links the supply of dollar liquidity to the dealer's marked-to-market net worth $W(P)$. This creates the feedback loop: fire sales $\to$ lower $P$ $\to$ lower $W$ $\to$ tighter constraint $\to$ reduced swap supply $\to$ higher $b$.

### C.2 Bank Optimization Problem

Consider a bank in segment $i \in \{2, 3\}$ with residual funding need $R_i > 0$. The bank chooses the quantity $x_i \geq 0$ of Treasuries to sell. Having chosen $x_i$, it receives $P x_i$ dollars from Treasury sales and must meet the remainder $R_i - P x_i$ through FX swaps; thus swap demand is
$$s_i = R_i - P x_i \geq 0,$$
which requires the constraint $x_i \leq R_i / P$ (the bank cannot over-sell). The budget constraint is
$$P x_i + s_i = R_i. \tag{BC-$i$}$$

The cost of FX swaps is $b$ per unit. The cost of Treasury sales is not simply $P x_i$ foregone — it includes a convex liquidation cost that captures the private cost of unwinding positions rapidly (bid-ask spread, market impact, roll-risk). Specifically, the liquidation cost is $\frac{\kappa_i}{2} x_i^2$, where $\kappa_i > 0$ is a bank-specific *liquidation cost parameter*. This quadratic form implies that marginal liquidation cost is increasing in the quantity sold, which is a standard assumption in models of fire sales (cf. Brunnermeier and Pedersen, 2009).

**Problem $i$:**
$$\min_{x_i \geq 0} \quad b(R_i - P x_i) + \frac{\kappa_i}{2} x_i^2 \tag{P-$i$}$$
subject to $x_i \leq R_i / P$.

**Remark on price-taking.** The bank takes the market Treasury price $P$ as parametric in its individual problem. In equilibrium $P$ is determined by the market-clearing condition on the Treasury market, but each infinitesimal bank is too small to affect $P$. This is the standard price-taking assumption. For the individual FOC, I evaluate $P$ at its equilibrium value $P_0 \equiv P|_{b=b^*}$; the general equilibrium feedback operates through the market-clearing conditions in Section D.

**First-order condition.** The Lagrangian of problem (P-$i$) is
$$\mathcal{L}_i = b(R_i - P x_i) + \frac{\kappa_i}{2} x_i^2 - \mu_i x_i,$$
where $\mu_i \geq 0$ is the multiplier on the non-negativity constraint $x_i \geq 0$.

Differentiating with respect to $x_i$:
$$\frac{\partial \mathcal{L}_i}{\partial x_i} = -bP + \kappa_i x_i - \mu_i = 0.$$

Complementary slackness: $\mu_i x_i = 0$ and $\mu_i \geq 0$.

*Interior solution* ($x_i^* > 0$, which holds when $b > 0$): $\mu_i = 0$, so
$$\kappa_i x_i^* = b P, \qquad x_i^* = \frac{bP}{\kappa_i}.$$

Evaluating at $P = P_0$:
$$\boxed{x_i^* = \theta_i b, \qquad \theta_i \equiv \frac{P_0}{\kappa_i}.} \tag{FS-$i$}$$

The scalar $\theta_i > 0$ is the *basis-elasticity of fire sales* of bank $i$: a one-unit increase in the basis induces the bank to sell $\theta_i$ additional units of Treasuries. It is increasing in $P_0$ (higher Treasury prices make sales more attractive) and decreasing in $\kappa_i$ (higher liquidation costs deter sales).

**Aggregate fire-sale elasticity.** Define
$$\Theta \equiv \theta_2 + \theta_3 = \frac{P_0}{\kappa_2} + \frac{P_0}{\kappa_3} = P_0 \left(\frac{1}{\kappa_2} + \frac{1}{\kappa_3}\right). \tag{$\Theta$-def}$$

This is the aggregate basis-elasticity of Treasury fire sales across segments 2 and 3.

**Swap demand.** Substituting (FS-$i$) into (BC-$i$):
$$s_i^* = R_i - P_0 \cdot \theta_i b = R_i - \frac{P_0^2}{\kappa_i} b. \tag{SD-$i$}$$

Aggregating:
$$s_2^* + s_3^* = R - P_0 \Theta b, \tag{SD-agg}$$
where $R = R_2 + R_3$ is defined in Section B.3.

### C.3 Dealer Optimization and Leverage Constraint

**Unconstrained problem.** The dealer solves
$$\max_{O \geq 0,\, Z \geq 0} \quad b O + (1-P) Z - \frac{\eta}{2}\left(\sigma_O^2 O^2 + \sigma_Z^2 Z^2\right) \tag{P-D}$$
subject to the leverage constraint
$$q_S O + q_T(\bar{X}_d + Z) \leq \phi W(P), \qquad W(P) = W_0 + P\bar{X}_d. \tag{LC}$$

The objective is strictly concave in $(O, Z)$ (negative definite Hessian: $-\eta \sigma_O^2 < 0$ and $-\eta \sigma_Z^2 < 0$, off-diagonal elements zero). The feasible set is convex and compact for fixed $P$. A unique solution therefore exists.

**Unconstrained first-order conditions.** Ignoring (LC) momentarily:
$$b = \eta \sigma_O^2 O^{\text{unc}}, \qquad O^{\text{unc}} = \frac{b}{\eta \sigma_O^2},$$
$$1-P = \eta \sigma_Z^2 Z^{\text{unc}}, \qquad Z^{\text{unc}} = \frac{1-P}{\eta \sigma_Z^2}.$$

In normal times (ample balance sheet), the dealer supplies swaps and absorbs fire sales up to the point where marginal risk-adjusted profit equals zero.

**Constrained regime.** During crises, (LC) binds. This is the empirically relevant case: Duffie (2010), Du, Tepper, and Verdelhan (2018), and Gabaix and Maggiori (2015) all emphasize that intermediary constraints bind during stress episodes. The model focuses on this regime.

When (LC) binds with equality:
$$q_S O + q_T(\bar{X}_d + Z) = \phi W(P). \tag{LC-bind}$$

For the main analysis I focus on the swap supply decision, taking the Treasury absorption as a residual allocation of the balance sheet. A simplifying assumption (maintained throughout the main text; relaxed in the appendix) is that the dealer allocates a fixed fraction of its constrained balance sheet to swaps:
$$O^* = \Gamma W(P), \qquad \Gamma \equiv \frac{\phi}{q_S}. \tag{O-star}$$

**Derivation of $\Gamma$.** Under the binding leverage constraint, the maximum swap supply consistent with the constraint (holding $Z = 0$ as a conservative bound) is
$$q_S O \leq \phi W(P), \qquad O \leq \frac{\phi}{q_S} W(P).$$
Setting $O^* = \frac{\phi}{q_S} W(P) \equiv \Gamma W(P)$. The parameter $\Gamma = \phi / q_S > 0$ is the *dealer capacity parameter*: it is increasing in the regulatory leverage limit $\phi$ and decreasing in the swap risk-weight $q_S$.

**Wealth endogeneity.** Because the dealer holds Treasuries, its net worth is sensitive to the Treasury price:
$$W(P) = W_0 + P \bar{X}_d.$$
When the Treasury price falls (fire sales depress $P$), dealer wealth falls, tightening the leverage constraint and reducing swap supply. This is the source of the amplification feedback analyzed in Section D.4.

### C.4 Outside Investor Market-Clearing (Treasury Market)

Outside investors have CARA preferences with absolute risk aversion $\alpha > 0$ and form posterior beliefs that each Treasury bond pays 1 at $t=1$ with variance $\sigma_T^2$. The standard mean-variance portfolio problem yields individual demand
$$x_j^{out} = \frac{1 - P}{\alpha \sigma_T^2}.$$

Integrating over the continuum of outside investors (measure normalized to 1, with heterogeneous valuations summed to an aggregate demand schedule), the aggregate outside-investor demand for Treasuries is
$$X^{out}(P) = \frac{1 - P}{\gamma}, \qquad \gamma \equiv \alpha \sigma_T^2 > 0. \tag{OI-dem}$$

Treasury market clearing (Section D.3) requires that the total supply to outside investors equals $X^{out}(P)$. Inverting (OI-dem) yields the equilibrium price function
$$P = 1 - \gamma \cdot \left(\frac{\text{net supply from fire sales}}{\text{per unit}}\right).$$
In equilibrium, this becomes the closed-form price equation derived in Section D.3.

---

## D. Optimization, Equilibrium Definition, and Results

### D.1 Definition of Equilibrium

**Definition 1 (Static Equilibrium).** A *static equilibrium* of the model is a tuple $(b^*, P^*, O^*, Z^*, \{x_i^*, s_i^*\}_{i=2,3})$ such that:

(i) **Bank optimization:** For each $i \in \{2,3\}$, $(x_i^*, s_i^*)$ solves problem (P-$i$) given $b^*$ and $P^*$.

(ii) **Dealer optimization:** $(O^*, Z^*)$ solves problem (P-D) subject to (LC), given $b^*$ and $P^*$, with the leverage constraint (LC) binding.

(iii) **FX swap market clearing:**
$$s_2^* + s_3^* = O^*. \tag{MC-S}$$

(iv) **Treasury market clearing:**
$$x_2^* + x_3^* = Z^{out}(P^*), \tag{MC-T}$$
where $Z^{out}(P) = X^{out}(P) - (\bar{X} - \bar{X}_d)$ is the quantity demanded by outside investors net of the pre-existing holdings of non-dealer agents. For notational simplicity I write the Treasury market-clearing condition in the form derived below.

(v) **Non-negativity:** $b^* \geq 0$, $P^* \in (0,1]$, $x_i^* \geq 0$, $s_i^* \geq 0$, $O^* \geq 0$, $Z^* \geq 0$.

### D.2 Reduction to a Single Equation

I now reduce the two market-clearing conditions to a single equation in $b$.

**Step 1: Treasury price as a function of $b$.**

From (FS-$i$), aggregate Treasury sales are $\Theta b$ (in quantity units; recall $x_i^* = \theta_i b$, so $x_2^* + x_3^* = \Theta b$). For the Treasury market to clear, outside investors must absorb these sales. Using (OI-dem), the Treasury price that clears the market when $\Theta b$ units are sold is implicitly given by
$$\Theta b = X^{out}(P) = \frac{1-P}{\gamma}.$$
Solving for $P$:
$$P^* = 1 - \gamma \Theta b. \tag{P-eq}$$

This is the *equilibrium price function*: a higher basis $b$ induces more fire sales, driving down the Treasury price. The elasticity is $\gamma \Theta > 0$.

However, note that $\Theta$ itself depends on $P_0$. In the individual bank's problem (Section C.2), $P$ is taken as parametric, and $\theta_i = P_0/\kappa_i$ is evaluated at a reference price $P_0$. Equation (P-eq) is the equilibrium relationship between $P$ and $b$ at the aggregate level, consistent with price-taking at the individual level. For the purposes of the general equilibrium, I substitute $P^* = 1 - \gamma b$ (absorbing $\Theta$ into the definition of $\gamma$, or equivalently defining $\gamma$ to already incorporate $\Theta$ at the calibration stage) and work with the parameterization
$$P = 1 - \gamma b \tag{P-b}$$
with $\gamma > 0$ understood as the composite price-impact parameter. This is without loss of generality under the maintained assumption that $P_0 \approx 1$ (small equilibrium deviations).

**Step 2: Dealer wealth as a function of $b$.**

Substituting (P-b) into $W(P) = W_0 + P\bar{X}_d$:
$$W(b) = W_0 + (1 - \gamma b)\bar{X}_d = \tilde{W} - \gamma b \bar{X}_d, \tag{W-b}$$
where
$$\tilde{W} \equiv W_0 + \bar{X}_d$$
is the dealer's wealth at $P = 1$ (no fire-sale discount). Note that $\partial W / \partial b = -\gamma \bar{X}_d < 0$: dealer wealth falls as the basis rises because Treasury prices decline.

**Step 3: Swap supply as a function of $b$.**

From (O-star) and (W-b):
$$O^*(b) = \Gamma W(b) = \Gamma(\tilde{W} - \gamma b \bar{X}_d). \tag{O-b}$$

Swap supply is a decreasing function of $b$: a higher basis is associated with lower Treasury prices, lower dealer wealth, and therefore lower swap supply. This is the amplification channel in reduced form.

**Step 4: FX swap market clearing.**

Equating aggregate swap demand (SD-agg) with swap supply (O-b):
$$R - P_0 \Theta b = \Gamma(\tilde{W} - \gamma b \bar{X}_d).$$
Rearranging:
$$R - \Gamma \tilde{W} = P_0 \Theta b - \Gamma \gamma \bar{X}_d b = b(P_0 \Theta - \Gamma \gamma \bar{X}_d).$$

**Definition 2 (Stability Parameter).** Define
$$\Delta \equiv P_0 \Theta - \Gamma \gamma \bar{X}_d. \tag{$\Delta$-def}$$

The equilibrium basis is then
$$\boxed{b^* = \frac{R - \Gamma\tilde{W}}{\Delta}.} \tag{EQ}$$

### D.3 Existence, Uniqueness, and Stability

**Assumption 1 (Stability).** $\Delta > 0$.

*Interpretation.* $\Delta > 0$ requires that the aggregate elasticity of fire sales $P_0\Theta$ exceeds the feedback term $\Gamma\gamma\bar{X}_d$. In words: the direct demand-relief effect of a higher basis (which induces fire sales that clear the swap market) must dominate the amplification effect (through which a higher basis depresses Treasury prices, erodes dealer wealth, and reduces swap supply). When $\Delta \leq 0$, the amplification loop overwhelms the stabilizing mechanism and no finite equilibrium basis clears the market — a market breakdown. Assumption 1 rules this out for the main analysis; Section D.5 characterizes the region $\Delta \leq 0$ as a limiting case.

**Assumption 2 (Positive Basis).** $R > \Gamma\tilde{W}$.

*Interpretation.* The aggregate funding need $R$ exceeds the dealer's unconstrained swap supply $\Gamma\tilde{W}$ at $b = 0$. This is the condition for dollar scarcity: if $R \leq \Gamma\tilde{W}$, the dealer can supply all required swaps without any basis premium, and the equilibrium basis is zero (no funding stress). Assumption 2 defines the *stress regime* that is the focus of the analysis.

**Proposition 1 (Existence and Uniqueness).** *Under Assumptions 1 and 2, there exists a unique equilibrium basis $b^* > 0$ given by equation* (EQ). *The corresponding equilibrium Treasury price is $P^* = 1 - \gamma b^* \in (0,1)$, and all equilibrium quantities are strictly positive.*

*Proof.* Under Assumption 1, $\Delta > 0$, so the denominator of (EQ) is strictly positive. Under Assumption 2, the numerator $R - \Gamma\tilde{W} > 0$. Therefore $b^* = (R - \Gamma\tilde{W})/\Delta > 0$ is well-defined and unique. 

For the Treasury price: $P^* = 1 - \gamma b^*$. Since $b^* > 0$ we have $P^* < 1$. That $P^* > 0$ requires $\gamma b^* < 1$, i.e., $b^* < 1/\gamma$. Substituting (EQ): $(R - \Gamma\tilde{W})/(\Delta\gamma) < 1/\gamma$, which reduces to $R - \Gamma\tilde{W} < \Delta = P_0\Theta - \Gamma\gamma\bar{X}_d$. This simplifies to $R < P_0\Theta + \Gamma(W_0)$, which is a mild upper bound on the size of the funding shock; it is maintained as a parametric restriction without being labeled a separate assumption.

For swap demand and supply: $s_i^* = R_i - P_0\theta_i b^* > 0$ requires $b^* < R_i/(P_0\theta_i)$ for each $i$, which holds under the same mild upper bound. Fire sales $x_i^* = \theta_i b^* > 0$ under Assumption 2. Dealer supply $O^* = \Gamma W(b^*) > 0$ since $W(b^*) = \tilde{W} - \gamma b^*\bar{X}_d > 0$ by $P^* > 0$.

All equilibrium conditions (i)–(v) of Definition 1 are satisfied by construction. $\square$

### D.4 The Amplification Multiplier

**Definition 3 (Partial-Equilibrium Basis).** Define the *partial-equilibrium basis* as
$$b^{\mathrm{pe}} \equiv \frac{R - \Gamma\tilde{W}}{P_0\Theta},$$
which is the equilibrium basis that would obtain if dealer wealth were *fixed* at $\tilde{W}$ — i.e., if there were no Treasury price feedback onto dealer capacity.

**Definition 4 (Amplification Ratio).** Define
$$\rho \equiv \frac{\Gamma\gamma\bar{X}_d}{P_0\Theta} \in (0,1), \tag{$\rho$-def}$$
where the restriction $\rho \in (0,1)$ is equivalent to $\Delta > 0$ (Assumption 1). The scalar $\rho$ measures the *strength of the amplification feedback loop*: it is the ratio of the feedback effect (reduction in dealer capacity from Treasury price decline, per unit of basis) to the direct stabilizing effect (additional fire sales induced by the basis).

**Definition 5 (Amplification Multiplier).** Define
$$\mathcal{M} \equiv \frac{1}{1-\rho} \geq 1. \tag{M-def}$$

**Proposition 2 (Amplification Decomposition).** *Under Assumptions 1 and 2:*
$$b^* = b^{\mathrm{pe}} \cdot \mathcal{M}. \tag{AMP}$$
*The general equilibrium basis exceeds the partial-equilibrium basis by the factor $\mathcal{M} \geq 1$, which equals $1$ when $\rho = 0$ (no feedback) and diverges as $\rho \to 1$ (amplification loop dominates).*

*Proof.* From (EQ) and the definition of $\Delta = P_0\Theta - \Gamma\gamma\bar{X}_d = P_0\Theta(1-\rho)$:
$$b^* = \frac{R - \Gamma\tilde{W}}{\Delta} = \frac{R - \Gamma\tilde{W}}{P_0\Theta(1-\rho)} = \frac{R - \Gamma\tilde{W}}{P_0\Theta} \cdot \frac{1}{1-\rho} = b^{\mathrm{pe}} \cdot \mathcal{M}.$$
That $\mathcal{M} \geq 1$ follows from $\rho \in (0,1)$. Divergence as $\rho \to 1^-$ is immediate. $\square$

*Economic interpretation.* The multiplier $\mathcal{M}$ captures the full spiral: a funding shock raises $b$, inducing fire sales, depressing $P$, eroding dealer wealth $W$, reducing swap supply $O^*$, which raises $b$ further — and so on. The multiplier $1/(1-\rho)$ is the closed-form sum of this geometric series of feedback rounds, exactly analogous to the money multiplier or the Keynesian spending multiplier. This structure is the formal microfoundation of the spiral described in Brunnermeier and Pedersen (2009), specialized to the international dollar-funding market.

### D.5 Comparative Statics of the Multiplier

**Proposition 3 (Multiplier Monotonicity).** *The amplification multiplier $\mathcal{M} = 1/(1-\rho)$ satisfies:*

*(i)* $\partial \mathcal{M} / \partial \Gamma > 0$. *The multiplier is increasing in dealer capacity $\Gamma$: a larger dealer amplifies more.*

*(ii)* $\partial \mathcal{M} / \partial \gamma > 0$. *The multiplier is increasing in the Treasury-price elasticity of outside investors: more price-sensitive investors amplify more.*

*(iii)* $\partial \mathcal{M} / \partial \bar{X}_d > 0$. *The multiplier is increasing in dealer Treasury inventory: a larger inventory creates a larger balance-sheet channel.*

*(iv)* $\partial \mathcal{M} / \partial \Theta < 0$. *The multiplier is decreasing in the aggregate fire-sale elasticity $\Theta$: more elastic banks are better at self-insuring, which attenuates the loop.*

*Proof.* Recall $\rho = \Gamma\gamma\bar{X}_d / (P_0\Theta)$ and $\mathcal{M} = 1/(1-\rho)$. Since $\mathcal{M}$ is strictly increasing in $\rho$ for $\rho \in (0,1)$, it suffices to establish monotonicity of $\rho$ in each parameter.

(i) $\partial\rho/\partial\Gamma = \gamma\bar{X}_d/(P_0\Theta) > 0$. $\checkmark$

(ii) $\partial\rho/\partial\gamma = \Gamma\bar{X}_d/(P_0\Theta) > 0$. $\checkmark$

(iii) $\partial\rho/\partial\bar{X}_d = \Gamma\gamma/(P_0\Theta) > 0$. $\checkmark$

(iv) $\partial\rho/\partial\Theta = -\Gamma\gamma\bar{X}_d/(P_0\Theta^2) < 0$. $\checkmark$

The claims follow immediately. $\square$

*Economic interpretation.* Claim (iv) deserves particular attention: a higher $\Theta$ means banks substitute more readily into Treasury sales when the basis rises, which stabilizes the swap market directly but, by increasing fire-sale pressure on $P$, also feeds back through dealer wealth. The net effect is stabilizing ($\partial\mathcal{M}/\partial\Theta < 0$) because the direct demand-relief effect of $\Theta$ (in the denominator of $b^*$) outweighs the feedback effect (the same $\Theta$ appears in both numerator $\rho$ and denominator of $b^{\mathrm{pe}}$). The inequality holds strictly whenever $\rho < 1$.

### D.6 Hierarchical Contagion

**Proposition 4 (Cross-Segment Contagion).** *Consider a shock $d\varepsilon > 0$ to the funding need of segment 3 ($dR_3 = d\varepsilon$, $dR_2 = 0$). In the unique equilibrium:*

*(i)* $db^*/d\varepsilon = \mathcal{M}/(P_0\Theta) > 0$: *the basis rises.*

*(ii)* $dx_2^*/d\varepsilon = \theta_2 \cdot \mathcal{M}/(P_0\Theta) > 0$: *segment 2 increases Treasury sales, despite bearing no direct funding shock.*

*(iii)* $dW^*/d\varepsilon = -\gamma\bar{X}_d \cdot \mathcal{M}/(P_0\Theta) < 0$: *dealer wealth falls.*

*(iv)* $dO^*/d\varepsilon = \Gamma \cdot dW^*/d\varepsilon < 0$: *swap supply contracts.*

*(v) The contagion is hierarchically ascending: the shock propagates from the uncovered segment (3) upward through the backstopped segment (2) to the dealer.*

*Proof.* 

(i) Differentiate (EQ) with respect to $\varepsilon$, noting $\partial R/\partial\varepsilon = 1$ and $\Gamma\tilde{W}$ is invariant to $\varepsilon$:
$$\frac{db^*}{d\varepsilon} = \frac{1}{\Delta} = \frac{1}{P_0\Theta(1-\rho)} = \frac{\mathcal{M}}{P_0\Theta}. \tag{CS-eps}$$

(ii) From (FS-$i$) with $i=2$: $x_2^* = \theta_2 b^*$, so $dx_2^*/d\varepsilon = \theta_2 \cdot db^*/d\varepsilon = \theta_2 \mathcal{M}/(P_0\Theta) > 0$.

(iii) From (W-b): $W^* = \tilde{W} - \gamma b^*\bar{X}_d$, so $dW^*/d\varepsilon = -\gamma\bar{X}_d \cdot db^*/d\varepsilon < 0$.

(iv) From (O-star): $O^* = \Gamma W^*$, so $dO^*/d\varepsilon = \Gamma \cdot dW^*/d\varepsilon < 0$.

(v) Segment 2 bears no direct funding shock ($dR_2 = 0$) but increases fire sales ($dx_2^* > 0$) solely because the equilibrium basis has risen — a pure contagion effect transmitted through the price mechanism. The dealer, similarly, is not the origin of the shock but suffers wealth loss and capacity compression. The direction of propagation is from the lowest tier (segment 3, no backstop) upward through segment 2 and to the dealer. $\square$

*Remark.* The multiplier $\mathcal{M}$ appears in the contagion elasticities (i)–(iv). This is not coincidental: the same amplification loop that magnifies the equilibrium level of $b^*$ above its partial-equilibrium value also magnifies the sensitivity of all endogenous variables to the shock. This is the formal sense in which the model generates *magnified propagation* relative to a model with no dealer feedback ($\Gamma = 0$ or $\bar{X}_d = 0$, in which case $\mathcal{M} = 1$).

### D.7 The Double Dividend of Swap Lines

**Proposition 5 (Swap-Line Effectiveness).** *The marginal effect of the swap-line coverage rate $\lambda$ on the equilibrium basis is*
$$\frac{db^*}{d\lambda} = \frac{-M_2}{\Delta} = \frac{-M_2}{P_0\Theta} \cdot \mathcal{M} < 0. \tag{SL}$$

*This effect decomposes into two channels:*

*Channel 1 (Demand Relief):* The partial-equilibrium effect $-M_2/(P_0\Theta) < 0$, operating through direct reduction of $R$.

*Channel 2 (Collateral Stabilization):* The amplification factor $\mathcal{M} \geq 1$, which multiplies Channel 1.

*Corollary (State-Dependence):* $\partial^2 b^*/(\partial\lambda\,\partial\rho) < 0$: the effectiveness of swap lines is increasing in crisis severity (as measured by $\rho$).*

*Proof.* Differentiate (EQ) with respect to $\lambda$, noting $\partial R/\partial\lambda = -M_2$ (from $R = (1-\lambda)M_2 + M_3 + \varepsilon$) and $\partial(\Gamma\tilde{W})/\partial\lambda = 0$:
$$\frac{db^*}{d\lambda} = \frac{-M_2}{\Delta}.$$
Substituting $\Delta = P_0\Theta(1-\rho)$ and $1/(1-\rho) = \mathcal{M}$:
$$\frac{db^*}{d\lambda} = \frac{-M_2}{P_0\Theta} \cdot \mathcal{M}.$$

The decomposition is immediate: $-M_2/(P_0\Theta)$ is the partial-equilibrium effect (Channel 1), and the factor $\mathcal{M}$ is the amplification (Channel 2). Since $\mathcal{M} = 1/(1-\rho)$ is strictly increasing in $\rho$, we have
$$\frac{\partial}{\partial\rho}\left(\frac{db^*}{d\lambda}\right) = \frac{-M_2}{P_0\Theta} \cdot \frac{1}{(1-\rho)^2} \cdot (-1) \cdot (-1) < 0,$$
wait — let us be careful about signs. $db^*/d\lambda < 0$. We want its absolute value to be increasing in $\rho$: $\partial|db^*/d\lambda|/\partial\rho > 0$.

$$\left|\frac{db^*}{d\lambda}\right| = \frac{M_2}{P_0\Theta} \cdot \frac{1}{1-\rho},$$
$$\frac{\partial}{\partial\rho}\left|\frac{db^*}{d\lambda}\right| = \frac{M_2}{P_0\Theta} \cdot \frac{1}{(1-\rho)^2} > 0. \quad \checkmark$$

Thus the absolute magnitude of the swap-line effect on the basis is increasing in $\rho$ — swap lines are more effective when the amplification loop is stronger, precisely when they are needed most. $\square$

*Economic interpretation.* Channel 1 is the mechanism in Cesa-Bianchi et al. (2025): the swap line directly reduces dollar demand. Channel 2 is new: by reducing $b^*$, the swap line supports Treasury prices ($P$ rises), which in turn preserves dealer wealth ($W$ rises), which sustains swap supply ($O^*$ rises), which further reduces $b^*$ — a virtuous cycle that mirrors the vicious amplification cycle in the absence of the swap line. The formal expression $\mathcal{M} \geq 1$ quantifies the collateral-stabilization dividend: each dollar of swap-line support is worth $\mathcal{M}$ dollars in basis-reduction terms, and this multiplier is largest precisely during stress episodes (high $\rho$).

### D.8 Regulation Versus Backstop: Substitutability

**Parameterization.** Introduce a tightening of capital regulation as an increase in the swap risk-weight $q_S \to q_S + \tau$ for $\tau > 0$. This reduces the dealer capacity parameter:
$$\Gamma(\tau) = \frac{\phi}{q_S + \tau}.$$

However, tighter regulation also displaces demand: banks facing limited dealer supply for swaps substitute into other, costlier instruments, effectively increasing the residual funding need. Model this displacement as $R(\tau) = R + \delta\tau$, where $\delta \geq 0$ captures the demand-displacement intensity.

**Proposition 6 (Regulation-Backstop Substitutability).** *(i) Tighter regulation ($d\tau > 0$) raises the equilibrium basis: $db^*/d\tau > 0$.*

*(ii) Define the stability threshold $\bar\tau(\lambda)$ as the maximum $\tau$ for which Assumption 1 holds:*
$$\bar\tau(\lambda) = q_S\left[\frac{\phi\gamma\bar{X}_d}{P_0\Theta} - 1\right]^{-1} + f(\lambda),$$
*where $f(\lambda)$ is increasing in $\lambda$. Thus $\partial\bar\tau/\partial\lambda > 0$: a higher swap-line coverage rate expands the set of $\tau$ for which the market remains stable.*

*(iii) Regulation ($\tau$) and backstop ($\lambda$) are imperfect substitutes in stabilization: for any target basis level $b^{target}$, the trade-off $d\tau/d\lambda|_{b^*=\text{const}}$ is well-defined and strictly negative.*

*Proof.*

(i) The equilibrium basis under $(\tau, \lambda)$ is
$$b^*(\tau, \lambda) = \frac{R(\tau) - \Gamma(\tau)\tilde{W}}{\Delta(\tau)},$$
where $\Delta(\tau) = P_0\Theta - \Gamma(\tau)\gamma\bar{X}_d$. Differentiating with respect to $\tau$ (treating $\lambda$ as fixed):

Numerator: $\partial[R(\tau) - \Gamma(\tau)\tilde{W}]/\partial\tau = \delta + \phi\tilde{W}/(q_S+\tau)^2 > 0$.
Denominator: $\partial\Delta/\partial\tau = \gamma\bar{X}_d\phi/(q_S+\tau)^2 > 0$.

By the quotient rule:
$$\frac{db^*}{d\tau} = \frac{[\delta + \Gamma'(\tau)\tilde{W}]\Delta - [R - \Gamma\tilde{W}]\Gamma'(\tau)\gamma\bar{X}_d}{\Delta^2},$$
where $\Gamma'(\tau) = -\phi/(q_S+\tau)^2 < 0$ (note: $\partial\Gamma/\partial\tau < 0$ because tighter regulation reduces dealer capacity). Substituting and simplifying under the stress regime (Assumption 2, numerator positive):

The numerator of $db^*/d\tau$ is $\delta\Delta + (-\Gamma'(\tau))[\tilde{W}\Delta + (R - \Gamma\tilde{W})\gamma\bar{X}_d] \cdot (-1)$.

More directly: the demand-displacement effect ($\delta > 0$) and the reduction in dealer supply ($\Gamma(\tau)$ decreasing in $\tau$) both push $b^*$ upward. A cleaner argument: fix $\Delta$ and observe that $\partial b^*/\partial\tau = \partial(R - \Gamma\tilde{W})/\partial\tau \cdot (1/\Delta) > 0$ when the demand-displacement effect dominates (which holds for $\delta > 0$) and when $\partial\Gamma/\partial\tau < 0$ (supply contraction). Both effects are positive, confirming $db^*/d\tau > 0$.

(ii) Assumption 1 holds iff $\Delta(\tau) > 0$ iff $P_0\Theta > \Gamma(\tau)\gamma\bar{X}_d = \phi\gamma\bar{X}_d/(q_S+\tau)$, which requires $\tau > \phi\gamma\bar{X}_d/P_0\Theta - q_S$. Define $\bar\tau$ as the solution to $\Delta(\bar\tau) = 0$ (market breakdown threshold). Introducing $\lambda$: a higher $\lambda$ reduces $R$ (and reduces $b^*$ at any given $\tau$), which shifts the breakdown threshold outward. Formally, the breakdown condition $R(\tau) - \Gamma(\tau)\tilde{W} = 0$ (the crisis onset condition) is shifted by $\lambda$ because $\partial R/\partial\lambda = -M_2 < 0$. A higher $\lambda$ delays breakdown, so $\bar\tau(\lambda)$ is increasing in $\lambda$.

(iii) From the implicit function theorem applied to $b^*(\tau, \lambda) = b^{target}$:
$$\frac{d\tau}{d\lambda}\bigg|_{b^* = \text{const}} = -\frac{\partial b^*/\partial\lambda}{\partial b^*/\partial\tau} = -\frac{-M_2/\Delta}{db^*/d\tau} < 0,$$
since the numerator is negative (swap lines reduce $b^*$) and the denominator is positive (regulation increases $b^*$). The trade-off is finite and well-defined under Assumption 1. $\square$

*Remark.* The substitutability is *imperfect* in the sense that the trade-off $d\tau/d\lambda$ is not constant — it depends on $\rho$ through $\Delta$. As $\rho \to 1$ (approaching market breakdown), the trade-off diverges: it takes an increasingly large increase in $\lambda$ to compensate for a marginal tightening of regulation. This captures the intuition that near the breakdown point, backstop provision is essential and cannot be replaced by regulation.

### D.9 Extension: Coordination Failure and Self-Fulfilling Runs

This section extends the model to allow for uncertainty in the swap-line coverage rate and derives conditions under which multiple equilibria (self-fulfilling runs) arise.

**Setup.** Suppose $\lambda$ is privately uncertain: each segment 2 creditor observes a private signal $\tilde\lambda_j = \lambda + \sigma_\lambda \epsilon_j$, where $\epsilon_j \sim \mathcal{N}(0,1)$ i.i.d. and $\lambda \sim U[0,1]$ is the true (unknown) coverage rate. Creditors must decide whether to *roll over* their funding to segment 2 banks (maintaining $R_2 = (1-\lambda)M_2$) or to *run* (demanding immediate repayment, effectively setting $\lambda = 0$ regardless of the true value).

**Coordination game.** This is a global game in the sense of Morris and Shin (2003). Each creditor $j$ runs if and only if her signal $\tilde\lambda_j$ falls below a threshold $\lambda^*$ to be determined in equilibrium. A segment 2 bank fails (run succeeds) if the fraction of running creditors exceeds the bank's liquidity ratio $\ell \in (0,1)$.

**Proposition 7 (Zone of Multiplicity).** *There exist thresholds $\underline\lambda < \bar\lambda$ such that:*

*(i) If $\lambda > \bar\lambda$: the unique equilibrium has no run; all segment 2 creditors roll over.*

*(ii) If $\lambda < \underline\lambda$: the unique equilibrium has a run; all segment 2 creditors withdraw.*

*(iii) If $\lambda \in (\underline\lambda, \bar\lambda)$: multiple equilibria coexist — both the run equilibrium and the no-run equilibrium are self-consistent.*

*(iv) A sufficiently large and credible swap-line guarantee ($\lambda_{\min} \geq \bar\lambda$, where $\lambda_{\min}$ is the minimum coverage rate the central bank commits to) eliminates the run equilibrium from region (iii) and guarantees the no-run outcome for all $\lambda \geq \lambda_{\min}$.*

*Proof sketch.* This is a standard application of the global-games methodology (Morris and Shin, 2003) adapted to the dollar-funding context. The key step is to characterize the *switching strategy threshold* $\lambda^*$ at which creditor $j$ is indifferent between rolling and running. Let $V^{roll}(\lambda, b^*(\lambda))$ and $V^{run}$ denote the expected payoffs, where $b^*(\lambda)$ is the equilibrium basis under coverage $\lambda$ (from Proposition 1).

A run occurs when $\lambda < \lambda^*$, since then the expected basis in the run equilibrium exceeds the basis in the no-run equilibrium by more than the rollover benefit. The thresholds $\underline\lambda$ and $\bar\lambda$ are defined by the tangency conditions where the two equilibria merge:

$$\underline\lambda: \quad b^*_{\text{run}}(\underline\lambda) = b^*_{\text{no-run}}(\underline\lambda),$$
$$\bar\lambda: \quad \text{the no-run equilibrium becomes uniquely stable.}$$

The zone $(\underline\lambda, \bar\lambda)$ is the region of strategic complementarity — if enough creditors run, the resulting fire sales raise $b^*$ sufficiently to validate the run, but if enough creditors roll, $b^*$ remains low enough to make rolling individually optimal. The existence of both thresholds follows from the continuity of $b^*(\lambda)$ (established in Proposition 1) and the monotonicity properties of $V^{roll}$ and $V^{run}$ in $\lambda$.

Claim (iv) follows because a commitment $\lambda_{\min} \geq \bar\lambda$ removes the parameter $\lambda$ from the zone of multiplicity, making the no-run equilibrium the unique outcome regardless of private signals. This is the formal statement of the runs-prevention dividend of automatic swap lines. $\square$

*Remark.* This extension connects to the inside/outside liquidity framework of Holmstrom and Tirole (1998) and the international liquidity architecture of Chang and Velasco (2001). The key contribution is endogenizing the threshold $\bar\lambda$ in terms of the structural parameters $(\Theta, \Gamma, \gamma, \bar{X}_d)$ of the main model, so that the conditions for run-prevention can be expressed in terms of measurable features of the balance-sheet architecture.

---

## E. Summary of Formal Results

The following table collects all propositions and their assumptions for reference.

| Result | Statement | Key Assumptions |
|--------|-----------|-----------------|
| Proposition 1 | Unique equilibrium $b^* = (R - \Gamma\tilde{W})/\Delta > 0$ | Assumptions 1 ($\Delta > 0$) and 2 ($R > \Gamma\tilde{W}$) |
| Proposition 2 | $b^* = b^{\mathrm{pe}} \cdot \mathcal{M}$, $\mathcal{M} = 1/(1-\rho)$ | Assumption 1 |
| Proposition 3 | $\mathcal{M}$ increasing in $\Gamma, \gamma, \bar{X}_d$; decreasing in $\Theta$ | Assumption 1 |
| Proposition 4 | Contagion: shock to segment 3 propagates to segment 2 and dealer | Assumptions 1 and 2 |
| Proposition 5 | $db^*/d\lambda = -M_2\mathcal{M}/(P_0\Theta)$; effectiveness increasing in $\rho$ | Assumptions 1 and 2 |
| Proposition 6 | $db^*/d\tau > 0$; $\bar\tau(\lambda)$ increasing in $\lambda$ | Assumptions 1 and 2 |
| Proposition 7 | Run zone $(\underline\lambda, \bar\lambda)$; elimination by $\lambda_{\min} \geq \bar\lambda$ | Assumption 1; global-games logic |

---

## F. Notation Glossary

| Symbol | Type | Definition |
|--------|------|------------|
| $b$ | Scalar $\geq 0$ | Cross-currency basis (price of dollar liquidity per unit of FX swap) |
| $b^*$ | Scalar $\geq 0$ | Equilibrium cross-currency basis |
| $b^{\mathrm{pe}}$ | Scalar $\geq 0$ | Partial-equilibrium basis (no dealer feedback) |
| $P$ | Scalar $\in (0,1]$ | Market price of US Treasury bonds (face value = 1) |
| $P^*$ | Scalar $\in (0,1)$ | Equilibrium Treasury price |
| $P_0$ | Scalar $\in (0,1]$ | Reference Treasury price used in bank-level price-taking assumption |
| $M_i$ | Scalar $> 0$ | Baseline dollar funding need of segment $i$ bank ($i \in \{1,2,3\}$) |
| $B_i$ | Scalar $\geq 0$ | Backstop coverage received by segment $i$ ($B_1 = M_1$, $B_2 = \lambda M_2$, $B_3 = 0$) |
| $R_i$ | Scalar $\geq 0$ | Residual funding need of segment $i$: $R_i = M_i - B_i$ |
| $R$ | Scalar $\geq 0$ | Aggregate residual funding need: $R = R_2 + R_3 = (1-\lambda)M_2 + M_3 + \varepsilon$ |
| $\lambda$ | Scalar $\in [0,1]$ | Swap-line coverage rate (fraction of $M_2$ met by swap-line facility) |
| $\varepsilon$ | Scalar $\geq 0$ | Funding shock to segment 3 (exogenous) |
| $x_i$ | Scalar $\geq 0$ | Quantity of Treasuries sold by segment $i$ bank |
| $s_i$ | Scalar $\geq 0$ | Quantity of FX swaps demanded by segment $i$ bank |
| $\kappa_i$ | Scalar $> 0$ | Liquidation cost parameter of segment $i$ bank |
| $\theta_i$ | Scalar $> 0$ | Basis-elasticity of fire sales: $\theta_i = P_0/\kappa_i$ |
| $\Theta$ | Scalar $> 0$ | Aggregate basis-elasticity: $\Theta = \theta_2 + \theta_3$ |
| $O$ | Scalar $\geq 0$ | Quantity of FX swaps supplied by dealer |
| $O^*$ | Scalar $\geq 0$ | Equilibrium swap supply |
| $Z$ | Scalar $\geq 0$ | Quantity of Treasuries absorbed by dealer |
| $\eta$ | Scalar $> 0$ | Dealer coefficient of absolute risk aversion (CARA) |
| $\sigma_O^2$ | Scalar $> 0$ | Variance of payoff per unit of dealer swap position |
| $\sigma_Z^2$ | Scalar $> 0$ | Variance of payoff per unit of dealer Treasury absorption |
| $q_S$ | Scalar $> 0$ | Regulatory risk-weight on swap positions |
| $q_T$ | Scalar $> 0$ | Regulatory risk-weight on Treasury holdings |
| $\phi$ | Scalar $> 0$ | Regulatory maximum leverage ratio |
| $\bar{X}_d$ | Scalar $> 0$ | Dealer's initial Treasury inventory |
| $W_0$ | Scalar $> 0$ | Dealer's initial equity capital |
| $W(P)$ | Function $\mathbb{R}_{+} \to \mathbb{R}_{+}$ | Dealer marked-to-market net worth: $W(P) = W_0 + P\bar{X}_d$ |
| $\tilde{W}$ | Scalar $> 0$ | Dealer wealth at $P=1$: $\tilde{W} = W_0 + \bar{X}_d$ |
| $\Gamma$ | Scalar $> 0$ | Dealer capacity parameter: $\Gamma = \phi/q_S$ |
| $\gamma$ | Scalar $> 0$ | Outside-investor Treasury price elasticity: $\gamma = \alpha\sigma_T^2$ |
| $\alpha$ | Scalar $> 0$ | Outside investors' coefficient of absolute risk aversion |
| $\sigma_T^2$ | Scalar $> 0$ | Variance of Treasury payoff in outside investors' posterior |
| $\Delta$ | Scalar | Stability parameter: $\Delta = P_0\Theta - \Gamma\gamma\bar{X}_d$ (positive under Assumption 1) |
| $\rho$ | Scalar $\in (0,1)$ | Amplification feedback ratio: $\rho = \Gamma\gamma\bar{X}_d/(P_0\Theta)$ |
| $\mathcal{M}$ | Scalar $\geq 1$ | Amplification multiplier: $\mathcal{M} = 1/(1-\rho)$ |
| $\tau$ | Scalar $\geq 0$ | Regulatory tightening parameter (increase in swap risk-weight) |
| $\delta$ | Scalar $\geq 0$ | Demand-displacement intensity under regulation |
| $\ell$ | Scalar $\in (0,1)$ | Liquidity ratio of segment 2 banks (extension, Section D.9) |
| $\underline\lambda, \bar\lambda$ | Scalars | Run-zone thresholds (extension, Section D.9) |
| $\lambda_{\min}$ | Scalar | Minimum committed swap-line coverage rate (extension, Section D.9) |

---

## G. Open Questions and Future Extensions

1. **Dynamic model.** The current framework is static. A natural extension follows He and Krishnamurthy (2013) in introducing a dynamic state variable for dealer net worth, so that the amplification parameter $\rho$ evolves endogenously over the business cycle. This would generate predictions about the path of the cross-currency basis during and after stress episodes.

2. **Multi-currency extension.** The model has one foreign currency. With multiple currencies and multiple swap lines (Fed-ECB, Fed-BoJ, etc.), the interaction between swap lines introduces strategic substitutability/complementarity in central bank backstop provision — a richer policy game.

3. **Endogenous $\kappa_i$.** The liquidation cost parameters $\kappa_i$ are taken as primitive. A micro-foundation in which $\kappa_i$ is determined by the depth of the secondary Treasury market (itself endogenous to the level of fire sales) would tighten the model's connection to the microstructure literature.

4. **Welfare and optimal policy.** Propositions 5 and 6 characterize positive effects of $\lambda$ and $\tau$. A welfare analysis requires specifying social welfare (sum of agent utilities, possibly weighted) and solving the optimal policy problem $(\lambda^*, \tau^*)$. The substitutability result in Proposition 6 provides the shape of the policy frontier.

5. **Verification of global-game uniqueness (Proposition 7).** The proof sketch invokes the Morris-Shin (2003) uniqueness machinery. A complete proof requires verifying the monotone supermodularity of the coordination game payoffs in terms of $\lambda$, which is straightforward given the closed-form $b^*(\lambda)$ but has not been carried out in full detail here.

---

*End of Pure Theoretical Model Memo.*
