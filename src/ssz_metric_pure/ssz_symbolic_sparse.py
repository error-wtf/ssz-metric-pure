#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ φ-spiral metric — Sparse Pack (symbolics + light validators)

Focus: g, g^{-1}, Gamma, Ricci, R, Einstein G
Plus: (∇g≈0) + energy conservation check

NO FULL RIEMANN, NO KRETSCHMANN - Perfect for CI/Unit-Tests

© 2025 Carmen Wrede & Lino Casu
Based on Lino's sparse pack specification
"""
import sympy as sp
import numpy as np

# -----------------------------
# Symbols & functions
# -----------------------------
T, r, th, ph = sp.symbols('T r theta phi_ang', real=True)
c, G, M = sp.symbols('c G M', positive=True)
phi = sp.Function('phi')(r)
gamma = sp.cosh(phi)        # γ(r)
beta  = sp.tanh(phi)        # β(r)

coords = (T, r, th, ph)
dim = 4

# -----------------------------
# Metric (diagonal 4D SSZ)
# ds^2 = -c^2/gamma^2 dT^2 + gamma^2 dr^2 + r^2 dθ^2 + r^2 sin^2θ dϕ^2
# -----------------------------
g = sp.diag(-c**2/gamma**2, gamma**2, r**2, r**2*sp.sin(th)**2)
g_inv = sp.simplify(g.inv())

# -----------------------------
# Christoffel Γ^a_{bc} (Levi-Civita)
# -----------------------------
def christoffel(g, g_inv, coords):
    dim = len(coords)
    Gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c_ in range(dim):
                s = sp.S.Zero
                for d in range(dim):
                    s += g_inv[a,d]*(sp.diff(g[d,b], coords[c_]) +
                                     sp.diff(g[d,c_], coords[b]) -
                                     sp.diff(g[b,c_], coords[d]))
                Gamma[a][b][c_] = sp.simplify(sp.Rational(1,2)*s)
    return Gamma

Gamma = christoffel(g, g_inv, coords)

# -----------------------------
# Ricci R_{μν}, scalar R, Einstein G^μ_ν
# -----------------------------
# Riemann contraction without forming full 4-index tensor:
dim = len(coords)
Ricci = sp.Matrix([[sp.S.Zero for _ in range(dim)] for _ in range(dim)])

for b in range(dim):
    for d in range(dim):
        # R_{bd} = ∂_a Γ^a_{bd} - ∂_d Γ^a_{ba} + Γ^a_{ae} Γ^e_{bd} - Γ^a_{de} Γ^e_{ba}
        term = sp.S.Zero
        for a in range(dim):
            term += sp.diff(Gamma[a][b][d], coords[a]) - sp.diff(Gamma[a][b][a], coords[d])
            for e in range(dim):
                term += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
        Ricci[b,d] = sp.simplify(term)

R_scalar = sp.simplify(sum(g_inv[b,d]*Ricci[b,d] for b in range(dim) for d in range(dim)))

G_mixed = sp.Matrix([[sp.S.Zero for _ in range(dim)] for _ in range(dim)])
for mu in range(dim):
    for nu in range(dim):
        s = sp.S.Zero
        for lam in range(dim):
            s += g_inv[mu,lam]*(Ricci[lam,nu] - sp.Rational(1,2)*g[lam,nu]*R_scalar)
        G_mixed[mu,nu] = sp.simplify(s)

# -----------------------------
# Weak-field calibration (optional): phi(r) = sqrt(2GM/(r c^2))
# -----------------------------
phi_cal = sp.sqrt(2*G*M/(r*c**2))

def calibrated(expr):
    subs = {
        phi: phi_cal,
        sp.diff(phi, r): sp.diff(phi_cal, r),
        sp.diff(phi, r, 2): sp.diff(phi_cal, r, 2),
        sp.cosh(phi): sp.cosh(phi_cal),
        sp.sinh(phi): sp.sinh(phi_cal),
        gamma: sp.cosh(phi_cal),
        beta: sp.tanh(phi_cal)
    }
    return sp.simplify(expr.xreplace(subs))

# -----------------------------
# Light validators
# -----------------------------
def validator_nabla_g_zero(max_r_samples=5, r_min=1.0, r_max=1e9, M_val=5.9722e24,
                           G_val=6.67430e-11, c_val=299792458.0, theta_val=sp.pi/3):
    """
    Numeric check: ||∇_α g_{μν}||_max ~ 0 using Γ and ∂g.
    Returns max absolute component over sampled radii.
    """
    # Build lambdified objects
    subs_phys = {G: G_val, M: M_val, c: c_val, th: float(theta_val)}
    # choose T, r, th, ph ordering: we only need r-derivative heavily; angular derivatives are analytic
    # construct ∇_r g_{μν} components
    nabla = []
    for mu in range(dim):
        for nu in range(dim):
            # ∇_r g_{μν} = ∂_r g_{μν} - Γ^β_{rμ} g_{βν} - Γ^β_{rν} g_{μβ}
            dr_g = sp.diff(g[mu,nu], r)
            expr = dr_g
            for beta_idx in range(dim):
                expr -= Gamma[beta_idx][mu][1]*g[beta_idx,nu]  # 1 = index of r
                expr -= Gamma[beta_idx][nu][1]*g[mu,beta_idx]
            nabla.append(sp.simplify(expr))

    # Substitute calibrated phi and physical constants
    nabla_cal = [calibrated(e).subs(subs_phys) for e in nabla]
    f = [sp.lambdify(r, e, 'numpy') for e in nabla_cal]

    rs = np.geomspace(r_min, r_max, max_r_samples)
    max_abs = 0.0
    for rv in rs:
        vals = [float(f_i(rv)) for f_i in f]
        max_abs = max(max_abs, max(abs(v) for v in vals))
    return max_abs

def validator_energy_conservation(M_val=5.9722e24, G_val=6.67430e-11, c_val=299792458.0,
                                  r0=7e6, steps=5000, dlam=1e-3):
    """
    Timelike radial geodesic (2D sector): check E = const with diagonal (T,r) metric.
    Uses: ds^2 = -(c^2/gamma^2)dT^2 + gamma^2 dr^2, E = (c^2/gamma^2) dT/dλ
    Evolves with simple ODEs from first integrals.
    """
    # Build numeric gamma(r)
    gam_expr = sp.cosh(phi_cal).subs({G:G_val, M:M_val, c:c_val})
    gam = sp.lambdify(r, gam_expr, 'numpy')

    # Choose E/c as slightly > c/gamma(r0) to move outward
    g0 = float(gam(r0))
    E = c_val**2 * 1.01 / g0  # small kinetic headroom

    r_vals = np.empty(steps); T_vals = np.empty(steps); lam_vals = np.empty(steps)
    r_vals[0] = r0; T_vals[0] = 0.0; lam_vals[0] = 0.0
    for i in range(1, steps):
        g = gam(r_vals[i-1])
        Rrad = (E**2)/(c_val**2) - (c_val**2)/(g**2)
        if Rrad <= 0:
            r_vals = r_vals[:i]; T_vals = T_vals[:i]; lam_vals = lam_vals[:i]
            break
        dr_dlam = np.sqrt(Rrad)
        dT_dlam = (g**2 / c_val**2) * E
        r_vals[i]   = r_vals[i-1] + dlam * dr_dlam
        T_vals[i]   = T_vals[i-1] + dlam * dT_dlam
        lam_vals[i] = lam_vals[i-1] + dlam

    # Check energy along the path
    E_recon = []
    for i in range(len(r_vals)):
        g = gam(r_vals[i])
        # finite difference for dT/dλ
        if i == 0:
            dTdl = (T_vals[i+1]-T_vals[i])/(lam_vals[i+1]-lam_vals[i])
        else:
            dTdl = (T_vals[i]-T_vals[i-1])/(lam_vals[i]-lam_vals[i-1])
        E_i = (c_val**2/g**2) * dTdl
        E_recon.append(E_i)
    E_recon = np.array(E_recon)
    rel_drift = np.max(np.abs(E_recon - E))/E
    return rel_drift

# -----------------------------
# Quick self-test (optional)
# -----------------------------
if __name__ == "__main__":
    print("="*70)
    print("SSZ Symbolic Sparse Pack - Self Test")
    print("="*70)
    
    # Print compact analytic results
    print("\nR (scalar):")
    print(sp.simplify(R_scalar))
    
    print("\nEinstein G^mu_nu (mixed):")
    sp.pprint(G_mixed)

    # Run validators (Earth defaults)
    print("\n" + "="*70)
    print("VALIDATORS")
    print("="*70)
    
    print("\n1. Metric Compatibility: nabla g = 0")
    nabla_max = validator_nabla_g_zero(max_r_samples=5, r_min=6.4e6, r_max=6.4e9)
    print(f"   max|nabla_r g_{{mu nu}}| = {nabla_max:.3e} (should be ~0)")
    if nabla_max < 1e-10:
        print("   Status: PASS (< 1e-10)")
    else:
        print("   Status: WARNING (> 1e-10)")

    print("\n2. Energy Conservation: E = const along geodesic")
    e_drift = validator_energy_conservation(r0=7.0e6)
    print(f"   Energy conservation drift = {e_drift:.3e}")
    if e_drift < 1e-6:
        print("   Status: PASS (< 1e-6)")
    else:
        print("   Status: WARNING (> 1e-6)")
    
    print("\n" + "="*70)
    print("SSZ Symbolic Sparse Pack - Self Test Complete")
    print("="*70)
