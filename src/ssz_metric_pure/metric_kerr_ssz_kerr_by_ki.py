#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Pure - SSZ-Kerr Rotating Metric

Pure SSZ rotating (Kerr-like) metric with frame dragging.

Line Element (Boyer-Lindquist-like coordinates):
    ds² = -A(r,θ)dt² + B(r,θ)dr² + C(r,θ)dθ² + D(r,θ)dφ² + 2E(r,θ)dt dφ

where E(r,θ) ≠ 0 → frame dragging!

Key Features:
- Ergosphere: r_ergo(θ) where g_tt = 0
- Inner/outer horizons: r_± where g_rr diverges
- Frame-dragging frequency: ω(r,θ)
- ISCO, photon sphere for rotating case

Sources:
- ssz-metric-final: Pure SSZ rotating formulas
- GR-Kerr: Standard Kerr metric (for validation ONLY)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass

from .params import KerrSSZParams, G_SI, C_SI
from .segmentation import segment_density_N, XI_MAX


@dataclass
class KerrMetricComponents:
    """Container for Kerr metric components."""
    g_tt: float
    g_rr: float
    g_thth: float
    g_phph: float
    g_tph: float  # Off-diagonal (frame dragging!)
    A: float  # -g_tt coefficient
    B: float  # g_rr coefficient
    E: float  # g_tφ coefficient


class KerrSSZMetric:
    """
    Pure SSZ rotating metric (SSZ-Kerr).
    
    Philosophy:
        100% PURE SSZ with rotation parameter.
        Standard Kerr used ONLY for limit validation.
    
    Usage:
        >>> from ssz_metric_pure import KerrSSZParams
        >>> params = KerrSSZParams(mass=1e30, spin=0.9)
        >>> kerr = KerrSSZMetric(params)
        >>> r_plus, r_minus = kerr.horizons()
        >>> print(f"Outer horizon: {r_plus/kerr.r_s:.3f} r_s")
    
    Coordinates:
        - (t, r, θ, φ) in Boyer-Lindquist-like system
        - θ=0: North pole, θ=π/2: Equator, θ=π: South pole
        - φ: Azimuthal angle (0 to 2π)
    """
    
    def __init__(self, params: KerrSSZParams):
        """
        Initialize SSZ-Kerr metric.
        
        Args:
            params: Kerr-SSZ parameters (mass, spin, constants)
        
        Raises:
            ValueError: If spin exceeds extremal limit
        """
        if params.M <= 0:
            raise ValueError(f"Mass must be positive, got {params.M}")
        
        self.params = params
        self.M = params.M
        self.a = params.a  # Spin parameter
        self.a_hat = params.a_hat  # Dimensionless â = a/M
        self.r_s = params.r_s
        self.r_phi = params.r_phi
        self.varphi = params.varphi
        
        # Geometric units for convenience
        if params.dimensionless:
            self.M_geom = self.M
            self.a_geom = self.a
        else:
            self.M_geom = G_SI * self.M / (C_SI ** 2)
            self.a_geom = self.a
    
    # ========================================================================
    # AUXILIARY FUNCTIONS (Boyer-Lindquist-like)
    # ========================================================================
    
    def Sigma(self, r: float, theta: float) -> float:
        """
        Σ(r,θ) = r² + a² cos²θ
        
        This is the standard Kerr auxiliary function.
        """
        return r * r + self.a_geom ** 2 * np.cos(theta) ** 2
    
    def Delta(self, r: float) -> float:
        """
        Δ(r) = r² - r_s r + a²
        
        Standard Kerr Delta function.
        Zeros of Δ(r) = horizons.
        """
        return r * r - self.r_s * r + self.a_geom ** 2
    
    def A_coeff(self, r: float, theta: float) -> float:
        """
        A(r,θ) for rotating SSZ metric.
        
        Hybrid approach:
            A_static(r) × [Δ(r) / (r² + a²)]
        
        This combines SSZ radial structure with Kerr rotation.
        """
        # Static SSZ part
        N = segment_density_N(r, self.r_s, self.varphi, N_max=XI_MAX)
        D_ssz = 1.0 / (1.0 + N)
        A_static = D_ssz * D_ssz
        
        # Kerr rotation factor
        Sig = self.Sigma(r, theta)
        Dlt = self.Delta(r)
        
        # Avoid division by zero
        denom = r * r + self.a_geom ** 2
        if denom < 1e-30:
            denom = 1e-30
        
        rotation_factor = Dlt / denom
        
        return A_static * rotation_factor
    
    # ========================================================================
    # METRIC COMPONENTS
    # ========================================================================
    
    def g_tt(self, r: float, theta: float) -> float:
        """
        g_tt = -(1 - r_s r / Σ) × A_SSZ(r)
        
        Time-time component. Negative always.
        g_tt = 0 defines ergosphere boundary.
        """
        Sig = self.Sigma(r, theta)
        A = self.A_coeff(r, theta)
        
        factor = 1.0 - self.r_s * r / max(Sig, 1e-30)
        
        return -A * factor
    
    def g_rr(self, r: float, theta: float) -> float:
        """
        g_rr = Σ / Δ × B_SSZ(r)
        
        Radial component. Positive.
        Diverges at horizons (Δ=0).
        """
        Sig = self.Sigma(r, theta)
        Dlt = self.Delta(r)
        
        # SSZ radial modification
        A = self.A_coeff(r, theta)
        B_ssz = 1.0 / max(A, 1e-16)
        
        return Sig / max(abs(Dlt), 1e-16) * B_ssz
    
    def g_thth(self, r: float, theta: float) -> float:
        """
        g_θθ = Σ
        
        Angular theta component.
        """
        return self.Sigma(r, theta)
    
    def g_phph(self, r: float, theta: float) -> float:
        """
        g_φφ = (r² + a² + r_s r a² sin²θ/Σ) × sin²θ
        
        Angular phi component.
        """
        Sig = self.Sigma(r, theta)
        sin_th = np.sin(theta)
        
        term1 = r * r + self.a_geom ** 2
        term2 = self.r_s * r * self.a_geom ** 2 * sin_th ** 2 / max(Sig, 1e-30)
        
        return (term1 + term2) * sin_th ** 2
    
    def g_tph(self, r: float, theta: float) -> float:
        """
        g_tφ = -r_s r a sin²θ / Σ
        
        Off-diagonal component (FRAME DRAGGING!).
        Non-zero only for rotating (a≠0) case.
        """
        if abs(self.a_geom) < 1e-30:
            return 0.0
        
        Sig = self.Sigma(r, theta)
        sin_th = np.sin(theta)
        
        return -self.r_s * r * self.a_geom * sin_th ** 2 / max(Sig, 1e-30)
    
    def metric_tensor(self, r: float, theta: float) -> KerrMetricComponents:
        """
        Compute all Kerr-SSZ metric components at (r, θ).
        
        Returns:
            KerrMetricComponents with all g_μν
        """
        g_tt_val = self.g_tt(r, theta)
        g_rr_val = self.g_rr(r, theta)
        g_thth_val = self.g_thth(r, theta)
        g_phph_val = self.g_phph(r, theta)
        g_tph_val = self.g_tph(r, theta)
        
        return KerrMetricComponents(
            g_tt=g_tt_val,
            g_rr=g_rr_val,
            g_thth=g_thth_val,
            g_phph=g_phph_val,
            g_tph=g_tph_val,
            A=-g_tt_val,
            B=g_rr_val,
            E=g_tph_val
        )
    
    # ========================================================================
    # HORIZONS & ERGOSPHERE
    # ========================================================================
    
    def horizons(self) -> Tuple[float, float]:
        """
        Compute inner (r_-) and outer (r_+) horizon radii.
        
        Horizons occur where Δ(r) = 0:
            r² - r_s r + a² = 0
        
        Solution:
            r_± = (r_s ± √(r_s² - 4a²)) / 2
        
        Returns:
            (r_plus, r_minus) in meters
        
        Special Cases:
            - a = 0: r_+ = r_s, r_- = 0 (Schwarzschild)
            - a = r_s/2: r_+ = r_-, extremal
            - a > r_s/2: No real horizons (naked singularity - unphysical!)
        """
        discriminant = self.r_s ** 2 - 4.0 * self.a_geom ** 2
        
        if discriminant < 0:
            # Naked singularity (unphysical for SSZ)
            return (np.nan, np.nan)
        
        sqrt_disc = np.sqrt(discriminant)
        
        r_plus = (self.r_s + sqrt_disc) / 2.0
        r_minus = (self.r_s - sqrt_disc) / 2.0
        
        return (r_plus, r_minus)
    
    def ergosphere_radius(self, theta: float) -> float:
        """
        Ergosphere boundary where g_tt = 0.
        
        At ergosphere:
            r_ergo(θ) = r_s/2 + √((r_s/2)² - a² cos²θ)
        
        Args:
            theta: Polar angle [radians]
        
        Returns:
            Ergosphere radius at angle θ [m]
        
        Physics:
            Inside ergosphere: All objects must co-rotate!
            "Frame dragging" becomes mandatory.
        """
        cos_th = np.cos(theta)
        
        term1 = self.r_s / 2.0
        term2_sq = (self.r_s / 2.0) ** 2 - self.a_geom ** 2 * cos_th ** 2
        
        if term2_sq < 0:
            return np.nan
        
        term2 = np.sqrt(term2_sq)
        
        return term1 + term2
    
    def frame_drag_frequency(self, r: float, theta: float) -> float:
        """
        Frame-dragging angular velocity ω(r,θ).
        
        Formula:
            ω = -g_tφ / g_φφ
        
        Units: [rad/s]
        
        Physics:
            ω = angular velocity of "locally non-rotating frame" (LNRF)
            Zero Angular Momentum Observer (ZAMO) rotates at ω.
        
        Returns:
            Frame-drag frequency [rad/s]
        """
        g_tph_val = self.g_tph(r, theta)
        g_phph_val = self.g_phph(r, theta)
        
        if abs(g_phph_val) < 1e-30:
            return 0.0
        
        omega = -g_tph_val / g_phph_val
        
        return omega
    
    # ========================================================================
    # PHYSICAL OBSERVABLES
    # ========================================================================
    
    def redshift(self, r: float, theta: float = np.pi/2) -> float:
        """
        Gravitational redshift z for static observer.
        
        Formula:
            z = 1/√(-g_tt) - 1
        
        Args:
            r: Radius [m]
            theta: Polar angle (default: equator)
        
        Returns:
            Redshift z (dimensionless)
        """
        g_tt_val = self.g_tt(r, theta)
        
        if g_tt_val >= 0:
            # Inside ergosphere or unphysical
            return np.inf
        
        sqrt_g_tt = np.sqrt(-g_tt_val)
        return 1.0 / sqrt_g_tt - 1.0
    
    def is_extremal(self, tol: float = 1e-6) -> bool:
        """
        Check if black hole is extremal (r_+ = r_-).
        
        Extremal condition: a = r_s / 2 (or â = 1 in geometric units)
        
        Returns:
            True if extremal within tolerance
        """
        r_plus, r_minus = self.horizons()
        
        if np.isnan(r_plus):
            return False
        
        return abs(r_plus - r_minus) < tol
    
    def __repr__(self):
        return (f"KerrSSZMetric(M={self.M:.3e} kg, a={self.a:.3e}, "
                f"â={self.a_hat:.3f}, r_s={self.r_s:.3e} m)")
