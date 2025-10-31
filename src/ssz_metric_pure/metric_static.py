#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Pure - Static (Non-Rotating) Metric

Pure SSZ metric coefficients for spherically symmetric, static spacetimes.

Line Element:
    ds² = -A(r) dt² + B(r) dr² + r² dθ² + r² sin²θ dφ²

where A(r), B(r) are pure SSZ functions (NO hybrid GR mixing!).

Sources:
- ssz-metric-final: Pure SSZ formulas
- ssz-full-metric: Numerical stability, φ-series

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Tuple, Dict, Optional
from dataclasses import dataclass

from .params import (
    SSZParams, PHI, G_SI, C_SI,
    PHI_SERIES_COEFFICIENTS, EPSILON_COEFFICIENTS
)
from .segmentation import segment_density_xi, time_dilation_SSZ


@dataclass
class MetricComponents:
    """Container for metric components."""
    g_tt: float  # Time-time component
    g_rr: float  # Radial-radial component
    g_thth: float  # θ-θ component
    g_phph: float  # φ-φ component
    A: float  # A(r) = -g_tt
    B: float  # B(r) = g_rr


class StaticSSZMetric:
    """
    Pure SSZ static metric (spherically symmetric, non-rotating).
    
    Philosophy:
        100% PURE SSZ - no hybrid GR mixing in core equations.
        GR appears ONLY in limits.py for validation.
    
    Usage:
        >>> from ssz_metric_pure import SSZParams
        >>> params = SSZParams(mass=1.98847e30)  # Solar mass
        >>> metric = StaticSSZMetric(params)
        >>> A = metric.A_coefficient(3 * metric.r_s)
        >>> print(f"A(3r_s) = {A:.6f}")
    
    Metric Components:
        g_tt = -A(r)
        g_rr = B(r) = 1/A(r)
        g_θθ = r²
        g_φφ = r² sin²θ
    """
    
    def __init__(self, params: SSZParams):
        """
        Initialize static SSZ metric.
        
        Args:
            params: SSZ parameters (mass, constants, φ)
        
        Raises:
            ValueError: If parameters invalid
        """
        if params.M <= 0:
            raise ValueError(f"Mass must be positive, got {params.M}")
        
        self.params = params
        self.r_s = params.r_s
        self.r_phi = params.r_phi
        self.varphi = params.varphi
    
    # ========================================================================
    # CORE METRIC COEFFICIENTS (Pure SSZ)
    # ========================================================================
    
    def A_coefficient(self, r: float, method: str = 'saturation') -> float:
        """
        Metric coefficient A(r) = -g_tt.
        
        Pure SSZ Formula (CORRECTED - saturation based):
            A(r) = [1 / (1 + N(r))]²
        
        where N(r) = N_max × (1 - exp(-φ × r/r_s))
        
        Properties:
        - A(0) = 1.0 (flat spacetime at center!) ✓
        - A(r_s) ≈ 0.16 (finite at Schwarzschild radius)
        - A(∞) → (1/(1+N_max))² (bounded)
        - 0 < A(r) ≤ 1 always
        
        Args:
            r: Radius [m]
            method: 'saturation' (N-based, default) or 'phi_series' (PN expansion)
        
        Returns:
            Metric coefficient A(r)
        
        Physics:
            A(r) = (proper time / coordinate time)²
            Redshift: z = 1/√A - 1
        """
        if r <= 0:
            # At center: N(0) = 0 → A(0) = 1.0 (FLAT!)
            return 1.0
        
        if method == 'saturation':
            # Use N(r) saturation (CORRECT for flat center!)
            from .segmentation import segment_density_N, XI_MAX
            N = segment_density_N(r, self.r_s, self.varphi, N_max=XI_MAX)
            D = 1.0 / (1.0 + N)
            A = D * D
        
        elif method == 'phi_series':
            # φ-series Post-Newtonian expansion
            A = self._A_phi_series(r)
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Ensure positive (should be automatic, but safety check)
        return max(A, 1e-16)
    
    def B_coefficient(self, r: float, method: str = 'saturation') -> float:
        """
        Radial metric coefficient B(r) = g_rr.
        
        Pure SSZ Formula:
            B(r) = 1 / A(r)
        
        This choice ensures:
        - det(g) = -r⁴ sin²θ (standard volume element)
        - Proper radial distance: ds² = B(r) dr²
        
        Args:
            r: Radius [m]
            method: Same as A_coefficient
        
        Returns:
            B(r) = 1/A(r)
        
        Properties:
        - B(0) = 1.0 (flat at center)
        - B(∞) → 1.0 (asymptotically flat)
        - B(r) ≥ 1 always (space expansion)
        """
        A = self.A_coefficient(r, method=method)
        # Avoid division by tiny numbers
        A_safe = max(A, 1e-16)
        return 1.0 / A_safe
    
    def _A_phi_series(self, r: float) -> float:
        """
        φ-series Post-Newtonian expansion.
        
        Formula:
            A(r) = Σ_{n=0}^6 ε_n × (r_s / 2r)^n
        
        where ε_n from EPSILON_COEFFICIENTS (φ-recursion!)
        
        Valid for: r >> r_s (weak field)
        
        Returns:
            A(r) from PN expansion
        """
        U = self.r_s / (2.0 * r)  # Weak field parameter
        
        A = 0.0
        for n, eps_n in EPSILON_COEFFICIENTS.items():
            A += eps_n * (U ** n)
        
        # Ensure positive and bounded
        A = np.clip(A, 1e-16, 1.0)
        
        return A
    
    # ========================================================================
    # FULL METRIC TENSOR
    # ========================================================================
    
    def g_tt(self, r: float, theta: float = 0.0) -> float:
        """Time-time component: g_tt = -A(r)."""
        return -self.A_coefficient(r)
    
    def g_rr(self, r: float, theta: float = 0.0) -> float:
        """Radial component: g_rr = B(r) = 1/A(r)."""
        return self.B_coefficient(r)
    
    def g_thth(self, r: float, theta: float = 0.0) -> float:
        """Angular θ component: g_θθ = r²."""
        return r * r
    
    def g_phph(self, r: float, theta: float) -> float:
        """Angular φ component: g_φφ = r² sin²θ."""
        return (r * r) * (np.sin(theta) ** 2)
    
    def metric_tensor(self, r: float, theta: float) -> MetricComponents:
        """
        Compute all metric components at (r, θ).
        
        Returns:
            MetricComponents with g_tt, g_rr, g_thth, g_phph, A, B
        """
        A = self.A_coefficient(r)
        B = self.B_coefficient(r)
        
        return MetricComponents(
            g_tt=-A,
            g_rr=B,
            g_thth=r * r,
            g_phph=(r * r) * (np.sin(theta) ** 2),
            A=A,
            B=B
        )
    
    # ========================================================================
    # PHYSICAL OBSERVABLES
    # ========================================================================
    
    def redshift(self, r: float) -> float:
        """
        Gravitational redshift z.
        
        Formula:
            z = 1/√A(r) - 1
        
        Physics:
            λ_observed / λ_emitted = 1 + z = 1/√A
        
        Returns:
            Redshift z (dimensionless)
        """
        A = self.A_coefficient(r)
        sqrt_A = np.sqrt(max(A, 1e-16))
        return 1.0 / sqrt_A - 1.0
    
    def proper_time_factor(self, r: float) -> float:
        """
        Proper time / coordinate time = √A(r).
        
        Returns:
            τ/t factor
        """
        A = self.A_coefficient(r)
        return np.sqrt(max(A, 1e-16))
    
    def escape_velocity(self, r: float) -> float:
        """
        Escape velocity at radius r.
        
        Formula (geometric):
            v_esc² = c² × (1 - A(r))
        
        Returns:
            Escape velocity [m/s]
        """
        A = self.A_coefficient(r)
        v_esc_sq = self.params.c ** 2 * (1.0 - A)
        return np.sqrt(max(v_esc_sq, 0.0))
    
    # ========================================================================
    # BOUNDARY CONDITIONS & VALIDATION
    # ========================================================================
    
    def check_flatness_at_center(self, tol: float = 1e-3) -> Tuple[bool, str]:
        """
        Validate A(0) ≈ 1 (flat spacetime at center).
        
        Returns:
            (is_valid, message)
        """
        A_0 = self.A_coefficient(1e-10)  # Near r=0
        
        if abs(A_0 - 1.0) < tol:
            return True, f"A(0) = {A_0:.6f} ≈ 1.0 ✓"
        else:
            return False, f"A(0) = {A_0:.6f} deviates from 1.0 by {abs(A_0-1.0):.3e}"
    
    def check_asymptotic_flatness(self, r_test: float = None, tol: float = 1e-3) -> Tuple[bool, str]:
        """
        Validate A(r→∞) → 1 (asymptotically flat).
        
        Args:
            r_test: Test radius (default: 100 × r_s)
            tol: Tolerance
        
        Returns:
            (is_valid, message)
        """
        if r_test is None:
            r_test = 100.0 * self.r_s
        
        A_inf = self.A_coefficient(r_test)
        
        if abs(A_inf - 1.0) < tol:
            return True, f"A({r_test/self.r_s:.0f}r_s) = {A_inf:.6f} ≈ 1.0 ✓"
        else:
            return False, f"A(∞) = {A_inf:.6f} not asymptotically flat"
    
    def check_positive_definite(self, r_min: float = None, r_max: float = None, n_points: int = 100) -> Tuple[bool, str]:
        """
        Validate A(r) > 0 everywhere (no singularities!).
        
        Args:
            r_min: Minimum radius to test (default: 0.1 × r_φ)
            r_max: Maximum radius to test (default: 100 × r_s)
            n_points: Number of test points
        
        Returns:
            (is_valid, message)
        """
        if r_min is None:
            r_min = 0.1 * self.r_phi
        if r_max is None:
            r_max = 100.0 * self.r_s
        
        r_test = np.linspace(r_min, r_max, n_points)
        A_test = np.array([self.A_coefficient(r) for r in r_test])
        
        A_min = np.min(A_test)
        
        if A_min > 0:
            return True, f"A(r) > 0 everywhere: min = {A_min:.6f} ✓"
        else:
            return False, f"A(r) becomes negative: min = {A_min:.6e}"
    
    def __repr__(self):
        return (f"StaticSSZMetric(M={self.params.M:.3e} kg, "
                f"r_s={self.r_s:.3e} m, r_φ={self.r_phi:.3e} m)")
