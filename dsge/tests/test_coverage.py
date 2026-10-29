"""Guards against a suite that is green because it is not looking.

Both defects found in this project by cross-checking were equations no target
exercised. The coverage checks also ensure that model entries exercise the mechanisms they declare.
three entries had no manifest.yaml, tests/test_golden.py filters on its presence, and
ten of the eighteen golden targets therefore never ran under pytest. Every equation of
the open-economy core was unverified, and the suite was green.

These tests make that condition fail.
"""
from pathlib import Path

import pytest
import yaml

from modellib.compose import component_dirs, load_component
from modellib.golden import load_targets

ROOT = Path(__file__).resolve().parent.parent
ENTRY_DIRS = sorted(d for d in (ROOT / "models").iterdir() if d.is_dir())


def test_every_entry_is_collected_by_the_golden_runner():
    """An entry carrying targets must carry a manifest, or its targets never run."""
    uncollected = [d.name for d in ENTRY_DIRS
                   if (d / "golden" / "targets.yaml").exists()
                   and not (d / "manifest.yaml").exists()]
    assert not uncollected, (
        f"entries with targets but no manifest, so tests/test_golden.py skips them "
        f"entirely: {uncollected}"
    )


def test_every_entry_declares_targets():
    missing = [d.name for d in ENTRY_DIRS if not load_targets(d).get("targets")]
    assert not missing, f"entries with no golden targets at all: {missing}"


@pytest.mark.parametrize("d", ENTRY_DIRS, ids=[d.name for d in ENTRY_DIRS])
def test_every_entry_composition_is_declared_and_assembles(d):
    from modellib.compose import Composition
    spec = yaml.safe_load((d / "manifest.yaml").read_text())["composition"]
    # The flexible-price twin is part of the composition, not a decoration on it: an
    # entry whose policy rule reads flexible-price output is not closed without its
    # twin, so the check that the composition assembles has to assemble the twin too.
    c = Composition(spec["core"], spec["blocks"], spec.get("shadow"))
    assert len(c.equations) == len(c.variables)


def test_every_component_appears_in_some_entry():
    """A component no entry uses is a component no target can verify."""
    used = set()
    for d in ENTRY_DIRS:
        spec = yaml.safe_load((d / "manifest.yaml").read_text())["composition"]
        used.add(spec["core"])
        used.update(spec["blocks"])
    # Variants deliberately held outside the default compositions are listed here, and
    # each must be exercised by a test of its own.
    variants = {"rotemberg-prices", "rule-cpi-inflation", "rule-exchange-rate-peg",
                "rule-optimal-domestic-price-stability", "core-rbc-hansen",
                # Closes the nominal side on its own, which is what lets the four
                # nominal frictions of the medium-scale family have nesting targets at
                # all: the estimated rule's output gap is measured against the very twin
                # a flexible-price limit collapses onto. Exercised by those targets and
                # by three tests of its own in tests/test_medium_scale.py.
                "rule-inflation-only"}
    orphans = {d.name for d in component_dirs()} - used - variants
    assert not orphans, f"components no entry composes and no variant list covers: {orphans}"


@pytest.mark.parametrize("d", sorted(component_dirs()), ids=lambda d: d.name)
def test_every_declared_shock_is_exercised_somewhere(d):
    """An unexercised shock is an unverified equation.

    The rule the natural-rate sign error produced: every shock a component declares must
    appear in at least one golden target or one test.
    """
    comp = load_component(d.name)
    declared = {s["id"] for s in (comp.get("shocks") or [])}
    if not declared:
        return
    text = ""
    for p in list((ROOT / "models").rglob("targets.yaml")) + list((ROOT / "tests").glob("*.py")) \
            + list((ROOT / "models").rglob("test_*.py")):
        text += p.read_text()
    unexercised = {s for s in declared if s not in text}
    assert not unexercised, (
        f"{d.name} declares shocks that no target or test fires: {sorted(unexercised)}"
    )
