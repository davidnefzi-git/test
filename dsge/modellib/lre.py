"""First-order solution of a linear rational-expectations model.

The composed model is written

    A2 E_t y_{t+1} + A0 y_t + A1 y_{t-1} + B eps_t = 0

and the solution sought is the stable recursive law of motion

    y_t = P y_{t-1} + Q eps_t .

Substituting gives A2 P^2 + A0 P + A1 = 0 and (A2 P + A0) Q + B = 0, and P is obtained
by iterating P <- -(A2 P + A0)^{-1} A1 from P = 0. The iteration converges to the stable
solution for a determinate model; non-convergence is reported rather than papered over,
because a silently wrong P is the worst possible outcome for a library whose purpose is
verified numbers.
"""
from __future__ import annotations

import numpy as np


class SolutionError(RuntimeError):
    pass


def solve(A2: np.ndarray, A0: np.ndarray, A1: np.ndarray, B: np.ndarray,
          tol: float = 1e-14, maxit: int = 20000) -> tuple[np.ndarray, np.ndarray]:
    n = A0.shape[0]
    P = np.zeros((n, n))
    for it in range(maxit):
        M = A2 @ P + A0
        if np.linalg.cond(M) > 1e14:
            raise SolutionError(
                f"singular coefficient matrix at iteration {it}: the composition is "
                "indeterminate or badly scaled"
            )
        P_new = -np.linalg.solve(M, A1)
        gap = np.max(np.abs(P_new - P))
        P = P_new
        if gap < tol:
            break
    else:
        raise SolutionError(
            f"the policy function did not converge in {maxit} iterations "
            f"(last change {gap:.3e}); check the Taylor principle and the calibration"
        )
    if np.max(np.abs(np.linalg.eigvals(P))) > 1 + 1e-8:
        raise SolutionError("the solution found is not stable: spectral radius of P exceeds one")
    Q = -np.linalg.solve(A2 @ P + A0, B)
    return P, Q


def irf(P: np.ndarray, Q: np.ndarray, shock_index: int, horizon: int,
        size: float = 1.0) -> np.ndarray:
    """Impulse responses, horizon x n_variables. Row 0 is the impact period."""
    n = P.shape[0]
    out = np.zeros((horizon, n))
    e = np.zeros(Q.shape[1])
    e[shock_index] = size
    y = Q @ e
    for h in range(horizon):
        out[h] = y
        y = P @ y
    return out
