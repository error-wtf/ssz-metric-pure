#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ φ-Spiral Metric - Einstein Tensor & Ricci Curvature (4D)

Provides:
- Einstein tensor G^μ_ν (mixed indices)
- Ricci tensor R_μν (lowered indices)
- Ricci scalar R
- Kretschmann scalar K (weak field approximation)
- All curvature invariants

Coordinates: (T, r, θ, φ)
Metric: ds² = -(c²/γ²)dT² + γ²dr² + r²dΩ²

© 2025 Carmen Wrede & Lino Casu
Based on Lino's Einstein tensor specification
"""
import numpy as np
from typing import Dict, Tuple

# Physical constants (SI units)
C_SI = 299792458.0  # m/s
G_SI = 6.67430e-11  # m³/(kg·s²)


class SSZEinsteinRicci4D:
    """
    Complete Einstein tensor and Ricci curvature for SSZ 4D metric.
    
    Implements all curvature tensors and invariants in paper-ready form.
    """
    
    def __init__(self, mass: float):
        """
        Initialize Einstein-Ricci calculator.
        
        Args:
            mass: Central mass [kg]
        """
        self.mass = mass
        self.r_g = 2.0 * G_SI * mass / (C_SI ** 2)  # Schwarzschild radius
    
    # ========================================================================
    # SPIRAL FUNCTIONS
    # ========================================================================
    
    def phi_G(self, r: float) -> float:
        """Calibrated spiral angle: φ_G(r) = √(r_g/r)."""
        return np.sqrt(self.r_g / r)
    
    def gamma(self, r: float) -> float:
        """γ(r) = cosh(φ_G(r))."""
        phi = self.phi_G(r)
        return np.cosh(phi)
    
    def beta(self, r: float) -> float:
        """β(r) = tanh(φ_G(r))."""
        phi = self.phi_G(r)
        return np.tanh(phi)
    
    def phi_prime(self, r: float) -> float:
        """φ'(r) = dφ_G/dr = -0.5·√(r_g/r³)."""
        return -0.5 * np.sqrt(self.r_g / (r ** 3))
    
    def phi_double_prime(self, r: float) -> float:
        """φ''(r) = d²φ_G/dr² = 0.75·√(r_g/r⁵)."""
        return 0.75 * np.sqrt(self.r_g / (r ** 5))
    
    def lambda_func(self, r: float) -> float:
        """λ(r) = ln(γ(r))."""
        return np.log(self.gamma(r))
    
    def lambda_prime(self, r: float) -> float:
        """λ'(r) = γ'/γ = β·φ'."""
        return self.beta(r) * self.phi_prime(r)
    
    def lambda_double_prime(self, r: float) -> float:
        """λ''(r) = (φ')²/γ² + β·φ''."""
        phi_p = self.phi_prime(r)
        phi_pp = self.phi_double_prime(r)
        gamma = self.gamma(r)
        beta = self.beta(r)
        
        return (phi_p ** 2) / (gamma ** 2) + beta * phi_pp
    
    # ========================================================================
    # EINSTEIN TENSOR G^μ_ν (MIXED INDICES)
    # ========================================================================
    
    def einstein_tensor(self, r: float) -> Dict[str, float]:
        """
        Complete Einstein tensor G^μ_ν (mixed indices).
        
        Returns dictionary with keys:
          'G_T_T', 'G_r_r', 'G_theta_theta', 'G_phi_phi'
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            einstein: Dict with Einstein tensor components
        """
        gamma = self.gamma(r)
        beta = self.beta(r)
        phi_p = self.phi_prime(r)
        lambda_p = self.lambda_prime(r)
        lambda_pp = self.lambda_double_prime(r)
        
        # Time component: G^T_T
        G_T_T = (1.0 / (r ** 2)) * (
            (2.0 * r * beta * phi_p) / (gamma ** 2)
            - 1.0 / (gamma ** 2)
            + 1.0
        )
        
        # Radial component: G^r_r
        G_r_r = (1.0 / (r ** 2)) * (
            1.0 / (gamma ** 2) - 1.0
        ) - (2.0 * beta * phi_p) / (r * gamma ** 2)
        
        # Angular components: G^θ_θ = G^φ_φ
        G_theta_theta = (1.0 / (gamma ** 2)) * (
            -lambda_pp + 2.0 * (lambda_p ** 2) - (2.0 * lambda_p) / r
        )
        
        return {
            'G_T_T': G_T_T,
            'G_r_r': G_r_r,
            'G_theta_theta': G_theta_theta,
            'G_phi_phi': G_theta_theta  # Same as theta
        }
    
    # ========================================================================
    # RICCI SCALAR R
    # ========================================================================
    
    def ricci_scalar(self, r: float) -> float:
        """
        Ricci scalar R.
        
        From trace: R = -(G^T_T + G^r_r + 2·G^θ_θ)
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            R: Ricci scalar
        """
        G = self.einstein_tensor(r)
        
        R = -(G['G_T_T'] + G['G_r_r'] + 2.0 * G['G_theta_theta'])
        
        return R
    
    def ricci_scalar_direct(self, r: float) -> float:
        """
        Ricci scalar R (direct formula).
        
        R = (2/γ²)[λ'' - 2λ'² + 2λ'/r]
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            R: Ricci scalar
        """
        gamma = self.gamma(r)
        lambda_p = self.lambda_prime(r)
        lambda_pp = self.lambda_double_prime(r)
        
        R = (2.0 / (gamma ** 2)) * (
            lambda_pp - 2.0 * (lambda_p ** 2) + (2.0 * lambda_p) / r
        )
        
        return R
    
    # ========================================================================
    # RICCI TENSOR R_μν (LOWERED INDICES)
    # ========================================================================
    
    def ricci_tensor(self, r: float) -> Dict[str, float]:
        """
        Complete Ricci tensor R_μν (lowered indices).
        
        From: R_μν = G_μν + (1/2)·g_μν·R
              where G_μν = g_μρ·G^ρ_ν
        
        Returns dictionary with keys:
          'R_TT', 'R_rr', 'R_theta_theta', 'R_phi_phi'
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            ricci: Dict with Ricci tensor components
        """
        gamma = self.gamma(r)
        G = self.einstein_tensor(r)
        R = self.ricci_scalar(r)
        
        # Metric components
        g_TT = -(C_SI ** 2) / (gamma ** 2)
        g_rr = gamma ** 2
        g_theta_theta = r ** 2
        
        # Ricci tensor: R_μν = g_μν(G^μ_ν - R/2)
        R_TT = g_TT * (G['G_T_T'] - 0.5 * R)
        R_rr = g_rr * (G['G_r_r'] - 0.5 * R)
        R_theta_theta = g_theta_theta * (G['G_theta_theta'] - 0.5 * R)
        
        return {
            'R_TT': R_TT,
            'R_rr': R_rr,
            'R_theta_theta': R_theta_theta,
            'R_phi_phi': R_theta_theta  # Same by symmetry
        }
    
    # ========================================================================
    # CURVATURE INVARIANTS
    # ========================================================================
    
    def ricci_squared(self, r: float, theta: float = np.pi/2) -> float:
        """
        Ricci squared invariant: R_μν·R^μν.
        
        Computed from R_μν with g^μν.
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            R_μν·R^μν: Ricci squared invariant
        """
        gamma = self.gamma(r)
        R_comp = self.ricci_tensor(r)
        
        # Inverse metric components
        g_inv_TT = -(gamma ** 2) / (C_SI ** 2)
        g_inv_rr = 1.0 / (gamma ** 2)
        g_inv_theta_theta = 1.0 / (r ** 2)
        
        sin_theta = np.sin(theta)
        if np.abs(sin_theta) > 1e-10:
            g_inv_phi_phi = 1.0 / ((r * sin_theta) ** 2)
        else:
            g_inv_phi_phi = 0.0
        
        # Contract: R_μν·R^μν = Σ_μν g^μν·R_μν²
        ricci_sq = (
            g_inv_TT * (R_comp['R_TT'] ** 2)
            + g_inv_rr * (R_comp['R_rr'] ** 2)
            + g_inv_theta_theta * (R_comp['R_theta_theta'] ** 2)
            + g_inv_phi_phi * (R_comp['R_phi_phi'] ** 2)
        )
        
        return ricci_sq
    
    def kretschmann_weak_field(self, r: float) -> float:
        """
        Kretschmann scalar K in weak field limit.
        
        K = 48·G²·M²/(c⁴·r⁶) + O(r_g³/r⁷)
        
        Same r^(-6) scaling as Schwarzschild.
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            K: Kretschmann scalar (weak field)
        """
        K = (48.0 * (G_SI ** 2) * (self.mass ** 2)) / ((C_SI ** 4) * (r ** 6))
        
        return K
    
    # ========================================================================
    # PHYSICAL PROPERTIES
    # ========================================================================
    
    def is_regular(self, r: float) -> bool:
        """
        Check if curvature is regular (finite) at radius r.
        
        All components of G^μ_ν, R_μν, R must be finite.
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            True if regular, False if any component diverges
        """
        try:
            G = self.einstein_tensor(r)
            R = self.ricci_scalar(r)
            R_comp = self.ricci_tensor(r)
            
            # Check all are finite
            for val in G.values():
                if not np.isfinite(val):
                    return False
            
            if not np.isfinite(R):
                return False
            
            for val in R_comp.values():
                if not np.isfinite(val):
                    return False
            
            return True
        
        except:
            return False
    
    def weak_field_expansion(self, r: float) -> Dict[str, float]:
        """
        Weak field expansion of Einstein tensor components.
        
        For φ ≪ 1 (r ≫ r_g).
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            expansion: Dict with leading-order terms
        """
        # Leading order in r_g/r
        G_T_T_weak = -(G_SI * self.mass) / (r ** 3)
        G_r_r_weak = +(G_SI * self.mass) / (r ** 3)
        
        return {
            'G_T_T': G_T_T_weak,
            'G_r_r': G_r_r_weak,
            'order': 'O(r_g/r^3)'
        }


# ========================================================================
# USAGE EXAMPLE
# ========================================================================

if __name__ == "__main__":
    # Example: Earth
    M_EARTH = 5.9722e24  # kg
    
    einstein = SSZEinsteinRicci4D(M_EARTH)
    
    # Test points
    r_tests = [
        10.0 * einstein.r_g,   # 10 Schwarzschild radii
        100.0 * einstein.r_g,  # 100 Schwarzschild radii
        1000.0 * einstein.r_g  # 1000 Schwarzschild radii (weak field)
    ]
    
    print("=" * 70)
    print("SSZ Einstein Tensor & Ricci Curvature - Example")
    print("=" * 70)
    print(f"\nMass: {M_EARTH:.3e} kg (Earth)")
    print(f"r_g: {einstein.r_g:.3e} m")
    
    for r_test in r_tests:
        print("\n" + "-" * 70)
        print(f"Test radius: r = {r_test / einstein.r_g:.1f} r_g = {r_test:.3e} m")
        print("-" * 70)
        
        # Einstein tensor
        G = einstein.einstein_tensor(r_test)
        print("\nEinstein Tensor G^mu_nu:")
        print(f"  G^T_T         = {G['G_T_T']:+.6e}")
        print(f"  G^r_r         = {G['G_r_r']:+.6e}")
        print(f"  G^theta_theta = {G['G_theta_theta']:+.6e}")
        print(f"  G^phi_phi     = {G['G_phi_phi']:+.6e}")
        
        # Ricci scalar
        R = einstein.ricci_scalar(r_test)
        R_direct = einstein.ricci_scalar_direct(r_test)
        print(f"\nRicci Scalar R:")
        print(f"  R (from trace)  = {R:+.6e}")
        print(f"  R (direct)      = {R_direct:+.6e}")
        print(f"  Difference      = {abs(R - R_direct):.3e}")
        
        # Ricci tensor
        R_comp = einstein.ricci_tensor(r_test)
        print(f"\nRicci Tensor R_munu:")
        print(f"  R_TT          = {R_comp['R_TT']:+.6e}")
        print(f"  R_rr          = {R_comp['R_rr']:+.6e}")
        print(f"  R_theta_theta = {R_comp['R_theta_theta']:+.6e}")
        
        # Ricci squared
        R_sq = einstein.ricci_squared(r_test)
        print(f"\nRicci Squared:")
        print(f"  R_munu R^munu = {R_sq:+.6e}")
        
        # Kretschmann (weak field)
        K = einstein.kretschmann_weak_field(r_test)
        print(f"\nKretschmann Scalar K (weak field):")
        print(f"  K = {K:+.6e}")
        
        # Regularity check
        is_reg = einstein.is_regular(r_test)
        print(f"\nRegularity:")
        print(f"  All components finite: {'YES' if is_reg else 'NO'}")
    
    # Weak field expansion
    print("\n" + "=" * 70)
    print("Weak Field Expansion (r >> r_g)")
    print("=" * 70)
    r_weak = 1e6 * einstein.r_g
    G_weak = einstein.weak_field_expansion(r_weak)
    print(f"\nAt r = {r_weak / einstein.r_g:.0f} r_g:")
    print(f"  G^T_T ~ {G_weak['G_T_T']:.6e}  [{G_weak['order']}]")
    print(f"  G^r_r ~ {G_weak['G_r_r']:.6e}  [{G_weak['order']}]")
    
    print("\n" + "=" * 70)
    print("(C) 2025 Carmen Wrede & Lino Casu")
    print("=" * 70)
