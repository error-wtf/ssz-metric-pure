#!/usr/bin/env python3
"""
SSZ Visualization CLI

Command-line interface for generating SSZ metric plots.

Usage:
    sszviz --plot=time_dilation --mass=1.0
    sszviz --plot=curvature --mass=4.3e6 --compare
    sszviz --plot=metric_a --metric=MirrorBlend

© 2025 Carmen Wrede & Lino Casu
"""

import argparse
import sys
import matplotlib.pyplot as plt

from ssz_core.metric import schwarzschild_radius
from ssz_core.constants import M_SUN
from ssz_viz import (
    plot_time_dilation,
    plot_metric_a,
    plot_curvature,
    plot_ssz_vs_gr,
)


def main():
    parser = argparse.ArgumentParser(
        description="SSZ Metric Visualization CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sszviz --plot=time_dilation --mass=1.0
  sszviz --plot=curvature --mass=4.3e6 
  sszviz --plot=metric_a --metric=MirrorBlend
  sszviz --plot=comparison --mass=10.0 --save=output.png
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--plot',
        type=str,
        required=True,
        choices=['time_dilation', 'metric_a', 'curvature', 'comparison'],
        help='Type of plot to generate'
    )
    
    # Optional arguments
    parser.add_argument(
        '--mass',
        type=float,
        default=1.0,
        help='Black hole mass in solar masses (default: 1.0)'
    )
    
    parser.add_argument(
        '--metric',
        type=str,
        default='MirrorBlend',
        choices=['MirrorBlend', 'Standard', 'SSZ', 'PN'],
        help='Metric mode for blending (default: MirrorBlend)'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare with GR (Schwarzschild)'
    )
    
    parser.add_argument(
        '--save',
        type=str,
        default=None,
        help='Path to save figure (default: show plot)'
    )
    
    parser.add_argument(
        '--r-min',
        type=float,
        default=None,
        help='Minimum radius in r_s units (default: auto)'
    )
    
    parser.add_argument(
        '--r-max',
        type=float,
        default=None,
        help='Maximum radius in r_s units (default: auto)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='Figure DPI for saving (default: 300)'
    )
    
    args = parser.parse_args()
    
    # Calculate Schwarzschild radius
    mass_kg = args.mass * M_SUN
    r_s = schwarzschild_radius(mass_kg)
    
    print(f"\n=== SSZ Visualization ===")
    print(f"Mass: {args.mass:.2e} M_☉")
    print(f"Schwarzschild radius: {r_s:.2e} m")
    print(f"Plot type: {args.plot}")
    print(f"Metric mode: {args.metric}\n")
    
    # Prepare common arguments
    plot_kwargs = {}
    if args.r_min is not None:
        plot_kwargs['r_min'] = args.r_min * r_s
    if args.r_max is not None:
        plot_kwargs['r_max'] = args.r_max * r_s
    if args.save:
        plot_kwargs['save_path'] = args.save
    
    # Generate plot
    try:
        if args.plot == 'time_dilation':
            fig = plot_time_dilation(
                r_s,
                show_intersection=True,
                **plot_kwargs
            )
        
        elif args.plot == 'metric_a':
            fig = plot_metric_a(r_s, **plot_kwargs)
        
        elif args.plot == 'curvature':
            use_mirror = (args.metric == 'MirrorBlend')
            fig = plot_curvature(
                r_s,
                use_mirror_blend=use_mirror,
                **plot_kwargs
            )
        
        elif args.plot == 'comparison':
            fig = plot_ssz_vs_gr(r_s, **plot_kwargs)
        
        # Show or save
        if args.save:
            print(f"✓ Saved: {args.save}")
        else:
            print("Displaying plot...")
            plt.show()
        
        print("\n✓ Done!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
