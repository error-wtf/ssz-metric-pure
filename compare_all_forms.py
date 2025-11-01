#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Comparison: All Metric Forms

Compares:
1. Original φ-Spiral (with g_tr)
2. Diagonal Form (T coordinate)
3. Static SSZ
4. Numerical values and differences

© 2025 Carmen Wrede & Lino Casu
"""
import sys
import os
import numpy as np
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ssz_metric_pure.metric_phi_spiral_ssz_by_human import PhiSpiralSSZMetric
from ssz_metric_pure.metric_static import StaticSSZMetric, SSZParams

M_SUN = 1.98847e30
C_SI = 299792458.0

print("\n" + "="*80)
print("VOLLSTÄNDIGER VERGLEICH: Alle Metrik-Formen")
print("="*80)

mass = M_SUN
phi_spiral = PhiSpiralSSZMetric(mass=mass, k=1.0)
static_ssz = StaticSSZMetric(SSZParams(mass=mass))

print(f"\nSetup:")
print(f"  Masse: {mass:.3e} kg (Sonnenmasse)")
print(f"  r_s: {phi_spiral.r_s:.3e} m")
print(f"  φ-Spiral k: 1.0")

# ============================================================================
# 1. ORIGINAL φ-SPIRAL (t, r Koordinaten)
# ============================================================================
print("\n" + "="*80)
print("1. ORIGINAL φ-SPIRAL METRIK (t,r Koordinaten)")
print("="*80)
print("\nds² = -c²(1-β²)dt² + 2βc dt dr + dr²")
print(f"\n{'r/r_s':<10} {'g_tt/c²':<12} {'g_tr/c':<12} {'g_rr':<12} {'β':<12} {'φ_G':<12}")
print("-"*80)

test_radii = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    g_tt = phi_spiral.g_tt(r) / (C_SI ** 2)
    g_tr = phi_spiral.g_tr(r) / C_SI
    g_rr = phi_spiral.g_rr(r)
    beta = phi_spiral.beta(r)
    phi_G = phi_spiral.phi_G(r)
    
    print(f"{r_factor:<10.1f} {g_tt:<12.6f} {g_tr:<12.6f} {g_rr:<12.6f} {beta:<12.6f} {phi_G:<12.6f}")

# ============================================================================
# 2. DIAGONALE FORM (T, r Koordinaten)
# ============================================================================
print("\n" + "="*80)
print("2. DIAGONALE FORM (T,r Koordinaten)")
print("="*80)
print("\nTransformation: dT = dt - (β·γ²/c) dr")
print("Metrik: ds² = -c²/γ² dT² + γ² dr²")
print(f"\n{'r/r_s':<10} {'g_TT/c²':<12} {'g_rr':<12} {'γ':<12} {'1/γ²':<12} {'γ²':<12}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    g_TT, g_rr_diag = phi_spiral.diagonal_form_coefficients(r)
    g_TT_norm = g_TT / (C_SI ** 2)
    gamma = phi_spiral.gamma(r)
    inv_gamma2 = 1.0 / (gamma ** 2)
    gamma2 = gamma ** 2
    
    print(f"{r_factor:<10.1f} {g_TT_norm:<12.6f} {g_rr_diag:<12.6f} {gamma:<12.6f} {inv_gamma2:<12.6f} {gamma2:<12.6f}")

# ============================================================================
# 3. STATIC SSZ
# ============================================================================
print("\n" + "="*80)
print("3. STATIC SSZ METRIK")
print("="*80)
print("\nds² = -A(r)dt² + B(r)dr²")
print(f"\n{'r/r_s':<10} {'A(r)':<12} {'B(r)':<12} {'-A/c²':<12} {'N(r)':<12}")
print("-"*80)

from ssz_metric_pure.segmentation import segment_density_N, XI_MAX

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    A = static_ssz.A_coefficient(r)
    B = static_ssz.B_coefficient(r)
    A_norm = -A / (C_SI ** 2)
    N = segment_density_N(r, static_ssz.r_s, static_ssz.varphi, N_max=XI_MAX)
    
    print(f"{r_factor:<10.1f} {A:<12.6f} {B:<12.6f} {A_norm:<12.6f} {N:<12.6f}")

# ============================================================================
# 4. ZEITKOMPONENTEN-VERGLEICH
# ============================================================================
print("\n" + "="*80)
print("4. ZEITKOMPONENTEN-VERGLEICH (alle normiert auf c²)")
print("="*80)
print(f"\n{'r/r_s':<10} {'Spiral (t)':<12} {'Spiral (T)':<12} {'Static':<12} {'Δ(t vs T)%':<15} {'Δ(T vs Static)%':<15}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    # φ-Spiral original
    g_tt_spiral_t = phi_spiral.g_tt(r) / (C_SI ** 2)
    
    # φ-Spiral diagonal
    g_TT, _ = phi_spiral.diagonal_form_coefficients(r)
    g_TT_norm = g_TT / (C_SI ** 2)
    
    # Static
    A_static = static_ssz.A_coefficient(r)
    g_tt_static = -A_static / (C_SI ** 2)
    
    # Differences
    diff_t_T = 100 * abs(g_tt_spiral_t - g_TT_norm) / abs(g_tt_spiral_t) if g_tt_spiral_t != 0 else 0
    diff_T_static = 100 * abs(g_TT_norm - g_tt_static) / abs(g_TT_norm) if g_TT_norm != 0 else 0
    
    print(f"{r_factor:<10.1f} {g_tt_spiral_t:<12.6f} {g_TT_norm:<12.6f} {g_tt_static:<12.6f} {diff_t_T:<15.2f} {diff_T_static:<15.2f}")

# ============================================================================
# 5. RADIALE KOMPONENTEN-VERGLEICH
# ============================================================================
print("\n" + "="*80)
print("5. RADIALE KOMPONENTEN-VERGLEICH")
print("="*80)
print(f"\n{'r/r_s':<10} {'Spiral (t)':<12} {'Spiral (T)':<12} {'Static':<12} {'γ² factor':<12}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    # φ-Spiral original (g_rr = 1)
    g_rr_spiral_t = phi_spiral.g_rr(r)
    
    # φ-Spiral diagonal (g_rr = γ²)
    _, g_rr_spiral_T = phi_spiral.diagonal_form_coefficients(r)
    
    # Static (B = 1/A)
    g_rr_static = static_ssz.B_coefficient(r)
    
    # γ² factor
    gamma = phi_spiral.gamma(r)
    gamma2 = gamma ** 2
    
    print(f"{r_factor:<10.1f} {g_rr_spiral_t:<12.6f} {g_rr_spiral_T:<12.6f} {g_rr_static:<12.6f} {gamma2:<12.6f}")

# ============================================================================
# 6. OFF-DIAGONAL TERM (nur in t-Koordinaten!)
# ============================================================================
print("\n" + "="*80)
print("6. OFF-DIAGONAL TERM g_tr/c")
print("="*80)
print("\nNur in Original-Koordinaten (t,r) vorhanden!")
print(f"\n{'r/r_s':<10} {'Spiral (t,r)':<15} {'Spiral (T,r)':<15} {'Static':<15}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    g_tr_t = phi_spiral.g_tr(r) / C_SI
    
    print(f"{r_factor:<10.1f} {g_tr_t:<15.6f} {'0.000000':<15} {'0.000000':<15}")

# ============================================================================
# 7. ZEITDILATATION
# ============================================================================
print("\n" + "="*80)
print("7. ZEITDILATATION dτ/dt")
print("="*80)
print(f"\n{'r/r_s':<10} {'Spiral sech(φ)':<15} {'Static √A':<15} {'Δ%':<12}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    dtau_spiral = phi_spiral.time_dilation_factor(r)
    
    A_static = static_ssz.A_coefficient(r)
    dtau_static = np.sqrt(A_static)
    
    diff_pct = 100 * abs(dtau_spiral - dtau_static) / dtau_static if dtau_static > 0 else 0
    
    print(f"{r_factor:<10.1f} {dtau_spiral:<15.6f} {dtau_static:<15.6f} {diff_pct:<12.2f}")

# ============================================================================
# 8. LICHTKEGEL-VERHALTEN
# ============================================================================
print("\n" + "="*80)
print("8. LICHTKEGEL-VERHALTEN")
print("="*80)

print("\nIn (t,r) Koordinaten:")
print("  Null-Geodäten: komplex (wegen g_tr)")
print("  Light cone tilt: α(r)")

print("\nIn (T,r) Koordinaten:")
print("  Null-Geodäten: dr/dT = ±c/γ² = ±c·sech²(φ_G)")
print("  Light cone closing (nicht divergierend!)")

print(f"\n{'r/r_s':<10} {'φ_G [rad]':<15} {'dr/dT / c':<15} {'Closing %':<15}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    phi_G = phi_spiral.phi_G(r)
    gamma = phi_spiral.gamma(r)
    
    dr_dT_norm = 1.0 / (gamma ** 2)
    closing_pct = (1.0 - dr_dT_norm) * 100
    
    print(f"{r_factor:<10.1f} {phi_G:<15.6f} {dr_dT_norm:<15.6f} {closing_pct:<15.2f}")

# ============================================================================
# 9. SUBSPACE LAYERS (nur φ-Spiral!)
# ============================================================================
print("\n" + "="*80)
print("9. SUBSPACE LAYERS (nur in φ-Spiral Metrik!)")
print("="*80)
print(f"\n{'r/r_s':<10} {'φ_G [rad]':<15} {'Layer n':<15} {'Progress to next':<20}")
print("-"*80)

for r_factor in test_radii:
    r = r_factor * phi_spiral.r_s
    
    phi_G = phi_spiral.phi_G(r)
    layer = phi_spiral.subspace_layer(r)
    
    # Progress to next 2π
    next_2pi = 2 * np.pi * (layer + 1)
    progress = (phi_G - layer * 2 * np.pi) / (2 * np.pi)
    
    print(f"{r_factor:<10.1f} {phi_G:<15.6f} {layer:<15d} {progress*100:<20.2f}%")

# ============================================================================
# ZUSAMMENFASSUNG
# ============================================================================
print("\n" + "="*80)
print("ZUSAMMENFASSUNG")
print("="*80)

print("""
KOORDINATEN-FORMEN:
───────────────────

1. φ-Spiral (t,r):
   • g_tt = -c²(1-β²)
   • g_tr = βc  ← NICHT-NULL!
   • g_rr = 1
   → Kopplung zwischen Zeit und Radius

2. φ-Spiral (T,r):
   • g_TT = -c²/γ²
   • g_Tr = 0  ← DIAGONAL!
   • g_rr = γ²
   → Orthogonale Koordinaten, einfachere Struktur

3. Static SSZ:
   • g_tt = -A(r)
   • g_tr = 0
   • g_rr = B(r) = 1/A(r)
   → Diagonal, aber andere funktionale Form

HAUPTUNTERSCHIEDE:
──────────────────

✓ KOORDINATEN-WAHL:
  • (t,r): Nicht-diagonal, g_tr ≠ 0
  • (T,r): Diagonal, g_Tr = 0
  • Beide physikalisch äquivalent!

✓ ZEITKOMPONENTE:
  • φ-Spiral (t): g_tt = -c²(1-β²)
  • φ-Spiral (T): g_TT = -c²/γ²
  • IDENTISCH (beide = -c²sech²(φ_G))

✓ RADIALE KOMPONENTE:
  • φ-Spiral (t): g_rr = 1
  • φ-Spiral (T): g_rr = γ² 
  • UNTERSCHIEDLICH wegen Transformation!

✓ vs STATIC SSZ:
  • Beide haben g_tr = 0 (Static immer, Spiral in T-Koordinate)
  • Unterschiedliche funktionale Formen
  • φ-Spiral hat Subspace-Layers
  • Static hat Segment-Dichte N(r)

LICHTKEGEL:
───────────

• (t,r): Komplex, Tilt α(r)
• (T,r): Einfach, dr/dT = ±c/γ²
• Closing mit wachsendem φ_G
• KEINE Divergenz (nur Schließung!)

PHYSIKALISCHE ÄQUIVALENZ:
─────────────────────────

Die φ-Spiral Metrik in (t,r) und (T,r) sind
PHYSIKALISCH IDENTISCH - nur andere Koordinaten!

Die Transformation dT = dt - (β·γ²/c)dr ist
eine reine Koordinaten-Umbenennung.

Invariante:
  • Eigenzeit τ
  • Null-Geodäten
  • Krümmung
  • Physikalische Observablen
""")

print("="*80)
print("\n© 2025 Carmen Wrede & Lino Casu\n")
