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


# Memoised solutions, keyed by equations and parameters; see Composition.solve for why
# the equations are in the key. Process-local, so a mutation test in a fresh process
# never sees another process's entries.
_SOLVE_CACHE: dict[tuple, tuple] = {}


class CompositionError(ValueError):
    pass


@lru_cache
def _component_validator() -> Draft202012Validator:
    with open(COMPONENT_SCHEMA_PATH) as f:
        return Draft202012Validator(json.load(f))


class _NoDuplicateKeys(yaml.SafeLoader):
    """A loader that refuses a mapping with a repeated key.

    yaml.safe_load keeps the last of two identical keys and says nothing. The
    namespace had `q` declared twice -- Tobin's q and the real exchange rate -- and
    for several commits the first declaration simply did not exist. Nothing failed:
    every check downstream asks whether a name is in the namespace, and the name was,
    with the wrong meaning attached. A namespace whose entries can be silently
    dropped is not a shared commitment, so the file is refused instead.
    """

    def construct_mapping(self, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise CompositionError(
                    f"taxonomy/variables.yaml declares '{key}' twice. YAML would keep "
                    f"only the second, so one declaration would be silently discarded."
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


@lru_cache
def variable_namespace() -> dict[str, dict]:
    """taxonomy/variables.yaml: the namespace component equations are written in."""
    with open(TAXONOMY_DIR / "variables.yaml") as f:
        return yaml.load(f, Loader=_NoDuplicateKeys) or {}


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


def _rename_vars(expr: str, mapping: dict[str, str]) -> str:
    """Rename variables in an equation string, leaving parameters and calls alone.

    One pass over identifier tokens, so a rename can never apply twice and `y_star`
    cannot be mangled by a rule for `y`.
    """
    return re.sub(r"[A-Za-z_][A-Za-z0-9_]*",
                  lambda m: mapping.get(m.group(0), m.group(0)), expr)


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

    def __init__(self, core: str, blocks: list[str] | None = None,
                 shadow: dict[str, Any] | None = None):
        self.core_id = core
        self.block_ids = list(blocks or [])
        self.shadow_spec = shadow
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

        # First of all, because it is the most basic coherence condition: every
        # component must write its equations in the same form. A mixed composition's
        # other symptoms would send the author looking in the wrong place.
        forms = {cid: c.get("equation_form", "log-linear-deviations")
                 for cid, c in comps.items()}
        distinct = set(forms.values())
        if len(distinct) > 1:
            detail = "; ".join(f"'{cid}' is {f}" for cid, f in sorted(forms.items()))
            raise CompositionError(
                "a composition cannot mix equation forms: a variable would mean a "
                f"deviation in one equation and a level in another ({detail}). No "
                "equation count would catch it, which is why it is refused here."
            )
        self.equation_form = distinct.pop()

        for cid, c in comps.items():
            for dep in c.get("depends_on") or []:
                if dep not in comps:
                    raise CompositionError(
                        f"component '{cid}' declares depends_on '{dep}', which is not included"
                    )

        # `compatible_cores` was declarative until this check existed, and it was not
        # decorative: it is the only place several components record which core supplies
        # the parameters their equations use. price-indexation's beta_bar, gamma_g and
        # kappa_p_inv are declared by core-nk-medium and reachable from that component
        # ONLY through this field, since its depends_on names calvo-prices-kimball. A
        # field that carries a real dependency and is enforced nowhere is worse than an
        # absent one: it reads as a contract and is not.
        for cid, c in comps.items():
            allowed = c.get("compatible_cores") or []
            if allowed and self.core_id not in allowed:
                raise CompositionError(
                    f"component '{cid}' declares compatible_cores "
                    f"{', '.join(allowed)} and this composition's core is "
                    f"'{self.core_id}'. "
                    f"Either the component works with this core, in which case add it to "
                    f"compatible_cores, or it does not, in which case the composition is "
                    f"not well posed."
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

        # A flexible-price twin, if the model needs one. Merged here, before the two
        # closure checks below, so that the twin is held to the same conditions as the
        # host rather than to none.
        self.shadow = None
        if self.shadow_spec is not None:
            self._merge_shadow()

        for cid, c in comps.items():
            wanted = c["variables"].get("requires_shadow") or []
            if not wanted:
                continue
            if self.shadow is None:
                raise CompositionError(
                    f"component '{cid}' requires {', '.join(wanted)} from a "
                    f"flexible-price twin, and this composition declares no shadow"
                )
            suffix = self.shadow["suffix"]
            absent = [v for v in wanted if v + suffix not in self.shadow["variables"]]
            if absent:
                raise CompositionError(
                    f"component '{cid}' requires {', '.join(v + suffix for v in absent)} "
                    f"from the twin, which does not provide it; the twin provides "
                    f"{', '.join(self.shadow['variables'])}"
                )

        missing = []
        for cid, c in comps.items():
            for v in c["variables"]["requires"]:
                if v not in provider:
                    missing.append((cid, v))
        if missing:
            detail = "; ".join(f"'{c}' requires '{v}'" for c, v in missing)
            raise CompositionError(f"unprovided variables: {detail}")

        if len(self.equations) != len(self.variables):
            raise CompositionError(
                f"composition is not closed: {len(self.equations)} equations for "
                f"{len(self.variables)} endogenous variables "
                f"({', '.join(self.variables)})"
            )


    # ------------------------------------------------------------------ shadow --
    def _merge_shadow(self) -> None:
        """Add a flexible-price twin of this model, built from its own components.

        WHY A MECHANISM AND NOT TEN MORE EQUATIONS

        Smets-Wouters's policy rule responds to the output gap, and the gap's second
        term is the output of a parallel economy in which prices and wages are flexible.
        The reference implementation writes that economy out a second time: eleven more
        equations, eleven more variables, every coefficient repeated. Nothing links the
        two copies, so an author who corrects the sticky Euler equation and not its twin
        gets a model that still assembles, still solves, and whose output gap is now
        measured against the wrong benchmark. The error is invisible because the twin
        has no observable of its own -- it only shifts the gap.

        So the twin is not written. It is COMPOSED, from a subset of the host's own
        components, and the subset is the point: the flexible-price economy is this
        model with its nominal frictions removed, which means every equation the two
        economies share is stored exactly once. Correcting the Euler equation corrects
        both, necessarily.

        The spec has four fields:

          components  which of the host's components the twin is built from. Required to
                      be a SUBSET of the host's, which is what rules out drift.
          suffix      appended to each twin variable: y -> y_f.
          shared      variables the two economies hold in common rather than duplicate.
                      The exogenous processes: both economies are driven by the same
                      realised technology, not by two independent draws.
          drop        equations of the twin that the host already supplies -- the laws
                      of motion of the shared processes. Stated explicitly, by id, so
                      that a mistake shows up as a closure failure and not as a second
                      technology process quietly fighting the first.
        """
        spec = self.shadow_spec
        unknown = set(spec) - {"components", "suffix", "shared", "drop", "note"}
        if unknown:
            raise CompositionError(f"shadow: unknown field(s) {', '.join(sorted(unknown))}")
        sub_ids = list(spec.get("components") or [])
        if not sub_ids:
            raise CompositionError("shadow: 'components' is empty")
        outside = [cid for cid in sub_ids if cid not in self.components]
        if outside:
            raise CompositionError(
                f"shadow uses component(s) the host does not compose: {', '.join(outside)}. "
                f"A twin may only be built from the host's own components -- that is what "
                f"makes it the same model with blocks removed, rather than a second model "
                f"free to drift from it."
            )
        suffix = spec.get("suffix", "_f")
        if not re.fullmatch(r"_[a-z][a-z0-9_]*", suffix):
            raise CompositionError(f"shadow: suffix '{suffix}' must match _[a-z][a-z0-9_]*")

        sub_core = [cid for cid in sub_ids if self.components[cid].get("kind") == "core"]
        if len(sub_core) != 1:
            raise CompositionError(
                f"shadow: expected exactly one core among its components, found "
                f"{len(sub_core)}"
            )
        inner = Composition(sub_core[0], [c for c in sub_ids if c != sub_core[0]])

        shared = list(spec.get("shared") or [])
        unknown_shared = [v for v in shared if v not in inner.provider]
        if unknown_shared:
            raise CompositionError(
                f"shadow: shared variable(s) not in the twin: {', '.join(unknown_shared)}"
            )
        not_in_host = [v for v in shared if v not in self.provider]
        if not_in_host:
            raise CompositionError(
                f"shadow: shared variable(s) the host does not provide: "
                f"{', '.join(not_in_host)}"
            )

        drop = list(spec.get("drop") or [])
        inner_ids = [eid for eid, _ in inner.equations]
        unknown_drop = [e for e in drop if e not in inner_ids]
        if unknown_drop:
            raise CompositionError(
                f"shadow: drop names equation(s) the twin does not contain: "
                f"{', '.join(unknown_drop)} (it has {', '.join(inner_ids)})"
            )

        rename = {v: v + suffix for v in inner.variables if v not in shared}
        twin_vars = sorted(rename.values())
        clash = [v for v in twin_vars if v in self.provider]
        if clash:
            raise CompositionError(
                f"shadow: twin variable(s) collide with the host: {', '.join(clash)}"
            )

        twin_eqs = [(f"{suffix.lstrip('_')}:{eid}", _rename_vars(expr, rename))
                    for eid, expr in inner.equations if eid not in drop]

        for v in twin_vars:
            self.provider[v] = f"shadow({suffix})"
        self.variables = sorted(self.provider)
        self.equations = self.equations + twin_eqs
        self.shadow = {
            "composition": inner,
            "suffix": suffix,
            "shared": shared,
            "dropped": drop,
            "variables": twin_vars,
            "rename": rename,
        }

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

    # ------------------------------------------------------------ steady state --
    def steady_state(self, overrides: dict[str, float] | None = None) -> dict[str, float]:
        """The point about which the model is linearised.

        Zero for log-linear components, by construction. For components written in
        levels, built from the analytic expressions they declare and, for anything they
        leave out, by a numerical solve of the composition's own residual at
        y(+1) = y = y(-1) and zero shocks. Either way the result is verified against
        every equation before it is used: a steady state that does not satisfy the model
        is reported, never differentiated around.
        """
        params = self.parameters(overrides)
        if self.equation_form == "log-linear-deviations":
            return {v: 0.0 for v in self.variables}

        analytic: dict[str, str] = {}
        guess: dict[str, float] = {}
        tol = 1e-10
        for c in self.components.values():
            ss = c.get("steady_state") or {}
            analytic.update(ss.get("analytic") or {})
            guess.update(ss.get("guess") or {})
            if ss.get("tolerance"):
                tol = float(ss["tolerance"])

        unknown = set(analytic) | set(guess) - set(self.variables)
        unknown = (set(analytic) | set(guess)) - set(self.variables)
        if unknown:
            raise CompositionError(
                f"steady_state names variables the composition does not have: "
                f"{', '.join(sorted(unknown))}"
            )

        psyms = {n: sp.Symbol(n) for n in params}
        vsyms = {v: sp.Symbol(v) for v in self.variables}
        table = dict(psyms); table.update(vsyms)
        values: dict[str, float] = {}
        pending = dict(analytic)
        while pending:
            progressed = False
            for name, formula in list(pending.items()):
                e = sp.sympify(formula.replace("^", "**"), locals=table)
                e = e.subs({psyms[k]: v for k, v in params.items()})
                e = e.subs({vsyms[k]: v for k, v in values.items()})
                if e.free_symbols:
                    continue
                values[name] = float(e.evalf())
                pending.pop(name)
                progressed = True
            if not progressed:
                raise CompositionError(
                    f"cannot resolve the analytic steady state for: "
                    f"{', '.join(sorted(pending))}"
                )

        missing = [v for v in self.variables if v not in values]
        if missing:
            from scipy.optimize import root
            resid = self._residual_function(params)
            x0 = np.array([guess.get(v, 1.0) for v in missing])
            fixed = dict(values)

            def f(z):
                point = dict(fixed)
                point.update(dict(zip(missing, z)))
                return resid([point[v] for v in self.variables])

            sol = root(f, x0, method="hybr")
            if not sol.success:
                raise CompositionError(
                    f"the numerical steady state did not converge for "
                    f"{', '.join(missing)}: {sol.message}"
                )
            values.update(dict(zip(missing, sol.x)))

        resid = self._residual_function(params)
        r = np.max(np.abs(resid([values[v] for v in self.variables])))
        if r > tol:
            raise CompositionError(
                f"the declared steady state does not satisfy the model: worst residual "
                f"{r:.3e} exceeds {tol:.3e}. The dynamics would be linearised about a "
                f"point that is not an equilibrium."
            )
        return values

    def _steady_state_spec(self) -> tuple:
        """The components' declared steady states, as part of the solve cache's key."""
        return tuple(sorted((cid, repr(c.get("steady_state")))
                            for cid, c in self.components.items()))

    def _residual_function(self, params: dict[str, float]):
        """F(y, y, y, 0) as a callable, for the steady-state solve and its check."""
        v, sh = self.variables, self.shocks
        psyms = {n: sp.Symbol(n) for n in params}
        vsyms = {x: sp.Symbol(x) for x in v}
        table = dict(psyms); table.update(vsyms)
        exprs = []
        for eq_id, expr in self.equations:
            text = _subst(expr.replace("^", "**"), v, sh)
            for x in v:
                for suf in (LEAD, LAG, NOW):
                    text = text.replace(x + suf, x)
            for s_ in sh:
                text = text.replace(s_ + "_shock", "0")
            e = sp.sympify(text, locals=table).subs({psyms[k]: val for k, val in params.items()})
            exprs.append(e)
        f = sp.lambdify([[vsyms[x] for x in v]], exprs, "numpy")
        return lambda point: np.array(f(list(point)), dtype=float)

    # --------------------------------------------------------------- matrices --
    def matrices(self, overrides: dict[str, float] | None = None):
        params = self.parameters(overrides)
        levels = self.equation_form == "levels"
        ss = self.steady_state(overrides)
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
            e = sp.sympify(_subst(expr.replace("^", "**"), v, s), locals=table)
            e = e.subs({psyms[k]: val for k, val in params.items()})
            free = {str(x) for x in e.free_symbols} - set(syms)
            if free:
                raise CompositionError(
                    f"equation '{eq_id}' contains unresolved names: {', '.join(sorted(free))}"
                )
            # Evaluate the Jacobians AT the steady state. A log-linear component's
            # derivatives are already constants, so the substitution is skipped there:
            # that is what keeps every earlier component working, and fast.
            if levels:
                at_ss = {syms[name + suf]: ss[name]
                         for name in v for suf in (LEAD, NOW, LAG)}
                at_ss.update({syms[name + "_shock"]: 0.0 for name in s})
                take = lambda d: float(d.subs(at_ss))
            else:
                take = float
            for j, name in enumerate(v):
                A2[r, j] = take(sp.diff(e, syms[name + LEAD]))
                A0[r, j] = take(sp.diff(e, syms[name + NOW]))
                A1[r, j] = take(sp.diff(e, syms[name + LAG]))
            for j, name in enumerate(s):
                B[r, j] = take(sp.diff(e, syms[name + "_shock"]))
        return A2, A0, A1, B, params

    # ------------------------------------------------------------------ solve --
    def solve(self, overrides: dict[str, float] | None = None):
        """Solve, with the result memoised on the equations and the parameters.

        The solution is a pure function of those two things, and building the Jacobians
        means differentiating every equation symbolically, which is by far the most
        expensive step in the library. Nothing above this layer knew to avoid repeating
        it: the golden runner is handed one target at a time, so a model with
        twenty-four targets was differentiated twenty-four times, and the suite spent
        most of its time recomputing a matrix it already had.

        The key includes the EQUATIONS and not only the component ids, so that a
        mutation test -- which changes an equation while leaving the ids alone -- cannot
        be served a stale solution. It includes the declared STEADY STATE for the same
        reason, which is less obvious and was caught by an existing test: for a
        composition written in levels the Jacobians are evaluated at that point, so two
        compositions can share every equation and every parameter and still have
        different solutions -- or, in that test's case, one solution and one refusal.
        The returned arrays are made read-only, because a caller that wrote to them would
        otherwise corrupt every later hit.
        """
        params = self.parameters(overrides)
        key = (tuple(self.equations), tuple(self.shocks), self.equation_form,
               self._steady_state_spec(), tuple(sorted(params.items())))
        hit = _SOLVE_CACHE.get(key)
        if hit is not None:
            return hit
        from .lre import solve as _solve
        A2, A0, A1, B, params = self.matrices(overrides)
        P, Q = _solve(A2, A0, A1, B)
        P.flags.writeable = False
        Q.flags.writeable = False
        out = (P, Q, params)
        _SOLVE_CACHE[key] = out
        return out

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
        if self.shadow:
            sh = self.shadow
            lines.append(
                f"  flexible-price twin '{sh['suffix']}' from "
                f"{' + '.join(sh['composition'].ids)}"
            )
            lines.append(f"    shared with the host: {', '.join(sh['shared'])}")
            lines.append(f"    twin variables: {', '.join(sh['variables'])}")
        lines.append(f"  shocks: {', '.join(self.shocks)}")
        lines.append(f"  equation form: {self.equation_form}")
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

    # The composition WITH the component: the recovering composition, this one, and
    # any component that exists only BECAUSE this one does. Sticky prices are the case
    # that forces the field: remove them and there is no inflation, hence no Fisher
    # equation and no interest-rate rule either, so the two sides of the test cannot be
    # the same component list. Listing them is not a loosening -- the limit still has to
    # be the composition in `recovers`, which contains neither.
    with_also = list(nt.get("with_also") or [])
    overlap = [cid for cid in with_also if cid in recovers]
    if overlap:
        raise CompositionError(
            f"{component_id}: nesting_target.with_also lists {', '.join(overlap)}, which "
            f"is already in `recovers`; with_also is for components present only on the "
            f"with-block side"
        )
    with_block = Composition(recovers[0], recovers[1:] + [component_id] + with_also)

    def response(comp, overrides):
        P, Q, params = comp.solve(overrides)
        path = irf(P, Q, comp.shock_index(probe["shock"]), period + 1)
        return float(path[period, comp.index(probe["variable"])]), params

    limit_value, _ = response(without, None)
    responses, ratios, params_last = [], [], None
    for value in probe["sequence"]:
        r, params_last = response(with_block, {nt["parameter"]: float(value)})
        responses.append(r)
        # Divided by the DISTANCE to the limit, not by the parameter. The two coincide
        # whenever the limit is zero, which it was for every component until capital
        # utilisation, whose limit is psi = 1.
        ratios.append((r - limit_value) / (float(value) - float(nt["limit"])))

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
