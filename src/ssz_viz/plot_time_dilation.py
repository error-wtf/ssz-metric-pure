"""
Time Dilation Visualization

Plot D_SSZ(r) vs D_GR(r) with intersection point.

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List
import imageio.v2 as imageio
import os

from ..ssz_core.segment_density import D_SSZ, D_GR, find_intersection
from ..ssz_core.metric import schwarzschild_radius
from ..ssz_core.constants import M_SUN


def plot_time_dilation(
    r_s: float,
    r_min: Optional[float] = None,
    r_max: Optional[float] = None,
    n_points: int = 1000,
    show_intersection: bool = True,
    save_path: Optional[str] = None,
    figsize: tuple = (10, 6)
) -> plt.Figure:
    """
    Plot SSZ and GR time dilation factors.
    
    Args:
        r_s: Schwarzschild radius (m)
        r_min: Minimum radius (default: 0.1 * r_s)
        r_max: Maximum radius (default: 10 * r_s)
        n_points: Number of plot points
        show_intersection: Mark r* intersection
        save_path: Path to save figure (optional)
        figsize: Figure size
        
    Returns:
        fig: Matplotlib figure
    """
    if r_min is None:
        r_min = 0.01 * r_s
    if r_max is None:
        r_max = 10.0 * r_s
    
    # Create radius array
    r_values = np.linspace(r_min, r_max, n_points)
    
    # Calculate time dilations
    d_ssz = D_SSZ(r_values, r_s)
    d_gr = D_GR(r_values, r_s)
    
    # Find intersection
    if show_intersection:
        try:
            r_star = find_intersection(r_s)
            d_star = D_SSZ(r_star, r_s)
        except ValueError:
            show_intersection = False
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot SSZ
    ax.plot(r_values / r_s, d_ssz, 'b-', linewidth=2.5, label='SSZ (Singularity-Free)')
    
    # Plot GR (only where defined)
    valid_gr = ~np.isnan(d_gr)
    ax.plot(r_values[valid_gr] / r_s, d_gr[valid_gr], 'r--', linewidth=2, 
            label='GR (Schwarzschild)')
    
    # Mark Schwarzschild radius
    ax.axvline(1.0, color='gray', linestyle=':', alpha=0.5, label='r_s')
    
    # Mark intersection
    if show_intersection:
        ax.plot([r_star / r_s], [d_star], 'go', markersize=10, 
                label=f'r* = {r_star/r_s:.2f} r_s', zorder=5)
        ax.axvline(r_star / r_s, color='green', linestyle=':', alpha=0.3)
    
    # Labels and styling
    ax.set_xlabel('Radius (r / r_s)', fontsize=12)
    ax.set_ylabel('Time Dilation Factor D(r)', fontsize=12)
    ax.set_title('SSZ vs GR Time Dilation', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.1)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return fig


def gif_time_dilation(
    mass_range: List[float],
    output_path: str = "time_dilation.gif",
    duration: float = 0.2,
    **plot_kwargs
) -> None:
    """
    Create animated GIF of time dilation for different masses.
    
    Args:
        mass_range: List of masses (in solar masses)
        output_path: Output GIF path
        duration: Frame duration (seconds)
        **plot_kwargs: Arguments for plot_time_dilation
    """
    frames = []
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    for i, mass in enumerate(mass_range):
        r_s = schwarzschild_radius(mass * M_SUN)
        
        # Create frame
        temp_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
        fig = plot_time_dilation(r_s, save_path=temp_path, **plot_kwargs)
        plt.close(fig)
        
        # Read frame
        frames.append(imageio.imread(temp_path))
    
    # Save GIF
    imageio.mimsave(output_path, frames, duration=duration)
    print(f"Created GIF: {output_path}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    # Example usage
    r_s_sun = schwarzschild_radius(M_SUN)
    fig = plot_time_dilation(r_s_sun, show_intersection=True)
    plt.show()
