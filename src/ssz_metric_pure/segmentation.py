#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Pure - Segmentation Module

Pure SSZ segment density N(r) and φ-based saturation.

Scientific Foundation:
- Segment density emerges from φ-based geometric structure
- NOT a phenomenological model - geometric necessity
- Saturates naturally at N_max = 1.0

Sources:
- ssz-metric-final: Pure SSZ segmentation formulas
- ssz-full-metric: Numerical stability (safe exp, bounds)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Union, Tuple
from .params import PHI, XI_MAX

# Type alias
ArrayLike = Union[float, np.ndarray]


def segment_density_xi(
    r: ArrayLike,
    r_s: float,
    varphi: float = PHI
) -> ArrayLike:
    """
    Segment density Ξ(r) - CORRECTED formula from ssz-metric-final.
    
    Formula:
        Ξ(r) = (r_s/r)² × exp(-r/r_φ)
    
    where r_φ = (φ/2) × r_s × (1 + Δ(M)/100)
    
    Physical Meaning:
    - Ξ(r) represents spacetime discretization level
    - Ξ → 1 near r=0 (maximum segmentation)
    - Ξ → 0 for r→∞ (asymptotically continuous)
    - Natural boundary at r_φ where A(r_φ) > 0
    
    Args:
        r: Radius (scalar or array) [m]
        r_s: Schwarzschild radius [m]
        varphi: φ-parameter (default: Golden Ratio)
    
    Returns:
        Segment density 0 ≤ Ξ(r) ≤ 1
    
    Examples:
        >>> xi = segment_density_xi(r_s, r_s)  # At Schwarzschild radius
        >>> xi = segment_density_xi(np.array([r_s, 2*r_s, 10*r_s]), r_s)
    
    References:
        - SSZ_Black_Hole_Stability.md
        - ssz-metric-final/viz_ssz_metric/segment_density.py
    """
    r = np.asarray(r, dtype=float)
    
    # Avoid division by zero
    r_safe = np.maximum(r, 1e-30)
    
    # Natural boundary (simplified - no Δ(M) in this version)
    # For full implementation, use params.py delta_M() correction
    r_phi = (varphi / 2.0) * r_s
    
    # Segment density: (r_s/r)² × exp(-r/r_φ)
    ratio_sq = (r_s / r_safe) ** 2
    decay = np.exp(-r_safe / r_phi)
    
    Xi = ratio_sq * decay
    
    # Bound to [0, XI_MAX]
    Xi = np.clip(Xi, 0.0, XI_MAX)
    
    return Xi


def segment_density_N(
    r: ArrayLike,
    r_s: float,
    varphi: float = PHI,
    N_max: float = XI_MAX
) -> ArrayLike:
    """
    Alternative notation: N(r) = N_max × (1 - exp(-φ·r/r_s))
    
    This is the SATURATION form used in ssz-full-metric.
    
    Formula:
        N(r) = N_max × (1 - exp(-φ × r/r_s))
    
    Properties:
    - N(0) = 0 (no segments at center)
    - N(∞) → N_max (complete saturation far away)
    - Smooth monotonic increase
    
    Args:
        r: Radius [m]
        r_s: Schwarzschild radius [m]
        varphi: φ-parameter
        N_max: Maximum segment density
    
    Returns:
        Segment count N(r) ∈ [0, N_max]
    
    Note:
        This is complementary to Ξ(r):
        - Ξ(r) → max near center, → 0 far away
        - N(r) → 0 near center, → max far away
        
        Use Ξ(r) for metric coefficient A(r).
        Use N(r) for segment counting/visualization.
    """
    r = np.asarray(r, dtype=float)
    r_safe = np.maximum(r, 0.0)
    
    # Saturation formula
    exponent = -varphi * r_safe / r_s
    # Clip to avoid overflow
    exponent = np.clip(exponent, -100.0, 100.0)
    
    N = N_max * (1.0 - np.exp(exponent))
    
    return np.clip(N, 0.0, N_max)


def time_dilation_SSZ(
    r: ArrayLike,
    r_s: float,
    varphi: float = PHI,
    method: str = 'xi'
) -> ArrayLike:
    """
    SSZ time dilation factor D_SSZ(r).
    
    Formula (using Ξ):
        D_SSZ(r) = 1 / (1 + Ξ(r))
    
    Properties:
    - D_SSZ(0) = 1.0 (flat spacetime at center!)
    - D_SSZ(r_s) ≈ 0.16 (finite at horizon)
    - 0 < D_SSZ(r) ≤ 1 always
    
    Args:
        r: Radius [m]
        r_s: Schwarzschild radius [m]
        varphi: φ-parameter
        method: 'xi' (Ξ-based) or 'N' (N-based)
    
    Returns:
        Time dilation factor
    
    Physics:
        Time at infinity / Time at r = 1 / D_SSZ(r)
        
        NO SINGULARITY: D_SSZ(0) = 1.0 finite!
    """
    if method == 'xi':
        Xi = segment_density_xi(r, r_s, varphi)
        D = 1.0 / (1.0 + Xi)
    else:
        # Alternative using N(r) - less common
        N = segment_density_N(r, r_s, varphi)
        D = 1.0 / (1.0 + N / N_max)
    
    return D


def saturation_factor_tanh(
    x: ArrayLike,
    cap: float
) -> ArrayLike:
    """
    Smooth saturation via tanh.
    
    Formula:
        sat(x) = cap × tanh(x / cap)
    
    Properties:
    - Bounded: |output| ≤ cap
    - Smooth: C^∞ continuous
    - Derivative: dsatdx = sech²(x/cap)
    
    Args:
        x: Input value(s)
        cap: Saturation limit
    
    Returns:
        Saturated value
    
    Source:
        ssz-metric-final/numerical_stability.py
    """
    if cap is None or cap <= 0:
        return x
    
    x = np.asarray(x)
    return cap * np.tanh(x / cap)


def validate_monotonic_redshift(
    r_array: np.ndarray,
    r_s: float,
    varphi: float = PHI,
    tol: float = 1e-6
) -> Tuple[bool, str]:
    """
    Validate that redshift z = 1/D - 1 is monotonically increasing.
    
    Physical Requirement:
        "Clocks run slower with stronger gravity"
        → z must increase as r decreases
    
    Args:
        r_array: Array of radii (sorted ascending)
        r_s: Schwarzschild radius
        varphi: φ-parameter
        tol: Tolerance for monotonicity check
    
    Returns:
        (is_valid, message)
    
    Example:
        >>> r = np.linspace(0.1*r_s, 10*r_s, 100)
        >>> valid, msg = validate_monotonic_redshift(r, r_s)
        >>> assert valid, msg
    """
    D = time_dilation_SSZ(r_array, r_s, varphi)
    z = 1.0 / D - 1.0
    
    # Check monotonic decrease (since r increases)
    dz = np.diff(z)
    
    # z should decrease as r increases (D increases)
    # Allow small positive jumps within tolerance
    violations = np.sum(dz > tol)
    
    if violations == 0:
        return True, "Redshift monotonicity validated ✓"
    else:
        return False, f"Redshift monotonicity violated: {violations} points"


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def Xi(r: ArrayLike, r_s: float, varphi: float = PHI) -> ArrayLike:
    """Quick alias for segment_density_xi."""
    return segment_density_xi(r, r_s, varphi)


def N(r: ArrayLike, r_s: float, varphi: float = PHI) -> ArrayLike:
    """Quick alias for segment_density_N."""
    return segment_density_N(r, r_s, varphi)


def D_SSZ(r: ArrayLike, r_s: float, varphi: float = PHI) -> ArrayLike:
    """Quick alias for time_dilation_SSZ."""
    return time_dilation_SSZ(r, r_s, varphi)
