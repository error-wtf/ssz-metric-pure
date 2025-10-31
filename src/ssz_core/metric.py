"""
SSZ Metric Tensor Components

Implements the complete SSZ metric with:
- Inner solution (segment saturation)
- Outer solution (φ-series/PN expansion)
- Mirror blending (optional smooth transition)
- Δ(M) mass correction
- Full metric tensor export

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Union, Tuple, Optional
import warnings

from .constants import PHI, C, G
from .segment_density import Xi, D_SSZ, D_GR, find_intersection


# φ-Series coefficients (from golden ratio recursion)
# Based on PN expansion: A_φ(r) = Σ ε_n (r_s/2r)^n
EPSILON_COEFFICIENTS = {
    0: 1.0,
    1: -2.0,
    2: 2.0,
    3: -PHI,  # Golden ratio contribution
    4: PHI**2 / 2.0,
    5: -PHI**3 / 6.0,
    6: PHI**4 / 24.0,
}


def delta_M(r_s: float, r_s_min: float = 1e-50, r_s_max: float = 1.0) -> float:
    """
    Calculate Δ(M) mass correction factor.
    
    Empirical formula that scales r_s based on mass:
        Δ(M) ≈ 100 for small masses (r_s → 0)
        Δ(M) ≈ 2 for large masses (r_s → ∞)
    
    Formula (empirical fit):
        Δ(M) = 2 + 98 · exp(-10 · r_s)
    
    Args:
        r_s: Schwarzschild radius (m)
        r_s_min: Minimum r_s for numerical stability
        r_s_max: Maximum r_s for scaling
        
    Returns:
        Δ(M): Correction factor ∈ [~2, ~100]
        
    Examples:
        >>> delta_M(1e-50)  # Small mass
        99.97...
        >>> delta_M(1.0)  # Large mass
        2.00...
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    
    # Empirical formula
    # For very small r_s: Δ → 100
    # For large r_s: Δ → 2
    delta = 2.0 + 98.0 * np.exp(-10.0 * r_s / r_s_max)
    
    return float(delta)


def corrected_r_s(r_s: float) -> float:
    """
    Apply Δ(M) correction to Schwarzschild radius.
    
    Formula:
        r_s_corrected = r_s · Δ(M)
    
    Args:
        r_s: Original Schwarzschild radius (m)
        
    Returns:
        Corrected Schwarzschild radius (m)
        
    Examples:
        >>> r_s_orig = 2950.0  # Solar mass
        >>> r_s_corr = corrected_r_s(r_s_orig)
        >>> r_s_corr > r_s_orig  # Correction typically increases r_s
        True
    """
    delta = delta_M(r_s)
    return r_s * delta


def A_Xi(r: Union[float, np.ndarray], r_s: float) -> Union[float, np.ndarray]:
    """
    Inner SSZ metric coefficient based on segment saturation.
    
    Formula:
        A_Ξ(r) = (1 + Ξ(r))^(-2) = D_SSZ(r)^2
    
    This is the singularity-free inner solution.
    
    Args:
        r: Radius (m)
        r_s: Schwarzschild radius (m)
        
    Returns:
        A_Ξ(r): Metric coefficient ∈ (0, 1]
        
    Physical Meaning:
        - A_Ξ(0) = 1 (flat spacetime at center!)
        - A_Ξ(r_s) ≈ 0.165 (finite!)
        - A_Ξ(∞) → 0 (approaches GR)
        
    Examples:
        >>> A_Xi(0.0, 2950.0)
        1.0
        >>> A_Xi(2950.0, 2950.0) < 1.0
        True
    """
    d_ssz = D_SSZ(r, r_s)
    return d_ssz ** 2


def A_phi_series(
    r: Union[float, np.ndarray],
    r_s: float,
    order: int = 6
) -> Union[float, np.ndarray]:
    """
    Outer metric coefficient using φ-series (PN expansion).
    
    Formula:
        A_φ(r) = Σ_{n=0}^N ε_n (r_s/2r)^n
    
    where ε_n are the φ-series coefficients.
    
    Args:
        r: Radius (m)
        r_s: Schwarzschild radius (m)
        order: Expansion order (0-6)
        
    Returns:
        A_φ(r): Metric coefficient
        
    Notes:
        - order=0: Minkowski (A=1)
        - order=1: Newtonian (A=1-r_s/r)
        - order=2+: Post-Newtonian corrections
        - order=6: Includes φ^4 term
        
    Examples:
        >>> A_phi_series(1e10, 2950.0, order=1)  # Far field, Newtonian
        0.9997...
    """
    if r_s <= 0:
        raise ValueError(f"Schwarzschild radius must be positive, got {r_s}")
    if order < 0 or order > 6:
        raise ValueError(f"Order must be 0-6, got {order}")
    
    r = np.asarray(r)
    
    # Initialize with first term (ε₀ = 1)
    A = np.ones_like(r, dtype=float)
    
    # Add higher-order terms
    x = r_s / (2.0 * r)  # Expansion parameter
    
    for n in range(1, order + 1):
        if n in EPSILON_COEFFICIENTS:
            A += EPSILON_COEFFICIENTS[n] * (x ** n)
    
    return float(A) if A.ndim == 0 else A


def A_blended(
    r: Union[float, np.ndarray],
    r_s: float,
    r_star: Optional[float] = None,
    blend_width: float = 0.1,
    mode: str = "O6"
) -> Union[float, np.ndarray]:
    """
    Blended metric coefficient (SSZ inner + φ-series outer).
    
    Uses tanh-based smooth transition between:
    - Inner: A_Ξ(r) for r < r*
    - Outer: A_φ(r) for r > r*
    
    Formula:
        h(r) = 0.5 · (1 - tanh((r - r*) / Δ))
        A_blend(r) = h(r) · A_Ξ(r) + (1-h(r)) · A_φ(r)
    
    Args:
        r: Radius (m)
        r_s: Schwarzschild radius (m)
        r_star: Transition radius (default: auto-find intersection)
        blend_width: Transition width parameter (0-1)
        mode: Metric mode - "O6" (order 6) or "O1" (Newtonian)
        
    Returns:
        A_blend(r): Blended metric coefficient
        
    Examples:
        >>> A_blended(0.0, 2950.0)  # Inner region
        1.0
        >>> A_blended(1e10, 2950.0)  # Outer region
        0.9997...  # Matches GR
    """
    if r_star is None:
        r_star = find_intersection(r_s)
    
    # Determine PN order
    order = 6 if mode == "O6" else 1
    
    # Calculate inner and outer metrics
    A_inner = A_Xi(r, r_s)
    A_outer = A_phi_series(r, r_s, order=order)
    
    # Blending function (tanh transition)
    Delta = blend_width * r_star
    h = 0.5 * (1.0 - np.tanh((r - r_star) / Delta))
    
    # Blend
    A = h * A_inner + (1.0 - h) * A_outer
    
    return A


def A_safe(
    r: Union[float, np.ndarray],
    r_s: float,
    r_star: Optional[float] = None,
    blend_width: float = 0.1,
    epsilon: float = 1e-10,
    beta: float = 100.0,
    use_mirror_blend: bool = True
) -> Union[float, np.ndarray]:
    """
    Safe metric coefficient with mirror blending and softplus floor.
    
    This is the most robust implementation, ensuring:
    - Smooth SSZ/GR transition (mirror blend)
    - Positive values everywhere (softplus)
    - Numerical stability (epsilon floor)
    
    Formula:
        A_mix(r) = mirror_blend(A_SSZ, A_GR)
        A_safe(r) = ε + (1/β) · ln(1 + exp(β·(A_mix - ε)))
    
    Args:
        r: Radius (m)
        r_s: Schwarzschild radius (m)
        r_star: Transition radius (default: auto-find)
        blend_width: Transition width (0-1)
        epsilon: Softplus floor (prevents A → 0)
        beta: Softplus steepness (higher = sharper)
        use_mirror_blend: Use mirror blending (default: True)
        
    Returns:
        A_safe(r): Safe metric coefficient > 0
        
    Notes:
        If use_mirror_blend=False, uses standard A_blended instead.
        
    Examples:
        >>> A_safe(0.0, 2950.0)
        1.0
        >>> A_safe(2950.0, 2950.0) > 0  # Always positive!
        True
    """
    if use_mirror_blend:
        # Mirror blend: mix SSZ and GR with tanh
        if r_star is None:
            r_star = find_intersection(r_s)
        
        A_ssz = A_Xi(r, r_s)
        A_gr = 1.0 - r_s / np.maximum(r, r_s + epsilon)  # GR (Schwarzschild)
        
        # Blending function
        Delta = blend_width * r_star
        h = 0.5 * (1.0 - np.tanh((r - r_star) / Delta))
        
        # Mix
        A_mix = h * A_ssz + (1.0 - h) * A_gr
    else:
        # Use standard blending
        A_mix = A_blended(r, r_s, r_star, blend_width)
    
    # Apply softplus for safety: A_safe = ε + (1/β)·ln(1 + exp(β·(A_mix - ε)))
    A_safe_value = epsilon + (1.0 / beta) * np.log1p(np.exp(beta * (A_mix - epsilon)))
    
    return A_safe_value


def B_coefficient(
    r: Union[float, np.ndarray],
    r_s: float,
    A: Optional[Union[float, np.ndarray]] = None
) -> Union[float, np.ndarray]:
    """
    Calculate radial metric coefficient B(r).
    
    For SSZ metric with spherical symmetry:
        B(r) = 1 / A(r)
    
    Args:
        r: Radius (m)
        r_s: Schwarzschild radius (m)
        A: Pre-calculated A(r) (optional, will compute if None)
        
    Returns:
        B(r): Radial metric coefficient
        
    Examples:
        >>> B_coefficient(1e10, 2950.0)
        1.0003...  # Inverse of A
    """
    if A is None:
        A = A_safe(r, r_s)
    
    # Avoid division by zero
    epsilon = 1e-10
    B = 1.0 / np.maximum(A, epsilon)
    
    return B


def metric_tensor(
    r: float,
    theta: float,
    r_s: float,
    use_mirror_blend: bool = True
) -> Tuple[np.ndarray, dict]:
    """
    Calculate full SSZ metric tensor g_μν.
    
    Metric in spherical coordinates (t, r, θ, φ):
        ds² = -A(r) dt² + B(r) dr² + r² dθ² + r² sin²θ dφ²
    
    where:
        - A(r): Time coefficient (from SSZ)
        - B(r) = 1/A(r): Radial coefficient
        - Angular terms: standard spherical
    
    Args:
        r: Radius (m)
        theta: Polar angle (radians)
        r_s: Schwarzschild radius (m)
        use_mirror_blend: Use mirror blending for A(r)
        
    Returns:
        g: 4×4 metric tensor (diagonal)
        components: Dict with individual components
        
    Examples:
        >>> g, comps = metric_tensor(1e10, np.pi/2, 2950.0)
        >>> g.shape
        (4, 4)
        >>> comps['g_tt'] < 0  # Time component negative
        True
    """
    # Calculate A(r)
    A = A_safe(r, r_s, use_mirror_blend=use_mirror_blend)
    B = B_coefficient(r, r_s, A=A)
    
    # Build diagonal metric tensor
    g = np.diag([
        -A,  # g_tt
        B,   # g_rr
        r**2,  # g_θθ
        r**2 * np.sin(theta)**2  # g_φφ
    ])
    
    # Components dict
    components = {
        'g_tt': -A,
        'g_rr': B,
        'g_theta_theta': r**2,
        'g_phi_phi': r**2 * np.sin(theta)**2,
        'A': A,
        'B': B,
        'r': r,
        'theta': theta,
    }
    
    return g, components


def schwarzschild_radius(mass: float) -> float:
    """
    Calculate Schwarzschild radius for given mass.
    
    Formula:
        r_s = 2GM/c²
    
    Args:
        mass: Mass (kg)
        
    Returns:
        r_s: Schwarzschild radius (m)
        
    Examples:
        >>> from .constants import M_SUN
        >>> schwarzschild_radius(M_SUN)
        2952.9...
    """
    if mass <= 0:
        raise ValueError(f"Mass must be positive, got {mass}")
    
    return 2.0 * G * mass / (C ** 2)
