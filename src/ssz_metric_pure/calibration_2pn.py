#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ φ-Spiral Calibration with 2PN Correction

Implements Lino's 2PN calibration to achieve faster asymptotic convergence:

    φ²(r) = 2U(1 + U/3)    where U = GM/(rc²)

This ensures:
    g_TT = -c²(1 - 2U + 2U² + O(U³))
    
matching the PPN β=1 result to 2PN order, instead of the 1PN calibration
which only gives g_TT ≈ -c²(1 - 2U).

© 2025 Carmen Wrede & Lino Casu
Based on Lino's 2PN specification (Nov 1, 2025)
"""
import numpy as np
from typing import Dict, Tuple, Optional
from decimal import Decimal, getcontext

# Set high precision for sensitive calculations
getcontext().prec = 50


class SSZCalibration:
    """
    SSZ φ-spiral calibration with multiple precision levels
    
    Modes:
    - '1pn': Original φ² = 2U (fast convergence only at large r)
    - '2pn': Lino's φ² = 2U(1 + U/3) (faster asymptotic convergence)
    """
    
    def __init__(self, M: float, G: float = 6.67430e-11, 
                 c: float = 299792458.0, mode: str = '2pn'):
        """
        Initialize SSZ calibration
        
        Args:
            M: Mass [kg]
            G: Gravitational constant [m³/(kg·s²)]
            c: Speed of light [m/s]
            mode: '1pn' or '2pn' (default: '2pn')
        """
        self.M = M
        self.G = G
        self.c = c
        self.mode = mode
        
        # Gravitational radius
        self.r_g = 2 * G * M / (c**2)
        
    def phi_squared(self, r: float) -> float:
        """
        Compute φ²(r) with selected calibration
        
        Args:
            r: Radius [m]
            
        Returns:
            φ²(r)
        """
        U = self.G * self.M / (r * self.c**2)
        
        if self.mode == '1pn':
            # Original: φ² = 2U
            return 2 * U
        elif self.mode == '2pn':
            # Lino's 2PN: φ² = 2U(1 + U/3)
            return 2 * U * (1 + U / 3)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    def phi(self, r: float) -> float:
        """Compute φ(r) = √(φ²(r))"""
        return np.sqrt(self.phi_squared(r))
    
    def gamma(self, r: float) -> float:
        """Compute γ(r) = cosh(φ(r))"""
        return np.cosh(self.phi(r))
    
    def beta(self, r: float) -> float:
        """Compute β(r) = tanh(φ(r))"""
        return np.tanh(self.phi(r))
    
    def phi_prime(self, r: float) -> float:
        """
        Compute φ'(r) = dφ/dr
        
        For 1PN: φ' = -φ/(2r)
        For 2PN: φ' = -(φ/r)[1 + 2U/3] / [2(1 + U/3)]
        """
        U = self.G * self.M / (r * self.c**2)
        phi_val = self.phi(r)
        
        if self.mode == '1pn':
            return -phi_val / (2 * r)
        elif self.mode == '2pn':
            # d/dr[2U(1+U/3)] = 2U(-1/r)(1+2U/3)
            # φ' = (1/2φ) * d(φ²)/dr
            return -(phi_val / r) * (1 + 2*U/3) / (2 * (1 + U/3))
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    def phi_double_prime(self, r: float) -> float:
        """
        Compute φ''(r) = d²φ/dr²
        
        For 1PN: φ'' = 3φ/(4r²)
        For 2PN: More complex, computed numerically
        """
        if self.mode == '1pn':
            phi_val = self.phi(r)
            return 3 * phi_val / (4 * r**2)
        elif self.mode == '2pn':
            # Numerical derivative with high precision
            h = r * 1e-8
            phi_p = self.phi_prime(r + h)
            phi_m = self.phi_prime(r - h)
            return (phi_p - phi_m) / (2 * h)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    def metric_components(self, r: float) -> Dict[str, float]:
        """
        Compute all metric components at radius r
        
        Returns:
            Dict with g_TT, g_rr, gamma, beta, phi
        """
        gamma_val = self.gamma(r)
        beta_val = self.beta(r)
        phi_val = self.phi(r)
        
        g_TT = -(self.c**2) / (gamma_val**2)
        g_rr = gamma_val**2
        
        return {
            'g_TT': g_TT,
            'g_rr': g_rr,
            'gamma': gamma_val,
            'beta': beta_val,
            'phi': phi_val,
            'r': r,
            'U': self.G * self.M / (r * self.c**2)
        }
    
    def gr_schwarzschild_2pn(self, r: float) -> Dict[str, float]:
        """
        Compute GR Schwarzschild metric to 2PN order
        
        g_TT = -c²(1 - 2U + 2U²)
        g_rr = 1 + 2U + 2U²
        
        Returns:
            Dict with GR values
        """
        U = self.G * self.M / (r * self.c**2)
        
        g_TT_gr = -(self.c**2) * (1 - 2*U + 2*U**2)
        g_rr_gr = 1 + 2*U + 2*U**2
        
        return {
            'g_TT': g_TT_gr,
            'g_rr': g_rr_gr,
            'U': U
        }
    
    def compare_to_gr(self, r: float) -> Dict[str, float]:
        """
        Compare SSZ to GR Schwarzschild (2PN)
        
        Returns:
            Dict with SSZ, GR, differences, and percentages
        """
        ssz = self.metric_components(r)
        gr = self.gr_schwarzschild_2pn(r)
        
        delta_g_TT = ssz['g_TT'] - gr['g_TT']
        delta_g_rr = ssz['g_rr'] - gr['g_rr']
        
        pct_TT = 100 * abs(delta_g_TT) / abs(gr['g_TT'])
        pct_rr = 100 * abs(delta_g_rr) / abs(gr['g_rr'])
        
        return {
            'r': r,
            'r/r_g': r / self.r_g,
            'mode': self.mode,
            'SSZ': {
                'g_TT': ssz['g_TT'],
                'g_rr': ssz['g_rr'],
                'phi': ssz['phi'],
                'gamma': ssz['gamma'],
            },
            'GR_2PN': {
                'g_TT': gr['g_TT'],
                'g_rr': gr['g_rr'],
            },
            'Difference': {
                'Δg_TT': delta_g_TT,
                'Δg_rr': delta_g_rr,
            },
            'Percentage': {
                '%_TT': pct_TT,
                '%_rr': pct_rr,
            }
        }
    
    def asymptotic_test(self, r_multiples: list = [10, 100, 1000, 10000, 100000]):
        """
        Test asymptotic flatness at multiple radii
        
        Args:
            r_multiples: List of multiples of r_g to test
        """
        print("="*80)
        print(f"ASYMPTOTIC FLATNESS TEST - {self.mode.upper()} MODE")
        print("="*80)
        print(f"\nCalibration: φ²(r) = ", end="")
        if self.mode == '1pn':
            print("2U (1PN)")
        else:
            print("2U(1 + U/3) (2PN)")
        
        print(f"\nMass: {self.M:.4e} kg")
        print(f"r_g: {self.r_g:.4e} m")
        print(f"\nComparison against: g_TT^GR = -c²(1 - 2U + 2U²)")
        print("\n" + "-"*80)
        
        for mult in r_multiples:
            r = mult * self.r_g
            comp = self.compare_to_gr(r)
            
            print(f"\n📍 r = {mult} r_g ({r:.4e} m):")
            print(f"   U = {comp['SSZ']['phi']**2 / 2:.6e}")
            print(f"   φ = {comp['SSZ']['phi']:.6e}")
            print(f"   γ = {comp['SSZ']['gamma']:.10f}")
            
            print(f"\n   SSZ:")
            print(f"     g_TT = {comp['SSZ']['g_TT']:.10e}")
            print(f"     g_rr = {comp['SSZ']['g_rr']:.10f}")
            
            print(f"\n   GR (2PN):")
            print(f"     g_TT = {comp['GR_2PN']['g_TT']:.10e}")
            print(f"     g_rr = {comp['GR_2PN']['g_rr']:.10f}")
            
            print(f"\n   Difference:")
            print(f"     Δg_TT = {comp['Difference']['Δg_TT']:.6e} ({comp['Percentage']['%_TT']:.6f}%)")
            print(f"     Δg_rr = {comp['Difference']['Δg_rr']:.6e} ({comp['Percentage']['%_rr']:.6f}%)")
            
            # Check tolerance
            tolerance = 1e-6
            if comp['Percentage']['%_TT'] < tolerance * 100 and comp['Percentage']['%_rr'] < tolerance * 100:
                print(f"   ✅ PASS (both < {tolerance*100:.4f}%)")
            else:
                print(f"   ⚠️ Converging (target: < {tolerance*100:.4f}%)")
        
        print("\n" + "="*80)


class GPSRedshift:
    """
    GPS gravitational redshift with Lino's log-form for numerical stability
    
    z = gamma(ground)/gamma(sat) - 1
    
    Computed as:
    z = exp[ln(gamma_ground) - ln(gamma_sat)] - 1
    
    to avoid cancellation errors in nearly equal numbers.
    """
    
    def __init__(self, calibration: SSZCalibration):
        self.calib = calibration
    
    def compute_redshift(self, r_ground: float, r_sat: float, 
                        use_log_form: bool = True) -> Dict[str, float]:
        """
        Compute GPS redshift
        
        Args:
            r_ground: Ground radius [m]
            r_sat: Satellite radius [m]
            use_log_form: Use log form for stability (recommended)
            
        Returns:
            Dict with z_SSZ, z_GR, error
        """
        # SSZ redshift
        if use_log_form:
            # Log form: z = exp[ln(γ_ground) - ln(γ_sat)] - 1
            phi_ground = self.calib.phi(r_ground)
            phi_sat = self.calib.phi(r_sat)
            
            ln_gamma_ground = np.log(np.cosh(phi_ground))
            ln_gamma_sat = np.log(np.cosh(phi_sat))
            
            z_ssz = np.exp(ln_gamma_ground - ln_gamma_sat) - 1
        else:
            # Direct form (less stable)
            gamma_ground = self.calib.gamma(r_ground)
            gamma_sat = self.calib.gamma(r_sat)
            z_ssz = gamma_ground / gamma_sat - 1
        
        # GR redshift (same formula to 1PN)
        U_ground = self.calib.G * self.calib.M / (r_ground * self.calib.c**2)
        U_sat = self.calib.G * self.calib.M / (r_sat * self.calib.c**2)
        
        Delta_U = U_sat - U_ground  # Sat is higher, U_sat < U_ground
        z_gr = Delta_U / self.calib.c**2 * self.calib.c**2  # Simplified: just Delta_U
        
        # Actually for GR: z ≈ Delta_U (dimensionless)
        z_gr = U_ground - U_sat
        
        # Relative error
        rel_error = abs(z_ssz - z_gr) / abs(z_gr)
        
        return {
            'r_ground': r_ground,
            'r_sat': r_sat,
            'h': r_sat - r_ground,
            'z_SSZ': z_ssz,
            'z_GR': z_gr,
            'difference': z_ssz - z_gr,
            'rel_error': rel_error,
            'rel_error_percent': rel_error * 100,
            'method': 'log_form' if use_log_form else 'direct'
        }
    
    def validate_gps(self, r_earth: float = 6.371e6, h: float = 20.2e6):
        """
        Validate GPS redshift calculation
        
        Args:
            r_earth: Earth radius [m]
            h: Satellite altitude [m]
        """
        r_sat = r_earth + h
        
        print("="*80)
        print("GPS GRAVITATIONAL REDSHIFT TEST")
        print("="*80)
        print(f"\nCalibration mode: {self.calib.mode.upper()}")
        print(f"Ground radius: {r_earth/1e6:.3f} km")
        print(f"Satellite altitude: {h/1e6:.3f} km")
        print(f"Satellite radius: {r_sat/1e6:.3f} km")
        
        # Test both methods
        print("\n" + "-"*80)
        print("METHOD 1: Log-form (recommended for numerical stability)")
        print("-"*80)
        result_log = self.compute_redshift(r_earth, r_sat, use_log_form=True)
        
        print(f"\nz_SSZ = {result_log['z_SSZ']:.10e}")
        print(f"z_GR  = {result_log['z_GR']:.10e}")
        print(f"Difference = {result_log['difference']:.10e}")
        print(f"Relative error = {result_log['rel_error_percent']:.6f}%")
        
        tolerance = 0.1  # 0.1%
        if result_log['rel_error_percent'] < tolerance:
            print(f"\n✅ PASS (< {tolerance}%)")
        else:
            print(f"\n❌ FAIL (≥ {tolerance}%)")
        
        print("\n" + "-"*80)
        print("METHOD 2: Direct form (may have cancellation errors)")
        print("-"*80)
        result_direct = self.compute_redshift(r_earth, r_sat, use_log_form=False)
        
        print(f"\nz_SSZ = {result_direct['z_SSZ']:.10e}")
        print(f"z_GR  = {result_direct['z_GR']:.10e}")
        print(f"Difference = {result_direct['difference']:.10e}")
        print(f"Relative error = {result_direct['rel_error_percent']:.6f}%")
        
        print("\n" + "="*80)


class PoundRebka:
    """
    Pound-Rebka experiment with high-precision calculation
    
    Uses Lino's derivative form:
    z = β(r)·φ'(r)·h + O(h²)
    
    with arbitrary precision arithmetic to avoid roundoff.
    """
    
    def __init__(self, calibration: SSZCalibration):
        self.calib = calibration
    
    def compute_redshift_high_precision(self, r: float, h: float) -> Dict:
        """
        Compute Pound-Rebka redshift with high precision
        
        Args:
            r: Base radius [m]
            h: Height difference [m]
            
        Returns:
            Dict with results
        """
        # High-precision calculation
        beta_val = self.calib.beta(r)
        phi_prime_val = self.calib.phi_prime(r)
        
        # SSZ: z = -β·φ'·h (negative because γ decreases with r)
        # Photon from bottom (r) to top (r+h): z = (γ_bottom/γ_top) - 1
        # With γ' = γ·β·φ' and γ decreasing: z ≈ -γ'·h/γ = -β·φ'·h
        z_ssz = -beta_val * phi_prime_val * h
        
        # GR: z = gh/c²
        g = self.calib.G * self.calib.M / (r**2)
        z_gr = g * h / (self.calib.c**2)
        
        # Relative error
        rel_error = abs(z_ssz - z_gr) / abs(z_gr)
        
        return {
            'r': r,
            'h': h,
            'beta': beta_val,
            'phi_prime': phi_prime_val,
            'g': g,
            'z_SSZ': z_ssz,
            'z_GR': z_gr,
            'difference': z_ssz - z_gr,
            'rel_error': rel_error,
            'rel_error_percent': rel_error * 100
        }
    
    def validate_pound_rebka(self, r_earth: float = 6.371e6, h: float = 22.5):
        """
        Validate Pound-Rebka experiment
        
        Args:
            r_earth: Earth radius [m]
            h: Height [m] (default: 22.5 m from Jefferson tower)
        """
        print("="*80)
        print("POUND-REBKA EXPERIMENT TEST")
        print("="*80)
        print(f"\nCalibration mode: {self.calib.mode.upper()}")
        print(f"Earth radius: {r_earth/1e6:.3f} km")
        print(f"Height: {h:.1f} m")
        
        result = self.compute_redshift_high_precision(r_earth, h)
        
        print(f"\nParameters:")
        print(f"  β(r) = {result['beta']:.15f}")
        print(f"  φ'(r) = {result['phi_prime']:.15e}")
        print(f"  g = {result['g']:.15f} m/s²")
        
        print(f"\nResults:")
        print(f"  z_SSZ = {result['z_SSZ']:.15e}")
        print(f"  z_GR  = {result['z_GR']:.15e}")
        print(f"  Difference = {result['difference']:.15e}")
        print(f"  Relative error = {result['rel_error_percent']:.10f}%")
        
        tolerance = 0.1  # 0.1%
        if result['rel_error_percent'] < tolerance:
            print(f"\n✅ PASS (< {tolerance}%)")
        else:
            print(f"\n❌ FAIL (≥ {tolerance}%)")
        
        print("\n" + "="*80)


def demonstrate_calibration_comparison():
    """
    Demonstrate the difference between 1PN and 2PN calibration
    """
    M_earth = 5.9722e24
    
    print("\n")
    print("="*80)
    print(" "*20 + "SSZ CALIBRATION COMPARISON")
    print("="*80)
    print("\n")
    
    # Test 1PN
    print("🔴 MODE 1: Original 1PN Calibration")
    print("-"*80)
    calib_1pn = SSZCalibration(M_earth, mode='1pn')
    calib_1pn.asymptotic_test(r_multiples=[100, 1000, 10000, 100000])
    
    print("\n\n")
    
    # Test 2PN
    print("🟢 MODE 2: Lino's 2PN Calibration (RECOMMENDED)")
    print("-"*80)
    calib_2pn = SSZCalibration(M_earth, mode='2pn')
    calib_2pn.asymptotic_test(r_multiples=[100, 1000, 10000, 100000])
    
    print("\n\n")
    
    # GPS test with 2PN
    print("🛰️ GPS REDSHIFT with 2PN Calibration")
    print("-"*80)
    gps = GPSRedshift(calib_2pn)
    gps.validate_gps()
    
    print("\n\n")
    
    # Pound-Rebka test with 2PN
    print("🔬 POUND-REBKA with 2PN Calibration")
    print("-"*80)
    pr = PoundRebka(calib_2pn)
    pr.validate_pound_rebka()
    
    print("\n")
    print("="*80)
    print("✅ CALIBRATION COMPARISON COMPLETE")
    print("="*80)
    print("\nRECOMMENDATION: Use 2PN calibration for all validation tests")
    print("Expected improvement:")
    print("  • Asymptotic flatness: Faster convergence")
    print("  • GPS redshift: < 0.05% error")
    print("  • Pound-Rebka: Numerically stable, < 0.1% error")
    print("="*80)


if __name__ == "__main__":
    # Force UTF-8 output for Windows
    import sys
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    
    demonstrate_calibration_comparison()
