#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Pure - φ-Spiral Segmented Spacetime Metric

Pure Segmented Spacetime metric derived from φ-based spiral rotation.
Replaces curvature with discrete rotational segmentation of local frames.

================================================================================
MATHEMATICAL FORMULATION
================================================================================

Line Element (φ-Spiral Form):
    ds² = -c² sech²(φ_G(r)) dt² + 2c tanh(φ_G(r)) dt dr + dr²

Alternative Form:
    ds² = -c² (1 - β²(r)) dt² + 2β(r)c dt dr + dr²

Diagonal Form (time coordinate transformation):
    dT = dt - (β·γ²/c) dr  (eliminates cross term)
    
    ds² = -c²/γ² dT² + γ² dr²
    ds² = -c² sech²(φ_G) dT² + cosh²(φ_G) dr²
    
    Null geodesics: dr/dT = ±c/γ² = ±c·sech²(φ_G)

LaTeX Tensor Notation:
    g_μν = ⎡ -c²sech²(φ_G)   c·tanh(φ_G)      0           0        ⎤
           ⎢  c·tanh(φ_G)          1           0           0        ⎥
           ⎢      0                0          r²           0        ⎥
           ⎣      0                0           0      r²sin²θ       ⎦

Signature: (-,+,+,+)

where:
    φ_G(r) = local gravitational rotation angle (spiral phase)
    β(r) = tanh(φ_G(r)) = local velocity field
    γ(r) = cosh(φ_G(r)) = local rapidity factor

Lorentz-like Transformation:
    [ct']   [ cosh(φ_G)  -sinh(φ_G) ] [ct]
    [r' ] = [ -sinh(φ_G)  cosh(φ_G) ] [r ]

================================================================================
PHYSICAL INTERPRETATION
================================================================================

Key Features:
- NO singularities (space folds into subspace layers)
- Subspace transitions at Δφ_G = 2π
- Local light cone tilts instead of diverging
- Natural time dilation: dτ/dt = sech(φ_G(r))
- Spiral velocity: v_r(r) = c·tanh(φ_G(r))

Physical Meaning:
- Gravitational field = local rotation angle φ_G(r), NOT curvature
- Each 2π rotation creates a new Subspace Sheet
- No event horizon singularity, only periodic transitions
- Explains ANITA-type anomalies as phase tunneling
- Light propagation across φ_G = 2π boundaries → gravitational phase tunneling

Limits:
- φ_G(r) → 0: Recovers flat Minkowski spacetime
- φ_G(r) → large: Event-horizon-like time dilation WITHOUT singularity

================================================================================
EXTENSIONS
================================================================================

Optional generalizations:
1. φ_G(r,θ): Include spin or anisotropic mass distribution
2. φ_G(r,t): Gravitational waves as local rotation oscillations
3. φ_G(r,θ,φ,t): Full 4D time-dependent rotational field

================================================================================
SOURCES
================================================================================

- Casu & Wrede: Segmented Spacetime Theory
- φ-Spiral Framework: Pure geometric rotation model
- WindSurf Prompt: Complete implementation specification

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Tuple, Optional, Callable
from dataclasses import dataclass

# Golden Ratio (emerges naturally in SSZ)
PHI = (1.0 + np.sqrt(5.0)) / 2.0  # ≈ 1.618033988749895

# Physical constants
C_SI = 299792458.0  # Speed of light [m/s]
G_SI = 6.67430e-11  # Gravitational constant [m³/(kg·s²)]


@dataclass
class PhiSpiralMetricComponents:
    """Container for φ-Spiral metric components."""
    g_tt: float  # Time-time component
    g_tr: float  # Time-radial cross term (spiral structure!)
    g_rr: float  # Radial-radial component
    g_thth: float  # Angular theta component
    g_phph: float  # Angular phi component
    
    # Auxiliary fields
    phi_G: float  # Gravitational rotation angle
    beta: float  # Local velocity β = tanh(φ_G)
    gamma: float  # Lorentz-like factor γ = cosh(φ_G)
    v_r: float  # Spiral radial velocity v_r = c·β
    tau_factor: float  # Time dilation dτ/dt = sech(φ_G)


class PhiSpiralSSZMetric:
    """
    Pure φ-Spiral Segmented Spacetime Metric.
    
    Philosophy:
        Gravitational field encoded as LOCAL ROTATION ANGLE φ_G(r),
        not as spacetime curvature. Each full 2π rotation creates
        a new subspace layer instead of forming a singularity.
    
    Line Element:
        ds² = -c² sech²(φ_G) dt² + 2c tanh(φ_G) dt dr + dr²
    
    Lorentz-like Transformation:
        [ct']   [ cosh(φ_G)  -sinh(φ_G) ] [ct]
        [r' ] = [ -sinh(φ_G)  cosh(φ_G) ] [r ]
    
    Usage:
        >>> from ssz_metric_pure import PhiSpiralSSZMetric
        >>> metric = PhiSpiralSSZMetric(mass=1.989e30, k=1.0, r0=2950.0)
        >>> phi_G = metric.phi_G(r=10000.0)
        >>> print(f"Rotation angle: {phi_G:.6f} rad")
        >>> 
        >>> # Metric components
        >>> r = 5 * metric.r_s
        >>> comps = metric.metric_components(r)
        >>> print(f"Time dilation factor: {comps.tau_factor:.6f}")
    
    Coordinates:
        - (t, r, θ, φ) in spherical-like system
        - r: Radial coordinate [m]
        - θ: Polar angle [rad]
        - φ: Azimuthal angle [rad]
    """
    
    def __init__(
        self,
        mass: float,
        k: float = 1.0,
        r0: Optional[float] = None,
        phi_G_profile: Optional[Callable] = None
    ):
        """
        Initialize φ-Spiral SSZ metric.
        
        Args:
            mass: Central mass [kg]
            k: Spiral rotation strength parameter (dimensionless)
            r0: Characteristic radius scale [m] (default: r_s)
            phi_G_profile: Custom φ_G(r) function (default: logarithmic)
        
        Raises:
            ValueError: If mass is not positive
        """
        if mass <= 0:
            raise ValueError(f"Mass must be positive, got {mass}")
        
        self.M = mass
        self.k = k
        
        # Schwarzschild radius
        self.r_s = 2.0 * G_SI * self.M / (C_SI ** 2)
        
        # Characteristic radius (default to r_s)
        self.r0 = r0 if r0 is not None else self.r_s
        
        # φ_G profile function
        if phi_G_profile is not None:
            self._phi_G_func = phi_G_profile
        else:
            # Default: logarithmic profile
            # φ_G(r) = k·log(1 + r/r₀)
            self._phi_G_func = lambda r: self.k * np.log(1.0 + r / self.r0)
    
    # ========================================================================
    # φ_G GRAVITATIONAL ROTATION ANGLE
    # ========================================================================
    
    def phi_G(self, r: float) -> float:
        """
        Gravitational rotation angle φ_G(r).
        
        Default profile (logarithmic):
            φ_G(r) = k·log(1 + r/r₀)
        
        Physical Meaning:
            - φ_G = 0 at r = 0 (flat spacetime at center)
            - φ_G increases with depth into gravitational well
            - Each Δφ_G = 2π creates new subspace sheet
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            φ_G: Rotation angle [rad]
        """
        if r < 0:
            raise ValueError(f"Radius must be non-negative, got {r}")
        
        return self._phi_G_func(r)
    
    def dphi_G_dr(self, r: float, epsilon: float = 1e-6) -> float:
        """
        Radial derivative of φ_G(r).
        
        Computed via finite differences:
            dφ_G/dr ≈ [φ_G(r+ε) - φ_G(r-ε)] / (2ε)
        
        Args:
            r: Radial coordinate [m]
            epsilon: Finite difference step [m]
        
        Returns:
            dφ_G/dr [rad/m]
        """
        r_plus = r + epsilon
        r_minus = max(0, r - epsilon)
        
        phi_plus = self.phi_G(r_plus)
        phi_minus = self.phi_G(r_minus)
        
        return (phi_plus - phi_minus) / (r_plus - r_minus)
    
    def subspace_layer(self, r: float) -> int:
        """
        Subspace sheet number (counts 2π rotations).
        
        Formula:
            n = floor(φ_G(r) / 2π)
        
        Physical Meaning:
            - n = 0: Original spacetime layer
            - n = 1: First subspace layer (φ_G ∈ [2π, 4π))
            - n = 2: Second subspace layer (φ_G ∈ [4π, 6π))
            - etc.
        
        Returns:
            Subspace layer number (integer)
        """
        phi = self.phi_G(r)
        return int(np.floor(phi / (2.0 * np.pi)))
    
    # ========================================================================
    # LORENTZ-LIKE FIELDS
    # ========================================================================
    
    def beta(self, r: float) -> float:
        """
        Local velocity field β(r) = tanh(φ_G(r)).
        
        Physical Meaning:
            - β ∈ (-1, 1) always (bounded!)
            - β = 0 at r = 0 (no rotation at center)
            - β → ±1 for large |φ_G| (light speed approach)
        
        Returns:
            β: Dimensionless velocity field
        """
        phi = self.phi_G(r)
        return np.tanh(phi)
    
    def gamma(self, r: float) -> float:
        """
        Local Lorentz-like factor γ(r) = cosh(φ_G(r)).
        
        Relation to β:
            γ = 1 / √(1 - β²)
        
        Physical Meaning:
            - γ ≥ 1 always
            - γ = 1 at r = 0 (flat spacetime)
            - γ → ∞ for large |φ_G| (extreme rotation)
        
        Returns:
            γ: Lorentz-like factor (dimensionless)
        """
        phi = self.phi_G(r)
        return np.cosh(phi)
    
    def v_radial(self, r: float) -> float:
        """
        Spiral radial velocity field v_r(r) = c·tanh(φ_G(r)).
        
        Physical Meaning:
            - Radial component of spiral flow
            - v_r ∈ (-c, c) always (subluminal!)
            - Indicates "tilt" of local light cone
        
        Returns:
            v_r: Radial velocity [m/s]
        """
        return C_SI * self.beta(r)
    
    def time_dilation_factor(self, r: float) -> float:
        """
        Time dilation factor dτ/dt = sech(φ_G(r)).
        
        Physical Meaning:
            - dτ/dt = 1 at r = 0 (no dilation at center)
            - dτ/dt → 0 for large φ_G (extreme time dilation)
            - Proper time τ runs slower than coordinate time t
        
        Returns:
            dτ/dt: Time dilation factor (dimensionless)
        """
        phi = self.phi_G(r)
        # sech(φ) = 1/cosh(φ)
        return 1.0 / np.cosh(phi)
    
    # ========================================================================
    # METRIC COMPONENTS
    # ========================================================================
    
    def g_tt(self, r: float) -> float:
        """
        Time-time metric component.
        
        Formula:
            g_tt = -c² sech²(φ_G(r)) = -c² / cosh²(φ_G)
        
        Alternative form:
            g_tt = -c² (1 - β²(r))
        
        Properties:
            - g_tt < 0 always (timelike coordinate)
            - g_tt = -c² at r = 0 (flat spacetime)
            - g_tt → 0 for large φ_G (extreme dilation)
        
        Returns:
            g_tt [m²/s²]
        """
        phi = self.phi_G(r)
        sech_phi = 1.0 / np.cosh(phi)
        return -(C_SI ** 2) * (sech_phi ** 2)
    
    def g_tr(self, r: float) -> float:
        """
        Time-radial cross term (SPIRAL STRUCTURE!).
        
        Formula:
            g_tr = c·tanh(φ_G(r)) = c·β(r)
        
        Physical Meaning:
            - NON-ZERO off-diagonal term
            - Encodes spiral/helical geometry
            - Couples time and radial coordinates
            - Causes "frame mixing" (not frame dragging!)
        
        Returns:
            g_tr [m/s]
        """
        beta_val = self.beta(r)
        return C_SI * beta_val
    
    def g_rr(self, r: float) -> float:
        """
        Radial-radial metric component.
        
        Formula:
            g_rr = 1
        
        Remarks:
            - Constant = 1 (no radial warping in this formulation)
            - All dynamics in g_tt and g_tr
        
        Returns:
            g_rr (dimensionless)
        """
        return 1.0
    
    def g_thth(self, r: float) -> float:
        """
        Angular theta component.
        
        Formula:
            g_θθ = r²
        
        Standard spherical coordinate geometry.
        
        Returns:
            g_θθ [m²]
        """
        return r ** 2
    
    def g_phph(self, r: float, theta: float) -> float:
        """
        Angular phi component.
        
        Formula:
            g_φφ = r² sin²θ
        
        Standard spherical coordinate geometry.
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            g_φφ [m²]
        """
        return (r ** 2) * (np.sin(theta) ** 2)
    
    def metric_tensor(self, r: float, theta: float) -> np.ndarray:
        """
        Full 4×4 metric tensor g_μν.
        
        Matrix form:
            g_μν = [ g_tt   g_tr    0      0    ]
                   [ g_tr   g_rr    0      0    ]
                   [  0      0    g_θθ    0    ]
                   [  0      0      0    g_φφ  ]
        
        Signature: (-,+,+,+) (timelike, spacelike, spacelike, spacelike)
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            g: 4×4 numpy array with metric components
        """
        g = np.zeros((4, 4), dtype=float)
        
        # Diagonal components
        g[0, 0] = self.g_tt(r)
        g[1, 1] = self.g_rr(r)
        g[2, 2] = self.g_thth(r)
        g[3, 3] = self.g_phph(r, theta)
        
        # Off-diagonal (symmetric)
        g_tr_val = self.g_tr(r)
        g[0, 1] = g_tr_val
        g[1, 0] = g_tr_val
        
        return g
    
    def metric_components(self, r: float, theta: float = np.pi/2) -> PhiSpiralMetricComponents:
        """
        Compute all metric components and auxiliary fields.
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad] (default: equator)
        
        Returns:
            PhiSpiralMetricComponents dataclass with all fields
        """
        phi = self.phi_G(r)
        beta_val = self.beta(r)
        gamma_val = self.gamma(r)
        
        return PhiSpiralMetricComponents(
            g_tt=self.g_tt(r),
            g_tr=self.g_tr(r),
            g_rr=self.g_rr(r),
            g_thth=self.g_thth(r),
            g_phph=self.g_phph(r, theta),
            phi_G=phi,
            beta=beta_val,
            gamma=gamma_val,
            v_r=C_SI * beta_val,
            tau_factor=1.0 / gamma_val
        )
    
    # ========================================================================
    # PHYSICAL OBSERVABLES
    # ========================================================================
    
    def redshift(self, r: float) -> float:
        """
        Gravitational redshift z.
        
        Formula:
            z = √(-g_tt(∞)) / √(-g_tt(r)) - 1
        
        For this metric:
            z = cosh(φ_G(r)) - 1
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            z: Redshift (dimensionless)
        """
        return self.gamma(r) - 1.0
    
    def proper_time_ratio(self, r: float) -> float:
        """
        Ratio of proper time to coordinate time.
        
        Formula:
            dτ/dt = √(-g_tt) / c = sech(φ_G(r))
        
        Physical Meaning:
            - Clock at radius r runs slower by this factor
            - = 1 at r = 0 (no time dilation)
            - → 0 for large φ_G (extreme dilation)
        
        Returns:
            dτ/dt (dimensionless)
        """
        return self.time_dilation_factor(r)
    
    def light_cone_tilt(self, r: float) -> float:
        """
        Local light cone tilt angle α(r).
        
        The null geodesic dr/dt satisfies:
            g_tt + 2 g_tr (dr/dt) + g_rr (dr/dt)² = 0
        
        Solutions give light cone tilt in (t,r) plane.
        
        Returns:
            α: Tilt angle [rad]
        """
        g_tt_val = self.g_tt(r)
        g_tr_val = self.g_tr(r)
        g_rr_val = self.g_rr(r)
        
        # Solve quadratic: g_rr u² + 2 g_tr u + g_tt = 0
        # where u = dr/dt
        discriminant = (2 * g_tr_val)**2 - 4 * g_rr_val * g_tt_val
        
        if discriminant < 0:
            return np.nan
        
        u_plus = (-2*g_tr_val + np.sqrt(discriminant)) / (2*g_rr_val)
        
        # Tilt angle from vertical (t-axis)
        alpha = np.arctan(u_plus)
        
        return alpha
    
    # ========================================================================
    # LIMITS & VALIDATION
    # ========================================================================
    
    def schwarzschild_limit(self, r: float) -> Tuple[float, float]:
        """
        Compare with Schwarzschild metric in weak field limit.
        
        For small φ_G:
            sech²(φ_G) ≈ 1 - φ_G² + ...
            tanh(φ_G) ≈ φ_G - φ_G³/3 + ...
        
        Schwarzschild:
            g_tt^GR = -(1 - r_s/r)c²
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            (g_tt_SSZ, g_tt_GR): Tuple of SSZ and GR values
        """
        g_tt_ssz = self.g_tt(r)
        g_tt_gr = -(1.0 - self.r_s / r) * (C_SI ** 2)
        
        return (g_tt_ssz, g_tt_gr)
    
    def is_minkowski_at_center(self, r: float = 1e-10, tol: float = 1e-6) -> bool:
        """
        Verify flat spacetime at center (r → 0).
        
        Expected:
            φ_G(0) = 0
            g_tt(0) = -c²
            g_tr(0) = 0
            g_rr(0) = 1
        
        Args:
            r: Small radius to test [m]
            tol: Tolerance for comparison
        
        Returns:
            True if metric is Minkowski at center
        """
        phi = self.phi_G(r)
        g_tt_val = self.g_tt(r)
        g_tr_val = self.g_tr(r)
        
        minkowski_g_tt = -(C_SI ** 2)
        
        return (
            abs(phi) < tol and
            abs(g_tt_val - minkowski_g_tt) / abs(minkowski_g_tt) < tol and
            abs(g_tr_val) < tol
        )
    
    # ========================================================================
    # DIAGONAL FORM (Correct Coordinate Transformation)
    # ========================================================================
    
    def time_coordinate_transformation_factor(self, r: float) -> float:
        """
        Compute f(r) for time coordinate transformation.
        
        The cross term g_tr can be eliminated via:
            dT = dt + f(r) dr
        
        where:
            f(r) = g_tr / g_tt = -β·γ²/c
        
        Formula:
            f(r) = -β(r)·γ²(r) / c
                 = -tanh(φ_G)·cosh²(φ_G) / c
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            f(r): Time transformation factor [s/m]
        """
        beta = self.beta(r)
        gamma = self.gamma(r)
        
        # f = -β·γ²/c
        f = -(beta * gamma ** 2) / C_SI
        
        return f
    
    def diagonal_form_coefficients(self, r: float) -> Tuple[float, float]:
        """
        Compute CORRECT diagonal form metric coefficients.
        
        Via time coordinate transformation:
            dT = dt - (β·γ²/c) dr
        
        the metric becomes diagonal:
            ds² = -c²/γ² dT² + γ² dr²
        
        or equivalently:
            ds² = -c² sech²(φ_G) dT² + cosh²(φ_G) dr²
        
        Derivation:
            Starting from: ds² = -c²(1-β²)dt² + 2βc dt dr + dr²
            
            With dT = dt - (β·γ²/c) dr, we get:
                g_TT = -c²/γ² = -c² sech²(φ_G)
                g_Tr = 0  (cross term eliminated!)
                g_rr = γ² = cosh²(φ_G)
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            (g_TT, g_rr): Diagonal metric coefficients
        
        Physical Meaning:
            - g_TT < 0: Time component in eigentime coordinate T
            - g_rr > 0: Radial component (enhanced by γ²)
            - NO cross term: coordinates are orthogonal!
        
        Null Geodesics:
            0 = -c²/γ² dT² + γ² dr²
            ⟹ dr/dT = ±c/γ² = ±c·sech²(φ_G)
            
            → Light cone closes as φ_G increases!
        """
        phi = self.phi_G(r)
        gamma = self.gamma(r)
        
        # g_TT = -c²/γ² = -c² sech²(φ_G)
        g_TT = -(C_SI ** 2) / (gamma ** 2)
        
        # g_rr = γ² = cosh²(φ_G)
        g_rr = gamma ** 2
        
        return (g_TT, g_rr)
    
    def coordinate_time_to_eigentime(self, r_start: float, r_end: float, 
                                     n_points: int = 1000) -> float:
        """
        Integrate time transformation to get eigentime coordinate T.
        
        Formula:
            T = t - (1/c) ∫ β(ρ)·γ²(ρ) dρ
        
        This is globally integrable since f = f(r) only.
        
        Args:
            r_start: Starting radius [m]
            r_end: Ending radius [m]
            n_points: Number of integration points
        
        Returns:
            ΔT: Change in eigentime coordinate [s]
        
        Note:
            This gives T(r) - T(r_start) for fixed t.
        """
        r_vals = np.linspace(r_start, r_end, n_points)
        
        # Integrand: β(r)·γ²(r)
        integrand = np.array([
            self.beta(r) * (self.gamma(r) ** 2) 
            for r in r_vals
        ])
        
        # Numerical integration (trapezoidal rule)
        delta_T = -(1.0 / C_SI) * np.trapz(integrand, r_vals)
        
        return delta_T
    
    # ========================================================================
    # VISUALIZATION HELPERS
    # ========================================================================
    
    def spiral_embedding_2d(self, r_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        2D spiral embedding for visualization.
        
        Maps r → (x, y) in spiral coordinates:
            x = r · cos(φ_G(r))
            y = r · sin(φ_G(r))
        
        Args:
            r_array: Array of radial coordinates [m]
        
        Returns:
            (x, y): Cartesian coordinates for spiral plot
        
        Usage:
            >>> r_vals = np.linspace(0, 10*metric.r_s, 1000)
            >>> x, y = metric.spiral_embedding_2d(r_vals)
            >>> plt.plot(x, y)
            >>> plt.title("φ-Spiral Embedding")
        """
        phi_vals = np.array([self.phi_G(r) for r in r_array])
        
        x = r_array * np.cos(phi_vals)
        y = r_array * np.sin(phi_vals)
        
        return (x, y)
    
    def spiral_embedding_3d(
        self,
        r_array: np.ndarray,
        z_scale: float = 1.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        3D spiral embedding for visualization.
        
        Maps r → (x, y, z) in helical coordinates:
            x = r · cos(φ_G(r))
            y = r · sin(φ_G(r))
            z = z_scale · φ_G(r)
        
        Args:
            r_array: Array of radial coordinates [m]
            z_scale: Vertical scale factor for φ_G axis
        
        Returns:
            (x, y, z): 3D coordinates for helix plot
        
        Usage:
            >>> r_vals = np.linspace(0, 10*metric.r_s, 1000)
            >>> x, y, z = metric.spiral_embedding_3d(r_vals)
            >>> ax.plot3D(x, y, z)
            >>> ax.set_zlabel("φ_G / 2π (Subspace Layers)")
        """
        phi_vals = np.array([self.phi_G(r) for r in r_array])
        
        x = r_array * np.cos(phi_vals)
        y = r_array * np.sin(phi_vals)
        z = z_scale * phi_vals
        
        return (x, y, z)
    
    def plot_metric_components(self, r_min: float, r_max: float, n_points: int = 500):
        """
        Plot metric components g_tt, g_tr, g_rr vs. radius.
        
        Requires matplotlib. Returns figure object.
        
        Args:
            r_min: Minimum radius [m]
            r_max: Maximum radius [m]
            n_points: Number of plot points
        
        Returns:
            fig: Matplotlib figure object
        
        Example:
            >>> fig = metric.plot_metric_components(0.1*metric.r_s, 10*metric.r_s)
            >>> fig.savefig("metric_components.png")
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib required for plotting. Install via: pip install matplotlib")
        
        r_vals = np.linspace(r_min, r_max, n_points)
        g_tt_vals = np.array([self.g_tt(r) for r in r_vals])
        g_tr_vals = np.array([self.g_tr(r) for r in r_vals])
        g_rr_vals = np.array([self.g_rr(r) for r in r_vals])
        
        fig, axes = plt.subplots(3, 1, figsize=(10, 12))
        
        # g_tt
        axes[0].plot(r_vals / self.r_s, g_tt_vals / (C_SI**2), 'b-', linewidth=2)
        axes[0].set_ylabel(r"$g_{tt} / c^2$", fontsize=14)
        axes[0].set_title("Time-Time Component", fontsize=16)
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(y=-1, color='k', linestyle='--', alpha=0.3, label='Minkowski')
        axes[0].legend()
        
        # g_tr
        axes[1].plot(r_vals / self.r_s, g_tr_vals / C_SI, 'r-', linewidth=2)
        axes[1].set_ylabel(r"$g_{tr} / c$", fontsize=14)
        axes[1].set_title("Time-Radial Cross Term (Spiral!)", fontsize=16)
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3, label='No Spiral')
        axes[1].legend()
        
        # g_rr
        axes[2].plot(r_vals / self.r_s, g_rr_vals, 'g-', linewidth=2)
        axes[2].set_ylabel(r"$g_{rr}$", fontsize=14)
        axes[2].set_xlabel(r"$r / r_s$", fontsize=14)
        axes[2].set_title("Radial-Radial Component", fontsize=16)
        axes[2].grid(True, alpha=0.3)
        axes[2].axhline(y=1, color='k', linestyle='--', alpha=0.3, label='Flat')
        axes[2].legend()
        
        plt.tight_layout()
        return fig
    
    def plot_subspace_layers(self, r_min: float, r_max: float):
        """
        Visualize subspace layer transitions at Δφ_G = 2π.
        
        Args:
            r_min: Minimum radius [m]
            r_max: Maximum radius [m]
        
        Returns:
            fig: Matplotlib figure object
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib required for plotting.")
        
        r_vals = np.linspace(r_min, r_max, 2000)
        phi_vals = np.array([self.phi_G(r) for r in r_vals])
        layer_vals = np.array([self.subspace_layer(r) for r in r_vals])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # φ_G(r) with 2π boundaries
        ax1.plot(r_vals / self.r_s, phi_vals, 'b-', linewidth=2, label=r"$\phi_G(r)$")
        
        # Mark 2π boundaries
        max_layer = int(np.max(layer_vals)) + 1
        for n in range(max_layer + 1):
            ax1.axhline(y=n * 2 * np.pi, color='red', linestyle='--', alpha=0.5)
            ax1.text(0.02, n * 2 * np.pi + 0.3, f"Layer {n}", fontsize=10, color='red')
        
        ax1.set_ylabel(r"$\phi_G(r)$ [rad]", fontsize=14)
        ax1.set_title("Gravitational Rotation Angle with Subspace Layers", fontsize=16)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=12)
        
        # Subspace layer number
        ax2.plot(r_vals / self.r_s, layer_vals, 'g-', linewidth=2)
        ax2.set_xlabel(r"$r / r_s$", fontsize=14)
        ax2.set_ylabel("Subspace Layer Number", fontsize=14)
        ax2.set_title("Discrete Subspace Sheet Transitions", fontsize=16)
        ax2.grid(True, alpha=0.3)
        ax2.set_yticks(range(max_layer + 1))
        
        plt.tight_layout()
        return fig
    
    # ========================================================================
    # OPTIONAL EXTENSIONS (Placeholder Methods)
    # ========================================================================
    
    def phi_G_anisotropic(
        self,
        r: float,
        theta: float,
        anisotropy_func: Optional[Callable] = None
    ) -> float:
        """
        Extended φ_G(r,θ) with angular dependence.
        
        Formula:
            φ_G(r,θ) = φ_G(r) · f(θ)
        
        where f(θ) is an anisotropy function (default: uniform).
        
        Use cases:
            - Spinning/rotating mass distributions
            - Anisotropic pressure
            - Quadrupole moments
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
            anisotropy_func: Function f(θ), default = 1 (isotropic)
        
        Returns:
            φ_G(r,θ): Anisotropic gravitational angle [rad]
        
        Example:
            >>> # Oblate deformation
            >>> f_oblate = lambda theta: 1 + 0.1 * np.sin(theta)**2
            >>> phi_G_ext = metric.phi_G_anisotropic(r, theta, f_oblate)
        """
        phi_radial = self.phi_G(r)
        
        if anisotropy_func is None:
            return phi_radial
        
        f_theta = anisotropy_func(theta)
        return phi_radial * f_theta
    
    def phi_G_time_dependent(
        self,
        r: float,
        t: float,
        wave_func: Optional[Callable] = None
    ) -> float:
        """
        Extended φ_G(r,t) with time dependence.
        
        Formula:
            φ_G(r,t) = φ_G(r) + δφ(r,t)
        
        where δφ(r,t) represents gravitational wave perturbations
        as local rotation oscillations.
        
        Use cases:
            - Gravitational waves
            - Dynamical collapse
            - Oscillating fields
        
        Args:
            r: Radial coordinate [m]
            t: Time coordinate [s]
            wave_func: Function δφ(r,t), default = 0 (static)
        
        Returns:
            φ_G(r,t): Time-dependent gravitational angle [rad]
        
        Example:
            >>> # Sinusoidal GW perturbation
            >>> omega_gw = 2 * np.pi * 100  # 100 Hz
            >>> delta_phi = lambda r, t: 0.01 * np.sin(omega_gw * t) * np.exp(-r/r_gw)
            >>> phi_G_dyn = metric.phi_G_time_dependent(r, t, delta_phi)
        """
        phi_static = self.phi_G(r)
        
        if wave_func is None:
            return phi_static
        
        delta_phi = wave_func(r, t)
        return phi_static + delta_phi
    
    def __repr__(self):
        return (f"PhiSpiralSSZMetric(M={self.M:.3e} kg, k={self.k:.3f}, "
                f"r_s={self.r_s:.3e} m, r0={self.r0:.3e} m)")
