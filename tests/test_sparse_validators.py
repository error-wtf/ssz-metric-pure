#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest suite for SSZ symbolic sparse validators

Tests:
- Metric compatibility: ∇_α g_μν = 0
- Energy conservation along geodesics
- Earth and Solar mass cases

© 2025 Carmen Wrede & Lino Casu
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ssz_metric_pure.ssz_symbolic_sparse import (
    validator_nabla_g_zero,
    validator_energy_conservation
)

# Physical constants
M_EARTH = 5.9722e24  # kg
M_SUN = 1.98847e30   # kg
G_SI = 6.67430e-11   # m³/(kg·s²)
C_SI = 299792458.0   # m/s

# Tolerance thresholds
NABLA_G_TOLERANCE = 1e-10
ENERGY_TOLERANCE = 1e-6


class TestMetricCompatibility:
    """Test ∇_α g_μν = 0 (metric compatibility)"""
    
    def test_nabla_g_earth_weak_field(self):
        """Test metric compatibility for Earth (weak field)"""
        max_error = validator_nabla_g_zero(
            max_r_samples=5,
            r_min=6.4e6,     # Earth radius
            r_max=6.4e9,     # 1000x Earth radius
            M_val=M_EARTH,
            G_val=G_SI,
            c_val=C_SI
        )
        
        print(f"\n  Earth weak field: max|∇_r g_μν| = {max_error:.3e}")
        assert max_error < NABLA_G_TOLERANCE, \
            f"Metric compatibility failed: {max_error:.3e} > {NABLA_G_TOLERANCE:.3e}"
    
    def test_nabla_g_earth_intermediate(self):
        """Test metric compatibility for Earth (intermediate field)"""
        max_error = validator_nabla_g_zero(
            max_r_samples=5,
            r_min=1e6,       # Below Earth surface
            r_max=1e8,       # ~100 Earth radii
            M_val=M_EARTH,
            G_val=G_SI,
            c_val=C_SI
        )
        
        print(f"\n  Earth intermediate: max|∇_r g_μν| = {max_error:.3e}")
        assert max_error < NABLA_G_TOLERANCE, \
            f"Metric compatibility failed: {max_error:.3e} > {NABLA_G_TOLERANCE:.3e}"
    
    def test_nabla_g_sun_weak_field(self):
        """Test metric compatibility for Sun (weak field)"""
        max_error = validator_nabla_g_zero(
            max_r_samples=5,
            r_min=6.96e8,    # Solar radius
            r_max=6.96e11,   # 1000x Solar radius
            M_val=M_SUN,
            G_val=G_SI,
            c_val=C_SI
        )
        
        print(f"\n  Sun weak field: max|∇_r g_μν| = {max_error:.3e}")
        assert max_error < NABLA_G_TOLERANCE, \
            f"Metric compatibility failed: {max_error:.3e} > {NABLA_G_TOLERANCE:.3e}"
    
    def test_nabla_g_sun_intermediate(self):
        """Test metric compatibility for Sun (intermediate field)"""
        max_error = validator_nabla_g_zero(
            max_r_samples=5,
            r_min=1e8,       # Below solar surface
            r_max=1e10,      # ~14 Solar radii
            M_val=M_SUN,
            G_val=G_SI,
            c_val=C_SI
        )
        
        print(f"\n  Sun intermediate: max|∇_r g_μν| = {max_error:.3e}")
        assert max_error < NABLA_G_TOLERANCE, \
            f"Metric compatibility failed: {max_error:.3e} > {NABLA_G_TOLERANCE:.3e}"


class TestEnergyConservation:
    """Test energy conservation along timelike geodesics"""
    
    def test_energy_earth_low_orbit(self):
        """Test energy conservation for Earth low orbit"""
        drift = validator_energy_conservation(
            M_val=M_EARTH,
            G_val=G_SI,
            c_val=C_SI,
            r0=7.0e6,        # ~500 km altitude
            steps=5000,
            dlam=1e-3
        )
        
        print(f"\n  Earth low orbit: E drift = {drift:.3e}")
        assert drift < ENERGY_TOLERANCE, \
            f"Energy conservation failed: {drift:.3e} > {ENERGY_TOLERANCE:.3e}"
    
    def test_energy_earth_high_orbit(self):
        """Test energy conservation for Earth high orbit"""
        drift = validator_energy_conservation(
            M_val=M_EARTH,
            G_val=G_SI,
            c_val=C_SI,
            r0=2.0e7,        # ~20000 km altitude
            steps=5000,
            dlam=1e-3
        )
        
        print(f"\n  Earth high orbit: E drift = {drift:.3e}")
        assert drift < ENERGY_TOLERANCE, \
            f"Energy conservation failed: {drift:.3e} > {ENERGY_TOLERANCE:.3e}"
    
    def test_energy_sun_surface(self):
        """Test energy conservation for Sun at surface"""
        drift = validator_energy_conservation(
            M_val=M_SUN,
            G_val=G_SI,
            c_val=C_SI,
            r0=7.0e8,        # Just above solar surface
            steps=5000,
            dlam=1e-3
        )
        
        print(f"\n  Sun surface: E drift = {drift:.3e}")
        assert drift < ENERGY_TOLERANCE, \
            f"Energy conservation failed: {drift:.3e} > {ENERGY_TOLERANCE:.3e}"
    
    def test_energy_sun_corona(self):
        """Test energy conservation for Sun in corona"""
        drift = validator_energy_conservation(
            M_val=M_SUN,
            G_val=G_SI,
            c_val=C_SI,
            r0=1.0e9,        # ~1.4 Solar radii
            steps=5000,
            dlam=1e-3
        )
        
        print(f"\n  Sun corona: E drift = {drift:.3e}")
        assert drift < ENERGY_TOLERANCE, \
            f"Energy conservation failed: {drift:.3e} > {ENERGY_TOLERANCE:.3e}"


class TestRobustness:
    """Test robustness and edge cases"""
    
    def test_nabla_g_different_samples(self):
        """Test with different sampling densities"""
        for n_samples in [3, 5, 10]:
            max_error = validator_nabla_g_zero(
                max_r_samples=n_samples,
                r_min=6.4e6,
                r_max=6.4e9,
                M_val=M_EARTH,
                G_val=G_SI,
                c_val=C_SI
            )
            
            print(f"\n  {n_samples} samples: max|∇_r g_μν| = {max_error:.3e}")
            assert max_error < NABLA_G_TOLERANCE
    
    def test_energy_different_steps(self):
        """Test with different integration steps"""
        for n_steps in [1000, 5000, 10000]:
            drift = validator_energy_conservation(
                M_val=M_EARTH,
                G_val=G_SI,
                c_val=C_SI,
                r0=7.0e6,
                steps=n_steps,
                dlam=1e-3
            )
            
            print(f"\n  {n_steps} steps: E drift = {drift:.3e}")
            assert drift < ENERGY_TOLERANCE
    
    def test_energy_different_dlam(self):
        """Test with different step sizes"""
        for dlam in [1e-4, 1e-3, 1e-2]:
            drift = validator_energy_conservation(
                M_val=M_EARTH,
                G_val=G_SI,
                c_val=C_SI,
                r0=7.0e6,
                steps=5000,
                dlam=dlam
            )
            
            print(f"\n  dlam={dlam:.1e}: E drift = {drift:.3e}")
            assert drift < ENERGY_TOLERANCE


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


if __name__ == "__main__":
    """Run tests directly with pytest"""
    pytest.main([__file__, "-v", "-s"])
