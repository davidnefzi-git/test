"""What can be checked mechanically about the library as a body of knowledge.

The composition engine already establishes that a model closes, that no variable is
provided twice and that no equation is replaced twice. Those are conditions on the
SOLVER. This file checks conditions on the KNOWLEDGE: that a declared interface matches
the equations beside it, that every equation says what it is with respect to its source,
that a derivation pointer resolves, that an assumption is attached to an equation that
exists, and that one symbol does not name two economic objects.

Each test here corresponds to a defect found by auditing the files rather than to a
defect imagined. The docstrings say which.

What these tests deliberately do NOT do is certify economics. No test here establishes
that a Phillips curve is Galli's, that two blocks are theoretically compatible, or that a
derivation is correct. Those require mathematics and reading, and the library's answer to
them is the `status` field, the theory documents and the `open_questions` -- not a green
tick.
"""
import re
from pathlib import Path

import pytest
import yaml

from modellib.compose import component_dirs, load_component, variable_namespace

ROOT = Path(__file__).resolve().parent.parent
DIRS = sorted(component_dirs())
COMPS = {d.name: load_component(d.name) for d in DIRS}
NS = variable_namespace()
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
CALLS = {"log", "exp", "sqrt"}

PARAM_OWNER: dict[str, set[str]] = {}
for _cid, _c in COMPS.items():
    for _p in _c.get("parameters") or []:
        PARAM_OWNER.setdefault(_p["name"], set()).add(_cid)
SHOCK_OWNER: dict[str, set[str]] = {}
for _cid, _c in COMPS.items():
    for _s in _c.get("shocks") or []:
        SHOCK_OWNER.setdefault(_s["id"], set()).add(_cid)

MODELS = {d.name: yaml.safe_load((d / "manifest.yaml").read_text())
          for d in sorted((ROOT / "models").iterdir())
          if (d / "manifest.yaml").exists()}
FAMILIES = yaml.safe_load((ROOT / "taxonomy" / "families.yaml").read_text())
MECHANISMS = yaml.safe_load((ROOT / "taxonomy" / "mechanisms.yaml").read_text())


def _tokens(comp):
    """Every identifier appearing in any of the component's equations."""
    out = set()
    for eq in comp["equations"]:
        out |= {t for t in IDENT.findall(eq["expr"]) if t not in CALLS}
    return out


def _shadow_names(comp):
    return {v + "_f" for v in (comp["variables"].get("requires_shadow") or [])}


# The origin of an equation is distinct from its verification against a source.
# A canonical status alone must never be read as a certified transcription.
SOURCE_CHECK_VALUES = {
    "verified_primary", "verified_working_paper", "pending", "standard_identity"
}

@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_every_equation_declares_primary_source_check(d):
    for eq in COMPS[d.name]["equations"]:
        assert eq.get("source_check") in SOURCE_CHECK_VALUES, (
            f"{d.name}.{eq['id']}: missing or invalid independent source-check status"
        )
        if eq["source_check"] in {"verified_primary", "verified_working_paper"}:
            assert eq.get("source"), f"{d.name}.{eq['id']}: no traceable source"

# ------------------------------------------------------------------ interfaces -------
@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_every_variable_used_is_declared(d):
    """The defect this check was written for.

    calvo-prices used `mc` and declared neither providing nor requiring it, while
    declaring `x`, which its equation no longer contained. Both halves matter. An
    undeclared requirement defeats the composition check, which verifies that what a
    component requires is provided: the block could be mounted on a core supplying no
    marginal cost and the error would surface only at matrix assembly. A stale
    requirement asserts a dependency the equations do not have.
    """
    c = COMPS[d.name]
    declared = (set(c["variables"].get("provides") or [])
                | set(c["variables"].get("requires") or [])
                | _shadow_names(c))
    used_vars = {t for t in _tokens(c) if t in NS} | (_tokens(c) & _shadow_names(c))
    undeclared = sorted(used_vars - declared)
    assert not undeclared, (
        f"{d.name}: {', '.join(undeclared)} appear in the equations but in neither "
        f"provides nor requires")


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_no_declared_requirement_is_unused(d):
    """The other half of the same defect: a requirement the equations do not have."""
    c = COMPS[d.name]
    used = _tokens(c)
    stale = sorted(v for v in (c["variables"].get("requires") or []) if v not in used)
    assert not stale, (
        f"{d.name}: {', '.join(stale)} are declared required and appear in no equation "
        f"of this component")


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_no_identifier_is_unresolved(d):
    """Every name in an equation is a taxonomy variable, a declared parameter, a
    declared shock, or a twin variable. Anything else is a typo that the solver would
    report much later and much less clearly."""
    c = COMPS[d.name]
    known = set(NS) | set(PARAM_OWNER) | set(SHOCK_OWNER) | _shadow_names(c)
    unresolved = sorted(_tokens(c) - known)
    assert not unresolved, f"{d.name}: unresolved identifiers {', '.join(unresolved)}"


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_every_parameter_used_is_reachable(d):
    """A component may use a parameter another declares, but the path has to exist.

    price-indexation uses beta_bar, gamma_g and kappa_p_inv, which core-nk-medium
    declares, and its depends_on names calvo-prices-kimball. The dependency is recorded
    only in compatible_cores -- which is why that field is now enforced by the assembler
    rather than being decorative metadata.
    """
    c = COMPS[d.name]
    own = {p["name"] for p in c.get("parameters") or []}
    reach = set(c.get("depends_on") or []) | set(c.get("compatible_cores") or []) | {d.name}
    used = {t for t in _tokens(c) if t in PARAM_OWNER}
    unreachable = sorted(p for p in used - own if not (PARAM_OWNER[p] & reach))
    assert not unreachable, (
        f"{d.name}: uses {', '.join(unreachable)}, declared by no component reachable "
        f"through depends_on or compatible_cores")


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_referenced_components_and_equations_exist(d):
    c = COMPS[d.name]
    for target in c.get("replaces") or []:
        owner, _, eqid = target.rpartition(".")
        assert owner in COMPS, f"{d.name}: replaces unknown component in '{target}'"
        assert eqid in {e["id"] for e in COMPS[owner]["equations"]}, \
            f"{d.name}: replaces '{target}', which that component does not define"
    for field in ("depends_on", "incompatible_with", "compatible_cores"):
        for other in c.get(field) or []:
            assert other in COMPS, f"{d.name}: {field} names unknown '{other}'"
    for core in c.get("compatible_cores") or []:
        assert COMPS[core]["kind"] == "core", \
            f"{d.name}: compatible_cores names '{core}', which is not a core"


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_incompatibility_is_reciprocal(d):
    """calvo-wages-kimball declared itself incompatible with calvo-wages and the
    declaration was one-sided. The assembler would still have refused the composition,
    for the right reason -- both provide the same variable -- while the metadata said
    nothing. A reader consulting only calvo-wages would have concluded the two compose.
    """
    c = COMPS[d.name]
    for other in c.get("incompatible_with") or []:
        back = COMPS[other].get("incompatible_with") or []
        assert d.name in back, (
            f"{d.name} declares itself incompatible with {other}, which does not "
            f"declare it in return")


def test_shared_parameter_symbols_are_registered():
    """phi_p named the fixed-cost share in core-nk-medium and the Rotemberg adjustment
    cost in rotemberg-prices: two unrelated objects, one symbol, defaults of 1.6 and
    372.79. The assembler refuses such a composition with 'parameter declared by two
    components', a message that reads like a bug rather than a name clash -- and a reader
    had no way to tell which object a given phi_p was.

    Comparing the components' free-text descriptions cannot decide whether two
    declarations mean the same thing: 'Discount factor' and 'Quarterly discount factor'
    differ as strings and not as objects. So the question is answered by declaration.
    taxonomy/parameters.yaml lists every symbol that more than one component may declare,
    with the meaning they share, and this test checks both directions.
    """
    registry = yaml.safe_load((ROOT / "taxonomy" / "parameters.yaml").read_text())
    multiple = {n: sorted(o) for n, o in PARAM_OWNER.items() if len(o) > 1}

    unregistered = sorted(set(multiple) - set(registry))
    assert not unregistered, (
        "declared by several components and absent from taxonomy/parameters.yaml: "
        + ", ".join(f"{n} ({', '.join(multiple[n])})" for n in unregistered))

    stale = sorted(set(registry) - set(multiple))
    assert not stale, (
        "listed in taxonomy/parameters.yaml and no longer declared by several "
        "components: " + ", ".join(stale))

    for name, entry in registry.items():
        assert entry.get("meaning"), f"{name}: the registry gives no shared meaning"
        listed = sorted(entry.get("declared_by") or [])
        assert listed == multiple[name], (
            f"{name}: the registry says {listed}, the components say {multiple[name]}")


# ------------------------------------------------------- scientific status -----------
@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_every_equation_declares_its_status(d):
    """The field exists so that a reader never has to infer, from prose, whether an
    equation is the publication's, a rearrangement of it, a deliberate departure from it,
    or unverified. Presenting an adaptation as an original equation is the error the
    field prevents."""
    for e in COMPS[d.name]["equations"]:
        assert e.get("status"), f"{d.name}.{e['id']} declares no status"


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_derived_and_adapted_equations_point_at_a_derivation(d):
    for e in COMPS[d.name]["equations"]:
        if e["status"] in ("derived", "adapted"):
            assert e.get("derivation"), (
                f"{d.name}.{e['id']} is '{e['status']}' and points at no derivation")


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_every_derivation_pointer_resolves(d):
    """A pointer is 'docs/theory/<file>.md#<anchor>' and the document declares the
    anchor in place, as a line reading **Anchor: `<name>`**. A derivation cannot then be
    renamed or deleted while a component still points at it.

    calvo-wages pointed at the Galí chapter-6 model specification for two of its equations. That
    document does not exist and never did in this tree.
    """
    for e in COMPS[d.name]["equations"]:
        ptr = e.get("derivation")
        if not ptr:
            continue
        path, _, anchor = ptr.partition("#")
        target = ROOT / path
        assert target.exists(), f"{d.name}.{e['id']}: '{path}' does not exist"
        assert anchor, f"{d.name}.{e['id']}: '{ptr}' names no anchor"
        declared = set(re.findall(r"\*\*Anchor: `([^`]+)`\.?\*\*", target.read_text()))
        assert anchor in declared, (
            f"{d.name}.{e['id']}: '{path}' declares no anchor '{anchor}' "
            f"(it declares {', '.join(sorted(declared))})")


# ------------------------------------------------------------- assumptions -----------
@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_every_component_declares_its_maintained_assumptions(d):
    """A composition check cannot establish that two blocks rest on the same view of the
    economy. Two components can agree on every variable name and still disagree about
    whether markets are complete, how expectations are formed, or what an asset return
    is. This field is where that disagreement is stated."""
    assert COMPS[d.name].get("assumptions"), \
        f"{d.name} declares no assumptions; see docs/composition/README.md section 2.2e"


@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_assumptions_are_attached_to_equations_that_exist(d):
    c = COMPS[d.name]
    known = {e["id"] for e in c["equations"]}
    seen = set()
    for a in c.get("assumptions") or []:
        assert a["id"] not in seen, f"{d.name}: assumption '{a['id']}' declared twice"
        seen.add(a["id"])
        bad = [e for e in a["embodied_in"] if e not in known]
        assert not bad, (
            f"{d.name}.{a['id']}: embodied_in names {', '.join(bad)}, which this "
            f"component does not define. An assumption embodied in no equation is "
            f"either not this component's or an equation that is missing.")


# ------------------------------------------------------- verification hygiene --------
@pytest.mark.parametrize("d", DIRS, ids=lambda d: d.name)
def test_open_questions_are_actually_open(d):
    """rotemberg-prices carried, in open_questions, an item prefixed RESOLVED, while its
    notes field said the same property was untested. A reader taking open_questions as a
    list of what remains open would have concluded that the component's central property
    was unestablished -- and taking notes at face value would have concluded it twice.

    Historical annotations belong in notes, where they can be read as history. The field
    reserved for unresolved questions holds unresolved questions.
    """
    for q in (COMPS[d.name].get("verification") or {}).get("open_questions") or []:
        assert not re.match(r"\s*(RESOLVED|RESOLU|DONE|FIXED)\b", str(q), re.I), (
            f"{d.name}: an item in open_questions is marked resolved: {str(q)[:70]}")


# ------------------------------------------------------------------ models -----------
@pytest.mark.parametrize("mid", sorted(MODELS), ids=lambda m: m)
def test_model_declares_its_family_vocabulary(mid):
    """A family declares common variables so that models can be compared. Declaring them
    and reporting none leaves the contract nominal. nk-gali-2015-ch3 mapped `inflationq`,
    `interest` and `outputgap` -- names in no family -- while the family's own names went
    unreported."""
    m = MODELS[mid]
    declared = set((FAMILIES.get(m.get("family")) or {}).get("common_variables") or {})
    mapped = set(m.get("common_variable_map") or {})
    outside = sorted(mapped - declared)
    assert not outside, (
        f"{mid}: common_variable_map uses {', '.join(outside)}, which the family "
        f"'{m.get('family')}' does not declare")
    assert mapped, (
        f"{mid}: reports none of the {len(declared)} common variables of family "
        f"'{m.get('family')}'")


@pytest.mark.parametrize("mid", sorted(MODELS), ids=lambda m: m)
def test_model_mechanism_tags_exist(mid):
    tags = ((MODELS[mid].get("economics") or {}).get("mechanisms")) or []
    bad = [t for t in tags if t not in MECHANISMS]
    assert not bad, f"{mid}: mechanisms not in taxonomy/mechanisms.yaml: {bad}"
    assert tags, f"{mid}: declares no mechanism, though taxonomy/mechanisms.yaml has " \
                 f"{len(MECHANISMS)} tags"


@pytest.mark.parametrize("mid", sorted(MODELS), ids=lambda m: m)
def test_model_carries_a_theory_document(mid):
    """Every canonical entry must include a substantive theoretical specification."""
    spec = ROOT / "models" / mid / "spec" / "model.md"
    assert spec.exists(), f"{mid}: no spec/model.md"
    assert len(spec.read_text()) > 2000, f"{mid}: spec/model.md is a stub"



def test_repository_exposes_contribution_and_model_documentation_policy():
    readme = (ROOT / "README.md").read_text()
    assert "CONTRIBUTING.md" in readme
    assert "docs/model-documentation-policy.md" in readme
    assert (ROOT / "CONTRIBUTING.md").exists()
    assert (ROOT / "docs" / "model-documentation-policy.md").exists()


@pytest.mark.parametrize("mid", sorted(MODELS), ids=lambda m: m)
def test_declared_estimation_resources_exist(mid):
    ref = MODELS[mid].get("estimation_reference")
    if not ref:
        return
    base = ROOT / "models" / mid
    assert (base / ref["specification"]).exists(), (
        f"{mid}: missing estimation specification {ref['specification']}"
    )
    assert (base / ref["interpretation"]).exists(), (
        f"{mid}: missing estimation interpretation {ref['interpretation']}"
    )


# -------------------------------------------------------- theory documents -----------
def test_theory_documents_are_indexed():
    index = (ROOT / "docs" / "theory" / "README.md").read_text()
    for f in sorted((ROOT / "docs" / "theory").glob("*.md")):
        if f.name == "README.md":
            continue
        assert f.name in index, f"docs/theory/{f.name} is not in the index"


# Sections of the theory documents that no single equation derives from, each because it
# documents context rather than a step. Listed here rather than attached artificially to
# an equation, because a pointer that does not correspond to a derivation is worse than
# an absent one.
CONTEXT_ANCHORS = {
    # kappa enters no equation: the library's Phillips curve is written in marginal cost.
    # The section explains why, and what kappa is retained for.
    "price-setting.md#output-gap-form",
    # The Kimball slope is used by calvo-prices-kimball, whose pointer goes to the
    # rearrangement that gives its equation its form. Both sections bear on that one
    # equation and a single pointer can name only one.
    "price-setting.md#kimball-slope",
    # Trend growth bears on every coefficient of the medium-scale family through derived
    # parameters, not on one equation.
    "consumption-and-capital.md#trend-growth",
    # The article-versus-replication differences bear on two equations in two components
    # and are reachable from the entry's verification notes and from its targets.
    "consumption-and-capital.md#article-versus-replication",
}


def test_every_theory_anchor_is_pointed_at_or_listed_as_context():
    """An anchor nothing points at is either a derivation no component uses, or a pointer
    that was renamed, or a context section. The first two are defects; the third is
    declared in CONTEXT_ANCHORS above, so that it is a decision and not an oversight."""
    pointed = set()
    for c in COMPS.values():
        for e in c["equations"]:
            if e.get("derivation"):
                pointed.add(e["derivation"].partition("#")[2])
    orphans = []
    for f in sorted((ROOT / "docs" / "theory").glob("*.md")):
        if f.name == "README.md":          # the index explains the convention, in prose
            continue
        for a in re.findall(r"\*\*Anchor: `([^`]+)`\.?\*\*", f.read_text()):
            if a not in pointed and f"{f.name}#{a}" not in CONTEXT_ANCHORS:
                orphans.append(f"{f.name}#{a}")
    assert not orphans, (
        "anchors no component points at and no context list covers: "
        + ", ".join(orphans))


# A prose reference to a file is a pointer like any other. The audit found seven broken
# ones, three introduced by this reorganisation (a test file renamed, a path relative to
# the wrong root) and four inherited from a tree where the target existed. None was
# caught by anything, because the convention was documentary rather than checked.
INTERNAL_REF = re.compile(
    r"(?:docs|models|components|tests|taxonomy|schema|modellib)"
    r"/[A-Za-z0-9_./-]+\.(?:md|yaml|py|json)")


def test_internal_file_references_resolve():
    """A reference to a file that does not exist sends a reader -- or a reasoning system
    reading this library -- to nothing. Checked over every document and every component,
    since the pointers in the YAML (`source`, `derivation`, notes) are the same kind of
    claim as the ones in the prose."""
    broken = []
    for f in sorted(list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.yaml"))):
        if ".git" in f.parts or "node_modules" in f.parts:
            continue
        for m in INTERNAL_REF.finditer(f.read_text()):
            if not (ROOT / m.group(0)).exists():
                broken.append(f"{f.relative_to(ROOT)} -> {m.group(0)}")
    assert not broken, "references to files that do not exist:\n  " + "\n  ".join(broken)
