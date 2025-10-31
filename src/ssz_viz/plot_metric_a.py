"""
Metric Coefficient A(r) Visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from ..ssz_core.metric import A_safe, A_Xi, A_phi_series

def plot_metric_a(r_s, save_path=None, figsize=(10, 6)):
    """Plot A(r) coefficient."""
    r_values = np.linspace(0.01 * r_s, 10 * r_s, 1000)
    
    A_ssz = A_Xi(r_values, r_s)
    A_phi = A_phi_series(r_values, r_s, order=6)
    A_blend = A_safe(r_values, r_s)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(r_values / r_s, A_ssz, 'b-', label='A_Ξ (Inner SSZ)', linewidth=2)
    ax.plot(r_values / r_s, A_phi, 'r--', label='A_φ (Outer PN)', linewidth=2)
    ax.plot(r_values / r_s, A_blend, 'g-', label='A_safe (Blended)', linewidth=2.5)
    ax.axvline(1.0, color='gray', linestyle=':', alpha=0.5, label='r_s')
    ax.set_xlabel('r / r_s')
    ax.set_ylabel('A(r)')
    ax.set_title('SSZ Metric Coefficient A(r)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def gif_metric_a(*args, **kwargs):
    """GIF placeholder."""
    pass
