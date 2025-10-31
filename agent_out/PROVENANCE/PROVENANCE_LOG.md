# SSZ Metric Pure - Provenance Log

**Repository:** ssz-metric-pure  
**Purpose:** Unified 100% Pure Segmented Spacetime implementation  
**Created:** 2025-10-31 23:15 UTC+01:00  
**Status:** 🔨 IN CONSTRUCTION

---

## Source Repositories (READ-ONLY)

### Repo 1: ssz-full-metric
**Location:** `E:\clone\ssz-full-metric\`  
**Last Commit:** `ed5d973` (DOCS: Final quality report and repo rename instructions)  
**GitHub:** https://github.com/error-wtf/ssz-metric-final  
**Status:** ✅ Immutable, read-only

**Key Components Used:**
- `viz_ssz_metric/ssz_mirror_metric.py` - Pure SSZ functions (Xi, D_SSZ, A_SSZ)
- `viz_ssz_metric/constants.py` - Physical constants (φ, G, C)
- `viz_ssz_metric/segment_density.py` - Segmentation logic
- LICENSE - Anti-Capitalist Software License v1.4

### Repo 2: Segmented-Spacetime-Mass-Projection-Unified-Results
**Location:** `E:\clone\Segmented-Spacetime-Mass-Projection-Unified-Results\`  
**Last Known Commit:** `7f81b57` (FIX: Complete test suite improvements)  
**Status:** ✅ Immutable, read-only

**Key Components Used:**
- `ssz_theory_segmented.py` - TOV + SSZ field equations
- `segspace_all_in_one_extended.py` - Δ(M) corrections, φ-geometry
- `*.md` files (396 found) - Scientific documentation

---

## Files Created in ssz-metric-pure

### Core Package: src/ssz_metric_pure/

| File | Source | Lines | Purpose |
|------|--------|-------|---------|
| `params.py` | **UNIFIED** | 342 | Parameters from both repos |
| `__init__.py` | New | TBD | Package interface |
| `segmentation.py` | ssz-full-metric + theory | TBD | N(r), φ-structure |
| `metric_static.py` | ssz_mirror_metric.py | TBD | Non-rotating SSZ |
| `metric_kerr_ssz.py` | **NEW** | TBD | Rotating SSZ-Kerr |
| `tensors.py` | **NEW** | TBD | Γ, Riemann, Ricci, Einstein |
| `geodesics.py` | **NEW** | TBD | Null/timelike paths |
| `limits.py` | **NEW** | TBD | GR validation layer |
| `validation.py` | **NEW** | TBD | Doc-driven checks |

### Legacy Package: src/ssz_core/ (Initial prototype)

| File | Source | Status |
|------|--------|--------|
| `constants.py` | ssz-full-metric | ⚠️ TO MERGE into params.py |
| `segment_density.py` | ssz-full-metric | ⚠️ TO MERGE into segmentation.py |
| `metric.py` | ssz-full-metric | ⚠️ TO MERGE into metric_static.py |

**Action:** Will consolidate into `ssz_metric_pure/` package

### Documentation

| File | Source | Status |
|------|--------|--------|
| `README.md` | New | ✅ Created |
| `LICENSE` | ssz-full-metric | ✅ Copied (Anti-Capitalist v1.4) |
| `docs/SPECIFICATION.md` | New | ✅ Created |
| `docs/imported_reports/` | Both repos (*.md) | 🔄 Pending import |

### Tests

| File | Source | Status |
|------|--------|--------|
| `tests/test_segment_density.py` | New | ✅ Created (comprehensive) |
| `tests/test_metric.py` | New | ✅ Created (comprehensive) |
| `tests/test_metric_symmetry.py` | **NEW** | 📝 TODO |
| `tests/test_limits_gr_kerr.py` | **NEW** | 📝 TODO |
| `tests/test_ergosphere_horizons.py` | **NEW** | 📝 TODO |
| `tests/test_bianchi_and_consistency.py` | **NEW** | 📝 TODO |
| `tests/test_units_dimensions.py` | **NEW** | 📝 TODO |
| `tests/test_doc_constraints.py` | **NEW** | 📝 TODO |

### Visualization

| File | Source | Status |
|------|--------|--------|
| `src/ssz_viz/plot_time_dilation.py` | New | ✅ Created |
| `src/ssz_viz/plot_curvature.py` | New | ✅ Created |
| `src/ssz_viz/plot_comparison.py` | New | ✅ Created |
| `src/ssz_viz/plot_metric_a.py` | New | ✅ Created |

### CLI Tools

| File | Status |
|------|--------|
| `bin/ssz_kerr_summary` | 📝 TODO |
| `src/sszviz.py` | ✅ Created (basic) |

---

## Extraction Details

### params.py (UNIFIED)
**Created:** 2025-10-31 23:18  
**Sources:**
1. `ssz-full-metric/viz_ssz_metric/ssz_mirror_metric.py`:
   - Constants: PHI, G_DEFAULT, C_DEFAULT
   - Softplus parameters: epsilon, beta
   
2. `Segmented-Spacetime/segspace_all_in_one_extended.py`:
   - Decimal precision setup
   - Δ(M) parameters: A=98.01, ALPHA=2.7177e4, B=1.96
   - φ-precise calculations
   
3. `Segmented-Spacetime/ssz_theory_segmented.py`:
   - TOV parameters: cs2, rho0, phi_cap, phip_cap
   - Scalar field: Z0, alpha, beta, mphi, lambda
   - Integration tolerances

**Unified Features:**
- Dimensionless mode (G=c=1)
- SSZParams class (static)
- KerrSSZParams class (rotating)
- High-precision Decimal support
- Validation tolerances

---

## Safety Confirmations

✅ **Zero modifications to source repos**  
✅ **All writes to ssz-metric-pure/ only**  
✅ **No destructive operations**  
✅ **Every file logged with source**  
✅ **Git commits regular and safe**

---

## Next Steps

1. [ ] Consolidate `ssz_core/` → `ssz_metric_pure/`
2. [ ] Import all `*.md` documentation to `docs/imported_reports/`
3. [ ] Extract pure SSZ from `ssz_mirror_metric.py`
4. [ ] Extract TOV from `ssz_theory_segmented.py`
5. [ ] Implement Kerr-SSZ (`metric_kerr_ssz.py`)
6. [ ] Implement tensors (`tensors.py` with SymPy)
7. [ ] Implement geodesics (`geodesics.py`)
8. [ ] Implement GR limits layer (`limits.py`)
9. [ ] Generate doc-driven tests (`test_doc_constraints.py`)
10. [ ] Create CLI tools (`bin/ssz_kerr_summary`)
11. [ ] Run full test suite
12. [ ] Generate final reports

---

**Last Updated:** 2025-10-31 23:20 UTC+01:00  
**Files Tracked:** 25  
**Sources:** 2 repos (read-only)  
**Target:** 100% Pure SSZ ✨
