"""First-order solution of a linear rational-expectations model.

The composed model is written

    A2 E_t y_{t+1} + A0 y_t + A1 y_{t-1} + B eps_t = 0

and the solution sought is the stable recursive law of motion

    y_t = P y_{t-1} + Q eps_t ,

so P must satisfy the quadratic matrix equation

    A2 P^2 + A0 P + A1 = 0 ,        then   (A2 P + A0) Q + B = 0 .

Method. The quadratic is solved by Newton's method, each step requiring one Sylvester
equation

    (A2 P + A0) dP + A2 dP P = -(A2 P^2 + A0 P + A1) ,

solved through its Kronecker form. A short fixed-point sweep,
P <- -(A2 P + A0)^{-1} A1, supplies the starting point, which selects the stable root.

Why not the fixed-point iteration alone, which an earlier version of this file used: it
converges linearly and its rate depends on the spectral properties of the system, so
adding two definitional equations to a model it handled was enough to stall it at a
residual of 2e-9 on a calibration it had solved before. Newton converges quadratically
and reaches machine precision on the same problems. The failure was not hypothetical:
it appeared on the flexible-wage limit of ehl-2000, a calibration the library needs.

Either way the result is checked and failure is reported rather than returned. A
plausible wrong solution is the one outcome a library of verified numbers cannot
tolerate.
"""
from __future__ import annotations

import numpy as np


class SolutionError(RuntimeError):
    pass


def _residual(A2: np.ndarray, A0: np.ndarray, A1: np.ndarray, P: np.ndarray) -> np.ndarray:
    return A2 @ P @ P + A0 @ P + A1


def solve(A2: np.ndarray, A0: np.ndarray, A1: np.ndarray, B: np.ndarray,
          tol: float = 1e-13, maxit: int = 60, sweep: int = 200
          ) -> tuple[np.ndarray, np.ndarray]:
    n = A0.shape[0]
    eye = np.eye(n)

    # Fixed-point sweep: cheap, and its iterates stay in the basin of the stable root.
    P = np.zeros((n, n))
    for _ in range(sweep):
        M = A2 @ P + A0
        if np.linalg.cond(M) > 1e14:
            break
        P_new = -np.linalg.solve(M, A1)
        if not np.all(np.isfinite(P_new)):
            break
        if np.max(np.abs(P_new - P)) < 1e-11:
            P = P_new
            break
        P = P_new

    # Newton on the matrix quadratic.
    best, best_norm = P.copy(), np.max(np.abs(_residual(A2, A0, A1, P)))
    for _ in range(maxit):
        R = _residual(A2, A0, A1, P)
        err = np.max(np.abs(R))
        if err < best_norm:
            best, best_norm = P.copy(), err
        if err < tol:
            break
        # (A2 P + A0) dP + A2 dP P = -R  ->  [I (x) (A2 P + A0) + P' (x) A2] vec(dP) = -vec(R)
        J = np.kron(eye, A2 @ P + A0) + np.kron(P.T, A2)
        if np.linalg.cond(J) > 1e15:
            break
        try:
            step = np.linalg.solve(J, -R.reshape(-1, order="F"))
        except np.linalg.LinAlgError:
            break
        P = P + step.reshape((n, n), order="F")
        if not np.all(np.isfinite(P)):
            P = best
            break
    else:
        R = _residual(A2, A0, A1, P)
        if np.max(np.abs(R)) < best_norm:
            best, best_norm = P.copy(), np.max(np.abs(R))

    P = best
    if best_norm > 1e-8:
        raise SolutionError(
            f"no solution to the matrix quadratic was found: residual {best_norm:.3e}. "
            "The composition may be indeterminate, or the calibration may violate the "
            "Taylor principle."
        )
    radius = float(np.max(np.abs(np.linalg.eigvals(P))))
    if radius > 1 + 1e-8:
        raise SolutionError(
            f"the solution found is not stable: spectral radius of P is {radius:.6f}. "
            "Check the Taylor principle and the calibration."
        )
    M = A2 @ P + A0
    if np.linalg.cond(M) > 1e14:
        raise SolutionError("A2 P + A0 is singular: the shock loading is not identified")
    Q = -np.linalg.solve(M, B)
    return P, Q


def irf(P: np.ndarray, Q: np.ndarray, shock_index: int, horizon: int,
        size: float = 1.0) -> np.ndarray:
    """Impulse responses, horizon x n_variables. Row 0 is the impact period."""
    out = np.zeros((horizon, P.shape[0]))
    e = np.zeros(Q.shape[1])
    e[shock_index] = size
    y = Q @ e
    for h in range(horizon):
        out[h] = y
        y = P @ y
    return out
