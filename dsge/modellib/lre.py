"""First-order solution of a linear rational-expectations model.

The composed model is written

    A2 E_t y_{t+1} + A0 y_t + A1 y_{t-1} + B eps_t = 0

and the solution sought is the stable recursive law of motion

    y_t = P y_{t-1} + Q eps_t ,

so P must satisfy the quadratic matrix equation

    A2 P^2 + A0 P + A1 = 0 ,        then   (A2 P + A0) Q + B = 0 .

Method, in two stages. The STABLE root is selected by a generalized Schur (QZ)
decomposition of the companion pencil, which is what makes the Blanchard-Kahn condition
checkable and reports its two failures separately. Newton's method on the quadratic then
polishes that root to machine precision, each step a Sylvester equation solved in
Kronecker form.

The history is worth keeping, because each stage was forced by a failure rather than
chosen in advance. A fixed-point iteration alone stalled at a residual of 2e-9 on the
flexible-wage limit of ehl-2000, a calibration it had previously solved, once two
definitional equations were added; Newton fixed that. Newton alone then returned a root
with spectral radius 1.07 for Hansen (1985) and called it a solution, because iteration
selects whichever root its starting point falls towards and a model with endogenous
capital is a saddle-path problem. Selecting the root is the QZ's job; refining it is
Newton's.

Either way the result is checked and failure is reported rather than returned. A
plausible wrong solution is the one outcome a library of verified numbers cannot
tolerate.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import ordqz


class SolutionError(RuntimeError):
    pass


def _residual(A2: np.ndarray, A0: np.ndarray, A1: np.ndarray, P: np.ndarray) -> np.ndarray:
    return A2 @ P @ P + A0 @ P + A1


def _qz_root(A2: np.ndarray, A0: np.ndarray, A1: np.ndarray) -> np.ndarray:
    """The stable root of the matrix quadratic, by generalized Schur decomposition.

    Stack the model into the companion pencil in xi_t = [y_t; y_{t-1}]:

        F E_t[xi_{t+1}] = G xi_t ,
        F = [[A2, 0], [0, I]] ,     G = [[-A0, -A1], [I, 0]] .

    Order the generalized eigenvalues of (G, F) so that those inside the unit circle
    come first; the first m columns of Z then span the stable deflating subspace. A
    bounded path must stay in it, so with xi_t = Z1 v_t and Z1 split into its top and
    bottom blocks, y_t = Z1_top v_t and y_{t-1} = Z1_bot v_t, whence

        P = Z1_top @ inv(Z1_bot) .

    Uniqueness requires exactly n stable eigenvalues: that is the Blanchard-Kahn
    condition, and both failures of it are reported with the count, because "too few"
    (explosive) and "too many" (indeterminate) are different diagnoses for the author.

    This replaces selecting the root by iteration. Iteration converges to whichever root
    its starting point falls towards, which for a model whose only state is an exogenous
    shock is usually the stable one and for a model with endogenous capital is usually
    not. Hansen (1985) is the case that forced the change: the iterative method returned
    a root with spectral radius 1.07 and called it a solution.
    """
    n = A0.shape[0]
    zero, eye = np.zeros((n, n)), np.eye(n)
    F = np.block([[A2, zero], [zero, eye]])
    G = np.block([[-A0, -A1], [eye, zero]])
    # A UNIT root counts as stable. An interest rate rule in inflation pins the
    # inflation rate and not the price level, so gali-monacelli-2005 has one by
    # construction and its solution is perfectly bounded. Sorting strictly inside the
    # unit circle would declare that model to have no solution.
    unit_tol = 1e-9
    S, T, alpha, beta_, _, Z = ordqz(
        G, F, sort=lambda a, b: np.abs(a) <= np.abs(b) * (1 + unit_tol), output="real"
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        modulus = np.where(np.abs(beta_) > 1e-12, np.abs(alpha) / np.abs(beta_), np.inf)
    n_stable = int(np.sum(modulus <= 1 + unit_tol))
    if n_stable != n:
        verdict = ("too few stable roots: the model has no bounded solution"
                   if n_stable < n else
                   "too many stable roots: the model is indeterminate")
        raise SolutionError(
            f"Blanchard-Kahn condition fails ({verdict}): {n_stable} stable "
            f"generalized eigenvalues for {n} variables"
        )

    Z1 = Z[:, :n]
    Z1_top, Z1_bot = Z1[:n, :], Z1[n:, :]
    if np.linalg.cond(Z1_bot) > 1e12:
        raise SolutionError(
            "the stable subspace is not spanned by the lagged variables: the model's "
            "state space is degenerate, or variables are linearly dependent"
        )
    return np.real(Z1_top @ np.linalg.inv(Z1_bot))


def solve(A2: np.ndarray, A0: np.ndarray, A1: np.ndarray, B: np.ndarray,
          tol: float = 1e-13, maxit: int = 60
          ) -> tuple[np.ndarray, np.ndarray]:
    n = A0.shape[0]
    eye = np.eye(n)
    P = _qz_root(A2, A0, A1)

    # Newton polish: the QZ root is already the right one, this takes it to machine
    # precision, which the closed-form targets are tight enough to notice.
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
