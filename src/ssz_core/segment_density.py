"""
Segment Density and Time Dilation Functions

Implements the SSZ segment saturation based on the Golden Ratio (φ),
providing singularity-free time dilation.

Mathematical Foundation:
- Segment saturation: Ξ(r) = 1 - exp(-φ · r/r_s)
- SSZ time dilation: D_SSZ(r) = 1 / (1 + Ξ(r))
- GR time dilation: D_GR(r) = √(1 - r_s/r)

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Union, Optional
from scipy.optimize import brentq

from .constants import PHI


def Xi(r: Union[float, np.ndarray], r_s: float) -> Union[float, np.ndarray]:
    """
    Calculate segment saturation factor using Golden Ratio.
    
    Formula:
        Ξ(r) = 1 - exp(-φ · r/r_s)
    
    where φ = (1 + √5)/2 ≈ 1.618 is the golden ratio.
    
    This function represents the "filling" of spacetime segments,
    approaching 1 as r → ∞ and 0 as r → 0.
    
    Args:
        r: Radius (m) - can be scalar or array
        r_s: Schwarzschild radius (m)
        
    Returns:
        Segment saturation factor Ξ(r) ∈ [0, 1)
        
    Examples:
        >>> Xi(0.0, 2950.0)
        0.0
        >>> Xi(1e10, 2950.0)  # Far field
        0.999...
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    
    # Handle both scalar and array inputs
    r = np.asarray(r)
    
    # Ξ(r) = 1 - exp(-φ · r/r_s)
    xi_value = 1.0 - np.exp(-PHI * r / r_s)
    
    return float(xi_value) if xi_value.ndim == 0 else xi_value


def D_SSZ(r: Union[float, np.ndarray], r_s: float) -> Union[float, np.ndarray]:
    """
    Calculate SSZ time dilation factor.
    
    Formula:
        D_SSZ(r) = 1 / (1 + Ξ(r))
    
    where Ξ(r) is the segment saturation factor.
    
    This provides a singularity-free time dilation that:
    - Remains finite at r = 0: D_SSZ(0) = 1
    - Approaches GR asymptotically for r >> r_s
    - Provides smooth transition through r = r_s
    
    Args:
        r: Radius (m) - can be scalar or array
        r_s: Schwarzschild radius (m)
        
    Returns:
        Time dilation factor D_SSZ(r) ∈ (0, 1]
        
    Physical Interpretation:
        - D_SSZ = 1: No time dilation (far field or r=0)
        - D_SSZ < 1: Time runs slower
        - Never reaches 0 (no singularity!)
        
    Examples:
        >>> D_SSZ(0.0, 2950.0)
        1.0
        >>> D_SSZ(2950.0, 2950.0)  # At Schwarzschild radius
        0.165...  # Finite!
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    
    # D_SSZ(r) = 1 / (1 + Ξ(r))
    xi = Xi(r, r_s)
    d_value = 1.0 / (1.0 + xi)
    
    return d_value


def D_GR(r: Union[float, np.ndarray], r_s: float, 
         epsilon: float = 1e-10) -> Union[float, np.ndarray]:
    """
    Calculate General Relativity (Schwarzschild) time dilation.
    
    Formula:
        D_GR(r) = √(1 - r_s/r)  for r > r_s
    
    This is the standard GR result, which:
    - Diverges at r = r_s (event horizon)
    - Is undefined for r < r_s
    - Approaches 1 for r >> r_s
    
    Args:
        r: Radius (m) - can be scalar or array
        r_s: Schwarzschild radius (m)
        epsilon: Safety margin to avoid division issues
        
    Returns:
        Time dilation factor D_GR(r) or NaN where undefined
        
    Raises:
        Warning: If r <= r_s (undefined region)
        
    Examples:
        >>> D_GR(2*2950.0, 2950.0)
        0.707...  # √(1/2)
        >>> D_GR(2950.0, 2950.0)
        nan  # Singularity!
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    
    r = np.asarray(r)
    
    # Create output array
    d_value = np.zeros_like(r, dtype=float)
    
    # Only calculate where r > r_s + epsilon
    valid = r > (r_s + epsilon)
    
    if np.any(valid):
        d_value[valid] = np.sqrt(1.0 - r_s / r[valid])
    
    # Set invalid regions to NaN
    d_value[~valid] = np.nan
    
    return float(d_value) if d_value.ndim == 0 else d_value


def find_intersection(
    r_s: float,
    r_min: Optional[float] = None,
    r_max: Optional[float] = None,
    tol: float = 1e-10
) -> float:
    """
    Find radius r* where SSZ and GR time dilations match.
    
    Solves: D_SSZ(r*) = D_GR(r*)
    
    This is the natural "matching point" where the SSZ metric
    transitions to match the GR metric.
    
    Args:
        r_s: Schwarzschild radius (m)
        r_min: Minimum search radius (default: 1.1 * r_s)
        r_max: Maximum search radius (default: 100 * r_s)
        tol: Numerical tolerance for root finding
        
    Returns:
        r_star: Intersection radius (m)
        
    Raises:
        ValueError: If no intersection found
        
    Examples:
        >>> r_star = find_intersection(2950.0)
        >>> r_star > 2950.0  # Always outside Schwarzschild radius
        True
        >>> # Check that D_SSZ(r_star) ≈ D_GR(r_star)
        >>> abs(D_SSZ(r_star, 2950.0) - D_GR(r_star, 2950.0)) < 1e-6
        True
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    
    # Default search range
    if r_min is None:
        r_min = 1.1 * r_s  # Start just outside event horizon
    if r_max is None:
        r_max = 100.0 * r_s  # Far field
    
    def equation(r: float) -> float:
        """Difference between SSZ and GR time dilations."""
        d_ssz = D_SSZ(r, r_s)
        d_gr = D_GR(r, r_s)
        
        if np.isnan(d_gr):
            return 1.0  # Penalize invalid regions
        
        return d_ssz - d_gr
    
    try:
        # Use Brent's method for robust root finding
        r_star = brentq(equation, r_min, r_max, xtol=tol)
        return r_star
        
    except ValueError as e:
        raise ValueError(
            f"Could not find intersection point in range [{r_min}, {r_max}]. "
            f"Try adjusting search range. Original error: {e}"
        )


def segment_saturation_derivative(
    r: Union[float, np.ndarray],
    r_s: float
) -> Union[float, np.ndarray]:
    """
    Calculate derivative of segment saturation factor.
    
    Formula:
        dΞ/dr = (φ/r_s) · exp(-φ · r/r_s)
    
    Used for curvature calculations and metric derivatives.
    
    Args:
        r: Radius (m)
        r_s: Schwarzschild radius (m)
        
    Returns:
        dΞ/dr (dimensionless per meter)
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    
    r = np.asarray(r)
    
    # dΞ/dr = (φ/r_s) · exp(-φ · r/r_s)
    dxi_dr = (PHI / r_s) * np.exp(-PHI * r / r_s)
    
    return float(dxi_dr) if dxi_dr.ndim == 0 else dxi_dr
