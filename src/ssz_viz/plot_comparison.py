"""
SSZ vs GR Comparison Plots
"""

import numpy as np
import matplotlib.pyplot as plt
from ..ssz_core.segment_density import D_SSZ, D_GR
from ..ssz_core.metric import A_safe

def plot_ssz_vs_gr(r_s, save_path=None, figsize=(12, 5)):
    """Side-by-side comparison of SSZ and GR."""
    r_values = np.linspace(0.01 * r_s, 10 * r_s, 1000)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Time dilation comparison
    d_ssz = D_SSZ(r_values, r_s)
    d_gr = D_GR(r_values, r_s)
    
    ax1.plot(r_values / r_s, d_ssz, 'b-', label='SSZ', linewidth=2.5)
    ax1.plot(r_values / r_s, d_gr, 'r--', label='GR', linewidth=2)
    ax1.axvline(1.0, color='gray', linestyle=':', alpha=0.5)
    ax1.set_xlabel('r / r_s')
    ax1.set_ylabel('D(r)')
    ax1.set_title('Time Dilation')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Metric coefficient comparison
    A_ssz = A_safe(r_values, r_s)
    A_gr = 1.0 - r_s / np.maximum(r_values, r_s)
    
    ax2.plot(r_values / r_s, A_ssz, 'b-', label='SSZ', linewidth=2.5)
    ax2.plot(r_values / r_s, A_gr, 'r--', label='GR', linewidth=2)
    ax2.axvline(1.0, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel('r / r_s')
    ax2.set_ylabel('A(r)')
    ax2.set_title('Metric Coefficient')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig
