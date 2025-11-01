#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
φ-Spiral Metric - Geodesic Equations

Complete geodesic solver for the φ-Spiral Segmented Spacetime metric.
Uses diagonal form for simplified calculations.

Geodesic Equations (in T,r coordinates):
    d²T/dλ² - 2(γ'/γ) dT/dλ dr/dλ = 0
    d²r/dλ² - (c²γ'/γ⁵)(dT/dλ)² + (γ'/γ)(dr/dλ)² = 0

First Integrals:
    E = (c²/γ²) dT/dλ  (conserved energy)
    
Timelike: dr²/dλ² = E²/c² - c²/γ²(r)  (effective potential)
Null: dr/dT = ±c/γ² = ±c·sech²(φ_G)  (light cone closing)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from scipy.integrate import odeint, solve_ivp
from typing import Tuple, Callable, Optional
from dataclasses import dataclass

# Physical constants
C_SI = 299792458.0  # m/s
G_SI = 6.67430e-11  # m³/(kg·s²)


@dataclass
class GeodesicInitialConditions:
    """Initial conditions for geodesic integration."""
    r0: float  # Initial radius [m]
    T0: float  # Initial time coordinate [s]
    dr_dlambda0: float  # Initial radial velocity
    dT_dlambda0: float  # Initial time velocity
    is_null: bool = False  # True for photons, False for massive particles


class PhiSpiralGeodesicSolver:
    """
    Solver for geodesics in φ-Spiral metric (diagonal form).
    
    Metric:
        ds² = -c²/γ² dT² + γ² dr²
        
    where γ(r) = cosh(φ_G(r)).
    """
    
    def __init__(self, phi_G_func: Callable[[float], float],
                 r_s: float, mass: float):
        """
        Initialize geodesic solver.
        
        Args:
            phi_G_func: Function φ_G(r) returning rotation angle [rad]
            r_s: Schwarzschild radius [m]
            mass: Central mass [kg]
        """
        self.phi_G = phi_G_func
        self.r_s = r_s
        self.mass = mass
    
    # ========================================================================
    # METRIC FUNCTIONS
    # ========================================================================
    
    def gamma(self, r: float) -> float:
        """γ(r) = cosh(φ_G(r))."""
        phi = self.phi_G(r)
        return np.cosh(phi)
    
    def gamma_prime(self, r: float, dr: float = 1.0) -> float:
        """
        dγ/dr via finite difference.
        
        Args:
            r: Radius [m]
            dr: Step size for finite difference [m]
        
        Returns:
            dγ/dr
        """
        gamma_plus = self.gamma(r + dr)
        gamma_minus = self.gamma(r - dr)
        return (gamma_plus - gamma_minus) / (2.0 * dr)
    
    def g_TT(self, r: float) -> float:
        """Metric component g_TT = -c²/γ²."""
        gamma = self.gamma(r)
        return -(C_SI ** 2) / (gamma ** 2)
    
    def g_rr(self, r: float) -> float:
        """Metric component g_rr = γ²."""
        gamma = self.gamma(r)
        return gamma ** 2
    
    # ========================================================================
    # CHRISTOFFEL SYMBOLS (Non-zero components)
    # ========================================================================
    
    def Gamma_T_Tr(self, r: float) -> float:
        """Γ^T_Tr = -γ'/γ."""
        gamma = self.gamma(r)
        gamma_p = self.gamma_prime(r)
        return -gamma_p / gamma
    
    def Gamma_r_TT(self, r: float) -> float:
        """Γ^r_TT = -c²γ'/γ⁵."""
        gamma = self.gamma(r)
        gamma_p = self.gamma_prime(r)
        return -(C_SI ** 2) * gamma_p / (gamma ** 5)
    
    def Gamma_r_rr(self, r: float) -> float:
        """Γ^r_rr = γ'/γ."""
        gamma = self.gamma(r)
        gamma_p = self.gamma_prime(r)
        return gamma_p / gamma
    
    # ========================================================================
    # CONSERVED QUANTITIES
    # ========================================================================
    
    def energy_parameter(self, r: float, dT_dlambda: float) -> float:
        """
        Conserved energy parameter E = -p_T = c²/γ² · dT/dλ.
        
        Args:
            r: Radius [m]
            dT_dlambda: Time velocity
        
        Returns:
            E: Energy parameter [m²/s²]
        """
        gamma = self.gamma(r)
        return (C_SI ** 2) / (gamma ** 2) * dT_dlambda
    
    def effective_potential(self, r: float) -> float:
        """
        Effective potential V_eff(r) = c²/γ²(r) = c²sech²(φ_G).
        
        For timelike geodesics: (dr/dλ)² = E²/c² - V_eff(r)
        
        Args:
            r: Radius [m]
        
        Returns:
            V_eff: Effective potential [m²/s²]
        """
        gamma = self.gamma(r)
        return (C_SI ** 2) / (gamma ** 2)
    
    # ========================================================================
    # GEODESIC EQUATIONS
    # ========================================================================
    
    def geodesic_equations(self, state: np.ndarray,
                          lambda_param: float) -> np.ndarray:
        """
        Geodesic equations for integration.
        
        State vector: [T, r, dT/dλ, dr/dλ]
        
        Equations:
            d²T/dλ² = 2(γ'/γ) dT/dλ dr/dλ
            d²r/dλ² = (c²γ'/γ⁵)(dT/dλ)² - (γ'/γ)(dr/dλ)²
        
        Args:
            state: [T, r, dT/dλ, dr/dλ]
            lambda_param: Affine parameter
        
        Returns:
            derivatives: [dT/dλ, dr/dλ, d²T/dλ², d²r/dλ²]
        """
        T, r, dT_dlambda, dr_dlambda = state
        
        # Avoid singularities
        if r < 0.1 * self.r_s:
            r = 0.1 * self.r_s
        
        # Christoffel symbols
        Gamma_T_Tr_val = self.Gamma_T_Tr(r)
        Gamma_r_TT_val = self.Gamma_r_TT(r)
        Gamma_r_rr_val = self.Gamma_r_rr(r)
        
        # Accelerations
        d2T_dlambda2 = -2.0 * Gamma_T_Tr_val * dT_dlambda * dr_dlambda
        
        d2r_dlambda2 = (Gamma_r_TT_val * (dT_dlambda ** 2) + 
                        Gamma_r_rr_val * (dr_dlambda ** 2))
        
        return np.array([dT_dlambda, dr_dlambda, d2T_dlambda2, d2r_dlambda2])
    
    # ========================================================================
    # NULL GEODESICS (Photons)
    # ========================================================================
    
    def null_geodesic_dr_dT(self, r: float, outgoing: bool = True) -> float:
        """
        Null geodesic slope dr/dT = ±c/γ² = ±c·sech²(φ_G).
        
        This gives the light cone closing behavior.
        
        Args:
            r: Radius [m]
            outgoing: True for outgoing light, False for infalling
        
        Returns:
            dr/dT: Radial velocity per coordinate time [dimensionless]
        """
        gamma = self.gamma(r)
        dr_dT = C_SI / (gamma ** 2)
        
        return dr_dT if outgoing else -dr_dT
    
    def null_geodesic_T(self, r_start: float, r_end: float, 
                       n_points: int = 1000) -> float:
        """
        Integrate T(r) for null geodesic via quadrature.
        
        Formula: T(r) = ±(1/c) ∫ γ²(ρ) dρ
        
        Args:
            r_start: Starting radius [m]
            r_end: Ending radius [m]
            n_points: Integration points
        
        Returns:
            ΔT: Time difference [s]
        """
        r_vals = np.linspace(r_start, r_end, n_points)
        
        # Integrand: γ²(r)
        integrand = np.array([self.gamma(r) ** 2 for r in r_vals])
        
        # Trapezoidal integration
        delta_T = (1.0 / C_SI) * np.trapz(integrand, r_vals)
        
        return delta_T
    
    # ========================================================================
    # TIMELIKE GEODESICS (Massive Particles)
    # ========================================================================
    
    def timelike_geodesic_radial_velocity(self, r: float, E: float) -> float:
        """
        Radial velocity for timelike geodesic from energy conservation.
        
        Formula: (dr/dλ)² = E²/c² - c²/γ²(r)
        
        Args:
            r: Radius [m]
            E: Energy parameter [m²/s²]
        
        Returns:
            |dr/dλ|: Radial velocity magnitude [m/s]
        """
        V_eff = self.effective_potential(r)
        
        # Check if kinetically allowed
        if E ** 2 / (C_SI ** 2) < V_eff:
            return 0.0
        
        dr_dlambda_squared = (E ** 2) / (C_SI ** 2) - V_eff
        
        return np.sqrt(max(0.0, dr_dlambda_squared))
    
    def integrate_timelike_geodesic(self, ic: GeodesicInitialConditions,
                                   lambda_span: Tuple[float, float],
                                   n_points: int = 1000) -> dict:
        """
        Integrate timelike geodesic.
        
        Args:
            ic: Initial conditions
            lambda_span: (lambda_start, lambda_end)
            n_points: Number of points
        
        Returns:
            dict with keys: 'lambda', 'T', 'r', 'dT_dlambda', 'dr_dlambda', 'E'
        """
        # Initial state
        state0 = np.array([ic.T0, ic.r0, ic.dT_dlambda0, ic.dr_dlambda0])
        
        # Lambda values
        lambda_vals = np.linspace(lambda_span[0], lambda_span[1], n_points)
        
        # Integrate
        solution = odeint(self.geodesic_equations, state0, lambda_vals)
        
        # Extract
        T_vals = solution[:, 0]
        r_vals = solution[:, 1]
        dT_dlambda_vals = solution[:, 2]
        dr_dlambda_vals = solution[:, 3]
        
        # Compute energy (should be conserved)
        E_vals = np.array([
            self.energy_parameter(r, dT) 
            for r, dT in zip(r_vals, dT_dlambda_vals)
        ])
        
        return {
            'lambda': lambda_vals,
            'T': T_vals,
            'r': r_vals,
            'dT_dlambda': dT_dlambda_vals,
            'dr_dlambda': dr_dlambda_vals,
            'E': E_vals
        }
    
    # ========================================================================
    # CONVENIENCE FUNCTIONS
    # ========================================================================
    
    def turning_points(self, E: float, r_min: float, r_max: float,
                      n_points: int = 1000) -> list:
        """
        Find turning points where dr/dλ = 0 for given energy.
        
        These occur where E²/c² = V_eff(r).
        
        Args:
            E: Energy parameter [m²/s²]
            r_min: Minimum radius to search [m]
            r_max: Maximum radius to search [m]
            n_points: Search resolution
        
        Returns:
            List of turning point radii [m]
        """
        r_vals = np.linspace(r_min, r_max, n_points)
        V_vals = np.array([self.effective_potential(r) for r in r_vals])
        
        target = (E ** 2) / (C_SI ** 2)
        
        # Find crossings
        turning_points = []
        for i in range(len(V_vals) - 1):
            if (V_vals[i] - target) * (V_vals[i+1] - target) < 0:
                # Linear interpolation
                r_turn = r_vals[i] + (r_vals[i+1] - r_vals[i]) * \
                         (target - V_vals[i]) / (V_vals[i+1] - V_vals[i])
                turning_points.append(r_turn)
        
        return turning_points
