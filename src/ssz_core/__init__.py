"""
SSZ Core - Segmented Spacetime Z-Metric Core Module

This package implements the pure SSZ (Segmented Spacetime Z-Metric) formalism,
combining the best components from ssz-full-metric and ssz-metric-final.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

__version__ = "1.0.0"
__author__ = "Carmen Wrede & Lino Casu"

from .segment_density import (
    Xi,
    D_SSZ,
    D_GR,
    find_intersection,
)

from .metric import (
    A_Xi,
    A_phi_series,
    A_blended,
    A_safe,
    delta_M,
    corrected_r_s,
    metric_tensor,
)

from .constants import (
    PHI,
    C,
    G,
    M_SUN,
    R_SUN,
)

__all__ = [
    # Segment density
    "Xi",
    "D_SSZ",
    "D_GR",
    "find_intersection",
    # Metric components
    "A_Xi",
    "A_phi_series",
    "A_blended",
    "A_safe",
    "delta_M",
    "corrected_r_s",
    "metric_tensor",
    # Constants
    "PHI",
    "C",
    "G",
    "M_SUN",
    "R_SUN",
]
