# Consumption, capital and investment

The derivations behind `habit-consumption`, `capital-utilisation`,
`investment-adjustment-cost`, and the capital block of `core-nk-medium`. Section 5
treats trend growth, which changes every coefficient in this document and several
elsewhere. Section 6 derives the five closures the core carries so that these frictions
have something to replace.

**What is established here.** Sections 1 to 4 set out the primitives and first-order
conditions and state the resulting log-linear relations as Smets and Wouters (2007) give
them. Two normalisations are theirs and are identified as such: the definition of the
utilisation-cost parameter in §3 and the scaling of the investment-specific shock in §4.
Section 6's limits are derived in full. Where the article and its widely used replication
differ, §4.3 says so and says which the library follows.

---

## 1. Preferences and the household's problem

**Utility.** Consumption enters relative to a habit stock, and consumption and hours are
non-separable:

$$U_t = \frac{1}{1-\sigma_c}\big(C_t - \lambda C_{t-1}\big)^{1-\sigma_c}
\exp\!\left(\frac{\sigma_c-1}{1+\sigma_l}\,L_t^{1+\sigma_l}\right).$$

Three features of this form matter for everything below.

**Habit is EXTERNAL.** The household takes $C_{t-1}$ — aggregate past consumption — as
given, and does not internalise the effect of its own consumption today on its habit
stock tomorrow. This is an assumption, not a formality. Under *internal* habit the Euler
equation acquires an $\mathbb{E}_t c_{t+2}$ term and the household's intertemporal margin
is genuinely third-order in time; under external habit it does not. The library
implements external habit, as the article does, and `habit-consumption` records the
assumption. A component implementing internal habit would not be a recalibration of this
one.

**Non-separability.** Unless $\sigma_c = 1$, the marginal utility of consumption depends
on hours. This is why the Euler equation below carries a term in expected hours growth
even when $\lambda = 0$ — a term that a reader who expects a textbook Euler equation
will mistake for an error.

**$\sigma_c$ is not the inverse intertemporal elasticity of substitution** in the usual
sense once $\lambda > 0$: habit drives a wedge between the two, and the article's
$\sigma_c$ is a utility-function parameter rather than a measured elasticity.

**Budget constraint.** The household holds bonds and physical capital, rents capital
services to firms, chooses utilisation, and receives labour income from monopolistically
supplied labour (see `wage-setting.md`):

$$\frac{B_t}{P_t} = R_{t-1}\frac{B_{t-1}}{P_t}\,\Xi_t
+ \frac{W_t L_t}{P_t} + R^k_t Z_t \bar K_{t-1} - a(Z_t)\bar K_{t-1}
- C_t - I_t + \frac{T_t}{P_t},$$

where $\Xi_t$ is a wedge between the policy rate and the return households actually
require — the **risk premium** of §1.1 — and $a(Z_t)$ is the resource cost of utilisation
of §3.

### 1.1 The risk-premium wedge

$\varepsilon^b_t$ is a wedge between the rate the central bank sets and the return on
assets. The article's text is explicit about its direction: *a positive shock to this
wedge increases the required return on assets and reduces current consumption*, and the
value of capital *depends negatively on the ex ante real interest rate and the risk
premium disturbance*.

The library follows that sign. It enters the Euler equation at $-c_3$ and the capital
arbitrage equation at $-1$. The widely used replication of the article rescales the wedge
by $c_3$ and carries the opposite sign, so a number taken from either must be read with
its own convention; `core-nk-medium` records both and the entry's targets pin the
library's.

This is worth stating plainly because the sign was wrong in an early version of this
library and three layers of verification agreed with it. A numerical cross-check that
fits a scale factor for a shock cannot see that shock's sign; and the sharpest closed
form available — that the wedge is exactly neutral in the flexible-price economy — is a
*cancellation* between the two coefficients, which holds whichever sign the pair carries
so long as they carry the same one.

---

## 2. The Euler equation and the marginal rate of substitution

**First-order conditions.** Let $\Lambda_t$ be the marginal utility of consumption. The
bond first-order condition is $\Lambda_t = \beta \mathbb{E}_t \Lambda_{t+1} R_t
\Xi_t/\Pi_{t+1}$, and the intratemporal margin equates the marginal rate of substitution
to the real wage a flexible-wage household would charge.

**Log-linear form.** Writing $h \equiv \lambda/\gamma$ for the habit parameter adjusted
for trend growth (see §5), the article's equation (2) is

$$\boxed{\;c_t = c_1 c_{t-1} + (1-c_1)\,\mathbb{E}_t c_{t+1}
+ c_2\big(l_t - \mathbb{E}_t l_{t+1}\big)
- c_3\big(rr_t + \varepsilon^b_t\big)\;}$$

$$c_1 = \frac{h}{1+h},
\qquad
c_2 = \frac{(\sigma_c-1)\,\frac{W^h L}{C}}{\sigma_c(1+h)},
\qquad
c_3 = \frac{1-h}{\sigma_c(1+h)} .$$

Three readings of these coefficients:

- $c_1$ is the weight on the past. At $\lambda = 0$ it is zero and consumption is purely
  forward-looking; at $\lambda \to 1$ it approaches one half. Habit is what makes
  consumption a **state variable**, and that is what produces a hump-shaped response
  rather than a jump.
- $c_2$ vanishes only at $\sigma_c = 1$. It is the non-separability term of §1, not a
  habit term, and it survives the $\lambda \to 0$ limit.
- $c_3$ is the interest elasticity. Habit reduces it: a household anchored to its past
  consumption responds less to the real rate. At the article's posterior means
  $c_3 \approx 0.124$, against $1/\sigma_c \approx 0.72$ without habit.

**The marginal rate of substitution.** The same preferences give

$$mrs_t = \sigma_l\, l_t + \frac{1}{1-h}\,c_t - \frac{h}{1-h}\,c_{t-1},$$

which is the bracket multiplying the wage markup in the article's equation (13). It
carries the habit lag: it is the gap between consumption and its habit stock, not
consumption itself, that the household trades against leisure.

**Why the library exposes this as a variable.** The article's own statement substitutes
this expression into the wage equation. The library gives it an equation of its own and a
name, so that the wage block can be composed with a different consumption specification
without being edited. The consequence is that `habit-consumption` replaces **two**
equations of the core rather than one — the Euler equation and the marginal rate of
substitution — and forgetting the second yields a model that assembles, solves, and has
habit in its intertemporal margin but not in its labour supply.

**Anchor: `habit-euler`.**

---

## 3. Capital utilisation

**Primitive.** Capital services are utilisation times the stock carried into the period,
$K_t = Z_t \bar K_{t-1}$, and running capital harder costs $a(Z_t)$ per unit of capital,
with

$$a(1) = 0,\qquad a'(1) = R^{k},\qquad a''(1) > 0 .$$

$a(1)=0$ normalises steady-state utilisation to one; $a'(1)=R^k$ makes that
normalisation consistent with the household's first-order condition.

**First-order condition.** $R^k_t = a'(Z_t)$: utilise until the marginal cost of doing so
equals the rental rate earned. Log-linearising,

$$z_t = \frac{a'(1)}{a''(1)}\,r^k_t
\;\equiv\; \frac{1-\psi}{\psi}\,r^k_t,
\qquad
\psi \equiv \frac{a''(1)}{a'(1)+a''(1)} \in (0,1).$$

The second equality is a **normalisation of the article's**, not a result: $\psi$ is
defined so that it lies in the unit interval and so that $\psi \to 1$ is the
infinitely-costly case. It is worth stating because the direction is counter-intuitive —
*larger* $\psi$ means *less* variation in utilisation — and because a reader who reads
$\psi$ as a curvature will get the limit backwards.

**Two consequences for the rest of the model.** Capital services and the stock cease to
coincide, so the production function and the factor-demand condition must use $k_t$,
services, while accumulation uses $\bar k_t$, the stock. And utilisation is a **resource
cost**: the term $R^k \frac{K}{Y} z_t$ appears in the resource constraint, and omitting
it is a conservation error rather than an approximation.

**Anchor: `utilisation`.**

---

## 4. Investment, adjustment costs and the value of capital

**Primitive.** Adjusting the **flow** of investment is costly:

$$\bar K_t = (1-\delta)\bar K_{t-1}
+ \Big[1 - S\!\left(\tfrac{I_t}{I_{t-1}}\right)\Big] I_t\, \varepsilon^i_t,
\qquad
S(\gamma)=0,\quad S'(\gamma)=0,\quad S''(\gamma)=\varphi>0 .$$

The distinction between a cost in the *flow* and a cost in the *level* of investment is
not a detail. A cost in the level gives a monotone investment response and leaves the
shadow price of installed capital nearly constant. A cost in the change gives the
hump-shaped response the data show, and makes that shadow price move — which is the only
reason Tobin's $q$ is a non-trivial variable in this class of model.

**First-order conditions.** Let $Q_t$ be the shadow price of installed capital. The
investment first-order condition and the arbitrage condition for capital are, in log
deviations and with $i_1 = 1/(1+\bar\beta\gamma)$:

$$i_t = i_1\, i_{t-1} + (1-i_1)\,\mathbb{E}_t i_{t+1}
+ \frac{1}{(1+\bar\beta\gamma)\gamma^2\varphi}\,q_t + \varepsilon^i_t,$$

$$q_t = -\,rr_t - \varepsilon^b_t
+ \frac{R^k}{R^k+1-\delta}\,\mathbb{E}_t r^k_{t+1}
+ \frac{1-\delta}{R^k+1-\delta}\,\mathbb{E}_t q_{t+1}.$$

The second is a present-value relation: installed capital is worth the discounted stream
of rentals plus resale value, discounted at the real rate and at the premium households
require. Its coefficients sum to one by construction at the steady state.

**Anchor: `value-of-capital`.**

### 4.1 Why the library writes the investment Euler multiplied through

As written, the coefficient on $q_t$ diverges as $\varphi \to 0$: the frictionless limit
cannot be taken and no nesting test has anything to converge to. Multiplying by
$\gamma^2\varphi(1+\bar\beta\gamma)$,

$$\gamma^2\varphi\Big[(1+\bar\beta\gamma)i_t - i_{t-1}
- \bar\beta\gamma\,\mathbb{E}_t i_{t+1}
- (1+\bar\beta\gamma)\varepsilon^i_t\Big] - q_t = 0,$$

which at $\varphi = 0$ reads $q_t = 0$: the core's no-adjustment-cost closure, equation
for equation. The two forms have the same solution; only the second has a limit.

**Anchor: `investment-euler`.**

### 4.2 Capital accumulation and the shock's coefficient

Log-linearising the accumulation equation,

$$\bar k_t = \frac{1-\delta}{\gamma}\,\bar k_{t-1}
+ \Big(1-\frac{1-\delta}{\gamma}\Big) i_t
+ \Big(1-\frac{1-\delta}{\gamma}\Big)(1+\bar\beta\gamma)\gamma^2\varphi\;\varepsilon^i_t .$$

The shock's coefficient carries $\varphi$ because $\varepsilon^i_t$ is **normalised** so
as to enter the investment Euler with coefficient one; that normalisation is the article's
and it fixes the coefficient here. The practical consequence is that at $\varphi = 0$ the
investment-specific shock has no effect anywhere, which is why the library gives the
shock to `investment-adjustment-cost` rather than to the core: it is not a shock the model
has independently of the friction.

**Anchor: `capital-accumulation`.**

### 4.3 Where the article and its replication disagree

Two differences, both documented in the components and both resolved in favour of the
article:

| | article | widely used replication |
|---|---|---|
| risk-premium wedge | coefficient $-1$ in the $q$ equation, $-c_3$ in the Euler | rescaled by $c_3$, opposite sign |
| $\varepsilon^i$ in accumulation | factor $(1+\bar\beta\gamma)$, about 1.997 at the posterior means | factor omitted |

The second was pointed out by Del Negro and Schorfheide (2012). The library implements
the article's version and the entry carries a target that isolates the coefficient, so
that an implementation following the replication fails it by a factor of two rather than
drifting silently.

**Anchor: `article-versus-replication`.**

---

## 5. Trend growth and stationarisation

The model has a balanced growth path along which output, consumption, investment,
capital and the real wage grow at the gross rate $\gamma$. Variables are expressed as
deviations from that path, and the consequence for the coefficients is systematic.

The stochastic discount factor along the path is
$\beta\,(C_{t+1}/C_t)^{-\sigma_c} \to \beta\gamma^{-\sigma_c} \equiv \bar\beta$, so

$$\textbf{wherever a no-growth model would carry } \beta,
\textbf{ this one carries } \bar\beta\gamma = \beta\gamma^{1-\sigma_c}.$$

That product appears in the Euler equation, the investment Euler, both Phillips curves
and the wage curve. At the article's posterior means $\bar\beta\gamma \approx 0.9968$
against $\beta \approx 0.9984$ — a small difference that compounds through the
forward-looking terms.

Growth also enters the steady-state ratios: the investment-to-capital ratio is
$1-(1-\delta)/\gamma$ rather than $\delta$, and the habit parameter enters everywhere as
$\lambda/\gamma$ rather than $\lambda$. `core-nk-medium` derives all of these as
parameters with `method: derived`, from the deep parameters, rather than carrying them as
numbers.

**A reader's warning.** Equations lifted from this family into a model without trend
growth must have $\bar\beta\gamma$ replaced by $\beta$ and the ratios recomputed. The
substitution is mechanical but it is not optional: the coefficients are not
dimensionless.

**Anchor: `trend-growth`.**

---

## 6. The core's closures, derived

`core-nk-medium` carries one closure equation for each friction, so that a composition
without the friction is still a complete model and so that each friction's limit is an
equation rather than a numerical coincidence. All five are derived here.

| closure | equation | limit it is |
|---|---|---|
| `euler-no-habit` | $c_t = \mathbb{E}_t c_{t+1} + c_2^{0}(l_t - \mathbb{E}_t l_{t+1}) - \frac{1}{\sigma_c}(rr_t+\varepsilon^b_t)$ | §2 at $\lambda = 0$ |
| `mrs-no-habit` | $mrs_t = \sigma_l l_t + c_t$ | §2 at $\lambda = 0$ |
| `flex-investment` | $q_t = 0$ | §4.1 at $\varphi = 0$ |
| `capital-accumulation` | $\bar k_t = \frac{1-\delta}{\gamma}\bar k_{t-1} + (1-\frac{1-\delta}{\gamma}) i_t$ | §4.2 at $\varphi = 0$ |
| `fixed-utilisation` | $z_t = 0$ | §3 at $\psi = 1$ |

**The first two.** At $\lambda = 0$, $h = 0$, so $c_1 = 0$, $c_3 = 1/\sigma_c$, and
$c_2 \to c_2^{0} = (\sigma_c-1)\frac{W^hL}{C}/\sigma_c$. The habit lag in $mrs_t$
disappears because $1/(1-h) \to 1$ and $h/(1-h) \to 0$. Both closures are therefore the
$\lambda \to 0$ case **exactly**, not approximately, which is what makes
`habit-consumption`'s nesting limit algebraic.

**The third and fourth.** Shown in §4.1 and §4.2.

**The fifth.** At $\psi = 1$ the coefficient $(1-\psi)/\psi$ is zero.

**Note that $c_2^{0} \neq 0$.** The habit-free Euler equation still carries the hours
term, because that term comes from non-separability and not from habit. A closure written
without it would not be the $\lambda \to 0$ limit, and the nesting test would fail —
which is how the library arrived at this form.

**Anchor: `core-closures`.**

---

## 7. What a transplant requires

| If the new environment changes | then |
|---|---|
| habit from external to internal | §2's Euler equation gains a second lead; the coefficients are not a reparameterisation of $c_1,c_2,c_3$ |
| preferences to separable ($\sigma_c=1$) | $c_2$ vanishes and the hours term disappears from both the Euler equation and its closure |
| the asset structure (incomplete markets, borrowing constraints, heterogeneity) | §1's budget constraint and therefore the Euler equation change; nothing in §3 or §4 does, since utilisation and investment are the firm-side and owner-side margins |
| the adjustment cost from the flow to the level of investment | §4's investment Euler changes shape and $q_t$ becomes nearly constant; the accumulation equation's shock coefficient disappears |
| trend growth away from the balanced path (stochastic trend, growth shocks) | §5's stationarisation is invalid as written; $\gamma$ is deterministic here |
| capital from household-owned to firm-owned | the arbitrage equation moves to the firm's problem; its form survives, its discount factor may not |

---

## References

- Christiano, L., M. Eichenbaum and C. Evans (2005). Nominal rigidities and the dynamic
  effects of a shock to monetary policy. *Journal of Political Economy* 113(1), 1–45.
- Del Negro, M. and F. Schorfheide (2012). Notes on New-Keynesian models.
- Smets, F. and R. Wouters (2007). Shocks and frictions in US business cycles.
  *American Economic Review* 97(3), 586–606.
