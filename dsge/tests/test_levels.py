"""The levels path, exercised end to end on core-rbc-hansen.

Hansen (1985) carries no golden target here, and that is deliberate rather than an
omission. This harness's analytic targets compare one impulse response against a closed
form in the parameters, and an RBC model on impact has no single response expressible
that way: the exact relations available — the rental rate against output, the capital
stock against investment — relate two responses to each other. Writing one of those
responses into the file as a literal would have put a number of my own computing there
and called it a target. The relations are asserted here instead.
"""
import numpy as np
import pytest

from modellib import Composition, CompositionError
from modellib.lre import irf


@pytest.fixture(scope="module")
def rbc():
    return Composition("core-rbc-hansen")


def test_the_core_is_closed_on_its_own(rbc):
    # Unlike the New Keynesian cores, which are one equation short until a policy
    # component is added, an RBC core is a model.
    assert len(rbc.equations) == len(rbc.variables) == 9
    assert rbc.equation_form == "levels"


def test_the_steady_state_is_solved_and_verified(rbc):
    ss = rbc.steady_state()
    assert ss["a"] == pytest.approx(1.0, rel=1e-12)
    assert ss["rk"] == pytest.approx(1 / 0.99 - (1 - 0.025), rel=1e-12)
    assert ss["k"] / ss["y"] == pytest.approx(10.256, rel=1e-3)
    assert ss["inv"] == pytest.approx(0.025 * ss["k"], rel=1e-12)
    assert ss["prod"] == pytest.approx(ss["y"] / ss["n"], rel=1e-12)


def test_a_steady_state_that_is_not_an_equilibrium_is_refused():
    """The assembler must not linearise about a point that does not solve the model."""
    import copy

    import modellib.compose as cp
    original = cp.load_component
    bad = copy.deepcopy(original("core-rbc-hansen"))
    bad["steady_state"]["analytic"]["c"] = "y - delta*k + 0.01"
    cp.load_component = lambda cid: bad if cid == "core-rbc-hansen" else original(cid)
    try:
        with pytest.raises(CompositionError, match="does not satisfy the model"):
            Composition("core-rbc-hansen").solve()
    finally:
        cp.load_component = original


def test_capital_and_investment_respond_identically_on_impact(rbc):
    # Exact, and the check that fails if the timing convention on capital is violated:
    # the stock available this period is predetermined.
    P, Q, _ = rbc.solve()
    r = irf(P, Q, rbc.shock_index("eps_a"), 3)
    assert r[0, rbc.index("k")] == pytest.approx(r[0, rbc.index("inv")], rel=1e-12)
    assert r[1, rbc.index("k")] != pytest.approx(r[1, rbc.index("inv")], rel=1e-6)


def test_investment_is_more_volatile_than_consumption_in_percent(rbc):
    """In levels output moves most; in percent investment does. That is the trap."""
    P, Q, _ = rbc.solve()
    ss = rbc.steady_state()
    r = irf(P, Q, rbc.shock_index("eps_a"), 1)
    lvl = {v: r[0, rbc.index(v)] for v in ("y", "c", "inv")}
    pct = {v: 100 * lvl[v] / ss[v] for v in lvl}
    assert pct["inv"] > pct["y"] > pct["c"] > 0, pct
    assert lvl["y"] > lvl["inv"] > lvl["c"], lvl


def test_the_technology_process_decays_at_its_own_persistence(rbc):
    """gamma_a, which a mutation test found unverified.

    Nothing pinned the persistence of productivity: the steady state does not involve
    it, and the impact responses are proportional to the shock whatever it is. The
    process itself has to be checked.
    """
    P, Q, p = rbc.solve()
    a = irf(P, Q, rbc.shock_index("eps_a"), 6)[:, rbc.index("a")]
    for h in range(4):
        assert a[h + 1] / a[h] == pytest.approx(p["gamma_a"], rel=1e-10), h
    # And at a different persistence, so the default cannot be what passes.
    P2, Q2, p2 = rbc.solve({"gamma_a": 0.5})
    a2 = irf(P2, Q2, rbc.shock_index("eps_a"), 4)[:, rbc.index("a")]
    assert a2[1] / a2[0] == pytest.approx(0.5, rel=1e-10)


def test_calvo_and_rotemberg_coincide_at_first_order():
    """Pins the Rotemberg coefficient, which the nesting limit alone does not.

    Driving phi_rotemberg to zero sends lambda_pr to infinity, so scaling lambda_pr leaves the
    limit unchanged and the nesting target passes either way. The first-order
    equivalence the literature asserts is the check that bites: set phi_rotemberg from the Calvo
    parameters rather than from a rounded default, and the two compositions must agree
    exactly. This also settles the open question recorded in the component.
    """
    calvo = Composition("core-nk-classical", ["calvo-prices", "taylor-rule"])
    rot = Composition("core-nk-classical", ["rotemberg-prices", "taylor-rule"])
    Pc, Qc, pc = calvo.solve()
    phi_rotemberg = (9.0 - 1.0) / pc["lambda_p"]          # epsilon_r - 1 over the Calvo slope
    Pr, Qr, pr = rot.solve({"phi_rotemberg": phi_rotemberg})
    assert pr["lambda_pr"] == pytest.approx(pc["lambda_p"], rel=1e-12)
    for shock in ("eps_v", "eps_a"):
        c = irf(Pc, Qc, calvo.shock_index(shock), 6)
        r = irf(Pr, Qr, rot.shock_index(shock), 6)
        for v in ("x", "pi", "i", "mc"):
            assert np.allclose(c[:, calvo.index(v)], r[:, rot.index(v)],
                               rtol=1e-10, atol=1e-14), (shock, v)


def test_the_saddle_path_root_is_selected(rbc):
    """What the QZ decomposition is for.

    Root-finding by iteration returned a root of spectral radius 1.07 for this model and
    reported it as a solution. A model with endogenous capital is a saddle-path problem.
    """
    P, _, _ = rbc.solve()
    assert np.max(np.abs(np.linalg.eigvals(P))) < 1.0 - 1e-6


def test_equation_forms_cannot_be_mixed():
    with pytest.raises(CompositionError, match="mix equation forms"):
        Composition("core-rbc-hansen", ["calvo-prices"])
