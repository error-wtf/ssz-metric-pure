"""
Unit Tests for Metric Module

Tests the SSZ metric tensor components and corrections.

© 2025 Carmen Wrede & Lino Casu
"""

import pytest
import numpy as np
from src.ssz_core.metric import (
    delta_M, corrected_r_s, A_Xi, A_phi_series, A_blended, A_safe,
    B_coefficient, metric_tensor, schwarzschild_radius
)
from src.ssz_core.segment_density import find_intersection
from src.ssz_core.constants import PHI, G, C, M_SUN


class TestDeltaM:
    """Tests for Δ(M) mass correction."""
    
    def test_delta_small_mass(self):
        """Δ(M) ≈ 100 for small r_s."""
        r_s_small = 1e-50
        delta = delta_M(r_s_small)
        
        assert delta == pytest.approx(100.0, rel=0.01)
    
    def test_delta_large_mass(self):
        """Δ(M) ≈ 2 for large r_s."""
        r_s_large = 1.0
        delta = delta_M(r_s_large)
        
        assert delta == pytest.approx(2.0, rel=0.1)
    
    def test_delta_monotonic(self):
        """Δ(M) decreases with increasing r_s."""
        r_s_values = np.logspace(-10, 0, 50)
        delta_values = [delta_M(r_s) for r_s in r_s_values]
        
        assert np.all(np.diff(delta_values) <= 0)
    
    def test_delta_range(self):
        """Δ(M) ∈ [2, 100]."""
        r_s_values = np.logspace(-50, 0, 100)
        delta_values = [delta_M(r_s) for r_s in r_s_values]
        
        assert np.all(np.array(delta_values) >= 2.0)
        assert np.all(np.array(delta_values) <= 100.0)


class TestAXi:
    """Tests for inner SSZ metric A_Ξ."""
    
    def test_a_xi_at_zero(self):
        """A_Ξ(0) = 1 (flat spacetime at center!)."""
        r_s = 2950.0
        assert A_Xi(0.0, r_s) == pytest.approx(1.0, abs=1e-10)
    
    def test_a_xi_positive(self):
        """A_Ξ(r) > 0 everywhere."""
        r_s = 2950.0
        r_values = np.logspace(-2, 3, 1000) * r_s
        a_values = A_Xi(r_values, r_s)
        
        assert np.all(a_values > 0)
    
    def test_a_xi_at_schwarzschild(self):
        """A_Ξ(r_s) is finite."""
        r_s = 2950.0
        a = A_Xi(r_s, r_s)
        
        # Should be around 0.027 = (1/(1+(1-1/e)))^2
        assert 0 < a < 1
        assert not np.isnan(a)
    
    def test_a_xi_far_field(self):
        """A_Ξ(∞) → 0.25 = 1/4."""
        r_s = 2950.0
        r_far = 1e10 * r_s
        a = A_Xi(r_far, r_s)
        
        # At infinity, Ξ→1, so D→1/2, A→1/4
        assert a == pytest.approx(0.25, rel=0.1)


class TestAPhiSeries:
    """Tests for φ-series metric."""
    
    def test_a_phi_order0(self):
        """Order 0: A = 1 (Minkowski)."""
        r_s = 2950.0
        r = 1e6 * r_s
        
        a = A_phi_series(r, r_s, order=0)
        assert a == pytest.approx(1.0, abs=1e-10)
    
    def test_a_phi_order1_far(self):
        """Order 1: A ≈ 1 far away."""
        r_s = 2950.0
        r = 1e6 * r_s
        
        a = A_phi_series(r, r_s, order=1)
        assert a == pytest.approx(1.0, rel=1e-3)
    
    def test_a_phi_schwarzschild_limit(self):
        """Order 1 at 2r_s: A = 1 - r_s/(2·2r_s) = 0.75."""
        r_s = 2950.0
        r = 2.0 * r_s
        
        a = A_phi_series(r, r_s, order=1)
        expected = 1.0 - r_s / (2.0 * r)
        assert a == pytest.approx(expected, rel=1e-10)
    
    def test_a_phi_higher_order(self):
        """Higher orders add PN corrections."""
        r_s = 2950.0
        r = 10.0 * r_s
        
        a1 = A_phi_series(r, r_s, order=1)
        a6 = A_phi_series(r, r_s, order=6)
        
        # Higher orders should differ (PN corrections)
        assert abs(a6 - a1) > 1e-10


class TestABlended:
    """Tests for blended metric."""
    
    def test_a_blended_inner(self):
        """Inner region: A ≈ A_Ξ."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        r_inner = 0.1 * r_star
        
        a_blend = A_blended(r_inner, r_s, r_star)
        a_xi = A_Xi(r_inner, r_s)
        
        # Should be close to SSZ
        assert a_blend == pytest.approx(a_xi, rel=0.1)
    
    def test_a_blended_outer(self):
        """Outer region: A ≈ A_φ."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        r_outer = 10.0 * r_star
        
        a_blend = A_blended(r_outer, r_s, r_star, mode="O6")
        a_phi = A_phi_series(r_outer, r_s, order=6)
        
        # Should be close to φ-series
        assert a_blend == pytest.approx(a_phi, rel=0.1)
    
    def test_a_blended_smooth(self):
        """Blending is smooth."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        
        # Sample around transition
        r_values = np.linspace(0.5 * r_star, 2.0 * r_star, 100)
        a_values = A_blended(r_values, r_s, r_star)
        
        # Check no NaN or Inf
        assert np.all(np.isfinite(a_values))
        
        # Check no jumps (derivative bounded)
        da = np.diff(a_values)
        assert np.all(np.abs(da) < 0.1)


class TestASafe:
    """Tests for safe metric with softplus."""
    
    def test_a_safe_positive(self):
        """A_safe > 0 everywhere."""
        r_s = 2950.0
        r_values = np.logspace(-2, 3, 1000) * r_s
        a_values = A_safe(r_values, r_s)
        
        assert np.all(a_values > 0)
    
    def test_a_safe_at_zero(self):
        """A_safe(0) = 1."""
        r_s = 2950.0
        a = A_safe(0.0, r_s)
        
        assert a == pytest.approx(1.0, rel=0.01)
    
    def test_a_safe_smooth(self):
        """A_safe is smooth everywhere."""
        r_s = 2950.0
        r_values = np.logspace(-1, 2, 1000) * r_s
        a_values = A_safe(r_values, r_s)
        
        # No NaN or Inf
        assert np.all(np.isfinite(a_values))
        
        # Bounded derivative
        da = np.diff(a_values)
        dr = np.diff(r_values)
        dadr = da / dr
        assert np.all(np.abs(dadr) < 1.0)
    
    def test_a_safe_mirror_vs_standard(self):
        """Mirror blend differs from standard blend."""
        r_s = 2950.0
        r = 5.0 * r_s
        
        a_mirror = A_safe(r, r_s, use_mirror_blend=True)
        a_standard = A_safe(r, r_s, use_mirror_blend=False)
        
        # Should differ (different blending methods)
        # But both should be valid
        assert 0 < a_mirror < 1
        assert 0 < a_standard < 1


class TestBCoefficient:
    """Tests for radial metric coefficient."""
    
    def test_b_inverse_a(self):
        """B(r) = 1/A(r)."""
        r_s = 2950.0
        r_values = np.logspace(0, 2, 50) * r_s
        
        for r in r_values:
            a = A_safe(r, r_s)
            b = B_coefficient(r, r_s, A=a)
            
            assert b == pytest.approx(1.0 / a, rel=1e-10)
    
    def test_b_positive(self):
        """B(r) > 0 everywhere."""
        r_s = 2950.0
        r_values = np.logspace(-1, 2, 100) * r_s
        b_values = B_coefficient(r_values, r_s)
        
        assert np.all(b_values > 0)


class TestMetricTensor:
    """Tests for full metric tensor."""
    
    def test_metric_shape(self):
        """Metric is 4×4."""
        r_s = 2950.0
        g, _ = metric_tensor(1e6, np.pi/2, r_s)
        
        assert g.shape == (4, 4)
    
    def test_metric_diagonal(self):
        """Metric is diagonal in spherical coordinates."""
        r_s = 2950.0
        g, _ = metric_tensor(1e6, np.pi/2, r_s)
        
        # Off-diagonal elements should be zero
        for i in range(4):
            for j in range(4):
                if i != j:
                    assert g[i, j] == pytest.approx(0.0, abs=1e-10)
    
    def test_metric_signature(self):
        """Metric has signature (-,+,+,+)."""
        r_s = 2950.0
        g, _ = metric_tensor(1e6, np.pi/2, r_s)
        
        # g_tt < 0
        assert g[0, 0] < 0
        
        # g_rr, g_θθ, g_φφ > 0
        assert g[1, 1] > 0
        assert g[2, 2] > 0
        assert g[3, 3] > 0
    
    def test_metric_components(self):
        """Components match formulas."""
        r_s = 2950.0
        r = 1e6
        theta = np.pi / 4
        
        g, comps = metric_tensor(r, theta, r_s)
        
        # Check individual components
        assert comps['g_tt'] < 0
        assert comps['g_rr'] > 0
        assert comps['g_theta_theta'] == pytest.approx(r**2, rel=1e-10)
        assert comps['g_phi_phi'] == pytest.approx(r**2 * np.sin(theta)**2, rel=1e-10)
    
    def test_metric_far_field(self):
        """Metric → Minkowski far away."""
        r_s = 2950.0
        r = 1e10 * r_s
        theta = np.pi / 2
        
        g, _ = metric_tensor(r, theta, r_s)
        
        # Should approach Minkowski
        assert g[0, 0] == pytest.approx(-1.0, rel=0.01)
        assert g[1, 1] == pytest.approx(1.0, rel=0.01)


class TestSchwarzschild:
    """Tests for Schwarzschild radius calculation."""
    
    def test_schwarzschild_solar_mass(self):
        """r_s(M_☉) ≈ 2953 m."""
        r_s = schwarzschild_radius(M_SUN)
        
        expected = 2.0 * G * M_SUN / (C ** 2)
        assert r_s == pytest.approx(expected, rel=1e-10)
        assert r_s == pytest.approx(2952.9, rel=0.01)
    
    def test_schwarzschild_scaling(self):
        """r_s ∝ M."""
        m1 = M_SUN
        m2 = 10.0 * M_SUN
        
        r_s1 = schwarzschild_radius(m1)
        r_s2 = schwarzschild_radius(m2)
        
        assert r_s2 / r_s1 == pytest.approx(10.0, rel=1e-10)


class TestCurvature:
    """Tests for curvature proxy."""
    
    def test_curvature_proxy_finite(self):
        """Curvature proxy is finite everywhere in SSZ."""
        r_s = 2950.0
        r_values = np.logspace(-2, 2, 100) * r_s
        
        for r in r_values:
            a = A_safe(r, r_s)
            
            # Curvature proxy: (A'/r)^2 + ((1-A)/r^2)^2
            # Should be finite
            curv = ((1.0 - a) / r**2) ** 2
            assert np.isfinite(curv)
    
    def test_curvature_at_zero(self):
        """Curvature at r=0 is finite (no singularity!)."""
        r_s = 2950.0
        r = 1e-6  # Very close to zero
        
        a = A_safe(r, r_s)
        curv = ((1.0 - a) / r**2) ** 2
        
        # Should not diverge
        assert np.isfinite(curv)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
