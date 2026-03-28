"""
01 — LP bound V(N) = 35.5/N^2 (Paper E, Section 3)

Solves the LP for small grid sizes and verifies the 1/N^2 scaling law.
For large N (>64), use the Lightning script lp_gap_c_lightningv2.py
in the main repo.

Run from repo root: python src/01_lp_bound.py
"""
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import det as la_det
import time

def sinc_kernel(x, y):
    d = x - y
    if abs(d) < 1e-14:
        return 1.0
    return np.sin(np.pi * d) / (np.pi * d)

def det3_sinc(v1, v2):
    """det3[sinc] at positions (0, v1, v2)."""
    M = np.array([
        [1.0, sinc_kernel(0, v1), sinc_kernel(0, v2)],
        [sinc_kernel(v1, 0), 1.0, sinc_kernel(v1, v2)],
        [sinc_kernel(v2, 0), sinc_kernel(v2, v1), 1.0]
    ])
    return np.linalg.det(M)

def solve_lp(N, v_max=2.5, tlimit=300):
    """Solve the 2D LP for grid size N.
    Returns V(N) = max |<phi, h>| subject to RS + positivity + marginalization."""
    dv = v_max / N
    v = np.arange(1, N+1) * dv

    # Build basis: pairs (v1, v2) with v1 < v2 and det3 > threshold
    pairs = []
    for i, v1 in enumerate(v):
        for j, v2 in enumerate(v):
            if v1 < v2:
                d3 = det3_sinc(v1, v2)
                if d3 > 0.01:
                    pairs.append((v1, v2, d3))

    n_basis = len(pairs)
    if n_basis == 0:
        return None, 0

    # Objective: maximize sum r(v1,v2) * h(v1,v2) * dv^2
    c_obj = np.zeros(n_basis)
    for k, (v1, v2, d3) in enumerate(pairs):
        s1 = min(v1, v2 - v1) if v2 > v1 else v1
        s2 = abs(v2 - v1) if v2 > v1 else v1
        s_min, s_max = min(s1, s2), max(s1, s2)
        r_val = s_min / s_max if s_max > 0 else 0
        c_obj[k] = r_val * dv**2

    # Positivity: h_k >= -det3_k
    bounds = [(-pairs[k][2], None) for k in range(n_basis)]

    # Marginalization: sum_j h(v_i, v_j) * dv = 0 for each v_i
    v_unique = sorted(set(p[0] for p in pairs) | set(p[1] for p in pairs))
    A_eq_rows = []
    for vi in v_unique:
        row = np.zeros(n_basis)
        for k, (v1, v2, d3) in enumerate(pairs):
            if abs(v1 - vi) < 1e-10 or abs(v2 - vi) < 1e-10:
                row[k] = dv
        if np.any(row != 0):
            A_eq_rows.append(row)

    A_eq = np.array(A_eq_rows) if A_eq_rows else None
    b_eq = np.zeros(len(A_eq_rows)) if A_eq_rows else None

    # Solve max
    res = linprog(-c_obj, bounds=bounds, A_eq=A_eq, b_eq=b_eq,
                  method='highs-ipm', options={'time_limit': tlimit})

    V = -res.fun if res.success else None
    return V, n_basis

# --- Run for small N values ---
print("=== LP bound V(N) ===")
print(f"{'N':>5s} {'V(N)':>12s} {'V*N^2':>10s} {'n_basis':>8s} {'time':>8s}")
print("-" * 48)

Ns_done = []
Vs_done = []

for N in [8, 12, 16, 20, 24, 32, 40, 48]:
    t0 = time.time()
    V, nb = solve_lp(N, tlimit=120)
    dt = time.time() - t0
    if V is not None:
        Ns_done.append(N)
        Vs_done.append(V)
        print(f"{N:5d} {V:12.6f} {V*N**2:10.2f} {nb:8d} {dt:7.1f}s")
    else:
        print(f"{N:5d} {'failed':>12s} {'---':>10s} {nb:8d} {dt:7.1f}s")

# --- Full results (precomputed) ---
print("\n=== Full results (20 points, precomputed) ===")
Ns_full = [20,24,28,32,36,40,44,48,52,56,60,64,72,80,88,96,104,112,120,128]
Vs_full = [0.076240,0.058360,0.043950,0.034113,0.027188,0.022158,
           0.018358,0.015426,0.013153,0.011318,0.009858,0.008671,
           0.006853,0.005551,0.004591,0.003860,0.003291,0.002839,
           0.002473,0.002175]

Ns_full = np.array(Ns_full)
Vs_full = np.array(Vs_full)
VN2 = Vs_full * Ns_full**2
mask = Ns_full >= 32
C = np.mean(VN2[mask])

print(f"V*N^2 = {C:.2f} +/- {np.std(VN2[mask]):.2f} (CV = {np.std(VN2[mask])/C*100:.1f}%)")

logN = np.log(Ns_full[mask])
logV = np.log(Vs_full[mask])
alpha, logA = np.polyfit(logN, logV, 1)
print(f"Power law: V = {np.exp(logA):.2f} / N^{-alpha:.3f}")

V_pred = C / Ns_full[mask]**2
R2 = 1 - np.sum((Vs_full[mask] - V_pred)**2) / np.sum((Vs_full[mask] - Vs_full[mask].mean())**2)
print(f"R^2 = {R2:.6f}")
