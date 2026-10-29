"""The open economy, and the four policy regimes the article compares.

These were missing from the published branch: the entry carried golden targets but no
property tests, and — worse — no manifest, so the golden runner skipped it entirely. A
mutation test found every equation of core-soe-gm unverified as a result. What follows
is what discriminates between a correct core and a perturbed one.
"""
import numpy as np
import pytest

from modellib import Composition, CompositionError
from modellib.lre import irf

CORE, PRICING = "core-soe-gm", "calvo-prices-domestic"
RULES = ("rule-domestic-inflation", "rule-cpi-inflation", "rule-exchange-rate-peg",
         "rule-optimal-domestic-price-stability")
OPEN = {"eta": 2.0, "gamma": 1.5, "alpha_open": 0.3, "sigma": 2.0}


def _irf(rule, shock="eps_a", horizon=4, overrides=None):
    c = Composition(CORE, [PRICING, rule])
    P, Q, params = c.solve(overrides)
    return {v: [float(x) for x in irf(P, Q, c.shock_index(shock), horizon)[:, c.index(v)]]
            for v in c.variables}, params


@pytest.mark.parametrize("rule", RULES)
def test_every_regime_composes_and_solves(rule):
    c = Composition(CORE, [PRICING, rule])
    assert len(c.equations) == len(c.variables) == 16


@pytest.mark.parametrize("pair", [(a, b) for i, a in enumerate(RULES) for b in RULES[i + 1:]])
def test_two_regimes_cannot_be_composed(pair):
    with pytest.raises(CompositionError):
        Composition(CORE, [PRICING, *pair])


def test_optimal_policy_closes_the_output_gap_exactly():
    r, _ = _irf("rule-optimal-domestic-price-stability")
    assert r["x"][0] == pytest.approx(0.0, abs=1e-12)
    assert r["pi_h"][0] == pytest.approx(0.0, abs=1e-12)


def test_under_optimal_policy_cpi_inflation_is_the_terms_of_trade():
    """Checks the CPI-domestic link, which no golden target touches."""
    r, params = _irf("rule-optimal-domestic-price-stability", horizon=3)
    a_o = params["alpha_open"]
    assert r["pi"][0] == pytest.approx(a_o * r["s"][0], rel=1e-10)
    for h in (1, 2):
        assert r["pi"][h] == pytest.approx(a_o * (r["s"][h] - r["s"][h - 1]), rel=1e-10, abs=1e-14)


def test_the_peg_distorts_most_and_the_optimal_rule_not_at_all():
    """The article's headline comparison."""
    gaps = {r: abs(_irf(r)[0]["x"][0]) for r in RULES}
    assert gaps["rule-optimal-domestic-price-stability"] == pytest.approx(0.0, abs=1e-12)
    assert gaps["rule-domestic-inflation"] < gaps["rule-cpi-inflation"] < gaps["rule-exchange-rate-peg"], gaps


def test_the_peg_holds_the_exchange_rate_and_the_others_do_not():
    assert _irf("rule-exchange-rate-peg")[0]["e"][0] == pytest.approx(0.0, abs=1e-12)
    for rule in RULES:
        if rule != "rule-exchange-rate-peg":
            assert abs(_irf(rule)[0]["e"][0]) > 1e-6


@pytest.mark.parametrize("shock", ["eps_a", "eps_star"])
def test_the_identities_that_determine_output_hold(shock):
    """Under BOTH shocks, and that is the substance rather than thoroughness.

    Under the technology shock alone foreign output is identically zero, so the term
    alpha_open*Psi_gm*y_star in natural-output multiplies zero and any coefficient on it
    passes. This test checks that distinction explicitly.
    """
    r, p = _irf("rule-domestic-inflation", shock=shock, horizon=4, overrides=OPEN)
    driver = "a" if shock == "eps_a" else "y_star"
    assert abs(r[driver][0]) > 1e-9, "the shock must move its own process"
    al, om, s_ = p["alpha_open"], p["omega_gm"], p["sigma"]
    for h in range(4):
        assert r["y_nat"][h] == pytest.approx(
            p["Gamma_gm"] * r["a"][h] + al * p["Psi_gm"] * r["y_star"][h],
            rel=1e-10, abs=1e-14)
        assert r["x"][h] == pytest.approx(r["y"][h] - r["y_nat"][h], rel=1e-9, abs=1e-14)
        assert r["y"][h] == pytest.approx(r["y_star"][h] + r["s"][h] / p["sigma_a"],
                                          rel=1e-10, abs=1e-14)
        assert r["y"][h] == pytest.approx(r["a"][h] + r["n"][h], rel=1e-10, abs=1e-14)
        assert r["q"][h] == pytest.approx((1 - al) * r["s"][h], rel=1e-10, abs=1e-14)
    for h in range(1, 4):
        assert r["pi"][h] == pytest.approx(r["pi_h"][h] + al * (r["s"][h] - r["s"][h - 1]),
                                           rel=1e-9, abs=1e-14)


@pytest.mark.parametrize("rule", RULES)
def test_each_regime_satisfies_its_own_rule_period_by_period(rule):
    """Each policy component as the residual of its own equation.

    The CPI rule requires its own direct verification:
    ORDERING of output gaps, and scaling phi_pi preserves an ordering while changing the
    model. An ordering is a weak check on a coefficient; the residual is exact.
    """
    r, p = _irf(rule, horizon=5, overrides=OPEN)
    for h in range(5):
        if rule == "rule-domestic-inflation":
            assert r["i"][h] == pytest.approx(p["phi_pi"] * r["pi_h"][h], rel=1e-9, abs=1e-14)
        elif rule == "rule-cpi-inflation":
            assert r["i"][h] == pytest.approx(p["phi_pi"] * r["pi"][h], rel=1e-9, abs=1e-14)
        elif rule == "rule-exchange-rate-peg":
            assert r["e"][h] == pytest.approx(0.0, abs=1e-12)
        else:
            assert r["pi_h"][h] == pytest.approx(0.0, abs=1e-12)
    if rule == "rule-domestic-inflation":
        assert abs(r["pi_h"][0]) > 1e-6
    elif rule == "rule-cpi-inflation":
        assert abs(r["pi"][0]) > 1e-6


def test_the_terms_of_trade_accumulate_depreciation_less_domestic_inflation():
    """Equation (15), the law of motion that makes s a state."""
    r, _ = _irf("rule-domestic-inflation", horizon=4, overrides=OPEN)
    for h in range(1, 4):
        assert r["s"][h] - r["s"][h - 1] == pytest.approx(
            r["e"][h] - r["e"][h - 1] - r["pi_h"][h], rel=1e-9, abs=1e-14)


def test_net_exports_consumption_and_the_real_wage_follow_the_terms_of_trade():
    """Equations (31), (27) and the labour supply condition, none of them in a target."""
    r, p = _irf("rule-domestic-inflation", horizon=3, overrides=OPEN)
    om, s_, al = p["omega_gm"], p["sigma"], p["alpha_open"]
    for h in range(3):
        assert r["nx"][h] == pytest.approx(al * (om / s_ - 1) * r["s"][h], rel=1e-10, abs=1e-14)
        assert r["c"][h] == pytest.approx(r["y"][h] - al * om / s_ * r["s"][h], rel=1e-10, abs=1e-14)
        assert r["w"][h] == pytest.approx(s_ * r["c"][h] + p["varphi"] * r["n"][h],
                                          rel=1e-9, abs=1e-14)
        assert r["q"][h] == pytest.approx((1 - al) * r["s"][h], rel=1e-10, abs=1e-14)
        assert r["y"][h] == pytest.approx(r["a"][h] + r["n"][h], rel=1e-10, abs=1e-14)
        assert r["x"][h] == pytest.approx(r["y"][h] - r["y_nat"][h], rel=1e-9, abs=1e-14)


def test_the_foreign_shock_moves_the_economy_only_when_the_foreign_terms_survive():
    """At the baseline Theta_gm is exactly zero and the foreign shock is neutral.

    The coincidence that hid these equations: a target at the baseline would have been
    satisfied by any wrong coefficient on the foreign terms.
    """
    base, pb = _irf("rule-domestic-inflation", shock="eps_star")
    open_, po = _irf("rule-domestic-inflation", shock="eps_star", overrides=OPEN)
    assert pb["Theta_gm"] == pytest.approx(0.0, abs=1e-12)
    assert base["x"][0] == pytest.approx(0.0, abs=1e-12)
    assert abs(po["Theta_gm"]) > 1.0
    assert abs(open_["x"][0]) > 1e-3
    assert open_["y_nat"][0] == pytest.approx(po["alpha_open"] * po["Psi_gm"] * open_["y_star"][0],
                                              rel=1e-10)


def test_an_inflation_rule_leaves_a_unit_root_and_a_peg_does_not():
    roots = {}
    for rule in RULES:
        P, _, _ = Composition(CORE, [PRICING, rule]).solve()
        roots[rule] = float(np.max(np.abs(np.linalg.eigvals(P))))
    for rule in ("rule-domestic-inflation", "rule-cpi-inflation",
                 "rule-optimal-domestic-price-stability"):
        assert roots[rule] == pytest.approx(1.0, abs=1e-9), (rule, roots[rule])
    assert roots["rule-exchange-rate-peg"] < 1.0 - 1e-6, roots
