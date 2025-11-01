#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ φ-spiral metric: full symbolic pack (SymPy)

Computes g, g^{-1}, Gamma, Riemann, Ricci, R, Einstein G, Kretschmann K
Optional calibration: phi(r) = sqrt(2GM/(r c^2))

© 2025 Carmen Wrede & Lino Casu
Based on Lino's compact symbolic specification
"""
import sympy as sp

# -----------------------------
# 0) Symbols & functions
# -----------------------------
T, r, th, ph = sp.symbols('T r theta phi_ang', real=True)
c, G, M = sp.symbols('c G M', positive=True)
phi = sp.Function('phi')(r)                 # φ(r)
gamma = sp.cosh(phi)                        # γ(r) = cosh φ
beta  = sp.tanh(phi)                        # β(r) = tanh φ

coords = (T, r, th, ph)
dim = 4

# -----------------------------
# 1) SSZ metric (diagonal 4D)
#     ds^2 = -c^2/gamma^2 dT^2 + gamma^2 dr^2 + r^2 dθ^2 + r^2 sin^2θ dϕ^2
# -----------------------------
g = sp.diag(-c**2/gamma**2, gamma**2, r**2, r**2*sp.sin(th)**2)
g_inv = sp.simplify(g.inv())

# -----------------------------
# 2) Christoffel symbols Γ^a_{bc} (Levi-Civita)
# -----------------------------
def christoffel(g, g_inv, coords):
    dim = len(coords)
    Gamma = [[ [sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c_ in range(dim):
                s = sp.S.Zero
                for d in range(dim):
                    s += g_inv[a,d]*(sp.diff(g[d,b], coords[c_])
                                     + sp.diff(g[d,c_], coords[b])
                                     - sp.diff(g[b,c_], coords[d]))
                Gamma[a][b][c_] = sp.simplify(sp.Rational(1,2)*s)
    return Gamma

Gamma = christoffel(g, g_inv, coords)

# Helpers for readability
def Gamma_comp(a,b,c_):  # returns Γ^a_{bc}
    return Gamma[a][b][c_]

# -----------------------------
# 3) Riemann, Ricci, scalar R
# -----------------------------
def riemann(Gamma, coords):
    dim = len(coords)
    Riem = [[[[sp.S.Zero for _ in range(dim)] for _ in range(dim)]
             for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c_ in range(dim):
                for d in range(dim):
                    term = sp.diff(Gamma[a][b][d], coords[c_]) - sp.diff(Gamma[a][b][c_], coords[d])
                    for e in range(dim):
                        term += Gamma[a][e][c_]*Gamma[e][b][d] - Gamma[a][e][d]*Gamma[e][b][c_]
                    Riem[a][b][c_][d] = sp.simplify(term)
    return Riem

print("Computing Riemann tensor (this may take a while)...")
Riem = riemann(Gamma, coords)
print("Riemann tensor computed!")

# Ricci: R_{bd} = R^a_{ bad}
Ricci = sp.Matrix([[sp.S.Zero for _ in range(dim)] for _ in range(dim)])
for b in range(dim):
    for d in range(dim):
        s = sp.S.Zero
        for a in range(dim):
            s += Riem[a][b][a][d]
        Ricci[b,d] = sp.simplify(s)

# Scalar curvature: R = g^{bd} R_{bd}
R_scalar = sp.simplify(sum(g_inv[b,d]*Ricci[b,d] for b in range(dim) for d in range(dim)))

# -----------------------------
# 4) Einstein tensor (mixed) G^μ_ν = g^{μλ} (R_{λν} - 1/2 g_{λν} R)
# -----------------------------
G_mixed = sp.Matrix([[sp.S.Zero for _ in range(dim)] for _ in range(dim)])
for mu in range(dim):
    for nu in range(dim):
        s = sp.S.Zero
        for lam in range(dim):
            s += g_inv[mu,lam]*(Ricci[lam,nu] - sp.Rational(1,2)*g[lam,nu]*R_scalar)
        G_mixed[mu,nu] = sp.simplify(s)

# -----------------------------
# 5) Kretschmann scalar K = R_{μνρσ} R^{μνρσ}
#    Contract using metric/inverse
# -----------------------------
def raise_index_Riemann(Riem, g_inv):
    """Compute R^{μν}{}_{ρσ} from R_{αβρσ} using g^{μα} g^{νβ}"""
    dim = g_inv.shape[0]
    R_upup_down = [[[[sp.S.Zero for _ in range(dim)] for _ in range(dim)]
                    for _ in range(dim)] for _ in range(dim)]
    for mu in range(dim):
        for nu in range(dim):
            for rho in range(dim):
                for sig in range(dim):
                    s = sp.S.Zero
                    for a in range(dim):
                        for b in range(dim):
                            s += g_inv[mu,a]*g_inv[nu,b]*Riem[a][b][rho][sig]
                    R_upup_down[mu][nu][rho][sig] = sp.simplify(s)
    return R_upup_down

print("Computing Kretschmann scalar (this may take a while)...")
R_upup_down = raise_index_Riemann(Riem, g_inv)

Kretschmann = sp.S.Zero
for mu in range(dim):
    for nu in range(dim):
        for rho in range(dim):
            for sig in range(dim):
                Kretschmann += R_upup_down[mu][nu][rho][sig]*Riem[mu][nu][rho][sig]
Kretschmann = sp.simplify(Kretschmann)
print("Kretschmann scalar computed!")

# -----------------------------
# 6) Optional calibration for φ(r)
#     phi(r) = sqrt(2 G M / (r c^2))
# -----------------------------
phi_cal = sp.sqrt(2*G*M/(r*c**2))

def calibrated(expr):
    """Return expr with phi and its r-derivatives substituted by the calibrated profile."""
    subs = {
        phi: phi_cal,
        sp.diff(phi, r): sp.diff(phi_cal, r),
        sp.diff(phi, r, 2): sp.diff(phi_cal, r, 2),
        sp.cosh(phi): sp.cosh(phi_cal),
        sp.sinh(phi): sp.sinh(phi_cal),
        gamma: sp.cosh(phi_cal),
        beta: sp.tanh(phi_cal)
    }
    return sp.simplify(sp.xreplace(expr, subs))

# -----------------------------
# 7) LaTeX export helpers
# -----------------------------
def latex_of(name, expr):
    print(f"\n--- {name} ---")
    print(sp.latex(sp.simplify(expr)))

def latex_matrix(name, M_):
    print(f"\n--- {name} ---")
    for i in range(M_.rows):
        row = [sp.latex(sp.simplify(M_[i,j])) for j in range(M_.cols)]
        print("  " + " & ".join(row))

# -----------------------------
# 8) Example usage (uncomment to print)
# -----------------------------
if __name__ == "__main__":
    print("\n" + "="*70)
    print("SSZ Symbolic Pack - Full Computation Complete")
    print("="*70)
    
    # Core tensors (general φ(r))
    latex_matrix("g_{\\mu\\nu}", g)
    latex_matrix("g^{\\mu\\nu}", g_inv)
    latex_matrix("Ricci\\ R_{\\mu\\nu}", Ricci)
    latex_of("Scalar\\ R", R_scalar)
    latex_matrix("Einstein\\ G^\\mu{}_{\\nu}", G_mixed)
    latex_of("Kretschmann\\ K", Kretschmann)

    # Calibrated weak-field versions (φ^2 ≈ 2GM/(rc^2))
    print("\n" + "="*70)
    print("Calibrated Versions (phi = sqrt(2GM/(rc^2)))")
    print("="*70)
    latex_of("R\\ (calibrated)", calibrated(R_scalar))
    latex_of("K\\ (calibrated)", calibrated(Kretschmann))
    
    print("\n" + "="*70)
    print("All tensors computed and ready for LaTeX export")
    print("="*70)
