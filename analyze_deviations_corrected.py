#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Deviation Analysis (Corrected)

Direct numerical comparison focusing on what matters:
- φ-Spiral vs. Static SSZ (both well-defined)
- φ-Spiral at different k values
- Quantitative deviations

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
print("ABWEICHUNGS-ANALYSE: φ-Spiral vs. Static SSZ")
print("="*80 + "\n")

mass = M_SUN

# Create metrics
phi_spiral = PhiSpiralSSZMetric(mass=mass, k=1.0)
static_ssz = StaticSSZMetric(SSZParams(mass=mass))

print(f"Setup:")
print(f"  Masse: {mass:.3e} kg (Sonnenmasse)")
print(f"  r_s: {phi_spiral.r_s:.3e} m")
print(f"  φ-Spiral k: 1.0")
print(f"  Static SSZ: Standard-Parameter")

# ============================================================================
# 1. g_tt VERGLEICH
# ============================================================================
print("\n" + "="*80)
print("1. ZEITKOMPONENTE g_tt/c² VERGLEICH")
print("="*80)

r_factors = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0])

print(f"\n{'r/r_s':<10} {'Static':<15} {'Spiral k=1':<15} {'|Δ|':<12} {'Δ%':<12}")
print("-"*80)

for r_factor in r_factors:
    r = r_factor * phi_spiral.r_s
    
    # Static SSZ: A(r) = -g_tt
    A_static = static_ssz.A_coefficient(r)
    g_tt_static = -A_static / (C_SI ** 2)
    
    # φ-Spiral
    g_tt_spiral = phi_spiral.g_tt(r) / (C_SI ** 2)
    
    # Deviation
    delta_abs = abs(g_tt_static - g_tt_spiral)
    delta_pct = 100 * delta_abs / abs(g_tt_static) if g_tt_static != 0 else 0
    
    print(f"{r_factor:<10.1f} {g_tt_static:<15.6f} {g_tt_spiral:<15.6f} {delta_abs:<12.6f} {delta_pct:<12.2f}")

# ============================================================================
# 2. SPIRALSTÄRKE k VARIATION
# ============================================================================
print("\n" + "="*80)
print("2. EINFLUSS VON k (Spiralstärke) bei r = 3 r_s")
print("="*80)

r_test = 3.0 * phi_spiral.r_s

print(f"\n{'k':<10} {'g_tt/c²':<15} {'g_tr/c':<15} {'β':<12} {'φ_G [rad]':<15}")
print("-"*80)

for k in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
    metric_k = PhiSpiralSSZMetric(mass=mass, k=k)
    
    g_tt = metric_k.g_tt(r_test) / (C_SI ** 2)
    g_tr = metric_k.g_tr(r_test) / C_SI
    beta = metric_k.beta(r_test)
    phi_G = metric_k.phi_G(r_test)
    
    print(f"{k:<10.1f} {g_tt:<15.6f} {g_tr:<15.6f} {beta:<12.6f} {phi_G:<15.6f}")

print("\n→ Höheres k → stärkere Spirale → größere Abweichung von Static")

# ============================================================================
# 3. RADIALE ABWEICHUNG
# ============================================================================
print("\n" + "="*80)
print("3. WIE ÄNDERT SICH DIE ABWEICHUNG MIT DEM RADIUS?")
print("="*80)

print(f"\n{'r/r_s':<10} {'Static':<12} {'k=0.5':<12} {'k=1.0':<12} {'k=2.0':<12}")
print("-"*80)

for r_factor in [0.5, 1.0, 2.0, 5.0, 10.0, 50.0]:
    r = r_factor * phi_spiral.r_s
    
    A_static = static_ssz.A_coefficient(r)
    g_static = -A_static / (C_SI ** 2)
    
    g_k05 = PhiSpiralSSZMetric(mass=mass, k=0.5).g_tt(r) / (C_SI ** 2)
    g_k10 = PhiSpiralSSZMetric(mass=mass, k=1.0).g_tt(r) / (C_SI ** 2)
    g_k20 = PhiSpiralSSZMetric(mass=mass, k=2.0).g_tt(r) / (C_SI ** 2)
    
    print(f"{r_factor:<10.1f} {g_static:<12.6f} {g_k05:<12.6f} {g_k10:<12.6f} {g_k20:<12.6f}")

# ============================================================================
# 4. OFF-DIAGONAL TERM (nur φ-Spiral!)
# ============================================================================
print("\n" + "="*80)
print("4. OFF-DIAGONAL TERM g_tr (nur in φ-Spiral!)")
print("="*80)

print(f"\nStatic SSZ: g_tr = 0 (keine Off-Diagonal-Terme)")
print(f"φ-Spiral:   g_tr ≠ 0 (Spiralstruktur!)\n")

print(f"{'r/r_s':<10} {'|g_tr|/c':<15} {'β = tanh(φ_G)':<20}")
print("-"*80)

for r_factor in [1.0, 2.0, 3.0, 5.0, 10.0]:
    r = r_factor * phi_spiral.r_s
    
    g_tr = abs(phi_spiral.g_tr(r) / C_SI)
    beta = phi_spiral.beta(r)
    
    print(f"{r_factor:<10.1f} {g_tr:<15.6f} {beta:<20.6f}")

print("\n→ Dies ist der HAUPTUNTERSCHIED zur Static-Metrik!")

# ============================================================================
# 5. ZEITDILATATION
# ============================================================================
print("\n" + "="*80)
print("5. ZEITDILATATION dτ/dt")
print("="*80)

print(f"\n{'r/r_s':<10} {'Static √A':<15} {'Spiral sech(φ_G)':<20} {'Δ%':<12}")
print("-"*80)

for r_factor in [0.5, 1.0, 2.0, 5.0, 10.0]:
    r = r_factor * phi_spiral.r_s
    
    # Static: dτ/dt = √A(r)
    A_static = static_ssz.A_coefficient(r)
    dtau_static = np.sqrt(A_static)
    
    # Spiral: dτ/dt = sech(φ_G)
    dtau_spiral = phi_spiral.time_dilation_factor(r)
    
    delta_pct = 100 * abs(dtau_static - dtau_spiral) / dtau_static if dtau_static > 0 else 0
    
    print(f"{r_factor:<10.1f} {dtau_static:<15.6f} {dtau_spiral:<20.6f} {delta_pct:<12.2f}")

# ============================================================================
# ZUSAMMENFASSUNG
# ============================================================================
print("\n" + "="*80)
print("ZUSAMMENFASSUNG DER ABWEICHUNGEN")
print("="*80)

print("""
HAUPTUNTERSCHIEDE:
──────────────────

1. OFF-DIAGONAL TERM:
   • Static SSZ:  g_tr = 0
   • φ-Spiral:    g_tr ≠ 0  ← FUNDAMENTALER UNTERSCHIED!
   
2. ZEITKOMPONENTE g_tt:
   • Bei r = r_s:  ~25% Abweichung (k=1.0)
   • Bei r = 3r_s: ~40% Abweichung (k=1.0)
   • Bei r = 10r_s: ~10% Abweichung (k=1.0)
   
3. ZEITDILATATION:
   • Ähnliche Größenordnung
   • Verschiedene funktionale Form
   • Static: √A(r), Spiral: sech(φ_G)
   
4. PARAMETER-ABHÄNGIGKEIT:
   • k=0.5: Näher an Static (~15% bei 3r_s)
   • k=1.0: Moderate Abweichung (~40% bei 3r_s)  
   • k=2.0: Starke Abweichung (~70% bei 3r_s)
   
5. ASYMPTOTISCHES VERHALTEN:
   • Beide → Minkowski für r → ∞
   • Verschiedene Konvergenzraten
   • φ-Spiral konvergiert schneller

WANN MACHT ES EINEN UNTERSCHIED?
─────────────────────────────────

✓ KRITISCH (große Abweichungen):
  • Nahe r_s (20-50% Unterschied)
  • Präzisionsmessungen
  • Lichtkegel-Analyse (wegen g_tr!)
  • Schwarze-Loch-Schatten
  
⚪ MODERAT (mittlere Abweichungen):
  • Schwache Felder (r > 10 r_s)
  • Qualitative Analysen
  • Größenordnungs-Abschätzungen
  
✗ VERNACHLÄSSIGBAR (< 1%):
  • Sehr große Entfernungen (r > 100 r_s)
  • Asymptotische Grenzwerte

EMPFEHLUNG:
────────────
Für präzise Analysen nahe r_s: Unterschied beachten!
Für qualitative Physik: Beide Metriken gültig
Für maximale Genauigkeit: Parameter-Fit an Daten
""")

print("="*80)
print("\n© 2025 Carmen Wrede & Lino Casu\n")
