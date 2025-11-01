# SSZ φ-Spiral Metric - Complete Comparison & Next Steps

**Comprehensive comparison of all validation tests with next action items**

© 2025 Carmen Wrede & Lino Casu  
Date: November 1, 2025

---

## 📊 COMPLETE VALIDATION MATRIX

### Status Legend
- ✅ **PASS**: Test passed with results within tolerance
- ⚠️ **CAUTION**: Test passed but issues noted (estimate, convergence, etc.)
- ❌ **FAIL**: Test failed, outside tolerance
- 🔄 **PENDING**: Test needs to be run or refined

---

## 1. CURRENT TEST RESULTS

### Test 1: Asymptotic Flatness (Fernfeld)

**Specification**: $|g_{TT}/c^2 + 1| \le 10^{-6}$, $|g_{rr} - 1| \le 10^{-6}$ für $r \gg r_g$

| Radius | g_TT Error | g_rr Error | Status |
|--------|------------|------------|--------|
| r = 100 r_g | 9.90×10⁻⁴ | 9.96×10⁻³ | ❌ FAIL |
| r = 1,000 r_g | 9.91×10⁻⁵ | 9.91×10⁻⁴ | ❌ FAIL |
| r = 10,000 r_g | 9.95×10⁻⁶ | 9.95×10⁻⁵ | ❌ FAIL (g_rr) |
| r = 100,000 r_g | 9.95×10⁻⁷ | 9.95×10⁻⁶ | ⚠️ g_TT pass, g_rr fail |
| r = 1,000,000 r_g | 9.95×10⁻⁸ | 9.95×10⁻⁷ | ✅ PASS |

**Issue**: Convergence appears to be $O(r_g/r)$ instead of expected $O((r_g/r)^2)$

**Next Check Needed**: 
```
r = 10⁵ r_g (SSZ) vs GR comparison
• Compute both g_TT and g_rr from GR: g_TT^GR ≈ -c²(1 - 2GM/(rc²))
• Compute SSZ: g_TT^SSZ = -c²/γ²
• Direct comparison: Are we matching GR or deviating systematically?
```

---

### Test 2: GPS Gravitational Redshift

**Specification**: Relative error $\le 10^{-3}$ (0.1%)

| Parameter | Value | Unit |
|-----------|-------|------|
| h | 20,200 | km |
| z_GR | 5.307×10⁻¹⁰ | - |
| z_SSZ | 5.300×10⁻¹⁰ | - |
| Relative Error | 1.3×10⁻³ | = 0.13% |

**Status**: ❌ **FAIL** (0.13% > 0.1%)

**Issues**:
1. Sign appears negative (should be positive redshift)
2. Error slightly above tolerance

**Next Check Needed**:
```python
# Recompute carefully:
γ_1 = cosh(φ(R_Earth))
γ_2 = cosh(φ(R_Earth + 20200 km))

# CORRECT formula:
z_SSZ = (γ_1/γ_2) - 1  # NOT γ_2/γ_1

# Should give POSITIVE value matching GR
```

---

### Test 3: Pound-Rebka Experiment

**Specification**: Relative error $\le 10^{-3}$ (0.1%)

| Parameter | Value | Unit |
|-----------|-------|------|
| h | 22.5 | m |
| z_GR | 2.457×10⁻¹⁵ | - |
| z_SSZ | ? | - |
| Relative Error | ? | - |

**Status**: 🔄 **PENDING** (needs precise calculation)

**Issue**: Numerical precision challenge at small h (22.5 m vs Earth radius)

**Next Check Needed**:
```python
# High-precision calculation:
import mpmath
mpmath.mp.dps = 50  # 50 decimal places

r1 = mpmath.mpf('6371000')  # R_Earth in meters
r2 = r1 + mpmath.mpf('22.5')

phi1 = mpmath.sqrt(2*G*M/(r1*c**2))
phi2 = mpmath.sqrt(2*G*M/(r2*c**2))

gamma1 = mpmath.cosh(phi1)
gamma2 = mpmath.cosh(phi2)

z_SSZ = (gamma1/gamma2) - 1

# Compare with:
z_GR = g*h/c^2 = 2.457×10⁻¹⁵
```

---

### Test 4: Shapiro Delay

**Specification**: $\le 5\%$ (geometry approximation)

| Parameter | Value | Unit |
|-----------|-------|------|
| b | R_☉ | m |
| Δt_GR | 226.0 | μs |
| Δt_SSZ (estimate) | 226.0003 | μs |
| Relative Error | 1.4×10⁻⁷ | 0.00001% |

**Status**: ⚠️ **CAUTION** (simplified estimate, well within tolerance)

**Note**: Full ray-tracing integration needed for precision

**Next Check Needed**:
```python
# Full null geodesic integration:
# Integrate: dT/dλ = (γ²/c²) × E
# along impact parameter b = R_☉

# Compare:
# - Straight-line approximation (current)
# - Full curved path (needed for < 1% precision)
```

---

### Test 5: Light Deflection

**Specification**: $\le 10\%$

| Parameter | Value | Unit |
|-----------|-------|------|
| b | R_☉ | m |
| α_GR | 1.749 | arcsec |
| α_SSZ (estimate) | 1.749 | arcsec |
| Relative Error | 1.4×10⁻⁷ | 0.00001% |

**Status**: ⚠️ **CAUTION** (simplified estimate, well within tolerance)

**Note**: Full 2+1D geodesic integration needed

**Next Check Needed**:
```python
# Full null geodesic in (r, φ) plane:
# Effective potential: V_eff(r) = (L²/r²)(1/γ²)
# Impact parameter: b = L/(E/c²)
# Integrate and compute total deflection angle
```

---

### Test 6: Metric Compatibility (∇g Test)

**Specification**: max $\lesssim 10^{-13}$ (double precision)

| Test Case | max\|∇g\| | Status |
|-----------|-----------|--------|
| Earth weak field | 0.000×10⁰ | ✅ PASS |
| Earth intermediate | 0.000×10⁰ | ✅ PASS |
| Sun weak field | 0.000×10⁰ | ✅ PASS |
| Sun intermediate | 0.000×10⁰ | ✅ PASS |
| Symbolic (SymPy) | Exact | ✅ PASS |

**Status**: ✅ **PASS** (machine precision < 10⁻¹⁰)

**No further action needed** - Test exceeds requirements

---

### Test 7: Energy Conservation (Timelike Radial)

**Specification**: Drift $\lesssim 10^{-12}$

| Test Case | Drift | Status |
|-----------|-------|--------|
| Earth low orbit | 7.648×10⁻¹² | ✅ PASS |
| Earth high orbit | 8.231×10⁻¹² | ✅ PASS |
| Sun surface | 9.104×10⁻¹² | ✅ PASS |
| Sun corona | 6.891×10⁻¹² | ✅ PASS |

**Status**: ✅ **PASS** (all scenarios < 10⁻¹²)

**No further action needed** - Test exceeds requirements

---

### Test 8: Light Cone Closing

**Specification**: $dr/dT = c \cdot \text{sech}^2 \phi(r)$ monotonic, smooth

| Radius | dr/dT | Closing % | Status |
|--------|-------|-----------|--------|
| 2 r_g | 0.635 c | 36.5% | ✅ |
| 5 r_g | 0.828 c | 17.2% | ✅ |
| 10 r_g | 0.906 c | 9.4% | ✅ |
| 100 r_g | 0.986 c | 1.4% | ✅ |
| 1000 r_g | 0.999 c | 0.1% | ✅ |

**Status**: ✅ **PASS** (monotonic, smooth, no singularity)

**No further action needed**

---

### Test 9: Curvature Invariants

**Specification**: R finite, R → 0; K ~ 48G²M²/(c⁴r⁶) far field

| Radius | Ricci R | Kretschmann K | Status |
|--------|---------|---------------|--------|
| 2 r_g | 3.42×10⁻⁶ m⁻² | 7.50×10⁻¹⁰ m⁻⁴ | ✅ Finite |
| 10 r_g | 2.18×10⁻⁸ m⁻² | 4.80×10⁻¹³ m⁻⁴ | ✅ Finite |
| 1000 r_g | 2.18×10⁻¹⁶ m⁻² | 4.80×10⁻²⁵ m⁻⁴ | ✅ → 0 |
| K theory | - | 4.80×10⁻²⁵ m⁻⁴ | ✅ Match |

**Status**: ✅ **PASS** (all finite, R → 0, K matches theory)

**No further action needed**

---

### Test 10: SSZ Kernel Elements

**Specification**: γ in metric, β·φ' in Γ, φ' in curvature

| Element | Expected | Found | Status |
|---------|----------|-------|--------|
| γ in g_TT | -c²/γ² | ✅ | ✅ PASS |
| γ in g_rr | γ² | ✅ | ✅ PASS |
| β·φ' in Γ^T_Tr | -β·φ' | ✅ | ✅ PASS |
| β·φ' in Γ^r_rr | +β·φ' | ✅ | ✅ PASS |
| φ' in G, R | Present | ✅ | ✅ PASS |

**Status**: ✅ **PASS** (all SSZ elements verified)

**No further action needed**

---

## 2. SUMMARY SCORECARD

```
╔══════════════════════════════════════════════════════════════╗
║                   VALIDATION SCORECARD                       ║
╚══════════════════════════════════════════════════════════════╝

Total Tests: 10

✅ PASS (no issues):        5/10
   • Test 6: ∇g = 0
   • Test 7: Energy conservation
   • Test 8: Light cone closing
   • Test 9: Curvature invariants
   • Test 10: SSZ kernel elements

⚠️ CAUTION (estimate/pass):  2/10
   • Test 4: Shapiro delay (estimate)
   • Test 5: Light deflection (estimate)

❌ FAIL (outside tolerance): 2/10
   • Test 1: Asymptotic flatness (slow convergence)
   • Test 2: GPS redshift (0.13% > 0.1%)

🔄 PENDING (needs work):     1/10
   • Test 3: Pound-Rebka (precision issue)

═══════════════════════════════════════════════════════════════
Current Score: 5/10 PASS, 2/10 CAUTION, 2/10 FAIL, 1/10 PENDING
═══════════════════════════════════════════════════════════════
```

---

## 3. NEXT CHECKS REQUIRED (Lino's List)

### Priority 1: Fix Failing Tests

#### Check 1.1: Asymptotic Flatness at r = 10⁵ r_g
```python
# Test Setup:
r_test = 1e5 * r_g  # For Earth: ~887 meters

# Compute:
phi = sqrt(2*G*M/(r*c^2))
gamma = cosh(phi)

g_TT = -c^2/gamma^2
g_rr = gamma^2

# GR comparison:
g_TT_GR = -c^2 * (1 - 2*G*M/(r*c^2))
g_rr_GR = 1 / (1 - 2*G*M/(r*c^2))

# Check:
error_TT = abs(g_TT/c^2 + 1)
error_rr = abs(g_rr - 1)

# Requirements:
# error_TT <= 1e-6 ✓ or ✗?
# error_rr <= 1e-6 ✓ or ✗?
```

**Expected Result**: Should PASS at r = 10⁵ r_g

**Action if FAIL**: 
- Analyze convergence rate
- Consider calibration adjustment: $\phi^2 = \frac{2GM}{rc^2}[1 + \alpha \frac{r_s}{r}]$

---

#### Check 1.2: GPS Redshift (Corrected Calculation)
```python
# Test Setup:
r1 = 6.371e6  # m (Earth surface)
r2 = r1 + 20.2e6  # m (GPS altitude)

# Compute:
phi1 = sqrt(2*G*M_Earth/(r1*c^2))
phi2 = sqrt(2*G*M_Earth/(r2*c^2))

gamma1 = cosh(phi1)
gamma2 = cosh(phi2)

# CORRECT formula (photon climbing OUT):
z_SSZ = (gamma1/gamma2) - 1  # Should be POSITIVE

# GR comparison:
z_GR = (G*M_Earth/c^2) * (1/r1 - 1/r2)

# Check:
rel_error = abs(z_SSZ - z_GR) / abs(z_GR)

# Requirement:
# rel_error <= 1e-3 (0.1%) ✓ or ✗?
```

**Expected Result**: Should PASS with corrected sign

**Action if FAIL**:
- Check if systematic offset due to φ calibration
- Consider weak-field expansion analysis

---

### Priority 2: Complete Pending Tests

#### Check 2.1: Pound-Rebka (High Precision)
```python
# Test Setup:
h = 22.5  # m
r1 = 6.371e6  # m
r2 = r1 + h

# Use high precision (mpmath):
import mpmath
mpmath.mp.dps = 50

# Compute:
phi1 = mpmath.sqrt(2*G*M/(r1*c^2))
phi2 = mpmath.sqrt(2*G*M/(r2*c^2))

gamma1 = mpmath.cosh(phi1)
gamma2 = mpmath.cosh(phi2)

z_SSZ = float((gamma1/gamma2) - 1)

# GR:
g_Earth = 9.8202  # m/s²
z_GR = g_Earth * h / c^2  # = 2.457×10⁻¹⁵

# Check:
rel_error = abs(z_SSZ - z_GR) / abs(z_GR)

# Requirement:
# rel_error <= 1e-3 (0.1%) ✓ or ✗?
```

**Expected Result**: Should PASS with high precision

---

### Priority 3: Refine Estimates to Precision

#### Check 3.1: Shapiro Delay (Full Integration)
```python
# Full null geodesic integration:
# Path: Earth → Sun closest approach → Mars

# Setup:
b = R_sun  # Impact parameter
r_E = 1.496e11  # m (1 AU)
r_M = 0.5 * r_E  # Mars at superior conjunction

# Integrate along path:
def integrand(r):
    gamma = cosh(sqrt(2*G*M_sun/(r*c^2)))
    # From null geodesic: dr = sqrt(1 - b²γ⁴/r²) × (c/γ²) dT
    return (gamma^2/c) / sqrt(1 - (b*gamma^2/r)^2)

# Numerical integration:
from scipy.integrate import quad
Delta_T_SSZ, _ = quad(integrand, b, r_E) + quad(integrand, b, r_M)

# GR comparison:
Delta_T_GR = (2*G*M_sun/c^3) * ln(4*r_E*r_M/b^2)

# Check:
rel_error = abs(Delta_T_SSZ - Delta_T_GR) / Delta_T_GR

# Requirement:
# rel_error <= 0.05 (5%) ✓ or ✗?
```

**Expected Result**: Should PASS (may need < 1% for precision)

---

#### Check 3.2: Light Deflection (Full Geodesic)
```python
# Full 2D null geodesic in (r, φ) plane:

# Setup:
b = R_sun  # Impact parameter
L = b * E / c  # Angular momentum

# Effective potential:
def V_eff(r):
    gamma = cosh(sqrt(2*G*M_sun/(r*c^2)))
    return (L^2 / r^2) * (1 / gamma^2)

# Integrate φ as function of r:
def dphi_dr(r):
    V = V_eff(r)
    return L / (r^2 * sqrt(E^2/c^2 - V))

# Total deflection:
from scipy.integrate import quad
alpha_SSZ, _ = 2 * quad(dphi_dr, b, np.inf) - np.pi

# Convert to arcseconds:
alpha_SSZ_arcsec = alpha_SSZ * 206265

# GR:
alpha_GR = 4*G*M_sun/(c^2*b) * 206265  # = 1.75''

# Check:
rel_error = abs(alpha_SSZ_arcsec - alpha_GR) / alpha_GR

# Requirement:
# rel_error <= 0.10 (10%) ✓ or ✗?
```

**Expected Result**: Should PASS (may achieve < 1%)

---

### Priority 4: Numerical Verification

#### Check 4.1: ∇g Test (Already Complete ✅)
```
Status: ✅ PASS
max|∇g| = 0 (exact, < 1e-10 numerical)
No action needed.
```

#### Check 4.2: Energy Conservation (Already Complete ✅)
```
Status: ✅ PASS
All drifts < 1e-12
No action needed.
```

---

## 4. RECOMMENDED ACTION PLAN

### Week 1: Fix Critical Issues
```
Day 1-2: ✅ Asymptotic Flatness
  • Run test at r = 10⁵ r_g
  • Analyze convergence rate
  • Document systematic behavior

Day 3-4: ✅ GPS Redshift
  • Fix sign error
  • Recompute with corrected formula
  • Verify against GR

Day 5: ✅ Pound-Rebka
  • High-precision calculation
  • Verify numerical stability
```

### Week 2: Complete Precision Tests
```
Day 1-3: 📐 Shapiro Delay
  • Implement full geodesic integration
  • Compare with simplified estimate
  • Document any deviations

Day 4-5: 📐 Light Deflection
  • Implement 2D geodesic solver
  • Compute exact deflection angle
  • Compare with Einstein formula
```

### Week 3: Final Validation & Documentation
```
Day 1-2: 📊 Complete validation matrix
Day 3-4: 📝 Write comprehensive report
Day 5: 🎯 Prepare for publication
```

---

## 5. CALIBRATION OPTIONS (If Needed)

### Option A: No Calibration (Current)
```
φ²(r) = 2GM/(rc²)

Status: 
• Works well for strong field
• Weak field convergence slower than expected
• GPS: 0.13% error (slightly high)
```

### Option B: Linear Correction
```
φ²(r) = (2GM)/(rc²) × [1 + α(r_s/r)]

where α ~ 0.01-0.05

Expected improvement:
• Faster asymptotic convergence
• GPS error: < 0.1%
• Preserves strong-field behavior
```

### Option C: Quadratic Correction
```
φ²(r) = (2GM)/(rc²) × [1 + α(r_s/r) + β(r_s/r)²]

where α ~ 0.01, β ~ 0.001

Expected improvement:
• Optimal weak-field match
• GPS error: << 0.1%
• May need strong-field verification
```

**Recommendation**: Try Option B first if GPS remains above tolerance after sign fix.

---

## 6. FINAL CHECKLIST BEFORE PUBLICATION

```
Physics Tests:
  ☐ All 10 tests PASS
  ☐ No CAUTION flags (or justified)
  ☐ All estimates replaced with precision calculations

Documentation:
  ☐ Complete test report
  ☐ All numerical values documented
  ☐ Comparison with GR detailed
  ☐ Any deviations explained

Code:
  ☐ All validation scripts working
  ☐ Pytest suite complete
  ☐ Examples documented
  ☐ README updated

Mathematical:
  ☐ All proofs verified
  ☐ LaTeX documents complete
  ☐ Appendix A finalized
  ☐ Consistency checks passed
```

---

## 7. CONTACT & NEXT STEPS

**Current Status**: 5/10 PASS, 2/10 CAUTION, 2/10 FAIL, 1/10 PENDING

**Next Immediate Actions**:
1. Fix GPS sign error → Retest
2. Run asymptotic test at r = 10⁵ r_g
3. Complete Pound-Rebka high-precision calculation

**Timeline**: 2-3 weeks to complete all precision tests

**Publication Target**: Ready after all tests PASS

---

**© 2025 Carmen Wrede & Lino Casu**  
**"Complete Analysis. Clear Path Forward. φ-Driven."** 📊✨🎯
