"""
Curvature Proxy Visualization

Plot curvature proxy showing singularity-free nature of SSZ.

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Union

from ..ssz_core.metric import A_safe


def curvature_proxy(
    r: Union[float, np.ndarray],
    A: Union[float, np.ndarray],
    epsilon: float = 1e-10
) -> Union[float, np.ndarray]:
    """
    Calculate curvature proxy (Kretschmann approximation).
    
    Formula:
        K_proxy(r) = ((1-A)/r²)² + (A'/r)²
    
    This approximates the Kretschmann scalar and shows curvature behavior.
    
    Args:
        r: Radius (m)
        A: Metric coefficient A(r)
        epsilon: Safety floor for r
        
    Returns:
        Curvature proxy (dimensionless)
    """
    r = np.maximum(np.asarray(r), epsilon)
    
    # First term: (1-A)/r²
    term1 = ((1.0 - A) / r**2) ** 2
    
    # Second term: (A'/r)² - approximate derivative
    if hasattr(r, '__len__'):
        # Numerical derivative for arrays
        dA_dr = np.gradient(A, r)
        term2 = (dA_dr / r) ** 2
    else:
        # For scalar, assume small contribution
        term2 = 0.0
    
    return term1 + term2


def plot_curvature(
    r_s: float,
    r_min: Optional[float] = None,
    r_max: Optional[float] = None,
    n_points: int = 1000,
    use_mirror_blend: bool = True,
    save_path: Optional[str] = None,
    figsize: tuple = (10, 6)
) -> plt.Figure:
    """
    Plot curvature proxy showing singularity-free SSZ.
    
    Args:
        r_s: Schwarzschild radius (m)
        r_min: Minimum radius (default: 0.01 * r_s)
        r_max: Maximum radius (default: 5 * r_s)
        n_points: Number of plot points
        use_mirror_blend: Use mirror blending
        save_path: Path to save figure
        figsize: Figure size
        
    Returns:
        fig: Matplotlib figure
    """
    if r_min is None:
        r_min = 0.01 * r_s
    if r_max is None:
        r_max = 5.0 * r_s
    
    # Create radius array
    r_values = np.linspace(r_min, r_max, n_points)
    
    # Calculate A(r)
    A_values = A_safe(r_values, r_s, use_mirror_blend=use_mirror_blend)
    
    # Calculate curvature proxy
    K_values = curvature_proxy(r_values, A_values)
    
    # Normalize to show structure
    K_normalized = K_values / (1.0 / r_s**2)
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(r_values / r_s, K_normalized, 'b-', linewidth=2.5, 
            label='SSZ Curvature Proxy')
    
    # Mark Schwarzschild radius
    ax.axvline(1.0, color='gray', linestyle=':', alpha=0.5, label='r_s')
    
    # Mark r=0 (no singularity!)
    ax.axvline(0.0, color='green', linestyle='--', alpha=0.3, 
               label='r=0 (Finite!)')
    
    # Labels
    ax.set_xlabel('Radius (r / r_s)', fontsize=12)
    ax.set_ylabel('Normalized Curvature Proxy', fontsize=12)
    ax.set_title('SSZ Curvature: Singularity-Free at r=0', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return fig


if __name__ == "__main__":
    from ..ssz_core.metric import schwarzschild_radius
    from ..ssz_core.constants import M_SUN
    
    r_s_sun = schwarzschild_radius(M_SUN)
    fig = plot_curvature(r_s_sun)
    plt.show()
