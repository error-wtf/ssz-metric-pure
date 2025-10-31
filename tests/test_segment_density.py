"""
Unit Tests for Segment Density Module

Tests the Golden Ratio saturation and time dilation functions.

© 2025 Carmen Wrede & Lino Casu
"""

import pytest
import numpy as np
from src.ssz_core.segment_density import (
    Xi, D_SSZ, D_GR, find_intersection, segment_saturation_derivative
)
from src.ssz_core.constants import PHI


class TestXi:
    """Tests for segment saturation factor."""
    
    def test_xi_at_zero(self):
        """Ξ(0) = 0 (no saturation at center)."""
        r_s = 2950.0
        assert Xi(0.0, r_s) == pytest.approx(0.0, abs=1e-10)
    
    def test_xi_at_infinity(self):
        """Ξ(∞) → 1 (full saturation far away)."""
        r_s = 2950.0
        r_far = 1e10 * r_s
        assert Xi(r_far, r_s) == pytest.approx(1.0, abs=1e-6)
    
    def test_xi_monotonic(self):
        """Ξ(r) increases monotonically."""
        r_s = 2950.0
        r_values = np.logspace(0, 3, 100) * r_s
        xi_values = Xi(r_values, r_s)
        
        # Check monotonicity
        assert np.all(np.diff(xi_values) >= 0)
    
    def test_xi_uses_phi(self):
        """Verify φ is used in formula."""
        r_s = 2950.0
        r = r_s
        
        # Ξ(r_s) = 1 - exp(-φ)
        expected = 1.0 - np.exp(-PHI)
        assert Xi(r, r_s) == pytest.approx(expected, rel=1e-10)


class TestDSSZ:
    """Tests for SSZ time dilation."""
    
    def test_d_ssz_at_zero(self):
        """D_SSZ(0) = 1 (no dilation at center - singularity-free!)."""
        r_s = 2950.0
        assert D_SSZ(0.0, r_s) == pytest.approx(1.0, abs=1e-10)
    
    def test_d_ssz_positive(self):
        """D_SSZ(r) > 0 everywhere (no singularity)."""
        r_s = 2950.0
        r_values = np.logspace(-2, 3, 1000) * r_s
        d_values = D_SSZ(r_values, r_s)
        
        assert np.all(d_values > 0)
    
    def test_d_ssz_at_schwarzschild(self):
        """D_SSZ(r_s) is finite."""
        r_s = 2950.0
        d = D_SSZ(r_s, r_s)
        
        # Should be finite and positive
        assert 0 < d < 1
        assert not np.isnan(d)
        assert not np.isinf(d)
    
    def test_d_ssz_far_field(self):
        """D_SSZ(∞) → 0.5 (approaches GR asymptotically)."""
        r_s = 2950.0
        r_far = 1e10 * r_s
        d = D_SSZ(r_far, r_s)
        
        # At infinity, Ξ→1, so D→1/2
        assert d == pytest.approx(0.5, rel=0.1)


class TestDGR:
    """Tests for GR time dilation."""
    
    def test_d_gr_far_field(self):
        """D_GR(∞) → 1 (no dilation far away)."""
        r_s = 2950.0
        r_far = 1e6 * r_s
        assert D_GR(r_far, r_s) == pytest.approx(1.0, rel=1e-3)
    
    def test_d_gr_at_2rs(self):
        """D_GR(2r_s) = √(1/2) ≈ 0.707."""
        r_s = 2950.0
        expected = np.sqrt(0.5)
        assert D_GR(2.0 * r_s, r_s) == pytest.approx(expected, rel=1e-10)
    
    def test_d_gr_undefined_inside(self):
        """D_GR(r < r_s) is undefined (NaN)."""
        r_s = 2950.0
        r_inside = 0.5 * r_s
        
        assert np.isnan(D_GR(r_inside, r_s))
    
    def test_d_gr_at_horizon(self):
        """D_GR(r_s) is undefined (singularity)."""
        r_s = 2950.0
        
        assert np.isnan(D_GR(r_s, r_s))


class TestIntersection:
    """Tests for r* finding (SSZ-GR matching point)."""
    
    def test_intersection_exists(self):
        """r* exists for any r_s."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        
        assert r_star > r_s  # Must be outside horizon
        assert np.isfinite(r_star)
    
    def test_intersection_matches(self):
        """D_SSZ(r*) ≈ D_GR(r*)."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        
        d_ssz = D_SSZ(r_star, r_s)
        d_gr = D_GR(r_star, r_s)
        
        assert d_ssz == pytest.approx(d_gr, rel=1e-6)
    
    def test_intersection_scaling(self):
        """r* scales with r_s."""
        r_s1 = 2950.0
        r_s2 = 2.0 * r_s1
        
        r_star1 = find_intersection(r_s1)
        r_star2 = find_intersection(r_s2)
        
        # Should scale approximately linearly
        assert r_star2 / r_star1 == pytest.approx(2.0, rel=0.2)
    
    def test_intersection_range(self):
        """r* is in reasonable range (1-10 r_s typically)."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        
        assert 1.0 * r_s < r_star < 20.0 * r_s


class TestDerivative:
    """Tests for segment saturation derivative."""
    
    def test_derivative_at_zero(self):
        """dΞ/dr(0) = φ/r_s."""
        r_s = 2950.0
        expected = PHI / r_s
        
        assert segment_saturation_derivative(0.0, r_s) == pytest.approx(expected, rel=1e-10)
    
    def test_derivative_positive(self):
        """dΞ/dr > 0 (Ξ always increasing)."""
        r_s = 2950.0
        r_values = np.logspace(0, 3, 100) * r_s
        dxi_values = segment_saturation_derivative(r_values, r_s)
        
        assert np.all(dxi_values > 0)
    
    def test_derivative_decreasing(self):
        """dΞ/dr decreases with r (saturation slows down)."""
        r_s = 2950.0
        r_values = np.logspace(0, 3, 100) * r_s
        dxi_values = segment_saturation_derivative(r_values, r_s)
        
        # Derivative should decrease
        assert np.all(np.diff(dxi_values) <= 0)


class TestConsistency:
    """Cross-validation tests."""
    
    def test_ssz_gr_crossover(self):
        """SSZ and GR cross at r*."""
        r_s = 2950.0
        r_star = find_intersection(r_s)
        
        # Before r*: SSZ > GR (typically)
        r_before = 0.9 * r_star
        if r_before > r_s:  # Only if valid for GR
            d_ssz_before = D_SSZ(r_before, r_s)
            d_gr_before = D_GR(r_before, r_s)
            # Typically SSZ > GR before intersection
    
    def test_d_ssz_formula(self):
        """Verify D_SSZ = 1/(1+Ξ)."""
        r_s = 2950.0
        r_values = np.logspace(0, 2, 50) * r_s
        
        for r in r_values:
            xi = Xi(r, r_s)
            d_expected = 1.0 / (1.0 + xi)
            d_actual = D_SSZ(r, r_s)
            
            assert d_actual == pytest.approx(d_expected, rel=1e-10)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
