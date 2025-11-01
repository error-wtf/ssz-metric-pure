#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric - Physically Calibrated Weak-Field Model

Calibrates φ_G(r) to match General Relativity in weak-field regime:
- GPS gravitational redshift
- Pound-Rebka experiment
- Shapiro delay
- Light deflection
- All standard GR tests

Calibration: φ_G^cal(r; M) = sqrt(2GM / (r c²))

This ensures SSZ time dilation matches GR to O(Φ_N/c²).

© 2025 Carmen Wrede & Lino Casu
Based on Lino's weak-field calibration specification
"""
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import PchipInterpolator
from typing import Tuple, Optional, Callable

# Handle scipy version compatibility
try:
    from scipy.integrate import trapezoid as trapz
    from scipy.integrate import simpson as simps
except ImportError:
    from scipy.integrate import trapz, simps

# Physical constants (SI units)
C_SI = 299792458.0  # m/s
G_SI = 6.67430e-11  # m³/(kg·s²)

# Standard masses (SI units)
M_SUN = 1.9885e30  # kg
M_EARTH = 5.9722e24  # kg

# Standard radii (SI units)
R_SUN = 6.9634e8  # m
R_EARTH = 6.371e6  # m

# Earth surface gravity (for convenience)
G_EARTH = 9.80665  # m/s²


class SSZCalibratedMetric:
    """
    Physically calibrated SSZ metric for weak-field regime.
    
    Calibration ensures agreement with GR tests:
    - GPS redshift
    - Pound-Rebka
    - Shapiro delay
    - Light deflection
    """
    
    def __init__(self, mass: float, name: str = ""):
        """
        Initialize calibrated SSZ metric.
        
        Args:
            mass: Central mass [kg]
            name: Optional name (e.g., "Earth", "Sun")
        """
        self.mass = mass
        self.name = name
        self.r_g = self.mass_to_rg(mass)
        
        # Numerical tolerances
        self.rel_tol = 1e-9
        self.abs_tol = 1e-12
        
        # Minimum radius (to avoid numerical issues)
        self.r_min = max(1e-3 * self.r_g, 1.0)
    
    @staticmethod
    def mass_to_rg(mass: float) -> float:
        """
        Schwarzschild radius r_g = 2GM/c².
        
        Args:
            mass: Mass [kg]
        
        Returns:
            r_g: Schwarzschild radius [m]
        """
        return 2.0 * G_SI * mass / (C_SI ** 2)
    
    # ========================================================================
    # CALIBRATED φ_G(r) - WEAK-FIELD MATCHED
    # ========================================================================
    
    def phi_calibrated(self, r: float) -> float:
        """
        Calibrated spiral angle φ_G^cal(r; M) = sqrt(2GM / (r c²)).
        
        This ensures SSZ time dilation matches GR in weak field:
            g_TT^SSZ ≈ -c²(1 - φ²) ≈ -c²(1 + 2Φ_N/c²) = g_tt^GR
        
        where Φ_N = -GM/r is Newtonian potential.
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            φ_G: Calibrated rotation angle [rad]
        """
        # Guard against too small r
        r_safe = max(r, self.r_min)
        
        # φ² = r_g / r
        phi_squared = self.r_g / r_safe
        
        return np.sqrt(phi_squared)
    
    def beta(self, r: float) -> float:
        """β(r) = tanh(φ_G^cal(r))."""
        phi = self.phi_calibrated(r)
        return np.tanh(phi)
    
    def gamma(self, r: float) -> float:
        """γ(r) = cosh(φ_G^cal(r))."""
        phi = self.phi_calibrated(r)
        return np.cosh(phi)
    
    def sech(self, r: float) -> float:
        """sech(φ_G(r)) = 1/cosh(φ_G(r))."""
        gamma = self.gamma(r)
        return 1.0 / gamma
    
    # ========================================================================
    # METRIC COMPONENTS (Diagonal T,r form)
    # ========================================================================
    
    def metric_diag(self, r: float) -> Tuple[float, float]:
        """
        Diagonal metric components (T,r).
        
        g_TT = -c²/γ²(r)
        g_rr = γ²(r)
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            (g_TT, g_rr): Metric components [SI units]
        """
        gamma = self.gamma(r)
        g_TT = -(C_SI ** 2) / (gamma ** 2)
        g_rr = gamma ** 2
        
        return g_TT, g_rr
    
    # ========================================================================
    # NULL GEODESICS
    # ========================================================================
    
    def null_slope(self, r: float, outgoing: bool = True) -> float:
        """
        Null geodesic slope dr/dT = ±c/γ²(r).
        
        Args:
            r: Radial coordinate [m]
            outgoing: True for outgoing light, False for infalling
        
        Returns:
            dr/dT [dimensionless, in units of c]
        """
        gamma = self.gamma(r)
        slope = C_SI / (gamma ** 2)
        
        return slope if outgoing else -slope
    
    def T_of_r_null(self, r_path: np.ndarray, method: str = 'trapz') -> np.ndarray:
        """
        Integrate T(r) for null geodesic: T = (1/c) ∫ γ²(r) dr.
        
        Args:
            r_path: Array of radial coordinates [m]
            method: 'trapz' or 'simps'
        
        Returns:
            T_path: Array of eigentime coordinates [s]
        """
        # Compute γ² at each point
        gamma_squared = np.array([self.gamma(r) ** 2 for r in r_path])
        
        # Integrate
        if method == 'trapz':
            # Cumulative trapezoidal
            T_cumulative = np.zeros_like(r_path)
            for i in range(1, len(r_path)):
                dT = (1.0 / C_SI) * 0.5 * (gamma_squared[i-1] + gamma_squared[i]) * (r_path[i] - r_path[i-1])
                T_cumulative[i] = T_cumulative[i-1] + dT
            return T_cumulative
        
        elif method == 'simps':
            # For validation: full Simpson's rule
            T_total = simps(gamma_squared, r_path) / C_SI
            # Return cumulative (approximate)
            return np.linspace(0, T_total, len(r_path))
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    # ========================================================================
    # COORDINATE TRANSFORMATION t ↔ T
    # ========================================================================
    
    def to_original_time_path(self, T_path: np.ndarray, r_path: np.ndarray) -> np.ndarray:
        """
        Reconstruct coordinate time t from eigentime T.
        
        Formula: dt = dT + (β·γ²/c) dr
        
        Args:
            T_path: Eigentime array [s]
            r_path: Radial array [m]
        
        Returns:
            t_path: Coordinate time array [s]
        """
        t_path = np.zeros_like(T_path)
        
        for i in range(1, len(T_path)):
            dT = T_path[i] - T_path[i-1]
            dr = r_path[i] - r_path[i-1]
            
            beta = self.beta(r_path[i])
            gamma = self.gamma(r_path[i])
            
            correction = (beta * gamma ** 2 / C_SI) * dr
            
            t_path[i] = t_path[i-1] + dT + correction
        
        return t_path
    
    # ========================================================================
    # REDSHIFT & TIME DILATION
    # ========================================================================
    
    def redshift_factor(self, r_emit: float, r_obs: float) -> float:
        """
        Gravitational redshift factor: 1 + z = γ(r_emit) / γ(r_obs).
        
        Light emitted deeper in potential well (smaller r, larger γ)
        is redshifted when observed at larger r (smaller γ).
        
        Args:
            r_emit: Emission radius [m]
            r_obs: Observer radius [m]
        
        Returns:
            1 + z: Redshift factor (> 1 for redshift)
        """
        gamma_emit = self.gamma(r_emit)
        gamma_obs = self.gamma(r_obs)
        
        # Correct formula: deeper potential (larger γ) → redshift
        return gamma_emit / gamma_obs
    
    def time_dilation(self, r: float) -> float:
        """
        Time dilation factor dτ/dT = 1/γ(r).
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            dτ/dT: Time dilation factor
        """
        return self.sech(r)
    
    # ========================================================================
    # GR COMPARISON (Weak Field)
    # ========================================================================
    
    def newtonian_potential(self, r: float) -> float:
        """Newtonian potential Φ_N = -GM/r."""
        r_safe = max(r, self.r_min)
        return -G_SI * self.mass / r_safe
    
    def gr_time_dilation_weak(self, r: float) -> float:
        """
        GR time dilation in weak field: dτ/dt ≈ sqrt(1 + 2Φ_N/c²).
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            dτ/dt: GR time dilation factor
        """
        Phi_N = self.newtonian_potential(r)
        return np.sqrt(1.0 + 2.0 * Phi_N / (C_SI ** 2))
    
    def gr_redshift_weak(self, r1: float, r2: float) -> float:
        """
        GR redshift in weak field: z ≈ (GM/c²)(1/r1 - 1/r2).
        
        Args:
            r1: Emission radius [m]
            r2: Observer radius [m]
        
        Returns:
            z: Redshift (dimensionless)
        """
        factor = G_SI * self.mass / (C_SI ** 2)
        return factor * (1.0 / r1 - 1.0 / r2)
    
    # ========================================================================
    # VALIDATION: Check numerical consistency
    # ========================================================================
    
    def validate_integration_consistency(self, r_path: np.ndarray) -> Tuple[float, float]:
        """
        Compare trapz vs simps integration.
        
        Args:
            r_path: Radial path [m]
        
        Returns:
            (T_trapz_final, T_simps_final): Final T values [s]
        """
        T_trapz = self.T_of_r_null(r_path, method='trapz')[-1]
        T_simps = self.T_of_r_null(r_path, method='simps')[-1]
        
        return T_trapz, T_simps
    
    def check_asymptotic_flatness(self, r: float) -> Tuple[float, float]:
        """
        Check metric approaches Minkowski for r >> r_g.
        
        Args:
            r: Large radius [m]
        
        Returns:
            (error_g_TT, error_g_rr): Deviations from Minkowski
        """
        g_TT, g_rr = self.metric_diag(r)
        
        error_g_TT = abs(g_TT / (C_SI ** 2) + 1.0)
        error_g_rr = abs(g_rr - 1.0)
        
        return error_g_TT, error_g_rr
    
    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    
    def __repr__(self) -> str:
        name_str = f" ({self.name})" if self.name else ""
        return f"SSZCalibratedMetric{name_str}(M={self.mass:.3e} kg, r_g={self.r_g:.3e} m)"
