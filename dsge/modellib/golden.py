"""Golden-target runner for composed models.

Two target kinds are implemented, both absent from the current repository format and
both required by the composition objective.

``analytic``
    ``expected`` is a closed-form expression in the model's own parameters rather than
    a transcribed number. Obstfeld-Rogoff (1995), Eggertsson-Woodford (2003) and
    Golosov et al. (2014) state propositions, not table cells; a numeric-only format
    cannot verify them. Where a closed form exists it is also a stronger target than a
    published number, because it holds at every calibration.

``nesting``
    The verification analogue of ``reproduces_paper`` for a block that has no paper of
    its own. The friction parameter is driven along a sequence towards its limit and
    two things are checked: that the response converges to the value produced by the
    composition WITHOUT the block, and that it does so at the stated rate. The rate
    check is what catches a sign error or a mis-stated timing convention, which a
    convergence-only check would let through.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
import yaml

from .compose import Composition
from .lre import irf


@dataclass
class GoldenResult:
    target_id: str
    kind: str
    expected: float | None
    actual: float | None
    passed: bool
    message: str = ""


def load_targets(model_dir: str | Path) -> dict[str, Any]:
    with open(Path(model_dir) / "golden" / "targets.yaml") as f:
        return yaml.safe_load(f) or {}


def evaluate_expression(expr: str, params: dict[str, float],
                        where: dict[str, str] | None = None) -> float:
    """Evaluate a closed form in the model's parameters, with named intermediates.

    Explicit symbols are built for every name because sympify would otherwise read
    ``beta`` as the Beta function and ``pi`` as the circle constant, substitute neither,
    and fail with a misleading message.
    """
    names = set(params) | set(where or {})
    syms = {n: sp.Symbol(n) for n in names}
    values = {syms[k]: v for k, v in params.items()}
    for name, formula in (where or {}).items():
        e = sp.sympify(formula, locals=syms).subs(values)
        values[syms[name]] = float(e.evalf())
    out = sp.sympify(expr, locals=syms).subs(values)
    return float(out.evalf())


def _response(comp: Composition, overrides: dict[str, float] | None,
              shock: str, variable: str, period: int) -> float:
    P, Q, params = comp.solve(overrides)
    path = irf(P, Q, comp.shock_index(shock), period + 1)
    return float(path[period, comp.index(variable)]), params


def run_golden(model_dir: str | Path) -> list[GoldenResult]:
    spec = load_targets(model_dir)
    results: list[GoldenResult] = []

    for t in spec.get("targets", []):
        kind = t.get("kind", "numeric")
        try:
            if kind == "analytic":
                comp = Composition(t["composition"][0], t["composition"][1:])
                actual, params = _response(comp, t.get("params"), t["shock"],
                                           t["variable"], t.get("period", 0))
                expected = evaluate_expression(t["expected"], params, t.get("where"))
                rtol = float(t.get("rtol", 1e-10))
                ok = bool(np.isclose(actual, expected, rtol=rtol, atol=0.0))
                msg = "" if ok else f"expected {expected!r}, got {actual!r} (rtol={rtol})"
                results.append(GoldenResult(t["id"], kind, expected, actual, ok, msg))

            elif kind == "nesting":
                with_block = Composition(t["composition"][0], t["composition"][1:])
                without = Composition(t["recovers"][0], t["recovers"][1:])
                limit_value, _ = _response(without, None, t["shock"], t["variable"],
                                           t.get("period", 0))
                seq = [float(s) for s in t["sequence"]]
                responses, ratios = [], []
                for value in seq:
                    r, params = _response(with_block, {t["parameter"]: value},
                                          t["shock"], t["variable"], t.get("period", 0))
                    responses.append(r)
                    ratios.append((r - limit_value) / value)
                converged = abs(responses[-1] - limit_value)
                monotone = all(
                    abs(responses[i + 1] - limit_value) < abs(responses[i] - limit_value)
                    for i in range(len(responses) - 1)
                )
                tol = float(t.get("tolerance", 1e-6))
                ok = converged < tol and monotone
                msg = ""
                if not monotone:
                    msg = f"convergence is not monotone: {responses}"
                elif converged >= tol:
                    msg = (f"did not reach the limit: |{responses[-1]} - {limit_value}| "
                           f"= {converged:.3e} > {tol:.3e}")
                if ok and t.get("rate"):
                    expected_rate = evaluate_expression(t["rate"], _response(
                        with_block, {t["parameter"]: seq[-1]}, t["shock"],
                        t["variable"], t.get("period", 0))[1], t.get("where"))
                    rate_tol = float(t.get("rate_rtol", 1e-3))
                    if not np.isclose(ratios[-1], expected_rate, rtol=rate_tol, atol=0.0):
                        ok = False
                        msg = (f"converges, but at the wrong rate: observed "
                               f"{ratios[-1]:.6f}, expected {expected_rate:.6f}")
                    results.append(GoldenResult(t["id"], kind, expected_rate,
                                                ratios[-1], ok, msg))
                else:
                    results.append(GoldenResult(t["id"], kind, limit_value,
                                                responses[-1], ok, msg))
            else:
                results.append(GoldenResult(t["id"], kind, None, None, False,
                                            f"unknown target kind '{kind}'"))
        except Exception as exc:  # report, never drop
            results.append(GoldenResult(t.get("id", "<no id>"), kind, None, None, False,
                                        f"{type(exc).__name__}: {exc}"))
    return results
