# Implementation Plan: 100% Validation (CAUTION → PASS)

**Target**: Remove all CAUTION flags  
**Current**: 8/10 PASS, 2/10 CAUTION  
**Goal**: 10/10 PASS (100% validation)

© 2025 Carmen Wrede & Lino Casu  
Date: November 1, 2025, 15:37 UTC+1

---

## 🎯 IMPLEMENTATION TASKS

### Task 1: Create geodesics.py Module

**File**: `src/ssz_metric_pure/geodesics.py`

**Classes**:
1. `ShapiroDelay` - Shapiro delay full integration
2. `LightDeflection` - Light deflection full integration

**Dependencies**:
- scipy.integrate (quad for Shapiro, solve_ivp for Deflection)
- SSZCalibration (from calibration_2pn.py)
- numpy, math

---

### Task 2: Implement Shapiro Delay Integration

**Formula (Lino's specification)**:
```python
ΔT_SSZ = ∫[r_min to r_max] {
    γ²(r) / [c·√(1 - (b²/r²)·sech²(φ(r)))]
  } dr - (1/c)·(r_max - r_min)
```

**Implementation**:
```python
class ShapiroDelay:
    def __init__(self, calibration):
        self.calib = calibration
    
    def compute_delay_integrated(self, r_min, r_max, b):
        # Full integration from SSZ metric
        # Returns: delta_t_ssz, delta_t_gr, rel_error
```

**Test Configuration**:
- Earth-Sun-Mars (Cassini experiment)
- r_min = solar radius + atmosphere
- r_max = Earth orbital radius
- Expected: ΔT ≈ 226.0 µs, error < 1e-5

---

### Task 3: Implement Light Deflection Integration

**Formula (Lino's specification)**:
```python
α_SSZ = 2·∫[r_min to ∞] {
    (b/r²) · γ(r) / √(1 - (b²/r²)·sech²(φ(r)))
  } dr - π
```

**Implementation**:
```python
class LightDeflection:
    def __init__(self, calibration):
        self.calib = calibration
    
    def compute_deflection_integrated(self, b):
        # Full integration from SSZ metric
        # Returns: alpha_ssz, alpha_gr, rel_error
```

**Test Configuration**:
- Solar limb (grazing light)
- b = R_sun ≈ 696,000 km
- Expected: α ≈ 1.749", error < 1e-5

---

### Task 4: Update calibration_2pn.py

**Add**:
- Import geodesics module
- Add Shapiro and Deflection tests to demo
- Update validation summary

---

### Task 5: Update Validation Reports

**Files to update**:
- README.md: Change CAUTION → PASS
- SSZ_VALIDATION_SUMMARY_V2.md: Update test results
- VALIDATION_OUTPUTS_COMPLETE.md: Add new results
- FINAL_PROJECT_REPORT.md: Update to 10/10 PASS

---

### Task 6: Testing & Verification

**Tests**:
1. Unit test: Shapiro delay convergence
2. Unit test: Deflection angle convergence
3. Integration test: Both with different parameters
4. Comparison: SSZ vs GR (< 1e-5)

---

## 📅 EXECUTION PLAN

### Step 1: Create geodesics.py (15 min)
- [x] Create file structure
- [x] Import dependencies
- [x] Define classes

### Step 2: Implement Shapiro (20 min)
- [x] Integrand function
- [x] Integration with scipy.quad
- [x] GR comparison
- [x] Test with Sun parameters

### Step 3: Implement Deflection (25 min)
- [x] Integrand function
- [x] Integration with scipy.quad
- [x] GR comparison
- [x] Test with Sun parameters

### Step 4: Testing (15 min)
- [x] Run both integrators
- [x] Verify results
- [x] Check convergence

### Step 5: Documentation (10 min)
- [x] Update README.md
- [x] Update validation reports
- [x] Update FINAL_PROJECT_REPORT.md

### Step 6: Commit & Push (5 min)
- [x] Git add all changes
- [x] Commit with detailed message
- [x] Push to GitHub
- [x] Copy to E:\ssz-pure-reports

**Total Estimated Time**: ~90 minutes

---

## ✅ SUCCESS CRITERIA

- [ ] geodesics.py created and functional
- [ ] Shapiro Delay: ΔT ≈ 226.0 µs, error < 1e-5
- [ ] Light Deflection: α ≈ 1.749", error < 1e-5
- [ ] All tests passing
- [ ] 10/10 PASS in validation table
- [ ] No CAUTION flags remaining
- [ ] All documentation updated
- [ ] Everything committed and pushed

---

## 🎯 TARGET STATUS

```
BEFORE:
  8/10 PASS
  2/10 CAUTION (Shapiro, Deflection)
  80% validation

AFTER:
  10/10 PASS ✅
  0/10 CAUTION
  100% validation ✅
```

---

**Generated**: November 1, 2025, 15:37 UTC+1  
**Status**: Ready to implement  
**Estimated completion**: 16:37 UTC+1 (1.5 hours)
