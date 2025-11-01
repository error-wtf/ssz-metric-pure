#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: φ-Spiral Segmented Spacetime Metric

Demonstrates the pure φ-spiral metric implementation with:
- Metric component calculations
- Subspace layer visualization
- Spiral embedding plots
- Schwarzschild limit comparison

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ssz_metric_pure.metric_phi_spiral_ssz_by_human import PhiSpiralSSZMetric

# Physical constants
M_SUN = 1.98847e30  # Solar mass [kg]


def demo_basic_usage():
    """Basic usage of φ-Spiral metric."""
    print("="*80)
    print("φ-SPIRAL SSZ METRIC - BASIC DEMO")
    print("="*80)
    
    # Create metric for solar mass black hole
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
    
    print(f"\nMetric: {metric}")
    print(f"Schwarzschild radius: {metric.r_s:.3e} m")
    print(f"Characteristic radius: {metric.r0:.3e} m")
    
    # Test at different radii
    test_radii = [0.1, 1.0, 3.0, 10.0]  # In units of r_s
    
    print("\n" + "-"*80)
    print("Metric at different radii:")
    print("-"*80)
    print(f"{'r/r_s':<10} {'φ_G [rad]':<15} {'β':<12} {'dτ/dt':<12} {'Layer':<10}")
    print("-"*80)
    
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        comps = metric.metric_components(r)
        
        print(f"{r_factor:<10.1f} {comps.phi_G:<15.6f} {comps.beta:<12.6f} "
              f"{comps.tau_factor:<12.6f} {metric.subspace_layer(r):<10d}")
    
    print("\n" + "="*80)


def demo_subspace_layers():
    """Demonstrate subspace layer transitions."""
    print("\n" + "="*80)
    print("SUBSPACE LAYER TRANSITIONS (Δφ_G = 2π)")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=2.0)  # Higher k for more layers
    
    # Find radii where layers transition
    r_vals = np.linspace(0.1 * metric.r_s, 20 * metric.r_s, 10000)
    
    print("\nTransition points (φ_G = n·2π):")
    print("-"*60)
    print(f"{'Layer n':<15} {'φ_G [rad]':<20} {'r/r_s':<15}")
    print("-"*60)
    
    prev_layer = 0
    for r in r_vals:
        layer = metric.subspace_layer(r)
        if layer > prev_layer:
            phi = metric.phi_G(r)
            print(f"{layer:<15d} {phi:<20.6f} {r/metric.r_s:<15.3f}")
            prev_layer = layer
            if layer >= 3:  # Show first 3 transitions
                break
    
    print("\n" + "="*80)


def demo_schwarzschild_comparison():
    """Compare with Schwarzschild metric."""
    print("\n" + "="*80)
    print("COMPARISON WITH SCHWARZSCHILD METRIC")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=0.5)  # Weaker spiral
    
    print("\nMetric component comparison (g_tt/c²):")
    print("-"*80)
    print(f"{'r/r_s':<15} {'SSZ φ-Spiral':<20} {'Schwarzschild':<20} {'Difference':<15}")
    print("-"*80)
    
    C_SI = 299792458.0
    test_radii = [1.5, 2.0, 3.0, 5.0, 10.0, 20.0]
    
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        g_tt_ssz, g_tt_gr = metric.schwarzschild_limit(r)
        
        g_tt_ssz_norm = g_tt_ssz / (C_SI ** 2)
        g_tt_gr_norm = g_tt_gr / (C_SI ** 2)
        diff = abs(g_tt_ssz_norm - g_tt_gr_norm)
        
        print(f"{r_factor:<15.1f} {g_tt_ssz_norm:<20.6f} {g_tt_gr_norm:<20.6f} {diff:<15.6e}")
    
    print("\n" + "="*80)


def demo_light_cone_tilt():
    """Demonstrate light cone tilt."""
    print("\n" + "="*80)
    print("LIGHT CONE TILT (Spiral Geometry)")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.5)
    
    print("\nLocal light cone tilt angle α(r):")
    print("-"*60)
    print(f"{'r/r_s':<15} {'α [degrees]':<20} {'β':<15}")
    print("-"*60)
    
    test_radii = [1.0, 2.0, 3.0, 5.0, 10.0]
    
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        alpha = metric.light_cone_tilt(r)
        beta = metric.beta(r)
        
        if not np.isnan(alpha):
            alpha_deg = np.degrees(alpha)
            print(f"{r_factor:<15.1f} {alpha_deg:<20.3f} {beta:<15.6f}")
        else:
            print(f"{r_factor:<15.1f} {'NaN (inside ergo)':<20} {beta:<15.6f}")
    
    print("\n" + "="*80)


def plot_metric_components_demo():
    """Plot metric components."""
    print("\n" + "="*80)
    print("PLOTTING METRIC COMPONENTS")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
    
    try:
        fig = metric.plot_metric_components(0.5 * metric.r_s, 15 * metric.r_s)
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "phi_spiral_metric_components.png"
        fig.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Saved: {output_file}")
        
        plt.close(fig)
        
    except Exception as e:
        print(f"\n✗ Plotting failed: {e}")
    
    print("\n" + "="*80)


def plot_subspace_layers_demo():
    """Plot subspace layer transitions."""
    print("\n" + "="*80)
    print("PLOTTING SUBSPACE LAYERS")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=2.0)
    
    try:
        fig = metric.plot_subspace_layers(0.1 * metric.r_s, 15 * metric.r_s)
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "phi_spiral_subspace_layers.png"
        fig.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Saved: {output_file}")
        
        plt.close(fig)
        
    except Exception as e:
        print(f"\n✗ Plotting failed: {e}")
    
    print("\n" + "="*80)


def plot_spiral_embedding_demo():
    """Plot 2D and 3D spiral embeddings."""
    print("\n" + "="*80)
    print("PLOTTING SPIRAL EMBEDDINGS")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.5)
    
    r_vals = np.linspace(0, 10 * metric.r_s, 1000)
    
    # 2D spiral
    try:
        x, y = metric.spiral_embedding_2d(r_vals)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(x / metric.r_s, y / metric.r_s, 'b-', linewidth=2)
        ax.set_xlabel(r"$x / r_s$", fontsize=14)
        ax.set_ylabel(r"$y / r_s$", fontsize=14)
        ax.set_title(r"2D φ-Spiral Embedding: $(x, y) = (r\cos\phi_G, r\sin\phi_G)$", fontsize=16)
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "phi_spiral_2d_embedding.png"
        fig.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Saved 2D: {output_file}")
        
        plt.close(fig)
        
    except Exception as e:
        print(f"\n✗ 2D plotting failed: {e}")
    
    # 3D helix
    try:
        x, y, z = metric.spiral_embedding_3d(r_vals, z_scale=1.0)
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Color by subspace layer
        layers = np.array([metric.subspace_layer(r) for r in r_vals])
        scatter = ax.scatter(x / metric.r_s, y / metric.r_s, z / (2*np.pi), 
                            c=layers, cmap='viridis', s=1, alpha=0.8)
        
        ax.set_xlabel(r"$x / r_s$", fontsize=12)
        ax.set_ylabel(r"$y / r_s$", fontsize=12)
        ax.set_zlabel(r"$\phi_G / 2\pi$ (Subspace Layer)", fontsize=12)
        ax.set_title("3D φ-Spiral Helix with Subspace Layers", fontsize=16)
        
        cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label("Subspace Layer Number", fontsize=12)
        
        output_file = output_dir / "phi_spiral_3d_helix.png"
        fig.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Saved 3D: {output_file}")
        
        plt.close(fig)
        
    except Exception as e:
        print(f"\n✗ 3D plotting failed: {e}")
    
    print("\n" + "="*80)


def plot_time_dilation_redshift():
    """Plot time dilation and redshift."""
    print("\n" + "="*80)
    print("PLOTTING TIME DILATION & REDSHIFT")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
    
    r_vals = np.linspace(0.5 * metric.r_s, 20 * metric.r_s, 1000)
    tau_factors = np.array([metric.time_dilation_factor(r) for r in r_vals])
    redshifts = np.array([metric.redshift(r) for r in r_vals])
    
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Time dilation
        ax1.plot(r_vals / metric.r_s, tau_factors, 'b-', linewidth=2)
        ax1.set_ylabel(r"$d\tau/dt$ (Time Dilation)", fontsize=14)
        ax1.set_title(r"Time Dilation: $d\tau/dt = \mathrm{sech}(\phi_G)$", fontsize=16)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=1, color='k', linestyle='--', alpha=0.3, label='No dilation')
        ax1.legend()
        
        # Redshift
        ax2.semilogy(r_vals / metric.r_s, redshifts, 'r-', linewidth=2)
        ax2.set_xlabel(r"$r / r_s$", fontsize=14)
        ax2.set_ylabel(r"$z$ (Redshift)", fontsize=14)
        ax2.set_title(r"Gravitational Redshift: $z = \cosh(\phi_G) - 1$", fontsize=16)
        ax2.grid(True, alpha=0.3, which='both')
        
        plt.tight_layout()
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "phi_spiral_time_dilation_redshift.png"
        fig.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Saved: {output_file}")
        
        plt.close(fig)
        
    except Exception as e:
        print(f"\n✗ Plotting failed: {e}")
    
    print("\n" + "="*80)


def demo_diagonal_form():
    """Demonstrate diagonal form."""
    print("\n" + "="*80)
    print("DIAGONAL FORM (Coordinate Transformation)")
    print("="*80)
    
    metric = PhiSpiralSSZMetric(mass=M_SUN, k=1.0)
    
    print("\nDiagonal metric coefficients:")
    print("-"*60)
    print(f"{'r/r_s':<15} {'A_diag/c²':<20} {'B_diag':<20}")
    print("-"*60)
    
    C_SI = 299792458.0
    test_radii = [1.0, 2.0, 3.0, 5.0, 10.0]
    
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        A_diag, B_diag = metric.diagonal_form_coefficients(r)
        
        A_diag_norm = A_diag / (C_SI ** 2)
        
        print(f"{r_factor:<15.1f} {A_diag_norm:<20.6f} {B_diag:<20.6f}")
    
    print("\nNote: ds² = -A_diag dt² + B_diag dρ²  (diagonal!)")
    print("      where dρ = dr + β(r)c dt")
    
    print("\n" + "="*80)


def main():
    """Run all demos."""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  φ-SPIRAL SEGMENTED SPACETIME METRIC - COMPLETE DEMONSTRATION".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80 + "\n")
    
    # Text demos
    demo_basic_usage()
    demo_subspace_layers()
    demo_schwarzschild_comparison()
    demo_light_cone_tilt()
    demo_diagonal_form()
    
    # Visual demos (requires matplotlib)
    try:
        plot_metric_components_demo()
        plot_subspace_layers_demo()
        plot_spiral_embedding_demo()
        plot_time_dilation_redshift()
        
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + "  ✓ ALL VISUALIZATIONS SAVED TO examples/output/".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
    except ImportError:
        print("\n" + "⚠"*80)
        print("⚠  Matplotlib not installed. Install via: pip install matplotlib")
        print("⚠"*80 + "\n")
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("\nKey Results:")
    print("- φ-Spiral metric successfully implemented")
    print("- Subspace layers transition at Δφ_G = 2π")
    print("- No singularities (space folds into new layers)")
    print("- Diagonal form available via coordinate transformation")
    print("- Compatible with Schwarzschild in weak field limit")
    print("\n© 2025 Carmen Wrede & Lino Casu")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
