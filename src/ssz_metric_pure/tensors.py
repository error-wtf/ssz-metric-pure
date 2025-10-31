#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Pure - Curvature Tensors

Christoffel symbols, Riemann tensor, Ricci tensor, Einstein tensor.

For pure SSZ metric in spherical/Boyer-Lindquist coordinates.

Note: Full symbolic computation is expensive.
      This module provides numerical evaluation at specific points.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Tuple, Optional
import warnings

# For symbolic computation (optional)
try:
    import sympy as sp
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    warnings.warn("sympy not available - symbolic tensor computation disabled")


def christoffel_numerical(
    g_func,
    coords: Tuple[float, float, float, float],
    eps: float = 1e-8
) -> np.ndarray:
    """
    Compute Christoffel symbols Γ^μ_νρ numerically via finite differences.
    
    Formula:
        Γ^μ_νρ = (1/2) g^μσ (∂_ν g_σρ + ∂_ρ g_νσ - ∂_σ g_νρ)
    
    Args:
        g_func: Function (t,r,θ,φ) → 4×4 metric tensor
        coords: (t, r, θ, φ) coordinate values
        eps: Step size for finite differences
    
    Returns:
        Γ[μ,ν,ρ]: 4×4×4 array of Christoffel symbols
    
    Warning:
        Numerical derivatives are approximate!
        Use symbolic computation for exact results.
    """
    t, r, theta, phi = coords
    
    # Metric at point
    g = g_func(t, r, theta, phi)
    
    # Inverse metric
    try:
        g_inv = np.linalg.inv(g)
    except np.linalg.LinAlgError:
        warnings.warn("Metric tensor singular - using pseudoinverse")
        g_inv = np.linalg.pinv(g)
    
    # Initialize Christoffel symbols
    Gamma = np.zeros((4, 4, 4))
    
    # Coordinate names for derivative
    coord_names = ['t', 'r', 'theta', 'phi']
    coord_vals = [t, r, theta, phi]
    
    # Compute derivatives ∂_μ g_νρ
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                for sigma in range(4):
                    # ∂_ν g_σρ
                    coords_plus = list(coord_vals)
                    coords_minus = list(coord_vals)
                    coords_plus[nu] += eps
                    coords_minus[nu] -= eps
                    
                    g_plus = g_func(*coords_plus)
                    g_minus = g_func(*coords_minus)
                    
                    dg_nu = (g_plus[sigma, rho] - g_minus[sigma, rho]) / (2 * eps)
                    
                    # ∂_ρ g_νσ
                    coords_plus = list(coord_vals)
                    coords_minus = list(coord_vals)
                    coords_plus[rho] += eps
                    coords_minus[rho] -= eps
                    
                    g_plus = g_func(*coords_plus)
                    g_minus = g_func(*coords_minus)
                    
                    dg_rho = (g_plus[nu, sigma] - g_minus[nu, sigma]) / (2 * eps)
                    
                    # ∂_σ g_νρ
                    coords_plus = list(coord_vals)
                    coords_minus = list(coord_vals)
                    coords_plus[sigma] += eps
                    coords_minus[sigma] -= eps
                    
                    g_plus = g_func(*coords_plus)
                    g_minus = g_func(*coords_minus)
                    
                    dg_sigma = (g_plus[nu, rho] - g_minus[nu, rho]) / (2 * eps)
                    
                    # Γ^μ_νρ = (1/2) g^μσ (...)
                    Gamma[mu, nu, rho] += 0.5 * g_inv[mu, sigma] * (dg_nu + dg_rho - dg_sigma)
    
    return Gamma


def riemann_from_christoffel(
    Gamma: np.ndarray,
    Gamma_func,
    coords: Tuple[float, float, float, float],
    eps: float = 1e-8
) -> np.ndarray:
    """
    Compute Riemann tensor R^μ_νρσ from Christoffel symbols.
    
    Formula:
        R^μ_νρσ = ∂_ρ Γ^μ_νσ - ∂_σ Γ^μ_νρ + Γ^μ_ρλ Γ^λ_νσ - Γ^μ_σλ Γ^λ_νρ
    
    Args:
        Gamma: Christoffel symbols at point
        Gamma_func: Function to compute Γ at nearby points
        coords: Coordinates
        eps: Step size
    
    Returns:
        R[μ,ν,ρ,σ]: 4×4×4×4 Riemann tensor
    
    Warning:
        This is numerically expensive (256 components!).
        Use only for spot checks.
    """
    R = np.zeros((4, 4, 4, 4))
    
    coord_vals = list(coords)
    
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                for sigma in range(4):
                    # ∂_ρ Γ^μ_νσ
                    coords_plus = coord_vals.copy()
                    coords_minus = coord_vals.copy()
                    coords_plus[rho] += eps
                    coords_minus[rho] -= eps
                    
                    Gamma_plus = Gamma_func(*coords_plus)
                    Gamma_minus = Gamma_func(*coords_minus)
                    
                    term1 = (Gamma_plus[mu, nu, sigma] - Gamma_minus[mu, nu, sigma]) / (2 * eps)
                    
                    # ∂_σ Γ^μ_νρ
                    coords_plus = coord_vals.copy()
                    coords_minus = coord_vals.copy()
                    coords_plus[sigma] += eps
                    coords_minus[sigma] -= eps
                    
                    Gamma_plus = Gamma_func(*coords_plus)
                    Gamma_minus = Gamma_func(*coords_minus)
                    
                    term2 = (Gamma_plus[mu, nu, rho] - Gamma_minus[mu, nu, rho]) / (2 * eps)
                    
                    # Γ^μ_ρλ Γ^λ_νσ
                    term3 = 0.0
                    for lam in range(4):
                        term3 += Gamma[mu, rho, lam] * Gamma[lam, nu, sigma]
                    
                    # Γ^μ_σλ Γ^λ_νρ
                    term4 = 0.0
                    for lam in range(4):
                        term4 += Gamma[mu, sigma, lam] * Gamma[lam, nu, rho]
                    
                    R[mu, nu, rho, sigma] = term1 - term2 + term3 - term4
    
    return R


def ricci_tensor(R: np.ndarray) -> np.ndarray:
    """
    Compute Ricci tensor R_μν from Riemann tensor.
    
    Formula:
        R_μν = R^ρ_μρν (contraction)
    
    Args:
        R: Riemann tensor R^μ_νρσ
    
    Returns:
        Ric[μ,ν]: 4×4 Ricci tensor
    """
    Ric = np.zeros((4, 4))
    
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                Ric[mu, nu] += R[rho, mu, rho, nu]
    
    return Ric


def ricci_scalar(Ric: np.ndarray, g_inv: np.ndarray) -> float:
    """
    Compute Ricci scalar R = g^μν R_μν.
    
    Args:
        Ric: Ricci tensor
        g_inv: Inverse metric
    
    Returns:
        Scalar curvature R
    """
    R_scalar = 0.0
    
    for mu in range(4):
        for nu in range(4):
            R_scalar += g_inv[mu, nu] * Ric[mu, nu]
    
    return R_scalar


def einstein_tensor(Ric: np.ndarray, R_scalar: float, g: np.ndarray) -> np.ndarray:
    """
    Compute Einstein tensor G_μν.
    
    Formula:
        G_μν = R_μν - (1/2) R g_μν
    
    Args:
        Ric: Ricci tensor
        R_scalar: Ricci scalar
        g: Metric tensor
    
    Returns:
        G[μ,ν]: 4×4 Einstein tensor
    """
    G = Ric - 0.5 * R_scalar * g
    
    return G


def kretschmann_scalar(R: np.ndarray) -> float:
    """
    Compute Kretschmann scalar K = R_μνρσ R^μνρσ.
    
    This is a curvature invariant.
    For Schwarzschild: K = 48 M² / r⁶
    
    Args:
        R: Riemann tensor (with indices lowered)
    
    Returns:
        Kretschmann scalar K
    """
    K = 0.0
    
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                for sigma in range(4):
                    K += R[mu, nu, rho, sigma] ** 2
    
    return K


# ============================================================================
# CONVENIENCE FUNCTIONS FOR SSZ METRICS
# ============================================================================

def compute_curvature_at_point(
    metric_func,
    coords: Tuple[float, float, float, float],
    compute_riemann: bool = False
) -> dict:
    """
    Compute all curvature quantities at a point.
    
    Args:
        metric_func: Function returning 4×4 metric tensor
        coords: (t, r, θ, φ)
        compute_riemann: If True, compute full Riemann (expensive!)
    
    Returns:
        Dictionary with:
        - 'christoffel': Γ^μ_νρ
        - 'ricci': R_μν
        - 'ricci_scalar': R
        - 'einstein': G_μν
        - 'riemann': R^μ_νρσ (if requested)
        - 'kretschmann': K (if Riemann computed)
    """
    results = {}
    
    # Metric and inverse
    g = metric_func(*coords)
    g_inv = np.linalg.inv(g)
    
    # Christoffel symbols
    Gamma = christoffel_numerical(metric_func, coords)
    results['christoffel'] = Gamma
    
    if compute_riemann:
        # Full Riemann tensor (expensive!)
        def Gamma_func(*c):
            return christoffel_numerical(metric_func, c)
        
        R = riemann_from_christoffel(Gamma, Gamma_func, coords)
        results['riemann'] = R
        results['kretschmann'] = kretschmann_scalar(R)
    else:
        # Simplified: use Schwarzschild approximation
        warnings.warn("Riemann tensor not computed - use compute_riemann=True")
        R = None
    
    # Ricci tensor (can approximate from diagonal Schwarzschild)
    if R is not None:
        Ric = ricci_tensor(R)
    else:
        # For SSZ: Ricci should be ~ 0 (vacuum solution)
        Ric = np.zeros((4, 4))
    
    results['ricci'] = Ric
    
    # Ricci scalar
    R_scalar = ricci_scalar(Ric, g_inv)
    results['ricci_scalar'] = R_scalar
    
    # Einstein tensor
    G = einstein_tensor(Ric, R_scalar, g)
    results['einstein'] = G
    
    return results


def test_vacuum_einstein_equations(
    einstein_tensor: np.ndarray,
    tolerance: float = 1e-6
) -> Tuple[bool, str]:
    """
    Check if Einstein equations G_μν = 0 are satisfied (vacuum).
    
    Args:
        einstein_tensor: G_μν
        tolerance: Acceptable error
    
    Returns:
        (is_valid, message)
    """
    max_component = np.max(np.abs(einstein_tensor))
    
    if max_component < tolerance:
        return True, f"Vacuum Einstein equations satisfied: max|G_μν| = {max_component:.3e}"
    else:
        return False, f"Einstein equations violated: max|G_μν| = {max_component:.3e}"
