#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Pipeline - Main Entry Point

Interactive pipeline to choose and run different SSZ metric implementations:
1. Kerr-SSZ Metric (rotating black holes, frame dragging)
2. φ-Spiral Metric (pure rotation-based, singularity-free)
3. Static SSZ Metric (non-rotating, classic SSZ)

Usage:
    # Interactive mode (asks user):
    python ssz_metric_pipeline.py
    
    # Command-line mode:
    python ssz_metric_pipeline.py --metric phi-spiral
    python ssz_metric_pipeline.py --metric kerr
    python ssz_metric_pipeline.py --metric static
    
    # With parameters:
    python ssz_metric_pipeline.py --metric phi-spiral --mass 1e30 --k 1.5

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import sys
import os
import argparse
import numpy as np
from pathlib import Path

# UTF-8 encoding for Windows (handles φ, Greek letters, Unicode symbols)
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import all metric types
from ssz_metric_pure.metric_phi_spiral_ssz_by_human import PhiSpiralSSZMetric
from ssz_metric_pure.metric_kerr_ssz_kerr_by_ki import KerrSSZMetric, KerrSSZParams
from ssz_metric_pure.metric_static import StaticSSZMetric, SSZParams

# Physical constants
M_SUN = 1.98847e30  # Solar mass [kg]
C_SI = 299792458.0  # Speed of light [m/s]


def print_banner():
    """Print welcome banner."""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  SSZ METRIC PIPELINE - UNIFIED ENTRY POINT".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    print("\nAvailable Metric Implementations:")
    print("  1. φ-Spiral Metric     (Pure rotation-based, subspace layers)")
    print("  2. Kerr-SSZ Metric     (Rotating black holes, frame dragging)")
    print("  3. Static SSZ Metric   (Non-rotating, classic SSZ)")
    print("="*80 + "\n")


def prompt_metric_choice():
    """Prompt user to choose metric interactively."""
    print("Please choose a metric implementation:\n")
    print("  [1] φ-Spiral Metric (φ_G-based rotation)")
    print("  [2] Kerr-SSZ Metric (Rotating black hole)")
    print("  [3] Static SSZ Metric (Non-rotating)")
    print()
    
    while True:
        choice = input("Enter choice [1-3]: ").strip()
        
        if choice == "1":
            return "phi-spiral"
        elif choice == "2":
            return "kerr"
        elif choice == "3":
            return "static"
        else:
            print("⚠ Invalid choice. Please enter 1, 2, or 3.")


def prompt_parameters(metric_type):
    """Prompt user for metric parameters."""
    print("\n" + "="*80)
    print("PARAMETER CONFIGURATION")
    print("="*80)
    
    # Common parameters
    print("\nMass configuration:")
    print("  [1] Solar mass (1.989e30 kg)")
    print("  [2] Custom mass")
    
    mass_choice = input("Choose mass [1-2] (default=1): ").strip() or "1"
    
    if mass_choice == "1":
        mass = M_SUN
        print(f"✓ Using solar mass: {mass:.3e} kg")
    else:
        mass_input = input("Enter mass in kg (e.g. 1e30): ").strip()
        try:
            mass = float(mass_input)
            print(f"✓ Using custom mass: {mass:.3e} kg")
        except ValueError:
            print("⚠ Invalid input, using solar mass")
            mass = M_SUN
    
    # Metric-specific parameters
    params = {"mass": mass}
    
    if metric_type == "phi-spiral":
        k_input = input("\nSpiral strength k (default=1.0): ").strip()
        if k_input:
            try:
                params["k"] = float(k_input)
            except ValueError:
                print("⚠ Invalid k, using default 1.0")
                params["k"] = 1.0
        else:
            params["k"] = 1.0
        
        print(f"✓ k = {params['k']:.2f}")
    
    elif metric_type == "kerr":
        spin_input = input("\nSpin parameter â (0-1, default=0.5): ").strip()
        if spin_input:
            try:
                params["spin"] = float(spin_input)
            except ValueError:
                print("⚠ Invalid spin, using default 0.5")
                params["spin"] = 0.5
        else:
            params["spin"] = 0.5
        
        print(f"✓ â = {params['spin']:.2f}")
    
    print("="*80)
    return params


def run_phi_spiral_pipeline(mass, k=1.0):
    """Run φ-Spiral metric pipeline."""
    print("\n" + "🌀"*40)
    print("φ-SPIRAL METRIC PIPELINE")
    print("🌀"*40 + "\n")
    
    # Create metric
    metric = PhiSpiralSSZMetric(mass=mass, k=k)
    
    print(f"Metric: {metric}")
    print(f"Schwarzschild radius: {metric.r_s:.3e} m")
    print(f"Spiral strength: k = {k:.2f}")
    
    # Test radii
    test_radii = [0.5, 1.0, 2.0, 5.0, 10.0]
    
    print("\n" + "="*80)
    print("METRIC EVALUATION AT DIFFERENT RADII")
    print("="*80)
    print(f"{'r/r_s':<10} {'φ_G [rad]':<15} {'β':<12} {'dτ/dt':<12} {'z':<12} {'Layer':<10}")
    print("-"*80)
    
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        comps = metric.metric_components(r)
        z = metric.redshift(r)
        layer = metric.subspace_layer(r)
        
        print(f"{r_factor:<10.1f} {comps.phi_G:<15.6f} {comps.beta:<12.6f} "
              f"{comps.tau_factor:<12.6f} {z:<12.3f} {layer:<10d}")
    
    # Subspace transitions
    print("\n" + "="*80)
    print("SUBSPACE LAYER TRANSITIONS (Δφ_G = 2π)")
    print("="*80)
    
    r_vals = np.linspace(0.1*metric.r_s, 20*metric.r_s, 10000)
    prev_layer = 0
    
    print(f"{'Layer':<10} {'φ_G [rad]':<20} {'r/r_s':<15}")
    print("-"*60)
    
    for r in r_vals:
        layer = metric.subspace_layer(r)
        if layer > prev_layer:
            phi = metric.phi_G(r)
            print(f"{layer:<10d} {phi:<20.6f} {r/metric.r_s:<15.3f}")
            prev_layer = layer
            if layer >= 3:
                break
    
    # Schwarzschild comparison
    print("\n" + "="*80)
    print("COMPARISON WITH SCHWARZSCHILD METRIC")
    print("="*80)
    print(f"{'r/r_s':<15} {'SSZ φ-Spiral':<20} {'Schwarzschild':<20} {'Δ%':<15}")
    print("-"*80)
    
    for r_factor in [2.0, 5.0, 10.0, 20.0]:
        r = r_factor * metric.r_s
        g_tt_ssz, g_tt_gr = metric.schwarzschild_limit(r)
        
        g_tt_ssz_norm = g_tt_ssz / (C_SI ** 2)
        g_tt_gr_norm = g_tt_gr / (C_SI ** 2)
        diff_pct = 100 * abs(g_tt_ssz_norm - g_tt_gr_norm) / abs(g_tt_gr_norm)
        
        print(f"{r_factor:<15.1f} {g_tt_ssz_norm:<20.6f} {g_tt_gr_norm:<20.6f} {diff_pct:<15.3f}")
    
    print("\n" + "🌀"*40)
    print("✓ φ-SPIRAL PIPELINE COMPLETE")
    print("🌀"*40 + "\n")


def run_kerr_pipeline(mass, spin=0.5):
    """Run Kerr-SSZ metric pipeline."""
    print("\n" + "🔄"*40)
    print("KERR-SSZ METRIC PIPELINE")
    print("🔄"*40 + "\n")
    
    # Create metric
    params = KerrSSZParams(mass=mass, spin=spin)
    metric = KerrSSZMetric(params)
    
    print(f"Metric: {metric}")
    print(f"Spin parameter: â = {metric.a_hat:.3f}")
    
    # Horizons
    r_plus, r_minus = metric.horizons()
    print(f"\nHorizons:")
    print(f"  r_+ (outer) = {r_plus/metric.r_s:.3f} r_s = {r_plus:.3e} m")
    print(f"  r_- (inner) = {r_minus/metric.r_s:.3f} r_s = {r_minus:.3e} m")
    
    if metric.is_extremal():
        print("  ⚠ EXTREMAL BLACK HOLE (r_+ = r_-)")
    
    # Ergosphere
    theta_vals = [0, np.pi/4, np.pi/2]
    print(f"\nErgosphere radii:")
    for theta in theta_vals:
        r_ergo = metric.ergosphere_radius(theta)
        theta_deg = np.degrees(theta)
        print(f"  θ = {theta_deg:>6.1f}°: r_ergo = {r_ergo/metric.r_s:.3f} r_s")
    
    # Metric components at equator
    print("\n" + "="*80)
    print("METRIC AT EQUATOR (θ = π/2)")
    print("="*80)
    print(f"{'r/r_s':<15} {'g_tt/c²':<20} {'g_tφ/c':<20} {'ω [rad/s]':<20}")
    print("-"*80)
    
    test_radii = [1.5, 2.0, 3.0, 5.0, 10.0]
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        theta = np.pi / 2
        
        g_tt = metric.g_tt(r, theta)
        g_tph = metric.g_tph(r, theta)
        omega = metric.frame_drag_frequency(r, theta)
        
        print(f"{r_factor:<15.1f} {g_tt/(C_SI**2):<20.6f} {g_tph/C_SI:<20.6f} {omega:<20.3e}")
    
    # Redshift
    print("\n" + "="*80)
    print("GRAVITATIONAL REDSHIFT")
    print("="*80)
    print(f"{'r/r_s':<15} {'z (equator)':<20}")
    print("-"*50)
    
    for r_factor in [2.0, 5.0, 10.0, 20.0]:
        r = r_factor * metric.r_s
        z = metric.redshift(r, theta=np.pi/2)
        print(f"{r_factor:<15.1f} {z:<20.6f}")
    
    print("\n" + "🔄"*40)
    print("✓ KERR-SSZ PIPELINE COMPLETE")
    print("🔄"*40 + "\n")


def run_static_pipeline(mass):
    """Run Static SSZ metric pipeline."""
    print("\n" + "⚫"*40)
    print("STATIC SSZ METRIC PIPELINE")
    print("⚫"*40 + "\n")
    
    # Create metric
    params = SSZParams(mass=mass)
    metric = StaticSSZMetric(params)
    
    # Import segment density function
    from ssz_metric_pure.segmentation import segment_density_N, XI_MAX
    
    print(f"Metric: {metric}")
    print(f"Schwarzschild radius: {metric.r_s:.3e} m")
    print(f"Natural boundary: {metric.r_phi:.3e} m ({metric.r_phi/metric.r_s:.3f} r_s)")
    
    # Key property: NO SINGULARITY!
    print("\n" + "="*80)
    print("KEY PROPERTY: SINGULARITY-FREE")
    print("="*80)
    A_center = metric.A_coefficient(1e-10)
    print(f"A(r→0) = {A_center:.6f} ← FLAT at center!")
    print(f"A(r_s) = {metric.A_coefficient(metric.r_s):.6f} ← FINITE at Schwarzschild radius!")
    
    # Metric at different radii
    print("\n" + "="*80)
    print("METRIC EVALUATION")
    print("="*80)
    print(f"{'r/r_s':<15} {'A(r)':<20} {'B(r)':<20} {'N(r)':<15}")
    print("-"*80)
    
    test_radii = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    for r_factor in test_radii:
        r = r_factor * metric.r_s
        A = metric.A_coefficient(r)
        B = metric.B_coefficient(r)
        N = segment_density_N(r, metric.r_s, metric.varphi, N_max=XI_MAX)
        
        print(f"{r_factor:<15.1f} {A:<20.6f} {B:<20.6f} {N:<15.6f}")
    
    # Schwarzschild limit
    print("\n" + "="*80)
    print("COMPARISON WITH SCHWARZSCHILD")
    print("="*80)
    print(f"{'r/r_s':<15} {'SSZ A(r)':<20} {'GR A(r)':<20} {'Δ%':<15}")
    print("-"*80)
    
    for r_factor in [2.0, 5.0, 10.0, 20.0]:
        r = r_factor * metric.r_s
        A_ssz = metric.A_coefficient(r)
        A_gr = 1.0 - metric.r_s / r
        diff_pct = 100 * abs(A_ssz - A_gr) / A_gr
        
        print(f"{r_factor:<15.1f} {A_ssz:<20.6f} {A_gr:<20.6f} {diff_pct:<15.3f}")
    
    print("\n" + "⚫"*40)
    print("✓ STATIC SSZ PIPELINE COMPLETE")
    print("⚫"*40 + "\n")


def main():
    """Main pipeline entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="SSZ Metric Pipeline - Choose and run different metric implementations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode:
  python ssz_metric_pipeline.py
  
  # φ-Spiral metric:
  python ssz_metric_pipeline.py --metric phi-spiral
  python ssz_metric_pipeline.py --metric phi-spiral --mass 1e30 --k 1.5
  
  # Kerr-SSZ metric:
  python ssz_metric_pipeline.py --metric kerr --spin 0.9
  
  # Static SSZ metric:
  python ssz_metric_pipeline.py --metric static --mass 2e30
        """
    )
    
    parser.add_argument(
        "--metric",
        choices=["phi-spiral", "kerr", "static"],
        help="Metric implementation to use"
    )
    parser.add_argument(
        "--mass",
        type=float,
        help="Mass in kg (default: solar mass = 1.989e30 kg)"
    )
    parser.add_argument(
        "--k",
        type=float,
        default=1.0,
        help="Spiral strength for φ-Spiral metric (default: 1.0)"
    )
    parser.add_argument(
        "--spin",
        type=float,
        default=0.5,
        help="Dimensionless spin parameter for Kerr metric (default: 0.5)"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Determine metric choice
    if args.metric:
        metric_type = args.metric
        print(f"Using metric: {metric_type} (from command-line argument)")
    else:
        metric_type = prompt_metric_choice()
        print(f"\n✓ Selected: {metric_type}")
    
    # Determine parameters
    if args.mass:
        params = {"mass": args.mass}
        if metric_type == "phi-spiral":
            params["k"] = args.k
        elif metric_type == "kerr":
            params["spin"] = args.spin
        print(f"\nUsing parameters from command-line")
    else:
        params = prompt_parameters(metric_type)
    
    # Run selected pipeline
    print("\n" + "="*80)
    print("RUNNING PIPELINE")
    print("="*80)
    
    try:
        if metric_type == "phi-spiral":
            run_phi_spiral_pipeline(params["mass"], params.get("k", 1.0))
        elif metric_type == "kerr":
            run_kerr_pipeline(params["mass"], params.get("spin", 0.5))
        elif metric_type == "static":
            run_static_pipeline(params["mass"])
        
        # Success message
        print("\n" + "="*80)
        print("✓ PIPELINE COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nNext steps:")
        print("  • Run with different parameters")
        print("  • Try other metric implementations")
        print("  • Generate visualizations (see examples/)")
        print("  • Run comprehensive demos")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print("\n" + "⚠"*80)
        print(f"ERROR: {e}")
        print("⚠"*80)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
