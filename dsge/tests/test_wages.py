"""The two-friction model, whose equations the published branch did not verify.

calvo-wages introduces three equations — the wage Phillips curve, the real wage gap
identity and the marginal-cost definition — and the tests below verify all three
survived, because the entry had no manifest and its golden targets were never collected.
These are the checks that discriminate.
"""
import numpy as np
import pytest

from modellib import Composition
from modellib.lre import irf

PRICE_ONLY = ("core-nk-classical", ["calvo-prices", "taylor-rule"])
BOTH = ("core-nk-classical", ["calvo-prices", "calvo-wages", "taylor-rule"])


def _irf(core, blocks, shock="eps_v", horizon=6, overrides=None):
    c = Composition(core, blocks)
    P, Q, params = c.solve(overrides)
    return {v: [float(z) for z in irf(P, Q, c.shock_index(shock), horizon)[:, c.index(v)]]
            for v in c.variables}, params


def test_the_two_friction_composition_is_closed():
    c = Composition(*BOTH)
    assert len(c.equations) == len(c.variables) == 11
    assert c.replaced == {"core-nk-classical.flex-price-output": "calvo-prices",
                          "core-nk-classical.flex-wage-mc": "calvo-wages"}


def test_marginal_cost_is_the_wage_gap_plus_the_decreasing_returns_term():
    """calvo-wages.mc-sticky-wage, at every horizon."""
    r, p = _irf(*BOTH, horizon=10)
    al = p["alpha"]
    for h in range(10):
        assert r["mc"][h] == pytest.approx(r["omega_tilde"][h] + al / (1 - al) * r["x"][h],
                                           rel=1e-10, abs=1e-14)


def test_the_real_wage_gap_accumulates_wage_less_price_inflation():
    """calvo-wages.real-wage-gap. Under a monetary shock technology is zero, so the
    identity reduces to the two inflation rates — which is also why it must be checked
    under a technology shock, where psi_wa enters."""
    r, _ = _irf(*BOTH, horizon=6)
    for h in range(1, 6):
        assert r["omega_tilde"][h] - r["omega_tilde"][h - 1] == pytest.approx(
            r["pi_w"][h] - r["pi"][h], rel=1e-9, abs=1e-14)


def test_the_real_wage_gap_identity_under_a_technology_shock():
    """The same identity with the natural real wage moving, which fires psi_wa."""
    r, p = _irf(*BOTH, shock="eps_a", horizon=6)
    psi = p["psi_wa"]
    for h in range(1, 6):
        assert r["omega_tilde"][h] - r["omega_tilde"][h - 1] == pytest.approx(
            r["pi_w"][h] - r["pi"][h] - psi * (r["a"][h] - r["a"][h - 1]),
            rel=1e-9, abs=1e-14)


def test_the_real_wage_gap_identity_at_a_calibration_where_psi_wa_is_not_one():
    """psi_wa is exactly one at the default calibration, so the default hides it."""
    r, p = _irf(*BOTH, shock="eps_a", horizon=6,
                overrides={"alpha": 0.4, "varphi": 2.0, "sigma": 2.0})
    assert abs(p["psi_wa"] - 1.0) > 1e-3, p["psi_wa"]
    for h in range(1, 6):
        assert r["omega_tilde"][h] - r["omega_tilde"][h - 1] == pytest.approx(
            r["pi_w"][h] - r["pi"][h] - p["psi_wa"] * (r["a"][h] - r["a"][h - 1]),
            rel=1e-9, abs=1e-14), h


def test_the_wage_phillips_curve_holds_period_by_period():
    """calvo-wages.wage-pc, checked as the residual of its own equation."""
    r, p = _irf(*BOTH, horizon=8)
    lw, s_, v_, al = p["lambda_w"], p["sigma"], p["varphi"], p["alpha"]
    for h in range(7):
        residual = (r["pi_w"][h] - p["beta"] * r["pi_w"][h + 1]
                    - lw * ((s_ + v_ / (1 - al)) * r["x"][h] - r["omega_tilde"][h]))
        assert residual == pytest.approx(0.0, abs=1e-12), (h, residual)


def test_sticky_wages_amplify_output_and_damp_inflation():
    one, _ = _irf(*PRICE_ONLY, horizon=1)
    two, _ = _irf(*BOTH, horizon=1)
    assert two["x"][0] < one["x"][0]
    assert abs(two["pi"][0]) < abs(one["pi"][0])


def test_the_real_wage_gap_gives_the_model_a_state_of_its_own():
    r, p = _irf(*BOTH, horizon=6)
    ratios = [r["x"][h + 1] / r["x"][h] for h in range(4)]
    assert not np.allclose(ratios, p["rho_v"], rtol=1e-6), ratios
    gap = [abs(v) for v in r["omega_tilde"][:5]]
    assert gap[1] > gap[0], gap


def test_the_wage_block_vanishes_as_wages_become_flexible():
    limit, _ = _irf(*PRICE_ONLY, horizon=1)
    for tw, tol in ((1e-4, 1e-3), (1e-6, 1e-5), (1e-8, 1e-7)):
        got, _ = _irf(*BOTH, horizon=1, overrides={"theta_w": tw})
        assert got["x"][0] == pytest.approx(limit["x"][0], abs=tol), tw
