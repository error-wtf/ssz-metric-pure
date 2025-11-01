#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ φ-Spiral Metric - Complete 4D Tensor Implementation

Provides:
- 4D metric tensor g_μν
- Inverse metric g^μν
- All non-vanishing Christoffel symbols Γ^ρ_μν
- Geodesic equations
- Null geodesic slopes

Coordinates: (T, r, θ, φ)
Order: μ,ν ∈ {0:T, 1:r, 2:θ, 3:φ}

© 2025 Carmen Wrede & Lino Casu
Based on Lino's complete 4D tensor specification
"""
import numpy as np
from typing import Tuple

# Physical constants (SI units)
C_SI = 299792458.0  # m/s
G_SI = 6.67430e-11  # m³/(kg·s²)


class SSZMetric4D:
    """
    Complete 4D SSZ φ-Spiral metric implementation.
    
    Provides metric tensor, inverse metric, and Christoffel symbols
    in paper-ready form for direct use in calculations.
    """
    
    def __init__(self, mass: float):
        """
        Initialize 4D SSZ metric.
        
        Args:
            mass: Central mass [kg]
        """
        self.mass = mass
        self.r_g = 2.0 * G_SI * mass / (C_SI ** 2)  # Schwarzschild radius
    
    # ========================================================================
    # SPIRAL FUNCTIONS
    # ========================================================================
    
    def phi_G(self, r: float) -> float:
        """Calibrated spiral angle: φ_G(r) = √(2GM/(rc²)) = √(r_g/r)."""
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
    
    def gamma_prime(self, r: float) -> float:
        """γ'(r) = γ·β·φ' = sinh(φ)·φ'."""
        return self.gamma(r) * self.beta(r) * self.phi_prime(r)
    
    # ========================================================================
    # METRIC TENSOR g_μν (4x4)
    # ========================================================================
    
    def metric_tensor(self, r: float, theta: float) -> np.ndarray:
        """
        4D metric tensor g_μν.
        
        Order: (T, r, θ, φ)
        
        g_μν = diag(-c²/γ², γ², r², r²sin²θ)
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            g: 4x4 metric tensor
        """
        gamma = self.gamma(r)
        g = np.zeros((4, 4))
        
        g[0, 0] = -(C_SI ** 2) / (gamma ** 2)  # g_TT
        g[1, 1] = gamma ** 2                    # g_rr
        g[2, 2] = r ** 2                        # g_θθ
        g[3, 3] = (r * np.sin(theta)) ** 2      # g_φφ
        
        return g
    
    def inverse_metric_tensor(self, r: float, theta: float) -> np.ndarray:
        """
        Inverse metric tensor g^μν.
        
        g^μν = diag(-γ²/c², 1/γ², 1/r², 1/(r²sin²θ))
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            g_inv: 4x4 inverse metric tensor
        """
        gamma = self.gamma(r)
        g_inv = np.zeros((4, 4))
        
        g_inv[0, 0] = -(gamma ** 2) / (C_SI ** 2)  # g^TT
        g_inv[1, 1] = 1.0 / (gamma ** 2)            # g^rr
        g_inv[2, 2] = 1.0 / (r ** 2)                # g^θθ
        
        sin_theta = np.sin(theta)
        if np.abs(sin_theta) > 1e-10:
            g_inv[3, 3] = 1.0 / ((r * sin_theta) ** 2)  # g^φφ
        else:
            g_inv[3, 3] = 0.0  # Avoid division by zero at poles
        
        return g_inv
    
    # ========================================================================
    # CHRISTOFFEL SYMBOLS Γ^ρ_μν
    # ========================================================================
    
    def christoffel_symbols(self, r: float, theta: float) -> dict:
        """
        All non-vanishing Christoffel symbols Γ^ρ_μν.
        
        Returns dictionary with keys (rho, mu, nu) and values Γ^ρ_μν.
        
        Indices: 0=T, 1=r, 2=θ, 3=φ
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            christoffel: Dict with (ρ, μ, ν) → Γ^ρ_μν
        """
        gamma = self.gamma(r)
        beta = self.beta(r)
        phi_p = self.phi_prime(r)
        
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        cot_theta = cos_theta / sin_theta if np.abs(sin_theta) > 1e-10 else 0.0
        
        Gamma = {}
        
        # ===== SSZ-specific (time-radial) =====
        
        # Γ^T_Tr = Γ^T_rT = -β·φ'
        Gamma[(0, 0, 1)] = -beta * phi_p
        Gamma[(0, 1, 0)] = -beta * phi_p
        
        # Γ^r_TT = -c²·β·φ'/γ⁴
        Gamma[(1, 0, 0)] = -(C_SI ** 2) * beta * phi_p / (gamma ** 4)
        
        # Γ^r_rr = +β·φ'
        Gamma[(1, 1, 1)] = beta * phi_p
        
        # ===== Spherical (modified by γ) =====
        
        # Γ^r_θθ = -r/γ²
        Gamma[(1, 2, 2)] = -r / (gamma ** 2)
        
        # Γ^r_φφ = -r·sin²θ/γ²
        Gamma[(1, 3, 3)] = -r * (sin_theta ** 2) / (gamma ** 2)
        
        # Γ^θ_rθ = Γ^θ_θr = 1/r
        Gamma[(2, 1, 2)] = 1.0 / r
        Gamma[(2, 2, 1)] = 1.0 / r
        
        # Γ^θ_φφ = -sinθ·cosθ
        Gamma[(2, 3, 3)] = -sin_theta * cos_theta
        
        # Γ^φ_rφ = Γ^φ_φr = 1/r
        Gamma[(3, 1, 3)] = 1.0 / r
        Gamma[(3, 3, 1)] = 1.0 / r
        
        # Γ^φ_θφ = Γ^φ_φθ = cotθ
        Gamma[(3, 2, 3)] = cot_theta
        Gamma[(3, 3, 2)] = cot_theta
        
        return Gamma
    
    def christoffel_component(self, rho: int, mu: int, nu: int, 
                             r: float, theta: float) -> float:
        """
        Get single Christoffel symbol Γ^ρ_μν.
        
        Indices: 0=T, 1=r, 2=θ, 3=φ
        
        Args:
            rho, mu, nu: Indices (0-3)
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            Γ^ρ_μν: Christoffel symbol value
        """
        Gamma = self.christoffel_symbols(r, theta)
        return Gamma.get((rho, mu, nu), 0.0)
    
    # ========================================================================
    # GEODESIC EQUATIONS
    # ========================================================================
    
    def geodesic_acceleration(self, x: np.ndarray, v: np.ndarray) -> np.ndarray:
        """
        Geodesic equation: d²x^ρ/dλ² = -Γ^ρ_μν · dx^μ/dλ · dx^ν/dλ.
        
        Args:
            x: Position 4-vector (T, r, θ, φ)
            v: Velocity 4-vector (dT/dλ, dr/dλ, dθ/dλ, dφ/dλ)
        
        Returns:
            a: Acceleration 4-vector (d²x^ρ/dλ²)
        """
        T, r, theta, phi = x
        
        # Guard against too small r or singular theta
        r = max(r, 0.1 * self.r_g)
        theta = np.clip(theta, 1e-6, np.pi - 1e-6)
        
        Gamma = self.christoffel_symbols(r, theta)
        
        a = np.zeros(4)
        
        # Sum over all non-zero Christoffel symbols
        for (rho, mu, nu), Gamma_val in Gamma.items():
            a[rho] -= Gamma_val * v[mu] * v[nu]
        
        return a
    
    # ========================================================================
    # NULL GEODESICS
    # ========================================================================
    
    def null_slope(self, r: float, outgoing: bool = True) -> float:
        """
        Null geodesic slope dr/dT = ±c/γ²(r) = ±c·sech²(φ_G).
        
        For photons (ds² = 0) in the equatorial plane.
        
        Args:
            r: Radial coordinate [m]
            outgoing: True for outgoing light, False for infalling
        
        Returns:
            dr/dT: Radial velocity [m/s]
        """
        gamma = self.gamma(r)
        slope = C_SI / (gamma ** 2)
        
        return slope if outgoing else -slope
    
    def light_cone_closing(self, r: float) -> float:
        """
        Light cone closing percentage: 100×(1 - sech²(φ_G)).
        
        Approaches 100% as r → 0 (progressive closing, no collapse).
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            Closing percentage [0-100]
        """
        gamma = self.gamma(r)
        sech_squared = 1.0 / (gamma ** 2)
        
        return 100.0 * (1.0 - sech_squared)
    
    # ========================================================================
    # TIME DILATION
    # ========================================================================
    
    def time_dilation(self, r: float) -> float:
        """
        Time dilation factor dτ/dT = 1/γ(r) = sech(φ_G).
        
        Args:
            r: Radial coordinate [m]
        
        Returns:
            dτ/dT: Proper time per coordinate time
        """
        gamma = self.gamma(r)
        return 1.0 / gamma
    
    # ========================================================================
    # VERIFICATION
    # ========================================================================
    
    def verify_inverse(self, r: float, theta: float = np.pi/2) -> bool:
        """
        Verify g_μν · g^νρ = δ_μ^ρ.
        
        Args:
            r: Radial coordinate [m]
            theta: Polar angle [rad]
        
        Returns:
            True if inverse is correct (within tolerance)
        """
        g = self.metric_tensor(r, theta)
        g_inv = self.inverse_metric_tensor(r, theta)
        
        # Compute product
        product = g @ g_inv
        identity = np.eye(4)
        
        # Check if close to identity
        max_error = np.max(np.abs(product - identity))
        
        return max_error < 1e-10


# ========================================================================
# USAGE EXAMPLE
# ========================================================================

if __name__ == "__main__":
    # Example: Earth metric
    M_EARTH = 5.9722e24  # kg
    
    metric = SSZMetric4D(M_EARTH)
    
    # Test point
    r_test = 10.0 * metric.r_g  # 10 Schwarzschild radii
    theta_test = np.pi / 2       # Equator
    
    print("=" * 70)
    print("SSZ 4D Metric Tensor - Example")
    print("=" * 70)
    print(f"\nMass: {M_EARTH:.3e} kg (Earth)")
    print(f"r_g: {metric.r_g:.3e} m")
    print(f"Test radius: r = {r_test / metric.r_g:.1f} r_g")
    print(f"Test angle: theta = pi/2 (equator)")
    
    # Metric tensor
    print("\n" + "-" * 70)
    print("Metric tensor g_munu:")
    print("-" * 70)
    g = metric.metric_tensor(r_test, theta_test)
    for i, name in enumerate(['T', 'r', 'theta', 'phi']):
        print(f"g_{name}{name} = {g[i,i]:+.6e}")
    
    # Inverse metric
    print("\n" + "-" * 70)
    print("Inverse metric g^munu:")
    print("-" * 70)
    g_inv = metric.inverse_metric_tensor(r_test, theta_test)
    for i, name in enumerate(['T', 'r', 'theta', 'phi']):
        print(f"g^{name}{name} = {g_inv[i,i]:+.6e}")
    
    # Verify inverse
    is_correct = metric.verify_inverse(r_test, theta_test)
    print(f"\nInverse verification: {'PASS' if is_correct else 'FAIL'}")
    
    # Christoffel symbols
    print("\n" + "-" * 70)
    print("Non-zero Christoffel symbols:")
    print("-" * 70)
    Gamma = metric.christoffel_symbols(r_test, theta_test)
    
    idx_names = ['T', 'r', 'theta', 'phi']
    for (rho, mu, nu), value in sorted(Gamma.items()):
        print(f"Gamma^{idx_names[rho]}_{idx_names[mu]}{idx_names[nu]} = {value:+.6e}")
    
    # Null geodesic
    print("\n" + "-" * 70)
    print("Null geodesic (light):")
    print("-" * 70)
    dr_dT = metric.null_slope(r_test, outgoing=True)
    closing = metric.light_cone_closing(r_test)
    print(f"dr/dT = {dr_dT:.6e} m/s = {dr_dT/C_SI:.6f} c")
    print(f"Light cone closing: {closing:.2f}%")
    
    # Time dilation
    print("\n" + "-" * 70)
    print("Time dilation:")
    print("-" * 70)
    dilation = metric.time_dilation(r_test)
    print(f"dtau/dT = {dilation:.6f}")
    
    print("\n" + "=" * 70)
    print("© 2025 Carmen Wrede & Lino Casu")
    print("=" * 70)
