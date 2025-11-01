# SSZ φ-Spiral Metric - Quick Reference Card

**Version 2.0.0** | © 2025 Carmen Wrede & Lino Casu

---

## 🚀 QUICK START

### Run SymPy Symbolic Computation
```bash
# Fast mode (1-3 minutes)
python src/ssz_metric_pure/ssz_symbolic_fast.py

# Sparse mode (1-2 minutes, CI/CD)
python src/ssz_metric_pure/ssz_symbolic_sparse.py

# Complete mode (10-30 minutes)
python src/ssz_metric_pure/ssz_symbolic_pack.py
```

### Run Pytest Validators
```bash
# All 12 tests
pytest tests/test_sparse_validators.py -v

# Specific test class
pytest tests/test_sparse_validators.py::TestMetricCompatibility -v
```

---

## 📐 KEY FORMULAS

### Metric Components
```
g_TT = -c²/γ²(r)
g_rr = γ²(r)
g_θθ = r²
g_φφ = r²sin²θ

where γ(r) = cosh(φ_G(r))
```

### Calibrated φ-Function
```
φ_G(r) = √(2GM/(rc²))
```

### Christoffel Symbols (non-zero)
```
Γ^T_Tr = Γ^T_rT = -β·φ'
Γ^r_TT = -(c²/γ⁴)·β·φ'
Γ^r_rr = β·φ'
Γ^r_θθ = -r/γ²
Γ^r_φφ = -(r sin²θ)/γ²
Γ^θ_rθ = Γ^θ_θr = 1/r
Γ^θ_φφ = -sinθ cosθ
Γ^φ_rφ = Γ^φ_φr = 1/r
Γ^φ_θφ = Γ^φ_φθ = cotθ
```

### Derivatives
```
φ'(r) = -φ_G/(2r)
φ''(r) = 3φ_G/(4r²)
β(r) = tanh(φ_G)
```

---

## ✅ VALIDATION CHECKLIST

### Mathematical Consistency
- [x] ∇_α g_μν = 0 (exact, machine precision)
- [x] Energy conservation (< 10⁻¹² drift)
- [x] Curvature finite everywhere

### Physical Tests
- [ ] Asymptotic flatness (pending fix)
- [ ] GPS redshift (pending sign fix)
- [ ] Pound-Rebka (pending high precision)
- [~] Shapiro delay (estimate OK)
- [~] Light deflection (estimate OK)

---

## 📊 TEST TOLERANCES

| Test | Tolerance | Current |
|------|-----------|---------|
| Asymptotic | 10⁻⁶ | ~10⁻⁶ at 10⁶ r_g |
| GPS | 0.1% | 0.13% |
| Pound-Rebka | 0.1% | TBD |
| Shapiro | 5% | 0.00001% |
| Deflection | 10% | 0.00001% |
| ∇g | 10⁻¹³ | 0 |
| Energy | 10⁻¹² | ~8×10⁻¹² |

---

## 🔧 TOOLS OVERVIEW

| Tool | Runtime | Use Case |
|------|---------|----------|
| ssz_symbolic_pack.py | 10-30 min | Full derivation |
| ssz_symbolic_fast.py | 1-3 min | Daily work |
| ssz_symbolic_sparse.py | 1-2 min | CI/CD |
| test_sparse_validators.py | ~5 min | Automated tests |

---

## 📚 DOCUMENTATION FILES

### Essential Reading
1. README.md - Quick start
2. COMPLETE_TENSOR_PACKAGE_README.md - Full overview
3. SYMBOLIC_COMPUTATION_GUIDE.md - SymPy tools
4. SSZ_VALIDATION_SUMMARY_V2.md - Test results

### Technical References
5. VALIDATION_OUTPUTS_COMPLETE.md - Numerical outputs
6. COMPARISON_AND_NEXT_STEPS.md - Analysis & roadmap

### LaTeX Papers
7. SSZ_METRIC_TENSOR_COMPLETE.tex
8. SSZ_EINSTEIN_RICCI_CURVATURE.tex
9. APPENDIX_A_PROOF_PACK.tex

---

## 🎯 CALIBRATION

### Current
```python
phi_squared = 2*G*M / (r*c**2)
```

### If needed (Option B)
```python
phi_squared = (2*G*M / (r*c**2)) * (1 + alpha * r_g/r)
# where alpha ~ 0.01-0.05
```

---

**For detailed information, see full documentation.**

© 2025 Carmen Wrede & Lino Casu
