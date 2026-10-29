"""The medium-scale model, its flexible-price twin, and the policy output gap.

Three kinds of check live here rather than in golden/targets.yaml, because a target
addresses ONE response of ONE composition and these do not:

  * identities between two responses -- the utilisation slope, the accumulation
    coefficient, capital services against the stock carried into the period;
  * conservation along the whole impulse response, at every horizon rather than one;
  * agreement between two COMPOSITIONS, which is the kind that closed the gap.
"""
import re

import numpy as np
import pytest
import sympy as sp

from modellib import Composition, CompositionError
from modellib.compose import load_component, variable_namespace
from modellib.lre import irf

CORE = "core-nk-medium"
REAL = ["capital-utilisation", "fiscal-block-simple", "habit-consumption",
        "investment-adjustment-cost"]
NOMINAL = ["calvo-prices-kimball", "price-indexation", "calvo-wages-kimball",
           "wage-indexation", "fisher-equation", "taylor-rule-sw"]
SIMPLE = ["calvo-prices-kimball", "price-indexation", "calvo-wages-kimball",
          "wage-indexation", "fisher-equation", "rule-inflation-only"]
SHADOW = {
    "components": [CORE] + REAL,
    "suffix": "_f",
    "shared": ["a", "b", "g", "zi"],
    "drop": [f"{CORE}.technology", f"{CORE}.risk-premium",
             "fiscal-block-simple.spending",
             "investment-adjustment-cost.investment-shock"],
}
SHOCKS = ["eps_a", "eps_b", "eps_g", "eps_zi", "eps_v", "eps_p", "eps_w"]
H = 16


def _build(blocks, overrides=None, shadow="auto"):
    sh = SHADOW if (shadow == "auto" and "taylor-rule-sw" in blocks) else (
        None if shadow in ("auto", None) else shadow)
    c = Composition(CORE, blocks, sh)
    P, Q, params = c.solve(overrides)
    return c, P, Q, params


def _path(c, P, Q, shock, variable, horizon=H):
    return irf(P, Q, c.shock_index(shock), horizon)[:, c.index(variable)]


@pytest.fixture(scope="module")
def full():
    return _build(REAL + NOMINAL)


# ---------------------------------------------------------------- shape of the model --
def test_the_composition_is_closed_and_stationary(full):
    c, P, _, _ = full
    assert len(c.equations) == len(c.variables) == 37
    assert float(np.max(np.abs(np.linalg.eigvals(P)))) < 1.0


def test_the_twin_is_thirteen_of_those_thirty_seven(full):
    c, _, _, _ = full
    sh = c.shadow
    assert sh is not None and len(sh["variables"]) == 13
    assert set(sh["shared"]) == {"a", "b", "g", "zi"}
    ns = variable_namespace()
    for v in sh["variables"]:
        assert v.endswith("_f") and v[:-2] in ns, v


def test_the_rule_cannot_be_composed_without_the_twin():
    with pytest.raises(CompositionError, match="flexible-price twin"):
        Composition(CORE, REAL + NOMINAL)


def test_a_twin_may_not_be_built_from_components_the_host_does_not_have():
    bad = dict(SHADOW, components=[CORE, "capital-utilisation", "rotemberg-prices"])
    with pytest.raises(CompositionError, match="the host does not compose"):
        Composition(CORE, REAL + NOMINAL, bad)


def test_dropping_a_shared_process_equation_is_not_optional():
    bad = dict(SHADOW, drop=SHADOW["drop"][:-1])
    with pytest.raises(CompositionError, match="not closed"):
        Composition(CORE, REAL + NOMINAL, bad)


# ------------------------------------------------------------------------ identities --
def test_utilisation_is_the_declared_fraction_of_the_rental_rate(full):
    c, P, Q, params = full
    slope = (1 - params["psi_u"]) / params["psi_u"]
    for s in SHOCKS:
        assert np.allclose(_path(c, P, Q, s, "u"), slope * _path(c, P, Q, s, "rk"),
                           rtol=1e-10, atol=1e-13), s


def test_capital_accumulation_carries_the_article_s_shock_coefficient(full):
    """The coefficient the article and its replication package disagree about."""
    c, P, Q, params = full
    own = (_path(c, P, Q, "eps_zi", "k")[0]
           - params["i_kbar"] * _path(c, P, Q, "eps_zi", "inv")[0])
    article = (params["i_kbar"] * (1 + params["beta_bar"] * params["gamma_g"])
               * params["gamma_g"] ** 2 * params["varphi_i"])
    assert np.isclose(own, article, rtol=1e-10)
    assert not np.isclose(own, article / (1 + params["beta_bar"] * params["gamma_g"]),
                          rtol=1e-2)


def test_the_resource_constraint_holds_along_every_impulse_response(full):
    c, P, Q, params = full
    for s in SHOCKS:
        lhs = _path(c, P, Q, s, "y")
        rhs = (params["c_y"] * _path(c, P, Q, s, "c")
               + params["i_y"] * _path(c, P, Q, s, "inv")
               + _path(c, P, Q, s, "g")
               + params["rkky"] * _path(c, P, Q, s, "u"))
        assert np.allclose(lhs, rhs, rtol=1e-9, atol=1e-12), s


def test_the_production_function_holds_along_every_impulse_response(full):
    c, P, Q, params = full
    for s in SHOCKS:
        lhs = _path(c, P, Q, s, "y")
        rhs = params["phi_p"] * (params["alpha"] * _path(c, P, Q, s, "ks")
                                 + (1 - params["alpha"]) * _path(c, P, Q, s, "n")
                                 + _path(c, P, Q, s, "a"))
        assert np.allclose(lhs, rhs, rtol=1e-9, atol=1e-12), s


def test_capital_services_use_the_stock_carried_into_the_period(full):
    """ks(t) = k(t-1) + u(t): the timing convention, checked rather than trusted."""
    c, P, Q, _ = full
    for s in SHOCKS:
        k = _path(c, P, Q, s, "k")
        lagged = np.concatenate([[0.0], k[:-1]])
        assert np.allclose(_path(c, P, Q, s, "ks"), lagged + _path(c, P, Q, s, "u"),
                           rtol=1e-9, atol=1e-12), s


# ---------------------------------------------------------- the twin, as an economy --
def test_the_twin_s_closures_bind_under_every_shock(full):
    c, P, Q, _ = full
    for s in SHOCKS:
        assert np.allclose(_path(c, P, Q, s, "mc_f"), 0.0, atol=1e-11), s
        assert np.allclose(_path(c, P, Q, s, "w_f"), _path(c, P, Q, s, "mrs_f"),
                           atol=1e-11), s


def test_the_twin_is_driven_by_the_same_shocks_and_not_by_copies_of_them(full):
    c, _, _, _ = full
    for v in ("a", "b", "g", "zi"):
        assert f"{v}_f" not in c.variables, f"{v}_f exists, so the process was duplicated"


def test_the_twin_does_not_respond_to_a_nominal_shock_at_all(full):
    c, P, Q, _ = full
    for s in ("eps_v", "eps_p", "eps_w"):
        for v in ("y_f", "c_f", "inv_f", "n_f", "w_f", "rk_f", "u_f", "k_f"):
            assert np.allclose(_path(c, P, Q, s, v), 0.0, atol=1e-11), f"{s}/{v}"
        assert abs(_path(c, P, Q, s, "y")[0]) > 1e-3, s


def test_the_risk_premium_is_neutral_in_the_twin_and_not_in_the_sticky_economy(full):
    c, P, Q, _ = full
    assert np.allclose(_path(c, P, Q, "eps_b", "y_f"), 0.0, atol=1e-11)
    assert np.allclose(_path(c, P, Q, "eps_b", "rr_f"),
                       -_path(c, P, Q, "eps_b", "b"), atol=1e-11)
    assert _path(c, P, Q, "eps_b", "c")[0] < -0.1
    assert _path(c, P, Q, "eps_b", "qk")[0] < -0.5


# --------------------------------------------------- policy output gap and its closure --
TOGGLE_BASE = ["fiscal-block-simple", "calvo-prices-kimball", "fisher-equation",
               "rule-inflation-only"]
REAL_FRICTIONS = {
    "capital-utilisation": ("psi_u", 1 - 1e-9),
    "habit-consumption": ("lambda_h", 1e-9),
    "investment-adjustment-cost": ("varphi_i", 1e-9),
}


@pytest.mark.parametrize("friction", sorted(REAL_FRICTIONS))
def test_removing_a_friction_and_driving_it_to_zero_give_the_same_model(friction):
    """Two routes to the same economy must arrive at the same economy.

    Route one composes WITHOUT the friction, so the core's own closure is the equation
    that operates. Route two adds the friction and drives its parameter to the limit, so
    the friction's equations operate and must collapse onto the core's.

    The nesting targets check that collapse already -- but in a composition with no
    nominal block, where marginal cost is pinned at zero. A mutation sweep found what
    that leaves open: adding 0.05*mc to any of five core equations failed nothing,
    because every composition the suite built in which they were live had mc identically
    zero. A user composing sticky prices without one of these frictions is building an
    ordinary model, and it was unverified.

    The other two frictions stay in, which is not a convenience: with none of the three
    the model is indeterminate by two stable roots. A nominal friction on a capital core
    needs some real friction to pin it down.
    """
    name, limit = REAL_FRICTIONS[friction]
    others = [f for f in REAL_FRICTIONS if f != friction]
    thin, Pt, Qt, _ = _build(TOGGLE_BASE + others, shadow=None)
    full_, Pf, Qf, _ = _build(TOGGLE_BASE + others + [friction],
                              overrides={name: limit}, shadow=None)

    mc_moves = max(max(abs(x) for x in _path(thin, Pt, Qt, s, "mc"))
                   for s in thin.shocks)
    assert mc_moves > 1.0, f"mc barely moves ({mc_moves:.3g}); the test would be vacuous"

    shared_vars = sorted(set(thin.variables) & set(full_.variables))
    shared_shocks = sorted(set(thin.shocks) & set(full_.shocks))
    assert {"mc", "k", "c", "mrs", "inv", "u"} <= set(shared_vars)
    worst, where = 0.0, ""
    for s in shared_shocks:
        for v in shared_vars:
            d = float(np.max(np.abs(_path(thin, Pt, Qt, s, v)
                                    - _path(full_, Pf, Qf, s, v))))
            if d > worst:
                worst, where = d, f"{s}/{v}"
    # 1e-3, not machine precision: the parameter is driven to within 1e-9 of its limit
    # rather than to it, and the investment Euler is written multiplied by gamma^2*phi,
    # so at phi = 1e-9 that row's conditioning sets the floor. Observed: 4.5e-9, 3.6e-9
    # and 2.4e-5. A mutation of any of the five core equations moves these paths by
    # order one.
    assert worst < 1e-3, f"the two routes disagree by {worst:.3e} on {where}"


# ------------------------------------------- the simple rule, as an identity --------
def test_the_simple_rule_holds_as_an_identity_at_every_horizon():
    """i = phi_pi*pi + v, period by period, under every shock.

    Written as the residual of its own equation rather than as a statement about a
    quantity the rule influences. This component is otherwise seen only by the nesting
    targets of the four nominal frictions, and those converge to the flexible-price
    allocation WHATEVER the rule is -- so a wrong coefficient here would change nothing
    any of them assert.
    """
    c, P, Q, params = _build(REAL + SIMPLE, shadow=None)
    for s in c.shocks:
        assert np.allclose(_path(c, P, Q, s, "i"),
                           params["phi_pi"] * _path(c, P, Q, s, "pi")
                           + _path(c, P, Q, s, "v"),
                           rtol=1e-9, atol=1e-12), s


def test_the_simple_rule_s_shock_is_white_noise_by_construction():
    c, P, Q, params = _build(REAL + SIMPLE, shadow=None)
    assert params["rho_v"] == 0.0
    v = _path(c, P, Q, "eps_v", "v")
    assert np.isclose(v[0], 1.0) and np.allclose(v[1:], 0.0, atol=1e-12)


def test_the_estimated_rule_smooths_and_the_simple_one_does_not(full):
    c, P, Q, _ = full
    smoothed = _path(c, P, Q, "eps_v", "i")
    c2, P2, Q2, _ = _build(REAL + SIMPLE, shadow=None)
    strict = _path(c2, P2, Q2, "eps_v", "i")
    assert abs(smoothed[3] / smoothed[0]) > abs(strict[3] / strict[0])


# --------------------------------- the rearranged equations, checked symbolically ----
VARS = ["pi", "mc", "mkp", "w", "mrs", "inv", "qk", "zi", "k"]
PARAMS = ["beta_bar", "gamma_g", "iota_p", "iota_w", "kappa_p", "kappa_p_inv",
          "kappa_w", "kappa_w_inv", "varphi_i", "i_kbar", "mkw"]
SYMS = {v + suf: sp.Symbol(v + suf) for v in VARS + PARAMS
        for suf in ("", "_LEAD", "_LAG")}
BB = SYMS["beta_bar"] * SYMS["gamma_g"]
SLOPE = {SYMS["kappa_p_inv"]: 1 / SYMS["kappa_p"],
         SYMS["kappa_w_inv"]: 1 / SYMS["kappa_w"]}


def _parse(expr):
    out = expr.replace("^", "**")
    for v in sorted(VARS + ["mkw"], key=len, reverse=True):
        out = re.sub(rf"\b{v}\s*\(\s*\+\s*1\s*\)", v + "_LEAD", out)
        out = re.sub(rf"\b{v}\s*\(\s*-\s*1\s*\)", v + "_LAG", out)
    e = sp.sympify(out, locals=SYMS)
    assert not ({str(s) for s in e.free_symbols} - set(SYMS)), expr
    return e.subs(SLOPE)


def _equation(cid, eid):
    (eq,) = [e for e in load_component(cid)["equations"] if e["id"] == eid]
    return _parse(eq["expr"])


def _ident(mine, scale, printed):
    return sp.simplify(sp.expand(sp.together(mine * scale - printed))) == 0


def test_the_price_curve_is_the_printed_one():
    """Multiplied through by the reciprocal of its slope, so that the flexible-price
    limit is the core closure exactly. Checked symbolically, for all parameter values,
    rather than through solutions that could agree for the wrong reason."""
    PI, MC, MKP, KP = SYMS["pi"], SYMS["mc"], SYMS["mkp"], SYMS["kappa_p"]
    printed = PI - (BB * SYMS["pi_LEAD"] + KP * MC + MKP)
    assert _ident(_equation("calvo-prices-kimball", "price-pc"), KP, printed)


def test_the_indexed_price_curve_is_the_printed_one():
    PI, MC, MKP, KP = SYMS["pi"], SYMS["mc"], SYMS["mkp"], SYMS["kappa_p"]
    IP = SYMS["iota_p"]
    printed = PI - ((BB * SYMS["pi_LEAD"] + IP * SYMS["pi_LAG"] + KP * MC)
                    / (1 + BB * IP) + MKP)
    assert _ident(_equation("price-indexation", "price-pc-indexed"),
                  KP / (1 + BB * IP), printed)


def test_the_wage_curve_is_the_printed_one():
    W, PI, MRS, KW = SYMS["w"], SYMS["pi"], SYMS["mrs"], SYMS["kappa_w"]
    printed = W - (W_m := SYMS["w_LAG"]) / (1 + BB) - BB / (1 + BB) * SYMS["w_LEAD"] \
        + 1 / (1 + BB) * PI - BB / (1 + BB) * SYMS["pi_LEAD"] \
        - KW / (1 + BB) * (MRS - W) - SYMS["mkw"]
    assert _ident(_equation("calvo-wages-kimball", "wage-pc"), KW / (1 + BB), printed)


def test_the_indexed_wage_curve_is_the_printed_one():
    W, PI, MRS, KW = SYMS["w"], SYMS["pi"], SYMS["mrs"], SYMS["kappa_w"]
    IW = SYMS["iota_w"]
    printed = W - SYMS["w_LAG"] / (1 + BB) - BB / (1 + BB) * SYMS["w_LEAD"] \
        - IW / (1 + BB) * SYMS["pi_LAG"] + (1 + BB * IW) / (1 + BB) * PI \
        - BB / (1 + BB) * SYMS["pi_LEAD"] - KW / (1 + BB) * (MRS - W) - SYMS["mkw"]
    assert _ident(_equation("wage-indexation", "wage-pc-indexed"),
                  KW / (1 + BB), printed)


def test_the_investment_euler_is_the_printed_one():
    INV, QK, ZI, PHI = SYMS["inv"], SYMS["qk"], SYMS["zi"], SYMS["varphi_i"]
    printed = INV - ((SYMS["inv_LAG"] + BB * SYMS["inv_LEAD"]
                      + QK / (SYMS["gamma_g"] ** 2 * PHI)) / (1 + BB) + ZI)
    assert _ident(_equation("investment-adjustment-cost", "investment-euler"),
                  1 / (SYMS["gamma_g"] ** 2 * PHI * (1 + BB)), printed)


def test_capital_accumulation_carries_the_article_s_factor_symbolically():
    K, INV, ZI = SYMS["k"], SYMS["inv"], SYMS["zi"]
    IKB, PHI, G = SYMS["i_kbar"], SYMS["varphi_i"], SYMS["gamma_g"]
    mine = _equation("investment-adjustment-cost", "capital-accumulation-adj")
    printed = K - ((1 - IKB) * SYMS["k_LAG"] + IKB * INV
                   + IKB * (1 + BB) * G ** 2 * PHI * ZI)
    assert sp.simplify(sp.expand(mine - printed)) == 0
    package = K - ((1 - IKB) * SYMS["k_LAG"] + IKB * INV + IKB * G ** 2 * PHI * ZI)
    assert sp.simplify(sp.expand(mine - package)) != 0
