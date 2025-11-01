# SSZ φ-Spiral Metric - Roadmap to 100% Validation

**Current Status**: 8/10 PASS (80% complete)  
**Target**: 10/10 PASS (100% complete)  
**Timeline**: 2-3 weeks

© 2025 Carmen Wrede & Lino Casu  
Date: November 1, 2025

---

## 🎯 CURRENT STATUS (v2.1.0)

### ✅ COMPLETED (8/10 tests PASS):

1. ✅ **Asymptotic Flatness** - < 10⁻⁶ @ 10⁵ r_g (100× faster with 2PN)
2. ✅ **GPS Redshift** - 0.000019% error (was 0.13% FAIL)
3. ✅ **Pound-Rebka** - 0.0% exact match (was PENDING)
4. ✅ **Metric Compatibility** - ∇g = 0 (exact symbolic)
5. ✅ **Energy Conservation** - < 1e-12 drift
6. ✅ **Light Cone Closing** - Smooth, monotonic
7. ✅ **Curvature Invariants** - R, K finite everywhere
8. ✅ **SSZ Kernel Elements** - γ, β, φ verified

### ⚠️ REMAINING (2/10 tests CAUTION):

9. ⚠️ **Shapiro Delay** - Formula correct, using estimate
10. ⚠️ **Light Deflection** - Formula correct, using estimate

---

## 🔧 WHAT NEEDS TO BE CHANGED

### Test 9: Shapiro Delay → Full Integration

**Current Status**: ⚠️ CAUTION (estimate: 0.00001% deviation)

**What's Missing**:
Full null geodesic integration along the photon path.

**Current Implementation**:
```python
# Using first-order estimate
Delta_t_shapiro ≈ (4GM/c³) ln(r_E r_M / b²)
```

**Needed Implementation**:
```python
# Full radial integration (Lino's specification)
Delta_T_SSZ = ∫ [(γ²(r)/c) - (1/c)] dr

where:
  • Integration along impact parameter b
  • Symmetric path (Earth → Sun → Mars)
  • Null geodesic: ds² = 0
```

**Technical Details**:
```python
def shapiro_delay_integrated(r_earth, r_mars, b, M, G, c):
    """
    Compute Shapiro delay via full integration
    
    Args:
        r_earth: Earth distance from Sun [m]
        r_mars: Mars distance from Sun [m]
        b: Impact parameter [m]
        M: Solar mass [kg]
        G: Gravitational constant
        c: Speed of light
        
    Returns:
        Delta_t: Time delay [s]
    """
    from scipy.integrate import quad
    
    def integrand(r, b, calib):
        """Integrand for Shapiro delay"""
        if r < b:
            return 0  # Avoid r < b (not on path)
        
        gamma = calib.gamma(r)
        
        # Path length factor for impact parameter b
        # r = sqrt(x² + b²) along straight line
        dr_dx = r / np.sqrt(r**2 - b**2)
        
        # Integrand: (γ²/c - 1/c) * dr/dx
        return (gamma**2 / c - 1 / c) * dr_dx
    
    # Initialize calibration
    calib = SSZCalibration(M, G, c, mode='2pn')
    
    # Closest approach distance
    r_min = b
    
    # Integrate: Earth → closest approach → Mars
    # (symmetric, so 2× one side)
    delta_t_half, error = quad(
        integrand, 
        r_min, 
        r_earth,
        args=(b, calib),
        limit=1000,
        epsabs=1e-10
    )
    
    delta_t_total = 2 * delta_t_half
    
    # GR comparison
    delta_t_gr = (4*G*M/c**3) * np.log((4*r_earth*r_mars)/(b**2))
    
    return {
        'delta_t_ssz': delta_t_total,
        'delta_t_gr': delta_t_gr,
        'difference': delta_t_total - delta_t_gr,
        'rel_error': abs(delta_t_total - delta_t_gr) / delta_t_gr
    }
```

**Expected Result**:
- Deviation: < 1% (likely < 0.1%)
- Status: ⚠️ CAUTION → ✅ PASS

**Effort**: ~4-6 hours
**Priority**: High
**Week**: 2 (Nov 11-15)

---

### Test 10: Light Deflection → 2D Geodesic Solver

**Current Status**: ⚠️ CAUTION (estimate: 0.00001% deviation)

**What's Missing**:
Full 2D null geodesic integration with angular coordinate.

**Current Implementation**:
```python
# Using first-order estimate
alpha ≈ 4GM/(c²·b)  # ≈ 1.75" for Sun
```

**Needed Implementation**:
```python
# Full 2D null geodesic with φ coordinate
# Solve: d²φ/dλ² + (geodesic equation in φ)

where:
  • Null geodesic: ds² = 0
  • Impact parameter b (angular momentum)
  • Asymptotic deflection angle from φ(λ→∞)
```

**Technical Details**:
```python
def light_deflection_integrated(b, M, G, c, r_start=1e12):
    """
    Compute light deflection via 2D null geodesic
    
    Args:
        b: Impact parameter [m]
        M: Mass [kg]
        G: Gravitational constant
        c: Speed of light
        r_start: Starting radius (far away) [m]
        
    Returns:
        alpha: Deflection angle [rad]
    """
    from scipy.integrate import solve_ivp
    
    calib = SSZCalibration(M, G, c, mode='2pn')
    
    # Conserved quantities for null geodesic
    # Energy: E = (c²/γ²) dT/dλ
    # Angular momentum: L = r² dφ/dλ = b·c
    L = b * c
    
    def geodesic_equations(lam, y):
        """
        Geodesic equations for (r, φ, dr/dλ, dφ/dλ)
        
        y = [r, phi, v_r, v_phi]
        """
        r, phi, v_r, v_phi = y
        
        # Get metric functions
        gamma = calib.gamma(r)
        phi_val = calib.phi(r)
        phi_prime = calib.phi_prime(r)
        beta = calib.beta(r)
        
        # Geodesic accelerations
        # d²r/dλ² from null geodesic constraint
        # ds² = -(c²/γ²)dT² + γ²dr² + r²dφ² = 0
        
        # From constraint: v_r² = (c²/γ⁴) - (L²/(γ²·r²))
        v_r_squared = (c**2 / gamma**4) - (L**2 / (gamma**2 * r**2))
        v_r_actual = np.sqrt(max(0, v_r_squared))
        
        # v_phi from angular momentum
        v_phi_actual = L / r**2
        
        # Accelerations
        a_r = -(c**2 / gamma**5) * beta * phi_prime * (c / gamma)**2 + \
              (gamma / gamma**3) * beta * phi_prime * v_r_actual**2 - \
              (r / gamma**2) * v_phi_actual**2
        
        a_phi = -(2 / r) * v_r_actual * v_phi_actual
        
        return [v_r_actual, v_phi_actual, a_r, a_phi]
    
    # Initial conditions (incoming from infinity)
    # Start at large r, moving inward
    r0 = r_start
    phi0 = -np.pi  # Coming from -x axis
    v_r0 = -np.sqrt((c**2 / calib.gamma(r0)**4) - (L**2 / (calib.gamma(r0)**2 * r0**2)))
    v_phi0 = L / r0**2
    
    y0 = [r0, phi0, v_r0, v_phi0]
    
    # Integrate until photon passes and goes back to infinity
    # Stop when r starts increasing again and reaches r_start
    def event_far_away(lam, y):
        return y[0] - r_start
    event_far_away.terminal = True
    event_far_away.direction = 1  # Increasing
    
    # Solve
    sol = solve_ivp(
        geodesic_equations,
        [0, 1e8],  # Large λ range
        y0,
        method='DOP853',
        events=event_far_away,
        dense_output=True,
        rtol=1e-10,
        atol=1e-12
    )
    
    # Final angle
    phi_final = sol.y[1, -1]
    
    # Deflection angle (difference from straight line)
    # Straight line: φ goes from -π to 0 (π change)
    # Actual: φ goes from -π to phi_final
    alpha = phi_final - (-np.pi) - np.pi  # Deviation from straight
    alpha = abs(alpha)  # Absolute deflection
    
    # GR comparison
    alpha_gr = 4*G*M / (c**2 * b)
    
    return {
        'alpha_ssz': alpha,
        'alpha_gr': alpha_gr,
        'alpha_ssz_arcsec': alpha * (180*3600/np.pi),
        'alpha_gr_arcsec': alpha_gr * (180*3600/np.pi),
        'difference': alpha - alpha_gr,
        'rel_error': abs(alpha - alpha_gr) / alpha_gr
    }
```

**Expected Result**:
- Deviation: < 1% (likely < 0.5%)
- Sun deflection: ~1.75" (should match GR)
- Status: ⚠️ CAUTION → ✅ PASS

**Effort**: ~6-8 hours
**Priority**: High
**Week**: 2 (Nov 11-15)

---

## 📅 TIMELINE TO 100%

### Week 1 (Nov 4-8): ✅ DONE

```
✅ 2PN calibration implementation
✅ GPS redshift fix (log-form)
✅ Pound-Rebka fix (high precision, sign)
✅ Asymptotic flatness verification
✅ Documentation complete
✅ All reports generated
✅ Lino's spec verified (97%)

Result: 8/10 PASS (80%)
```

### Week 2 (Nov 11-15): Geodesic Integration

```
Day 1-2 (Nov 11-12): Shapiro Delay
  • Implement shapiro_delay_integrated()
  • Test with Earth-Sun-Mars configuration
  • Verify against GR (< 1%)
  • Update validation reports
  
Day 3-4 (Nov 13-14): Light Deflection
  • Implement light_deflection_integrated()
  • Test with Solar limb (b = R_sun)
  • Verify ~1.75" deflection
  • Update validation reports
  
Day 5 (Nov 15): Integration & Testing
  • Add both to calibration_2pn.py
  • Run complete test suite
  • Generate final validation reports
  • Verify 10/10 PASS

Expected Result: 10/10 PASS (100%) ✅
```

### Week 3 (Nov 18-22): Publication Preparation

```
Day 1-2 (Nov 18-19): Final Validation Report
  • SSZ_VALIDATION_FINAL_v2.1.md
  • Complete numerical results
  • All 10 tests documented
  • Error statistics

Day 3-4 (Nov 20-21): Manuscript Preparation
  • Update all LaTeX papers
  • Add new validation results
  • Prepare figures
  • DOI-ready format

Day 5 (Nov 22): Submission
  • Final review
  • arXiv submission
  • GitHub release v2.2.0

Target: 100% Complete, Publication-Ready ✅
```

---

## 🔬 IMPLEMENTATION CHECKLIST

### Shapiro Delay Integration:

```
File: src/ssz_metric_pure/geodesics.py (NEW)

Functions to add:
  ☐ shapiro_integrand(r, b, calib)
  ☐ shapiro_delay_integrated(r_earth, r_mars, b, M, G, c)
  ☐ shapiro_test_earth_mars()
  ☐ Compare with GR formula

Dependencies:
  ✅ scipy.integrate.quad (already available)
  ✅ SSZCalibration (already implemented)
  ✅ 2PN calibration (already working)

Testing:
  ☐ Unit test: test_shapiro_delay()
  ☐ Earth-Mars configuration
  ☐ Different impact parameters
  ☐ Convergence check (grid refinement)
  ☐ GR comparison (< 1% deviation)

Expected Output:
  ΔT_SSZ ≈ ΔT_GR with small correction
  Typical value: ~200 μs for Earth-Mars
```

### Light Deflection Integration:

```
File: src/ssz_metric_pure/geodesics.py (NEW)

Functions to add:
  ☐ null_geodesic_equations(lam, y, calib, L)
  ☐ light_deflection_integrated(b, M, G, c)
  ☐ deflection_test_sun()
  ☐ Compare with GR: 4GM/(c²b)

Dependencies:
  ✅ scipy.integrate.solve_ivp (already available)
  ✅ SSZCalibration (already implemented)
  ✅ 2PN calibration (already working)

Testing:
  ☐ Unit test: test_light_deflection()
  ☐ Solar limb (b = R_sun ≈ 696,000 km)
  ☐ Different impact parameters
  ☐ Numerical stability check
  ☐ GR comparison: expect ~1.75"

Expected Output:
  α_SSZ ≈ 1.75" ± 0.01"
  Match GR within < 1%
```

### Integration into Validation:

```
File: src/ssz_metric_pure/calibration_2pn.py

Add classes:
  ☐ class ShapiroDelay(calib)
  ☐ class LightDeflection(calib)

Update:
  ☐ demonstrate_calibration_comparison()
  ☐ Add Shapiro test
  ☐ Add Deflection test

File: tests/test_validation_complete.py (NEW)

Add tests:
  ☐ test_shapiro_delay_integrated()
  ☐ test_light_deflection_integrated()
  ☐ test_all_10_validation_points()

Expected:
  ✅ 10/10 tests PASS
```

---

## 📊 EXPECTED FINAL RESULTS

### After Implementation (v2.2.0):

| # | Test | Target | Status | Result |
|---|------|--------|--------|--------|
| 1 | Asymptotic Flatness | \|g/c²+1\| ≤ 10⁻⁶ | ✅ PASS | < 10⁻⁶ @ 10⁵ r_g |
| 2 | GPS Redshift | Error ≤ 0.1% | ✅ PASS | 0.000019% |
| 3 | Pound-Rebka | Error ≤ 0.1% | ✅ PASS | 0.0% (exact) |
| 4 | Shapiro Delay | Error ≤ 5% | ✅ PASS | < 1% (integrated) |
| 5 | Light Deflection | Error ≤ 10% | ✅ PASS | < 1% (integrated) |
| 6 | Metric Compatibility | max\|∇g\| ≤ 10⁻¹³ | ✅ PASS | 0 (exact) |
| 7 | Energy Conservation | Drift ≤ 10⁻¹² | ✅ PASS | ~8×10⁻¹² |
| 8 | Light Cone Closing | Monotonic | ✅ PASS | Smooth |
| 9 | Curvature Invariants | R, K finite | ✅ PASS | All finite |
| 10 | SSZ Kernel Elements | γ, β, φ | ✅ PASS | Verified |

**Summary**: ✅ **10/10 PASS** → **100% COMPLETE**

---

## 💡 ALTERNATIVE APPROACHES

### Quick Win Option (Less Rigorous):

If full integration is too complex, could use:

1. **Higher-order expansion** instead of full integration:
   ```python
   # Shapiro: Include 2PN terms
   Delta_t = (4GM/c³)[ln(4r_E r_M/b²) + correction_2pn]
   
   # Deflection: Include 2PN correction
   alpha = (4GM/c²b)[1 + (15πGM)/(4c²b) + ...]
   ```

2. **Perturbative approach**:
   - Integrate along GR geodesic
   - Apply SSZ corrections as perturbation
   - Faster but less accurate

**Recommendation**: Full integration (more rigorous, better for publication)

---

## 🎯 SUMMARY

```
╔══════════════════════════════════════════════════════════════╗
║           WHAT'S NEEDED FOR 100% VALIDATION                  ║
╚══════════════════════════════════════════════════════════════╝

Currently:    8/10 PASS (80%)
Missing:      2 geodesic integrators

Required Implementation:
  1. Shapiro Delay → Full null geodesic integration
     Effort: 4-6 hours
     
  2. Light Deflection → 2D geodesic solver
     Effort: 6-8 hours

Total Effort: ~10-14 hours
Timeline:     Week 2 (Nov 11-15)

Expected Result:
  ✅ 10/10 PASS (100%)
  ✅ All tests < 1% deviation
  ✅ Publication-ready validation
  
Next Steps:
  1. Create geodesics.py module
  2. Implement both integrators
  3. Add to test suite
  4. Generate final reports
  5. Update all documentation

Target Date: November 22, 2025 (3 weeks)
```

---

**© 2025 Carmen Wrede & Lino Casu**  
**"Roadmap to 100%. Only 2 integrators needed. 2 weeks to perfection. φ-Driven."**
