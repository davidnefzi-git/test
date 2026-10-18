"""Assemble a model from a core and a list of component blocks.

The point of this module is not to solve models — lre.py does that — but to refuse to
assemble one that is not well posed. Four failures are caught before any number is
produced:

  * a required variable that no included component provides;
  * two components providing the same variable;
  * two components replacing the same equation;
  * a mismatch between the number of equations and the number of endogenous variables.

A composition that is not closed, or that is doubly determined, otherwise solves without
complaint and yields dynamics that mean nothing. That silent failure is the reason the
provides / requires / replaces fields exist.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import json
from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import sympy as sp
import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_DIR = REPO_ROOT / "taxonomy"

COMPONENTS_DIR = REPO_ROOT / "components"
COMPONENT_SCHEMA_PATH = REPO_ROOT / "schema" / "component.schema.json"
LEAD, LAG, NOW = "_tp1", "_tm1", "_t"


class CompositionError(ValueError):
    pass


@lru_cache
def _component_validator() -> Draft202012Validator:
    with open(COMPONENT_SCHEMA_PATH) as f:
        return Draft202012Validator(json.load(f))


@lru_cache
def variable_namespace() -> dict[str, dict]:
    """taxonomy/variables.yaml: the namespace component equations are written in."""
    with open(TAXONOMY_DIR / "variables.yaml") as f:
        return yaml.safe_load(f) or {}


def component_dirs():
    if not COMPONENTS_DIR.exists():
        return
    for d in sorted(COMPONENTS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith(("_", ".")) and (d / "component.yaml").exists():
            yield d


def load_component(component_id: str) -> dict[str, Any]:
    path = COMPONENTS_DIR / component_id / "component.yaml"
    if not path.exists():
        raise CompositionError(f"no component '{component_id}' under components/")
    with open(path) as f:
        return yaml.safe_load(f)


def validate_component(component: dict[str, Any], folder_name: str | None = None) -> list[str]:
    """Return a list of human-readable problems (empty list = valid).

    Mirrors manifest.validate_manifest: schema first, then the checks a schema cannot
    express — that every variable is declared in the namespace, and that `replaces`
    names an equation of a component that actually defines it.
    """
    errors = [
        f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message}"
        for e in sorted(_component_validator().iter_errors(component), key=lambda e: list(e.path))
    ]
    if errors:
        return errors

    if folder_name and component["id"] != folder_name:
        errors.append(f"id '{component['id']}' does not match folder name '{folder_name}'")

    ns = variable_namespace()
    for key in ("provides", "requires"):
        for v in component["variables"][key]:
            if v not in ns:
                errors.append(
                    f"variables/{key}: '{v}' is not declared in taxonomy/variables.yaml "
                    f"(add it in a taxonomy/ PR first)"
                )

    for target in component.get("replaces") or []:
        if "." not in target:
            errors.append(f"replaces: '{target}' is not of the form <component-id>.<equation-id>")
            continue
        owner, eq_id = target.split(".", 1)
        try:
            owner_component = load_component(owner)
        except CompositionError as exc:
            errors.append(f"replaces: {exc}")
            continue
        if eq_id not in {e["id"] for e in owner_component["equations"]}:
            errors.append(f"replaces: component '{owner}' defines no equation '{eq_id}'")

    nt = component.get("nesting_target")
    if nt and not nt.get("pathological"):
        if nt["probe"]["variable"] not in ns:
            errors.append(
                f"nesting_target/probe/variable: '{nt['probe']['variable']}' is not "
                f"declared in taxonomy/variables.yaml"
            )
        if nt["parameter"] not in {p["name"] for p in component.get("parameters") or []}:
            errors.append(
                f"nesting_target/parameter: '{nt['parameter']}' is not a parameter of "
                f"this component"
            )

    names = [p["name"] for p in component.get("parameters") or []]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        errors.append(f"duplicate parameter names: {sorted(dupes)}")

    for p in component.get("parameters") or []:
        if p["method"] == "derived" and not p.get("formula"):
            errors.append(f"parameter '{p['name']}': method 'derived' requires a formula")
        if p["method"] == "estimated" and not p.get("prior"):
            errors.append(
                f"parameter '{p['name']}': method 'estimated' requires a prior "
                f"(an estimation cannot be replicated without one)"
            )
    return errors


def _subst(expr: str, variables: list[str], shocks: list[str]) -> str:
    """Rewrite x(+1), x(-1) and x into distinct sympy symbol names."""
    out = expr
    for v in sorted(variables, key=len, reverse=True):
        out = re.sub(rf"\b{re.escape(v)}\s*\(\s*\+\s*1\s*\)", v + LEAD, out)
        out = re.sub(rf"\b{re.escape(v)}\s*\(\s*-\s*1\s*\)", v + LAG, out)
    for v in sorted(variables, key=len, reverse=True):
        out = re.sub(rf"\b{re.escape(v)}\b(?!{LEAD}|{LAG}|{NOW})", v + NOW, out)
    for s in sorted(shocks, key=len, reverse=True):
        out = re.sub(rf"\b{re.escape(s)}\b", s + "_shock", out)
    return out


class Composition:
    """A core plus a set of blocks, with the checks that make it a model."""

    def __init__(self, core: str, blocks: list[str] | None = None):
        self.core_id = core
        self.block_ids = list(blocks or [])
        self.ids = [core] + self.block_ids
        if len(set(self.ids)) != len(self.ids):
            raise CompositionError("a component is listed twice")
        self.components = {cid: load_component(cid) for cid in self.ids}
        core_comp = self.components[core]
        if core_comp.get("kind") != "core":
            raise CompositionError(f"'{core}' has kind '{core_comp.get('kind')}', not 'core'")
        self.check()

    # ---------------------------------------------------------------- checks --
    def check(self) -> None:
        comps = self.components

        for cid, c in comps.items():
            for dep in c.get("depends_on") or []:
                if dep not in comps:
                    raise CompositionError(
                        f"component '{cid}' declares depends_on '{dep}', which is not included"
                    )

        for cid, c in comps.items():
            for other in c.get("incompatible_with") or []:
                if other in comps:
                    raise CompositionError(
                        f"components '{cid}' and '{other}' are declared incompatible "
                        f"and cannot be composed"
                    )

        ns = variable_namespace()
        for cid, c in comps.items():
            for key in ("provides", "requires"):
                for v in c["variables"][key]:
                    if v not in ns:
                        raise CompositionError(
                            f"component '{cid}' uses variable '{v}', which is not declared "
                            f"in taxonomy/variables.yaml"
                        )

        provider: dict[str, str] = {}
        for cid, c in comps.items():
            for v in c["variables"]["provides"]:
                if v in provider:
                    raise CompositionError(
                        f"variable '{v}' is provided by both '{provider[v]}' and '{cid}'"
                    )
                provider[v] = cid
        self.provider = provider
        self.variables = sorted(provider)

        missing = []
        for cid, c in comps.items():
            for v in c["variables"]["requires"]:
                if v not in provider:
                    missing.append((cid, v))
        if missing:
            detail = "; ".join(f"'{c}' requires '{v}'" for c, v in missing)
            raise CompositionError(f"unprovided variables: {detail}")

        replaced: dict[str, str] = {}
        all_eq_ids = {f"{cid}.{e['id']}" for cid, c in comps.items() for e in c["equations"]}
        for cid, c in comps.items():
            for target in c.get("replaces") or []:
                if target not in all_eq_ids:
                    raise CompositionError(
                        f"component '{cid}' replaces '{target}', which no included "
                        f"component defines"
                    )
                if target in replaced:
                    raise CompositionError(
                        f"equation '{target}' is replaced by both '{replaced[target]}' "
                        f"and '{cid}'"
                    )
                replaced[target] = cid
        self.replaced = replaced

        self.equations = [
            (f"{cid}.{e['id']}", e["expr"])
            for cid, c in comps.items()
            for e in c["equations"]
            if f"{cid}.{e['id']}" not in replaced
        ]

        self.shocks = sorted(
            {s["id"] for c in comps.values() for s in (c.get("shocks") or [])}
        )

        if len(self.equations) != len(self.variables):
            raise CompositionError(
                f"composition is not closed: {len(self.equations)} equations for "
                f"{len(self.variables)} endogenous variables "
                f"({', '.join(self.variables)})"
            )

    # ------------------------------------------------------------ parameters --
    def parameters(self, overrides: dict[str, float] | None = None) -> dict[str, float]:
        declared: dict[str, dict] = {}
        for cid, c in self.components.items():
            for p in c.get("parameters") or []:
                if p["name"] in declared:
                    raise CompositionError(
                        f"parameter '{p['name']}' declared by two components"
                    )
                declared[p["name"]] = p

        for k in (overrides or {}):
            if k not in declared:
                raise CompositionError(f"unknown parameter '{k}' for this composition")

        values = {
            n: p["default"] for n, p in declared.items()
            if p["method"] != "derived" and p["default"] is not None
        }
        values.update(overrides or {})

        # Explicit symbols for every parameter name. Without this, sympify would read
        # `beta` as the Beta function and `pi` as the circle constant, substitute
        # nothing, and fail with a misleading message.
        psyms = {n: sp.Symbol(n) for n in declared}
        pending = {n: p for n, p in declared.items() if p["method"] == "derived"}
        while pending:
            progressed = False
            for n, p in list(pending.items()):
                try:
                    e = sp.sympify(p["formula"], locals=psyms)
                    e = e.subs({psyms[k]: val for k, val in values.items() if k in psyms})
                    values[n] = float(e.evalf())
                except Exception:
                    continue
                if not np.isfinite(values[n]):
                    raise CompositionError(f"derived parameter '{n}' is not finite")
                pending.pop(n)
                progressed = True
            if not progressed:
                raise CompositionError(
                    f"cannot resolve derived parameters: {', '.join(sorted(pending))}"
                )
        return values

    # --------------------------------------------------------------- matrices --
    def matrices(self, overrides: dict[str, float] | None = None):
        params = self.parameters(overrides)
        v, s = self.variables, self.shocks
        n, k = len(v), len(s)
        syms = {name: sp.Symbol(name) for name in
                [x + suf for x in v for suf in (NOW, LEAD, LAG)]
                + [x + "_shock" for x in s]}
        psyms = {name: sp.Symbol(name) for name in params}
        table = dict(syms)
        table.update(psyms)
        A2 = np.zeros((n, n)); A0 = np.zeros((n, n)); A1 = np.zeros((n, n)); B = np.zeros((n, k))
        for r, (eq_id, expr) in enumerate(self.equations):
            e = sp.sympify(_subst(expr, v, s), locals=table)
            e = e.subs({psyms[k]: val for k, val in params.items()})
            free = {str(x) for x in e.free_symbols} - set(syms)
            if free:
                raise CompositionError(
                    f"equation '{eq_id}' contains unresolved names: {', '.join(sorted(free))}"
                )
            for j, name in enumerate(v):
                A2[r, j] = float(sp.diff(e, syms[name + LEAD]))
                A0[r, j] = float(sp.diff(e, syms[name + NOW]))
                A1[r, j] = float(sp.diff(e, syms[name + LAG]))
            for j, name in enumerate(s):
                B[r, j] = float(sp.diff(e, syms[name + "_shock"]))
        return A2, A0, A1, B, params

    # ------------------------------------------------------------------ solve --
    def solve(self, overrides: dict[str, float] | None = None):
        from .lre import solve as _solve
        A2, A0, A1, B, params = self.matrices(overrides)
        P, Q = _solve(A2, A0, A1, B)
        return P, Q, params

    def index(self, variable: str) -> int:
        return self.variables.index(variable)

    def shock_index(self, shock: str) -> int:
        return self.shocks.index(shock)

    def describe(self) -> str:
        lines = [f"composition: {' + '.join(self.ids)}",
                 f"  endogenous variables ({len(self.variables)}): {', '.join(self.variables)}",
                 f"  equations ({len(self.equations)}):"]
        lines += [f"    {eid:<45} 0 = {expr}" for eid, expr in self.equations]
        if self.replaced:
            lines.append("  replaced equations:")
            lines += [f"    {t} removed by {by}" for t, by in self.replaced.items()]
        lines.append(f"  shocks: {', '.join(self.shocks)}")
        return "\n".join(lines)


# --------------------------------------------------------------------- nesting --
@dataclass
class NestingResult:
    component_id: str
    passed: bool
    limit_value: float | None = None
    responses: list[float] | None = None
    expected_rate: float | None = None
    observed_rate: float | None = None
    message: str = ""


def run_nesting(component_id: str) -> NestingResult:
    """Drive a component's friction parameter to its declared limit.

    Two things are checked, not one: that the response converges to the value produced
    by the composition WITHOUT the component, and that it converges at the rate implied
    analytically where the component states one. Convergence alone is satisfied by a
    block with a sign error whose effect happens to vanish in the limit; the rate is not.
    """
    from .golden import evaluate_expression
    from .lre import irf

    component = load_component(component_id)
    nt = component.get("nesting_target")
    if nt is None:
        return NestingResult(component_id, False, message="no nesting_target declared")
    if nt.get("pathological"):
        return NestingResult(component_id, True,
                             message="pathological limit, documented rather than tested")

    probe = nt["probe"]
    period = probe.get("period", 0)
    recovers = list(nt["recovers"])
    without = Composition(recovers[0], recovers[1:])

    # The composition WITH the component: the recovering composition plus this one.
    with_block = Composition(recovers[0], recovers[1:] + [component_id])

    def response(comp, overrides):
        P, Q, params = comp.solve(overrides)
        path = irf(P, Q, comp.shock_index(probe["shock"]), period + 1)
        return float(path[period, comp.index(probe["variable"])]), params

    limit_value, _ = response(without, None)
    responses, ratios, params_last = [], [], None
    for value in probe["sequence"]:
        r, params_last = response(with_block, {nt["parameter"]: float(value)})
        responses.append(r)
        ratios.append((r - limit_value) / float(value))

    monotone = all(
        abs(responses[k + 1] - limit_value) < abs(responses[k] - limit_value)
        for k in range(len(responses) - 1)
    )
    reached = abs(responses[-1] - limit_value)
    tol = float(nt["tolerance"])
    if not monotone:
        return NestingResult(component_id, False, limit_value, responses,
                             message=f"convergence towards the limit is not monotone: {responses}")
    if reached >= tol:
        return NestingResult(component_id, False, limit_value, responses,
                             message=(f"did not reach the limit: |{responses[-1]:.6g} - "
                                      f"{limit_value:.6g}| = {reached:.3e} >= {tol:.3e}"))
    if not nt.get("rate"):
        return NestingResult(component_id, True, limit_value, responses,
                             message="converged; no analytic rate declared")
    expected = evaluate_expression(nt["rate"], params_last)
    observed = ratios[-1]
    if not np.isclose(observed, expected, rtol=1e-3, atol=0.0):
        return NestingResult(component_id, False, limit_value, responses, expected, observed,
                             message=(f"converges, but at the wrong rate: observed "
                                      f"{observed:.6f}, expected {expected:.6f}"))
    return NestingResult(component_id, True, limit_value, responses, expected, observed)
