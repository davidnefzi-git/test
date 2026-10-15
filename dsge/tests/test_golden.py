"""Run every golden target of every model entry."""
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


@pytest.mark.parametrize("model_dir,target_id", list(_cases()),
                         ids=[f"{d.name}:{tid}" for d, tid in _cases()])
def test_golden_target(model_dir, target_id):
    results = {r.target_id: r for r in run_golden(model_dir)}
    r = results[target_id]
    assert r.passed, f"{r.kind} target '{target_id}' failed: {r.message}"
