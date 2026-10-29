"""Run every golden target of every model entry."""
from functools import lru_cache
from pathlib import Path

import pytest

from modellib.golden import load_targets, run_golden

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIRS = sorted(d for d in (ROOT / "models").iterdir()
                    if d.is_dir() and (d / "manifest.yaml").exists())


def _cases():
    for d in MODEL_DIRS:
        for t in load_targets(d).get("targets", []):
            yield d, t["id"]


@lru_cache(maxsize=None)
def _results(model_dir: Path) -> dict:
    """Every target of one entry, evaluated once.

    Without this cache the function ran once per TARGET, so an entry with n targets
    evaluated n^2 of them. That was invisible at nine targets and is not at thirty-five:
    smets-wouters-2007's targets evaluate in twenty-three seconds, and running them
    thirty-five times over was 455 of the suite's 460.
    """
    return {r.target_id: r for r in run_golden(model_dir)}


@pytest.mark.parametrize("model_dir,target_id", list(_cases()),
                         ids=[f"{d.name}:{tid}" for d, tid in _cases()])
def test_golden_target(model_dir, target_id):
    r = _results(model_dir)[target_id]
    assert r.passed, f"{r.kind} target '{target_id}' failed: {r.message}"
