"""CLI: python -m modellib describe|golden|irf"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        print("\n  describe <core> [block ...]   print the assembled model and its checks")
        print("  golden <model-id>             run the model's golden targets")
        print("  irf <core> [block ...]        print 8 quarters of responses to eps_v")
        return 0
    cmd, rest = argv[0], argv[1:]

    if cmd == "describe":
        from .compose import Composition
        print(Composition(rest[0], rest[1:]).describe())
        return 0

    if cmd == "golden":
        from .golden import run_golden
        model_dir = ROOT / "models" / rest[0]
        failed = 0
        for r in run_golden(model_dir):
            mark = "pass" if r.passed else "FAIL"
            exp = "-" if r.expected is None else f"{r.expected:.10g}"
            act = "-" if r.actual is None else f"{r.actual:.10g}"
            print(f"  [{mark}] {r.target_id:<48} {r.kind:<9} expected {exp:<16} got {act}")
            if r.message:
                print(f"         {r.message}")
            failed += not r.passed
        print(f"\n{failed} failing target(s)")
        return 1 if failed else 0

    if cmd == "irf":
        import numpy as np
        from .compose import Composition
        from .lre import irf as _irf
        c = Composition(rest[0], rest[1:])
        P, Q, _ = c.solve()
        path = _irf(P, Q, c.shock_index("eps_v"), 8)
        print("response to eps_v (one unit, contractionary)")
        print("  h  " + "".join(f"{v:>12}" for v in c.variables))
        for h, row in enumerate(path):
            print(f"  {h}  " + "".join(f"{x:>12.6f}" for x in row))
        return 0

    print(f"unknown command '{cmd}'")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
