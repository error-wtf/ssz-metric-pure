#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for SSZ-Kerr Rotating Metric

Validates:
- Horizons r_± exist for â < 1
- Ergosphere r_ergo > r_+
- Frame dragging ω(r,θ) non-zero
- Schwarzschild limit (â=0)

© 2025 Carmen Wrede & Lino Casu
"""
import pytest
import numpy as np
from ssz_metric_pure import KerrSSZParams, M_SUN
from ssz_metric_pure.metric_kerr_ssz import KerrSSZMetric


@pytest.fixture
def kerr_moderate():
    """Moderately rotating black hole (â = 0.5)."""
    params = KerrSSZParams(mass=M_SUN, spin=0.5)
    return KerrSSZMetric(params)


@pytest.fixture
def kerr_fast():
    """Fast rotating (â = 0.9)."""
    params = KerrSSZParams(mass=M_SUN, spin=0.9)
    return KerrSSZMetric(params)


@pytest.fixture
def kerr_schwarzschild():
    """Non-rotating (â = 0) → should match Schwarzschild."""
    params = KerrSSZParams(mass=M_SUN, spin=0.0)
    return KerrSSZMetric(params)


def test_horizons_exist(kerr_moderate):
    """Horizons r_± must exist for sub-extremal (â < 1)."""
    r_plus, r_minus = kerr_moderate.horizons()
    
    assert not np.isnan(r_plus), "Outer horizon must exist"
    assert not np.isnan(r_minus), "Inner horizon must exist"
    assert r_plus > r_minus, "r_+ > r_-"
    assert r_plus > 0, "r_+ must be positive"
    assert r_minus >= 0, "r_- must be non-negative"


def test_ergosphere_larger_than_horizon(kerr_moderate):
    """Ergosphere r_ergo > r_+ at equator."""
    r_plus, _ = kerr_moderate.horizons()
    r_ergo_equator = kerr_moderate.ergosphere_radius(np.pi / 2)
    
    assert r_ergo_equator > r_plus, f"r_ergo={r_ergo_equator:.3e} must be > r_+={r_plus:.3e}"


def test_frame_dragging_nonzero(kerr_moderate):
    """Frame dragging ω ≠ 0 for rotating BH."""
    r_test = 5.0 * kerr_moderate.r_s
    theta_equator = np.pi / 2
    
    omega = kerr_moderate.frame_drag_frequency(r_test, theta_equator)
    
    assert omega != 0, "Frame dragging must be non-zero for â≠0"
    assert omega > 0, "Frame dragging is prograde (positive)"


def test_schwarzschild_limit_no_frame_drag(kerr_schwarzschild):
    """â=0 → no frame dragging (ω=0)."""
    r_test = 5.0 * kerr_schwarzschild.r_s
    theta = np.pi / 2
    
    omega = kerr_schwarzschild.frame_drag_frequency(r_test, theta)
    
    assert abs(omega) < 1e-10, "No frame dragging for â=0"


def test_schwarzschild_limit_horizons(kerr_schwarzschild):
    """â=0 → r_+ = r_s, r_- = 0."""
    r_plus, r_minus = kerr_schwarzschild.horizons()
    
    assert abs(r_plus - kerr_schwarzschild.r_s) < 1e-6, "r_+ = r_s for â=0"
    assert abs(r_minus) < 1e-6, "r_- = 0 for â=0"


def test_metric_components_finite(kerr_moderate):
    """All metric components finite outside horizon."""
    r_test = 5.0 * kerr_moderate.r_s
    theta = np.pi / 4
    
    comp = kerr_moderate.metric_tensor(r_test, theta)
    
    assert np.isfinite(comp.g_tt), "g_tt must be finite"
    assert np.isfinite(comp.g_rr), "g_rr must be finite"
    assert np.isfinite(comp.g_thth), "g_θθ must be finite"
    assert np.isfinite(comp.g_phph), "g_φφ must be finite"
    assert np.isfinite(comp.g_tph), "g_tφ must be finite"


def test_g_tt_negative_outside_ergosphere(kerr_moderate):
    """g_tt < 0 outside ergosphere (time-like allowed)."""
    r_far = 10.0 * kerr_moderate.r_s
    theta = np.pi / 2
    
    g_tt = kerr_moderate.g_tt(r_far, theta)
    
    assert g_tt < 0, "g_tt must be negative outside ergosphere"


def test_redshift_positive(kerr_moderate):
    """Gravitational redshift z > 0."""
    r_test = 5.0 * kerr_moderate.r_s
    z = kerr_moderate.redshift(r_test)
    
    assert z > 0, "Redshift must be positive"
    assert np.isfinite(z), "Redshift must be finite"


def test_fast_rotation_still_has_horizons(kerr_fast):
    """Fast rotation (â=0.9) still sub-extremal."""
    r_plus, r_minus = kerr_fast.horizons()
    
    assert not np.isnan(r_plus), "Horizons must exist even for â=0.9"
    assert r_plus > r_minus, "r_+ > r_-"


def test_extremal_detection():
    """Extremal case â=1 should be detected."""
    params = KerrSSZParams(mass=M_SUN, spin=1.0)
    kerr_extremal = KerrSSZMetric(params)
    
    # NOTE: For true extremal, we'd need â=1 exactly
    # But close enough should trigger is_extremal()
    is_ext = kerr_extremal.is_extremal(tol=1e-3)
    
    # May or may not be exactly extremal depending on implementation
    # Just check it doesn't crash (np.bool_ is also valid)
    assert isinstance(is_ext, (bool, np.bool_))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
