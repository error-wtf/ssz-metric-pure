#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Static SSZ Metric

Validates:
- A(r) > 0 everywhere (singularity-free!)
- A(0) ≈ 1.0 (flat at center)
- A(∞) → 1.0 (asymptotically flat)
- Redshift monotonicity

© 2025 Carmen Wrede & Lino Casu
"""
import pytest
import numpy as np
from ssz_metric_pure import SSZParams, M_SUN
from ssz_metric_pure.metric_static import StaticSSZMetric


@pytest.fixture
def solar_mass_metric():
    """1 Solar mass SSZ metric."""
    params = SSZParams(mass=M_SUN)
    return StaticSSZMetric(params)


def test_A_positive_everywhere(solar_mass_metric):
    """A(r) > 0 everywhere - NO SINGULARITY!"""
    metric = solar_mass_metric
    
    # Test from near-center to far field
    r_test = np.logspace(
        np.log10(0.1 * metric.r_phi),
        np.log10(100 * metric.r_s),
        num=100
    )
    
    A_values = [metric.A_coefficient(r) for r in r_test]
    
    assert all(A > 0 for A in A_values), "A(r) must be positive everywhere!"
    assert min(A_values) > 0.1, f"A_min = {min(A_values):.3f} too small"


def test_flatness_at_center(solar_mass_metric):
    """A(0) ≈ 1.0 - flat spacetime at center."""
    A_center = solar_mass_metric.A_coefficient(1e-10)
    
    assert abs(A_center - 1.0) < 0.1, f"A(0) = {A_center:.3f} not flat"


def test_asymptotic_flatness(solar_mass_metric):
    """A(r→∞) → 1.0 - asymptotically flat."""
    r_far = 100.0 * solar_mass_metric.r_s
    A_far = solar_mass_metric.A_coefficient(r_far)
    
    assert abs(A_far - 1.0) < 0.01, f"A(∞) = {A_far:.3f} not asymptotically flat"


def test_B_equals_1_over_A(solar_mass_metric):
    """B(r) = 1/A(r) relation."""
    r_test = 5.0 * solar_mass_metric.r_s
    
    A = solar_mass_metric.A_coefficient(r_test)
    B = solar_mass_metric.B_coefficient(r_test)
    
    assert abs(A * B - 1.0) < 1e-10, "B ≠ 1/A"


def test_metric_tensor(solar_mass_metric):
    """Full metric tensor computation."""
    r = 3.0 * solar_mass_metric.r_s
    theta = np.pi / 4
    
    components = solar_mass_metric.metric_tensor(r, theta)
    
    assert components.g_tt < 0, "g_tt must be negative"
    assert components.g_rr > 0, "g_rr must be positive"
    assert components.g_thth == r * r, "g_θθ ≠ r²"
    assert components.A > 0, "A must be positive"
    assert components.B > 0, "B must be positive"


def test_redshift_positive(solar_mass_metric):
    """Gravitational redshift z > 0."""
    r = 2.0 * solar_mass_metric.r_s
    z = solar_mass_metric.redshift(r)
    
    assert z > 0, f"Redshift {z:.3f} must be positive"


def test_escape_velocity(solar_mass_metric):
    """Escape velocity v_esc < c."""
    from ssz_metric_pure import C_SI
    
    r = 5.0 * solar_mass_metric.r_s
    v_esc = solar_mass_metric.escape_velocity(r)
    
    assert 0 < v_esc < C_SI, f"v_esc = {v_esc:.3e} unphysical"


def test_validation_checks(solar_mass_metric):
    """Run all validation checks."""
    valid_center, msg_center = solar_mass_metric.check_flatness_at_center()
    valid_inf, msg_inf = solar_mass_metric.check_asymptotic_flatness()
    valid_pos, msg_pos = solar_mass_metric.check_positive_definite()
    
    assert valid_center, msg_center
    assert valid_inf, msg_inf
    assert valid_pos, msg_pos


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
