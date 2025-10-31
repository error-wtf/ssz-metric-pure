"""
Basic Usage Example for SSZ Metric Pure

Demonstrates core functionality of the SSZ metric.

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
import matplotlib.pyplot as plt

from src.ssz_core import (
    Xi, D_SSZ, D_GR, find_intersection,
    A_Xi, A_phi_series, A_safe,
    metric_tensor, schwarzschild_radius
)
from src.ssz_core.constants import PHI, M_SUN

print("="*60)
print("SSZ Metric Pure - Basic Usage Example")
print("="*60)

# 1. Calculate Schwarzschild radius for solar mass
print("\n1. Schwarzschild Radius")
print("-" * 40)
r_s = schwarzschild_radius(M_SUN)
print(f"Solar mass: {M_SUN:.3e} kg")
print(f"r_s: {r_s:.2f} m")

# 2. Segment saturation (Golden Ratio!)
print("\n2. Segment Saturation (φ = {:.6f})".format(PHI))
print("-" * 40)
r_test = r_s
xi = Xi(r_test, r_s)
print(f"Ξ({r_test/r_s:.1f} r_s) = {xi:.6f}")
print(f"Ξ(0) = {Xi(0.0, r_s):.6f} (empty at center)")
print(f"Ξ(∞) → {Xi(100*r_s, r_s):.6f} (full saturation)")

# 3. SSZ time dilation (singularity-free!)
print("\n3. Time Dilation")
print("-" * 40)
print(f"D_SSZ(0) = {D_SSZ(0.0, r_s):.6f} ← NO SINGULARITY!")
print(f"D_SSZ(r_s) = {D_SSZ(r_s, r_s):.6f} ← FINITE!")
print(f"D_GR(r_s) = {D_GR(r_s, r_s)} ← NaN (singularity)")

# 4. Find intersection point r*
print("\n4. Intersection Point r*")
print("-" * 40)
r_star = find_intersection(r_s)
d_ssz_star = D_SSZ(r_star, r_s)
d_gr_star = D_GR(r_star, r_s)
print(f"r* = {r_star/r_s:.3f} r_s = {r_star:.2f} m")
print(f"D_SSZ(r*) = {d_ssz_star:.6f}")
print(f"D_GR(r*) = {d_gr_star:.6f}")
print(f"Match: {abs(d_ssz_star - d_gr_star) < 1e-6}")

# 5. Metric coefficients
print("\n5. Metric Coefficients")
print("-" * 40)
r = 5 * r_s
A_inner = A_Xi(r, r_s)
A_outer = A_phi_series(r, r_s, order=6)
A_blended = A_safe(r, r_s, use_mirror_blend=True)
print(f"At r = {r/r_s:.1f} r_s:")
print(f"  A_Ξ (inner SSZ) = {A_inner:.6f}")
print(f"  A_φ (outer PN) = {A_outer:.6f}")
print(f"  A_safe (blended) = {A_blended:.6f}")

# 6. Full metric tensor
print("\n6. Metric Tensor")
print("-" * 40)
r = 10 * r_s
theta = np.pi / 2
g, comps = metric_tensor(r, theta, r_s, use_mirror_blend=True)
print(f"At r = {r/r_s:.1f} r_s, θ = π/2:")
print(f"  g_tt = {comps['g_tt']:.6f}")
print(f"  g_rr = {comps['g_rr']:.6f}")
print(f"  g_θθ = {comps['g_theta_theta']:.2f}")
print(f"  g_φφ = {comps['g_phi_phi']:.2f}")

# 7. Visualization
print("\n7. Creating Visualization...")
print("-" * 40)

# Create comparison plot
r_values = np.linspace(0.01 * r_s, 10 * r_s, 1000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Time dilation
d_ssz = D_SSZ(r_values, r_s)
d_gr = D_GR(r_values, r_s)

ax1.plot(r_values / r_s, d_ssz, 'b-', linewidth=2.5, label='SSZ')
ax1.plot(r_values / r_s, d_gr, 'r--', linewidth=2, label='GR')
ax1.axvline(1.0, color='gray', linestyle=':', alpha=0.5, label='r_s')
ax1.plot([r_star/r_s], [d_ssz_star], 'go', markersize=10, label='r*')
ax1.set_xlabel('r / r_s', fontsize=12)
ax1.set_ylabel('D(r)', fontsize=12)
ax1.set_title('Time Dilation: SSZ vs GR', fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1.1)

# Metric coefficient
A_ssz = A_safe(r_values, r_s, use_mirror_blend=True)
A_gr = 1.0 - r_s / np.maximum(r_values, r_s)

ax2.plot(r_values / r_s, A_ssz, 'b-', linewidth=2.5, label='SSZ')
ax2.plot(r_values / r_s, A_gr, 'r--', linewidth=2, label='GR')
ax2.axvline(1.0, color='gray', linestyle=':', alpha=0.5, label='r_s')
ax2.set_xlabel('r / r_s', fontsize=12)
ax2.set_ylabel('A(r)', fontsize=12)
ax2.set_title('Metric Coefficient: SSZ vs GR', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('examples/ssz_basic_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: examples/ssz_basic_comparison.png")

print("\n" + "="*60)
print("✓ Example Complete!")
print("="*60)
print("\nKey Takeaways:")
print("  • SSZ has NO singularity at r=0: D_SSZ(0) = 1")
print("  • Metric is finite everywhere: A(r) > 0")
print("  • Golden Ratio φ determines saturation")
print("  • Smooth transition to GR at r*")
print("\n" + "="*60)

plt.show()
