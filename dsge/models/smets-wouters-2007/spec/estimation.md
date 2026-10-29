# Bayesian estimation — Smets and Wouters (2007, AER)

The empirical specification is part of the canonical model, not a by-product of the
solver. The source is Smets and Wouters (2007), *American Economic Review* 97(3),
586–606. **This document describes the published Bayesian estimation, not an estimate
obtained from the current library.** Exact values from Tables 1A and 1B, together with
the observation system and comparison targets, are transcribed once in
[`../estimation.yaml`](../estimation.yaml).

## 1. Observables and measurement equations

The model is estimated on seven quarterly US macroeconomic series from **1966Q1 to
2004Q4** (Section II and eq. (15), AER p. 592). The variables are real GDP, real
consumption, real investment, the real wage, hours worked, the GDP deflator and the
federal funds rate. The paper uses the first log differences of the first four real
series, the log level of hours, inflation and the nominal interest rate. The symbols
`y`, `c`, `inv`, `w`, `n`, `pi` and `i` below denote the library's
stationary model variables, **not the seven observed series themselves**.

In the notation of equation (15), the observation system is

$$ Y_t = \begin{bmatrix} d\ell GDP_t \\ d\ell CONS_t \\ d\ell INV_t \\ d\ell WAG_t \\ \ell HOURS_t \\ d\ell P_t \\ FEDFUNDS_t \end{bmatrix} = \begin{bmatrix} \bar\gamma \\ \bar\gamma \\ \bar\gamma \\ \bar\gamma \\ \bar\ell \\ \bar\pi \\ \bar r \end{bmatrix} + \begin{bmatrix} y_t-y_{t-1} \\ c_t-c_{t-1} \\ inv_t-inv_{t-1} \\ w_t-w_{t-1} \\ n_t \\ \pi_t \\ i_t \end{bmatrix}. $$

Here `d` and `ell` denote **100 times** a log difference and a log level.
The common growth intercept is
$$ \bar\gamma = 100(\gamma-1), $$
the quarterly inflation intercept is
$$ \bar\pi = 100(\bar\Pi-1), $$
and the derived nominal-rate intercept is
$$ \bar r = 100(\beta^{-1}\gamma^{\sigma_c}\bar\Pi-1). $$

The paper normalises the steady-state log hours intercept `\bar\ell` independently
of the structural hours process. Accordingly, `\bar\ell` and `\bar\pi` are
estimated **measurement-system parameters**; they are not variables or parameters of
the current component solver. The trend growth parameter and discount factor are
shared with the structural model. The observation equation does **not** introduce
seven arbitrary measurement errors.

The printed article refers to a separate Data Appendix. The supplied 21-page AER
PDF does not reproduce the original raw series, metadata, seasonal adjustments or
every transformation performed before forming equation (15). Those details are
**not reconstructed by assumption** in this library.

## 2. Likelihood and Bayesian posterior

The first-order rational-expectations equilibrium, together with the seven structural
shock processes, supplies a linear state-space representation. With a parameter vector
`theta`, observable data `Y` and structural innovations, Bayesian inference is
based on

$$ p(\theta\mid Y) \propto p(Y\mid\theta)\,p(\theta). $$

The likelihood is the Gaussian likelihood of the linear state-space model (computed
using a state-space filter in the original Dynare estimation), while the prior
`p(theta)` is the product of the distributions given in Tables 1A and 1B.
The seven innovations, not the 36 estimated parameter entries, determine the
model's stochastic driving dimension. The government-spending process additionally
loads on the technology innovation through `rho_ga`.

**The paper's estimation strategy is two-stage** (AER p. 592 and footnote 6).
First, the posterior mode is obtained by maximising the log posterior.
Second, a Metropolis–Hastings algorithm approximates the posterior distribution.
The article reports a sample of **250,000 draws**, discards the first **50,000**,
and sets a proposal scale of **0.3**, giving a rejection frequency of about **65%**.
It discusses Brooks–Gelman diagnostics across chains and a diagnostic based on
cumulative versus overall posterior means. The exact transition function, likelihood
initialisation and auxiliary software details are not fully contained in the printed
paper; those should not be invented.

The article also uses the posterior to evaluate the *marginal likelihood*, notably
through a modified harmonic-mean estimator and a Laplace approximation around the
posterior mode (AER p. 595, footnote 11). Distinguish the posterior mode, the
posterior mean and the integrated marginal likelihood: they are different objects.

## 3. Prior distributions and identification

Tables 1A and 1B (AER pp. 593–594) specify **36** estimated quantities:

- **19 structural and steady-state quantities**, including two intercepts
  `pi_bar` and `hours_bar` that are absent from the current dynamic core.
- **17 shock-process quantities**: seven innovation standard deviations, seven
  AR(1) persistences, two MA(1) coefficients for the price and wage mark-up
  disturbances, and one spending/technology correlation-loading parameter.

Table 1A uses normal, beta and gamma priors on the behavioral, policy and
steady-state parameters; the hyperparameters are prior means and standard
deviations. Table 1B reports inverse-gamma priors on standard deviations of
innovations (mean 0.10, two degrees of freedom) and beta priors on the
persistence and moving-average coefficients (mean 0.50, SD 0.20). **The
`rho_ga` prior is beta, not normal.**

Five other quantities are held fixed (AER p. 592): depreciation `delta=0.025`,
spending/GDP `g_y=0.18`, wage mark-up `markup_w=1.5`, and the two
Kimball curvature parameters `curv_p=curv_w=10`. These values are not
posterior estimates. The structural components store the corresponding equations,
default posterior means, theoretical calibrations and source citations.

**Parameter normalization matters.** The AER Table 1A reports quarterly trend
growth `gamma_bar` and `100*(beta^(-1)-1)`, not gross growth
or the discount factor themselves. The steady-state nominal interest intercept
`r_bar` is **derived** from the estimated trend, inflation and discount factor,
not estimated independently.

The shock labelled `sigma_b` has a posterior **mean of 0.23 in AER Table 1B**,
attached to the paper's `epsilon_b` process as introduced in equations (2) and
(4). An independently rescaled innovation may have another standard deviation,
but its scale must be explicitly transformed together with the structural
coefficients. The published `0.23` must not be silently replaced by the
`1.85` used in an earlier library version.

## 4. Posterior results: what is identified by the data?

The source-of-truth tabulation in `estimation.yaml` preserves for every entry
the **prior distribution, posterior mode, posterior mean, 5th percentile and
95th percentile**. A selection of results illustrates the paper's main economic
findings:

| Parameter | AER posterior mean | Economic interpretation |
| --- | ---: | --- |
| Price Calvo probability `xi_p` | 0.66 | Average price duration of approximately three quarters |
| Wage Calvo probability `xi_w` | 0.70 | Wage contracts last somewhat longer than price contracts |
| Price indexation `iota_p` | 0.24 | Limited backward-looking price indexation |
| Wage indexation `iota_w` | 0.58 | Larger backward-looking wage indexation |
| External habit `lambda_h` | 0.71 | Consumption persistence |
| Investment adjustment cost `varphi_i` | 5.74 | Material adjustment friction in the growth rate of investment |
| Interest-rate smoothing `rho_i` | 0.81 | Highly persistent policy rate |
| Inflation response `r_pi` | 2.04 | Strong long-run monetary response to inflation |
| Technology AR coefficient `rho_a` | 0.95 | Persistent technology disturbances |
| Spending AR coefficient `rho_g` | 0.97 | Persistent spending disturbances |
| Wage-markup AR coefficient `rho_w` | 0.96 | Persistent wage mark-up disturbances |

The paper emphasizes that conditioning on observed GDP, consumption, investment,
wages, hours, inflation and the policy rate jointly helps identify the shock
processes as well as the behavioral parameters. Nevertheless a single posterior
mode or a small posterior SD is not by itself evidence that a component is
structurally identified in another economy or under another observable system.

## 5. Model comparison and empirical importance of frictions

In Section III the authors compare the estimated DSGE with unrestricted VARs and
a Sims–Zha BVAR, using a common **1956Q1–1965Q4 training sample** for the
forecast comparison. **This training window is not the 1966Q1–2004Q4 estimation
sample.** Table 2 (AER p. 595) reports a DSGE log marginal likelihood of
**−905.8**, while the Sims–Zha BVAR(4) produces **−906.6** and the
unrestricted VAR(1) **−928.0**.

Table 3 additionally compares out-of-sample RMSEs at different forecast horizons.
This is empirical validation against statistical benchmarks, not a test of
whether the DSGE equations are square.

The friction restrictions in Table 4 (AER p. 597) are re-estimated **rather
than evaluated at the unrestricted baseline parameters**. The table reports a
reference marginal likelihood of **−923**. Restricting the investment
adjustment elasticity to `0.1` decreases the reported criterion to **−1084**;
reducing price and wage Calvo probabilities to `0.1` gives **−975** and
**−973**, respectively. Lowering consumption habit to `0.1` gives **−959**.
Reducing price indexation to zero yields **−918**, an improvement relative
to that table's reference, which is consistent with the small estimated price
indexation. The other experiments and their values are recorded in
`estimation.yaml`.

**Do not conflate** Table 4's `−923` baseline with Table 2's `−905.8`
DSGE marginal likelihood. The AER contains different estimation and comparison
exercises; absent full underlying auxiliary files their difference should not
be explained away or treated as a transcription error.

## 6. Posterior-based economic results

The estimation supports more than a point-calibrated impulse response:

- **Figure 1 (p. 598):** forecast-error variance contributions by structural shock
  and horizon, including demand, productivity, mark-up and policy disturbances.
- **Figures 2 and 3 (p. 599):** posterior impulse responses to demand and wage
  mark-up shocks, with uncertainty bands.
- **Figure 4 (p. 600):** historical decompositions of GDP growth and inflation.
- **Figure 5 (p. 601):** inflation/output correlation comparison between data
  and the posterior-implied DSGE model.
- **Figures 6 and 7 (pp. 601–602):** monetary-policy and productivity
  impulse responses, with counterfactual nominal/real frictions.
- **Table 5 (p. 603):** posterior modes and standard deviations for
  **1966Q1–1979Q2** and **1984Q1–2004Q4**, to study the Great Moderation.
- **Table 6 (p. 604):** actual, model-based and counterfactual standard
  deviations of GDP growth and inflation.

The paper's main economic distinction is that different shocks dominate at
different horizons and for different observables; persistent productivity
and wage mark-up disturbances are important over long horizons, while demand
disturbances play a larger role in the short run. The reported fall in volatility
in the Great Moderation is mostly associated with changes in the stochastic
disturbances, rather than just a re-estimated monetary policy rule.

These are **published posterior-dependent findings**; the library's
`golden/targets.yaml` checks theoretical IRFs at a fixed calibration, not the
posterior uncertainty bands, marginal likelihoods or variance decompositions.

## 7. What is represented in the library

The distinction between theoretical and empirical information is deliberate.

| Resource | Contents |
| --- | --- |
| `component.yaml` | Dynamic equations and associated structural coefficients |
| `../manifest.yaml` | Model composition and its seven innovations |
| `../estimation.yaml` | AER equation (15), priors, posterior tables, five fixed calibrations, MCMC settings and published empirical reference values |
| `golden/targets.yaml` | Analytical and numerical checks on the model solution |
| This document | Mathematical/statistical interpretation and source boundaries |

There is **no estimation run, Kalman filter or MCMC engine in this library**;
neither the full original dataset nor the original estimation appendix is
reproduced. Consequently the AER posterior numbers in `estimation.yaml`
are *published reference values*, never outputs generated by this repository.

The paper is also not identical to ECB Working Paper No. 722 in all
presentational details. The published AER text is now available as a primary
source and is the controlling version for the model's empirical description.

## References

Smets, F., and R. Wouters (2007). Shocks and Frictions in US Business Cycles:
A Bayesian DSGE Approach. *American Economic Review* 97(3), 586–606.
doi:10.1257/aer.97.3.586.
