#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Geodesics - Compact Implementation
Pure numpy + matplotlib, no dependencies

Implements null and timelike geodesics for φ-Spiral SSZ metric
using the diagonal form.

© 2025 Carmen Wrede & Lino Casu
Based on Lino's compact geodesic solver
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# UTF-8 encoding for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

c = 299_792_458.0  # m/s

# -----------------------------
# 1) Spiral-/Gravitationsprofil φ_G(r)
#    --> hier frei variieren!
# -----------------------------
def phi_G(r, k=0.75, r0=1.0):
    """
    Gravitational rotation angle.
    
    Example: Smooth logarithmic growth (dimensionless)
    k: Spiral strength
    r0: Characteristic radius
    """
    return k * np.log1p(r / r0)

def beta(r):        # tanh φ
    x = phi_G(r)
    return np.tanh(x)

def gamma(r):       # cosh φ
    x = phi_G(r)
    return np.cosh(x)

def sech2(r):       # sech^2 φ = 1/cosh^2 φ
    g = gamma(r)
    return 1.0 / (g * g)

# ---------------------------------------------
# 2) Koordinatenwechsel: (t,r) <-> (T,r)
#    dT = dt - (β γ^2 / c) dr
# ---------------------------------------------
def t_from_T_path(T, r, sign_dt_dr=+1):
    """
    Reconstructs t(s) from T(s), r(s) along a trajectory.
    
    Formula: dt = dT + (β γ^2 / c) dr
    
    Args:
        T: Array of T coordinates
        r: Array of r coordinates
        sign_dt_dr: +1 for forward, -1 for backward
    
    Returns:
        t: Reconstructed coordinate time
    """
    # dt = dT + (β γ^2 / c) dr
    dT = np.gradient(T)
    dr = np.gradient(r)
    corr = (beta(r) * gamma(r)**2 / c) * dr
    t = np.cumsum(dT + corr)
    # Normalization: t(0) = T(0), pure convention:
    t = t - t[0] + T[0]
    return t

# ---------------------------------------------
# 3) Nullgeodäten (ds^2 = 0):
#    dr/dT = ± c * sech^2 φ_G(r) = ± c / γ^2
#    ==> T(r) = ± (1/c) ∫ γ^2(r) dr
# ---------------------------------------------
def null_geodesic(r_start, r_end, n=2000, sign=+1):
    """
    Null geodesic (photon) in diagonal form.
    
    Formula: dr/dT = ±c/γ²(r) = ±c·sech²(φ_G)
    
    Args:
        r_start: Starting radius
        r_end: Ending radius
        n: Number of points
        sign: +1 for outgoing, -1 for infalling
    
    Returns:
        r: Radius array
        T: Eigentime coordinate array
    """
    r = np.linspace(r_start, r_end, n)
    g2 = gamma(r)**2
    
    # Numerical quadrature (trapezoidal):
    T = sign * (1.0 / c) * np.cumsum((g2[:-1] + g2[1:]) / 2.0 * np.diff(r))
    T = np.concatenate(([0.0], T))
    
    # Set to absolute zero point:
    T = T - T[0]
    return r, T

# ------------------------------------------------
# 4) Timelike-Geodäten (g_{μν}\dot x^μ \dot x^ν = -c^2):
#    First integrals:
#      E = (c^2/γ^2) dT/dλ  (constant)
#      (dr/dλ)^2 = E^2/c^2 - c^2/γ^2(r)
# ------------------------------------------------
def timelike_geodesic(r0, E_over_c=None, dlam=1e-3, steps=20000, sign=+1):
    """
    Timelike geodesic (massive particle) in diagonal form.
    
    Formula: (dr/dλ)² = E²/c² - c²/γ²(r)
    
    Args:
        r0: Starting radius
        E_over_c: E/c (dimensions: speed); default ~ c for 'free radial motion'
        dlam: Step size in proper time λ
        steps: Maximum number of steps
        sign: +1 outward, -1 inward
    
    Returns:
        lam: Proper time array
        r: Radius array
        T: Eigentime coordinate array
    """
    if E_over_c is None:
        E_over_c = c
    
    r = np.empty(steps)
    T = np.empty(steps)
    lam = np.empty(steps)
    r[0] = r0
    T[0] = 0.0
    lam[0] = 0.0

    for i in range(1, steps):
        g = gamma(r[i-1])
        
        # Radicand:
        R = (E_over_c**2) - (c**2) / (g**2)
        
        if R <= 0:
            # Turning point reached
            r = r[:i]
            T = T[:i]
            lam = lam[:i]
            break
        
        dr_dlam = sign * np.sqrt(R)
        dT_dlam = (g**2 / c**2) * (E_over_c * c)  # = γ^2 * E / c^2
        
        # Euler step (RK4 optional)
        r[i]   = r[i-1] + dlam * dr_dlam
        T[i]   = T[i-1] + dlam * dT_dlam
        lam[i] = lam[i-1] + dlam

    return lam, r, T

# ---------------------------------------------
# 5) Light Cone Closing Analysis
# ---------------------------------------------
def light_cone_closing(r_array):
    """
    Compute light cone closing as function of radius.
    
    Returns:
        r_array: Input radius array
        dr_dT: Light speed dr/dT in units of c
        closing_pct: Percentage of closing
    """
    dr_dT = sech2(r_array)  # Already in units of c
    closing_pct = (1.0 - dr_dT) * 100.0
    
    return r_array, dr_dT, closing_pct

# ---------------------------------------------
# 6) Effective Potential
# ---------------------------------------------
def effective_potential(r_array):
    """
    Effective potential V_eff(r) = c²/γ²(r) for timelike geodesics.
    
    Returns:
        r_array: Input radius array
        V_eff: Effective potential [m²/s²]
    """
    g2 = gamma(r_array)**2
    V_eff = (c ** 2) / g2
    
    return r_array, V_eff

# -----------------------------
# 7) DEMO / PLOTS
# -----------------------------
def demo_geodesics():
    """Run complete geodesic demonstration."""
    print("\n" + "="*80)
    print("SSZ GEODESICS - Compact Demo")
    print("="*80)
    
    # Setup
    k_val = 1.0
    r0_val = 1.0
    
    print(f"\nConfiguration:")
    print(f"  φ_G(r) = {k_val} * log(1 + r/{r0_val})")
    print(f"  γ(r) = cosh(φ_G)")
    print(f"  β(r) = tanh(φ_G)")
    
    # Nullgeodäten (purely radial, forward and backward)
    r_null, T_null_out = null_geodesic(0.0, 20.0, n=3000, sign=+1)
    r_null2, T_null_in = null_geodesic(20.0, 0.0, n=3000, sign=-1)
    
    print(f"\nNull geodesics computed:")
    print(f"  Outgoing: r = 0 → 20 (3000 points)")
    print(f"  Infalling: r = 20 → 0 (3000 points)")

    # Timelike (Example): Start at r0=2, E/c ~ 0.9 c -> subluminal
    lam, r_tim, T_tim = timelike_geodesic(
        r0=2.0, 
        E_over_c=0.9*c, 
        dlam=2e-4, 
        steps=20000, 
        sign=+1
    )
    
    print(f"\nTimelike geodesic computed:")
    print(f"  Start: r0 = 2.0")
    print(f"  Energy: E/c = 0.9c")
    print(f"  Steps: {len(lam)}")
    print(f"  Final radius: r = {r_tim[-1]:.3f}")
    
    # t(T,r)-coordinate reconstruction (optional):
    t_tim = t_from_T_path(T_tim, r_tim)
    
    print(f"\nCoordinate time t reconstructed from T")

    # Light cone closing
    r_cone = np.linspace(0.1, 20.0, 200)
    _, dr_dT, closing = light_cone_closing(r_cone)
    
    print(f"\nLight cone closing:")
    print(f"  At r = 1.0: {closing[np.argmin(np.abs(r_cone - 1.0))]:.1f}%")
    print(f"  At r = 5.0: {closing[np.argmin(np.abs(r_cone - 5.0))]:.1f}%")
    print(f"  At r = 10.0: {closing[np.argmin(np.abs(r_cone - 10.0))]:.1f}%")

    # ---- Plots ----
    fig, axs = plt.subplots(2, 3, figsize=(15, 9))

    # (a) Nullgeodäten T(r)
    axs[0, 0].plot(r_null, T_null_out, label="null (out)", lw=2)
    axs[0, 0].plot(r_null2, T_null_in, label="null (in)", lw=2, ls='--')
    axs[0, 0].set_xlabel("r [units]")
    axs[0, 0].set_ylabel("T [s]")
    axs[0, 0].set_title("Null Geodesics: T(r)")
    axs[0, 0].legend()
    axs[0, 0].grid(True, alpha=0.3)

    # (b) Timelike: r(λ), T(λ)
    axs[0, 1].plot(lam, r_tim, label="r(λ)", lw=2)
    ax_twin = axs[0, 1].twinx()
    ax_twin.plot(lam, T_tim, label="T(λ)", color='orange', lw=2)
    axs[0, 1].set_xlabel("λ [proper time]")
    axs[0, 1].set_ylabel("r", color='blue')
    ax_twin.set_ylabel("T [s]", color='orange')
    axs[0, 1].set_title("Timelike Geodesic: r(λ), T(λ)")
    axs[0, 1].grid(True, alpha=0.3)

    # (c) Timelike: Trajectory in (T,r)-diagram
    axs[0, 2].plot(T_tim, r_tim, lw=2.5, color='green')
    axs[0, 2].set_xlabel("T [s]")
    axs[0, 2].set_ylabel("r [units]")
    axs[0, 2].set_title("Timelike Geodesic in (T,r)")
    axs[0, 2].grid(True, alpha=0.3)

    # (d) Light cone closing
    axs[1, 0].plot(r_cone, dr_dT, lw=2, color='red')
    axs[1, 0].set_xlabel("r [units]")
    axs[1, 0].set_ylabel("dr/dT / c")
    axs[1, 0].set_title("Light Cone: dr/dT = c·sech²(φ_G)")
    axs[1, 0].axhline(1.0, color='k', ls='--', alpha=0.5, label='flat space')
    axs[1, 0].legend()
    axs[1, 0].grid(True, alpha=0.3)

    # (e) Light cone closing percentage
    axs[1, 1].plot(r_cone, closing, lw=2, color='purple')
    axs[1, 1].set_xlabel("r [units]")
    axs[1, 1].set_ylabel("Closing [%]")
    axs[1, 1].set_title("Light Cone Closing Percentage")
    axs[1, 1].grid(True, alpha=0.3)

    # (f) Effective potential
    _, V_eff = effective_potential(r_cone)
    axs[1, 2].plot(r_cone, V_eff / (c ** 2), lw=2, color='brown')
    axs[1, 2].set_xlabel("r [units]")
    axs[1, 2].set_ylabel("V_eff / c²")
    axs[1, 2].set_title("Effective Potential")
    axs[1, 2].grid(True, alpha=0.3)

    plt.tight_layout()
    
    print("\n" + "="*80)
    print("Plots generated. Close window to continue.")
    print("="*80 + "\n")
    
    plt.show()


if __name__ == "__main__":
    demo_geodesics()
