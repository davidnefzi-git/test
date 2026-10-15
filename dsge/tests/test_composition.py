"""The checks that must fail. A composition that is not closed, or that is doubly
determined, otherwise solves without complaint and produces dynamics that mean
nothing; these tests exist to make that failure loud."""
import numpy as np
import pytest

from modellib import Composition, CompositionError


def test_nk_composition_is_closed():
    nk = Composition("core-nk-classical", ["calvo-prices", "taylor-rule"])
    assert len(nk.equations) == len(nk.variables) == 6
    assert "core-nk-classical.flex-price-output" in nk.replaced
    assert nk.replaced["core-nk-classical.flex-price-output"] == "calvo-prices"


def test_classical_composition_is_closed_and_keeps_the_replaced_equation():
    cl = Composition("core-nk-classical", ["taylor-rule"])
    assert len(cl.equations) == len(cl.variables) == 6
    assert cl.replaced == {}
    assert any(eid == "core-nk-classical.flex-price-output" for eid, _ in cl.equations)


def test_core_alone_is_not_closed():
    with pytest.raises(CompositionError, match="not closed"):
        Composition("core-nk-classical")


def test_missing_policy_block_is_caught():
    with pytest.raises(CompositionError, match="not closed"):
        Composition("core-nk-classical", ["calvo-prices"])


def test_two_pricing_blocks_are_rejected():
    with pytest.raises(CompositionError, match="incompatible"):
        Composition("core-nk-classical", ["calvo-prices", "rotemberg-prices", "taylor-rule"])


def test_a_friction_block_cannot_serve_as_a_core():
    with pytest.raises(CompositionError, match="not 'core'"):
        Composition("calvo-prices")


def test_unknown_component_is_reported():
    with pytest.raises(CompositionError, match="no component"):
        Composition("core-nk-classical", ["financial-accelerator-bgg"])


def test_unknown_parameter_override_is_reported():
    nk = Composition("core-nk-classical", ["calvo-prices", "taylor-rule"])
    with pytest.raises(CompositionError, match="unknown parameter"):
        nk.solve({"theta": 0.5})


def test_derived_parameters_resolve_in_dependency_order():
    nk = Composition("core-nk-classical", ["calvo-prices", "taylor-rule"])
    p = nk.parameters()
    assert np.isclose(p["Theta"], (1 - 0.25) / (1 - 0.25 + 0.25 * 9.0))
    assert np.isclose(p["kappa"], p["lambda_p"] * (p["sigma"] + (p["varphi"] + p["alpha"]) / (1 - p["alpha"])))


def test_taylor_principle_violation_is_reported_not_silently_solved():
    nk = Composition("core-nk-classical", ["calvo-prices", "taylor-rule"])
    from modellib import SolutionError
    with pytest.raises((SolutionError, CompositionError)):
        nk.solve({"phi_pi": 0.5, "phi_x": 0.0})
