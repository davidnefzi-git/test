"""Source-reference integrity for Smets–Wouters (2007, American Economic Review).

The paper's Bayesian estimates are *information*, not results of an estimation
performed by the library. Check the transcribed tables against the component
defaults and priors so a future update cannot silently make the empirical
reference disagree with the canonical structural representation.
"""
from pathlib import Path

import pytest
import yaml

from modellib.compose import load_component

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "models" / "smets-wouters-2007" / "estimation.yaml"
EST = yaml.safe_load(PATH.read_text(encoding="utf-8"))


def test_aer_observables_and_sample():
    o = EST["observations"]
    assert o["source_equation"].startswith("(15)")
    assert (o["estimation_sample"]["start"], o["estimation_sample"]["end"]) == (
        "1966Q1", "2004Q4"
    )
    assert o["estimation_sample"]["quarters"] == 156
    assert [x["series"] for x in o["measurement_system"]] == [
        "dlGDP", "dlCONS", "dlINV", "dlWAG", "lHOURS", "dlP", "FEDFUNDS"
    ]
    assert {x["name"] for x in o["additional_estimated_measurement_parameters"]} == {
        "hours_bar", "pi_bar"
    }


def test_aer_posterior_table_dimensions_and_ranges():
    structural = EST["structural_table_1a"]
    shocks = EST["shock_table_1b"]
    assert len(structural) == 19
    assert len(shocks) == 17
    assert len({x["name"] for x in structural}) == 19
    assert len({x.get("name", x.get("shock")) for x in shocks}) == 17
    for item in structural + shocks:
        assert item["p05"] <= item["mean"] <= item["p95"], item
        assert item["p05"] <= item["mode"] <= item["p95"], item
        assert len(item["prior"]) == 3
    assert [x["name"] for x in structural if x["component"] is None] == [
        "pi_bar", "hours_bar"
    ]


def test_aer_published_priors_and_means_match_components():
    for row in EST["structural_table_1a"] + EST["shock_table_1b"]:
        if row["component"] is None:
            continue
        component = load_component(row["component"])
        if "shock" in row:
            item = next(s for s in component["shocks"] if s["id"] == row["shock"])
            assert item["sd"] == pytest.approx(row["mean"]), row["shock"]
            continue
        item = next(p for p in component["parameters"] if p["name"] == row["name"])
        assert item["default"] == pytest.approx(row["mean"]), row["name"]
        prior = item["prior"]
        assert prior["family"] == row["prior"][0], row["name"]
        assert prior["hyperparameters"] == pytest.approx(row["prior"][1:]), row["name"]


def test_aer_fixed_calibrations_match_components():
    assert len(EST["fixed_calibrations"]["values"]) == 5
    for row in EST["fixed_calibrations"]["values"]:
        component, name = row["component_parameter"].split(".")
        params = load_component(component)["parameters"]
        param = next(p for p in params if p["name"] == name)
        assert param["method"] == "calibrated"
        assert param["default"] == pytest.approx(row["value"])


def test_aer_mh_and_marginal_likelihood_are_reference_only():
    assert EST["status"] == "published-reference-only"
    m = EST["estimation_procedure"]["mh"]
    assert (m["draws"], m["burn_in"], m["proposal_scale"]) == (250000, 50000, 0.3)
    assert EST["estimation_procedure"]["forecast_comparison"]["reported_log_marginal_likelihood"]["DSGE"] == -905.8
    assert EST["reported_robustness"]["friction_sensitivity"]["reference_log_marginal_likelihood"] == -923
    # These distinct AER tabulations must not be conflated.
    assert -905.8 != -923
