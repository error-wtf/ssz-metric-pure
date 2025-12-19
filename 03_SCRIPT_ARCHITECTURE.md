# SSZ Script Architecture - Complete Code Structure Documentation

**Documentation of all script architectures and code structures**  
**Date:** 2025-11-13  
**Focus:** Module design, data flows, test systems

---

## 1. Repository Structure Overview

### 1.1 Main Repository: Segmented-Spacetime-Mass-Projection-Unified-Results

```
Segmented-Spacetime-Mass-Projection-Unified-Results/
├── core/                      # Core modules (10 files)
│   ├── __init__.py
│   ├── compare.py            # GR vs SSZ comparisons
│   ├── inference.py          # Bayesian Inference
│   ├── lensing.py            # Gravitational lensing
│   ├── predict.py            # Prediction engine
│   ├── stability.py          # Stability analyses
│   ├── stats.py              # Extended statistics
│   ├── sweep.py              # Parameter sweeps
│   ├── uncertainty.py        # Uncertainty quantification
│   └── xval.py               # Cross-validation
│
├── scripts/                   # Analysis scripts (112 files!)
│   ├── tests/                # Physics tests (15+ tests)
│   ├── cosmology/            # Cosmological analyses
│   ├── visualization/        # Plot generators
│   └── validation/           # Validation pipelines
│
├── tests/                     # Pytest test suite
│   ├── cosmos/               # Cosmology tests
│   └── test_segwave_*.py     # SegWave tests
│
├── data/                      # Datasets
│   ├── real_data_full.csv    # 427 observations, 117 sources
│   ├── gaia/                 # GAIA DR3 samples
│   └── planck/               # CMB Power Spectra (2 GB)
│
├── papers/                    # Theoretical papers
│   └── validation/           # 19 validation documents
│
└── reports/                   # Generated reports
    └── figures/              # Plots & visualizations
```

---

## 2. Core Script Architecture

### 2.1 segspace_all_in_one_extended.py - Main Analysis Engine

**Purpose:** Complete paired-test analysis SSZ vs GR×SR

**Architecture:**
```python
# 780 lines, modularly structured

┌─────────────────────────────────────┐
│  SAFETY PREFLIGHT                   │
│  - Directory setup                  │
│  - Determinism (Seed 137)           │
│  - Decimal Precision (200 digits)   │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  PHYSICAL CONSTANTS                 │
│  - G, c, φ, α_fs, h, M_☉           │
│  - Δ(M) Parameters (A, α, B)        │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  CORE MODEL                         │
│  - raw_delta(M)                     │
│  - delta_percent(M, Lmin, Lmax)     │
│  - rphi_from_mass(M, delta_pct)     │
│  - f_mass / df_dM (Newton-Raphson)  │
│  - invert_mass(r_obs, M0)           │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  REDSHIFT CALCULATIONS              │
│  - z_gravitational(M, r)            │
│  - z_special_rel(v_tot, v_los)      │
│  - z_combined(z_gr, z_sr)           │
│  - z_seg_pred(mode, ...)            │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  STATISTICAL ANALYSIS               │
│  - bootstrap_ci(data, n_boot=2000)  │
│  - binomial_sign_test(wins, total)  │
│  - paired_test(data, z_seg, z_grsr) │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  STRATIFICATION                     │
│  - Mass-binned medians              │
│  - Regime-specific analysis         │
│  - Distance/velocity strata         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  OUTPUT GENERATION                  │
│  - CSV Exports                      │
│  - JSON Metadata                    │
│  - Matplotlib Plots (optional)      │
│  - Manifest File                    │
└─────────────────────────────────────┘
```

**Key Features:**
- Decimal arithmetic for extreme precision
- Deterministic seeding (reproducibility)
- Multiple redshift prediction modes (hint, deltaM, hybrid, geodesic)
- Bootstrap confidence intervals
- Exact binomial test

**CLI Arguments:**
```bash
--prec 200                    # Decimal precision
--drop-na                     # Filter incomplete rows
--paired-stats                # Enable paired test
--ci 2000                     # Bootstrap iterations
--bins 10                     # Mass bins
--plots                       # Generate plots
--filter-complete-gr          # Require complete GR data
```

---

### 2.2 perfect_paired_test.py - ESO Validation

**Purpose:** 97.9% breakthrough validation with ESO data

**Architecture:**
```python
# Simplified, focused on clean dataset

┌─────────────────────────────────────┐
│  LOAD CLEAN DATASET                 │
│  - 47 complete ESO observations     │
│  - All parameters present           │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  COMPUTE PREDICTIONS                │
│  - SSZ: z_seg (φ-based)             │
│  - GR: z_grsr (classical)           │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  PAIRED COMPARISON                  │
│  - |Δz_seg| vs |Δz_grsr|            │
│  - Win if |Δz_seg| < |Δz_grsr|      │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  BINOMIAL TEST                      │
│  - p-value exact calculation        │
│  - Significance assessment          │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  OUTPUT                             │
│  - Console: "SSZ wins: 46/47"       │
│  - CSV: out/clean_results.csv       │
└─────────────────────────────────────┘
```

**Expected Output:**
```
SSZ wins: 46/47 (97.9%)
p-value: 0.0000
```

**Runtime:** ~10 seconds

---

### 2.3 derive_effective_stress_energy.py - Einstein Tensor Computation

**Purpose:** Reverse-engineer T_μν from SSZ metric

**Architecture:**
```python
# 193 lines, SymPy-based

┌─────────────────────────────────────┐
│  SYMBOLIC SETUP                     │
│  - Coordinates: (t, r, θ, φ)        │
│  - Metric: g_μν diagonal            │
│  - A(U) = 1 - 2U + 2U² + ε₃U³       │
│  - B(r) = 1/A(r)                    │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  CHRISTOFFEL SYMBOLS                │
│  - Γ^α_βγ = ½g^αδ(∂_βg_δγ + ...)    │
│  - Symbolic differentiation         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  RIEMANN TENSOR                     │
│  - R^α_βγδ = ∂_γΓ^α_βδ - ...        │
│  - 4D tensor (256 components!)      │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  RICCI TENSOR & SCALAR              │
│  - R_μν = R^α_μαν                   │
│  - R = g^μν R_μν                    │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  EINSTEIN TENSOR                    │
│  - G_μν = R_μν - ½g_μν R            │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  EFFECTIVE STRESS-ENERGY            │
│  - T_μν = (c⁴/8πG) G_μν             │
│  - Extract: ρ, p_r, p_t             │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  COVARIANT DIVERGENCE               │
│  - ∇_μ T^μ_ν = 0? (check)           │
└─────────────────────────────────────┘
```

**Key Relations Extracted:**
```python
8πρ   = (1-A)/r² - A'/r
8πp_r = A'/r + (A-1)/r²  → p_r = -ρ
8πp_t = A''/2 + A'/r
```

**CLI:**
```bash
python derive_effective_stress_energy.py \
  --M 1.98847e30 \
  --eps3 -4.8 \
  --r-mults 1.1,1.5,2,5,10 \
  --latex out_latex.txt
```

---

## 3. Test System Architecture

### 3.1 Test Suite Hierarchy

```
run_all_validations.py  (Master Runner)
├── run_full_suite.py           (116 tests)
│   ├── [PHASE 1] Root Tests    (6 physics)
│   ├── [PHASE 2] SegWave       (20 tests)
│   ├── [PHASE 3] Scripts       (15 tests)
│   ├── [PHASE 4] Cosmos        (1 test)
│   ├── [PHASE 5] SSZ Analysis  (extended)
│   ├── [PHASE 6] Examples      (G79, Cygnus)
│   └── [PHASE 7-8] Reporting   (MD generation)
│
├── run_ssz_validation.py       (6 steps)
│   └── GR vs SSZ comparison
│
├── run_ssz_theory_validation.py (10 steps)
│   └── Theory validation
│
├── run_ssz_unified_validation.py (11 steps)
│   └── Unified ToE proof
│
└── run_complete_test_suite.py  (~18 scripts)
    └── Auto-discovery & execution
```

**Total:** 161 Tests (116 original + 45 ToE)

---

### 3.2 Physics Test Template

**Standard Format (all 35 Physics Tests):**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
# UTF-8 Windows fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, 
        encoding='utf-8', 
        errors='replace'
    )

def main():
    print("\n" + "="*80)
    print("TEST TITLE: Physical Phenomenon")
    print("="*80)
    
    print(f"\nConfiguration:")
    print(f"  Parameter = Value")
    
    # Compute results
    results = compute_physics()
    
    print(f"\nResults:")
    print(f"  Value = {results}")
    
    print(f"\nPhysical Interpretation:")
    print(f"  • Point 1")
    print(f"  • Point 2")
    
    # Pass/Fail Logic
    if test_passed(results):
        print(f"\n{'='*80}")
        print(f"✓ Test PASSED")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'='*80}")
        print(f"✗ Test FAILED")
        print(f"{'='*80}\n")
        raise SystemExit(1)

if __name__ == '__main__':
    main()
```

**35 Physics Tests:**
1. test_ppn_exact.py - β = γ = 1
2. test_vfall_duality.py - v_esc × v_fall = c²
3. test_energy_conditions.py - WEC/DEC/SEC
4. test_c1_segments.py - C¹ continuity
5. test_c2_segments_strict.py - C² strict
6. test_c2_curvature_proxy.py - Curvature proxy
7-22. test_segwave_core.py - 16 subtests
23-26. test_ssz_kernel.py - 4 subtests
27-32. test_ssz_invariants.py - 6 subtests
33-34. test_segmenter.py - 2 subtests
35. test_multi_body_sigma.py - 1 test

---

### 3.3 Silent Technical Tests (23 Tests)

**Run in background, show only PASSED:**

```python
# test_utf8_encoding.py
def test_utf8():
    # Test UTF-8 handling
    encoding = getattr(sys.stdout, 'encoding', None)
    assert encoding and encoding.lower() == 'utf-8'
    # Silent - no verbose output

# tests/test_segwave_cli.py (16 tests)
@pytest.mark.parametrize("args", [...])
def test_cli_argument(args):
    # Test CLI parsing
    result = subprocess.run(...)
    assert result.returncode == 0
    # Silent

# tests/test_print_all_md.py (6 tests)
def test_markdown_printing():
    # Test MD generation
    output = generate_markdown()
    assert output is not None
    # Silent
```

---

### 3.4 run_full_suite.py - Logging System

**Architecture:**

```python
class TeeOutput:
    """Dual output: Console + StringIO"""
    def __init__(self, stdout, log):
        self.stdout = stdout
        self.log = log
    
    def write(self, data):
        self.stdout.write(data)
        self.log.write(data)
    
    def flush(self):
        self.stdout.flush()

# Setup
output_log = io.StringIO()
sys.stdout = TeeOutput(sys.__stdout__, output_log)

# Run tests
run_all_tests()

# Generate reports
with open("reports/RUN_SUMMARY.md", "w") as f:
    f.write(generate_summary())

with open("reports/summary-output.md", "w") as f:
    f.write(output_log.getvalue())
```

**Cache Clearing (CRITICAL!):**

```python
# BEFORE any tests!
import shutil
from pathlib import Path

# Recursive cache clearing
for cache_pattern in ['.pytest_cache', '__pycache__']:
    for cache_dir in Path('.').rglob(cache_pattern):
        if cache_dir.is_dir():
            try:
                shutil.rmtree(cache_dir)
            except Exception:
                pass

# Clear .pyc files
for pyc_pattern in ['*.pyc', '*.pyo']:
    for pyc_file in Path('.').rglob(pyc_pattern):
        try:
            pyc_file.unlink()
        except Exception:
            pass
```

**Why CRITICAL?** Corrupted pytest cache → false failures!

---

## 4. Data Flow Architectures

### 4.1 ESO Data Acquisition Pipeline

```
User Request
    ↓
ESO TAP Query (ADQL)
    ↓
FITS Download (500 MB-1 GB)
    ↓
astropy.io.fits parsing
    ↓
Wavelength/Flux Arrays
    ↓
Redshift Derivation (z = Δλ/λ)
    ↓
SSZ Prediction (z_geom_hint)
    ↓
Data Cleaning (complete rows only)
    ↓
perfect_paired_test.py
    ↓
97.9% Result!
```

**Time:** 8-14 hours (first time), 1-2 hours (recurring)

---

### 4.2 Mass Validation Pipeline

```
Input: r_obs (observed radius)
    ↓
Guess: M₀ = M_☉
    ↓
┌──────────────────────┐
│ Newton-Raphson Loop  │
│ Max 200 iterations   │
│ Tolerance: 10⁻¹²⁰    │
└──────────────────────┘
    ↓
Compute: f(M) = r_φ(M) - r_obs
    ↓
Compute: f'(M) via finite diff
    ↓
Update: M_next = M - f/f'
    ↓
Check: |f(M)| < TOL?
    │ No → Continue loop
    │ Yes → Converged!
    ↓
Output: M_reconstructed
    ↓
Validate: |M_reconstructed - M_input| < ε
    ↓
✓ Mass validation passed!
```

**Result:** Perfect reconstruction across 12 orders of magnitude!

---

### 4.3 Stratified Analysis Pipeline

```
Load: real_data_full.csv (427 obs)
    ↓
┌──────────────────────────────────┐
│ Stratification Dimensions        │
├──────────────────────────────────┤
│ • Mass bins (10)                 │
│ • Distance ranges (near/far)     │
│ • Velocity ranges (low/high)     │
│ • Radius regimes (photon/strong) │
└──────────────────────────────────┘
    ↓
For each stratum:
    ↓
Compute SSZ & GR predictions
    ↓
Paired test: |Δz_seg| < |Δz_grsr|?
    ↓
Bootstrap CI (2000 iterations)
    ↓
Binomial test (exact p-value)
    ↓
Store results
    ↓
┌──────────────────────────────────┐
│ Aggregate Statistics             │
├──────────────────────────────────┤
│ • Photon Sphere: 100% (11/11)    │
│ • Strong Field: 97.2% (35/36)    │
│ • High Velocity: 94.4% (17/18)   │
│ • Overall: 97.9% (46/47)         │
└──────────────────────────────────┘
    ↓
Generate Plots:
- Stratified Performance
- φ-Geometry Impact
- Win Rate vs Radius
- Performance Heatmap
```

---

## 5. Modularity & Reusability

### 5.1 core/ Modules

**core/predict.py:**
```python
def predict_redshift(M, r, v_tot, v_los, mode='hybrid'):
    """
    Main prediction engine
    
    Args:
        M: Mass [kg]
        r: Radius [m]
        v_tot: Total velocity [m/s]
        v_los: Line-of-sight velocity [m/s]
        mode: 'hint', 'deltaM', 'hybrid', 'geodesic'
    
    Returns:
        z_predicted: Predicted redshift
    """
    z_gr = gravitational_redshift(M, r)
    z_sr = special_relativistic_redshift(v_tot, v_los)
    
    if mode == 'deltaM':
        delta = compute_delta(M)
        z_gr_scaled = z_gr * (1 + delta/100)
        return combine_redshifts(z_gr_scaled, z_sr)
    # ... other modes
```

**Used by:**
- segspace_all_in_one_extended.py
- perfect_paired_test.py
- run_ssz_validation.py
- All validation pipelines

---

**core/stats.py:**
```python
def bootstrap_ci(data, n_boot=2000, q=0.5):
    """
    Bootstrap confidence intervals
    
    Args:
        data: List of values
        n_boot: Bootstrap iterations
        q: Quantile (0.5 = median)
    
    Returns:
        (lower, upper): 95% CI
    """
    stats = []
    for _ in range(n_boot):
        sample = np.random.choice(data, size=len(data))
        stats.append(np.quantile(sample, q))
    return np.quantile(stats, [0.025, 0.975])

def binomial_sign_test(wins, total):
    """
    Exact binomial test
    
    Args:
        wins: Number of wins
        total: Total comparisons
    
    Returns:
        p_value: Significance
    """
    from scipy.stats import binom
    return binom.cdf(total - wins, total, 0.5)
```

**Used by:**
- All paired tests
- Stratified analysis
- Validation pipelines

---

### 5.2 Dependency Management

**requirements.txt:**
```
# Core
numpy>=1.21.0
scipy>=1.7.0
pandas>=1.3.0
matplotlib>=3.4.0
sympy>=1.9

# Astronomy
astropy>=4.3
astroquery>=0.4.6

# Testing
pytest>=6.2.5
pytest-cov>=2.12.1

# Optional
plotly>=5.3.0  (interactive plots)
dash>=2.0.0    (dashboards)
numba>=0.54.0  (JIT compilation)
```

**Platform-Specific:**
```python
# Windows UTF-8 fix
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
    
# Linux/Mac (usually already UTF-8)
else:
    sys.stdout.reconfigure(encoding='utf-8')
```

---

## 6. Error Handling & Robustness

### 6.1 Safe Math Operations

```python
def safe_divide(a, b, default=float('nan')):
    """Prevents division by zero"""
    try:
        return a / b if b != 0 else default
    except:
        return default

def finite_check(x):
    """Checks for NaN/Inf"""
    try:
        return math.isfinite(float(x))
    except:
        return False

def safe_sqrt(x):
    """Prevents sqrt of negative numbers"""
    return math.sqrt(max(0, x))
```

---

### 6.2 Input Validation

```python
def validate_mass(M):
    """Checks mass plausibility"""
    if M is None or M <= 0:
        raise ValueError(f"Invalid mass: {M}")
    if M < 1e20:  # < 0.00001 M_☉
        warnings.warn("Mass very small, results may be inaccurate")
    return M

def validate_radius(r, r_s):
    """Checks radius > Schwarzschild radius"""
    if r <= r_s:
        raise ValueError(f"r={r} <= r_s={r_s}, invalid!")
    return r
```

---

### 6.3 Convergence Monitoring

```python
def newton_raphson_monitored(f, df, x0, max_iter=200, tol=1e-120):
    """Newton-Raphson with logging"""
    x = x0
    for i in range(max_iter):
        y = f(x)
        if abs(y) < tol:
            print(f"[Newton] Converged at {i} iterations")
            return x
        
        step = -y / df(x)
        
        # Step size control
        while abs(step) > abs(x):
            step *= 0.5
        
        x += step
        
        if i % 10 == 0:
            print(f"[Newton] iter={i:03d} |res|={abs(y):.3e}")
        
        if abs(step/x) < tol:
            print(f"[Newton] Relative step < tol")
            return x
    
    raise RuntimeError(f"Did not converge in {max_iter} iterations")
```

---

## 7. Performance Optimizations

### 7.1 Decimal Arithmetic Tuning

```python
from decimal import Decimal as D, getcontext

# Set precision ONCE at start
getcontext().prec = 200

# Use constants
G = D('6.67430e-11')     # NOT float!
c = D('2.99792458e8')
phi = (D(1) + D(5).sqrt()) / D(2)

# Careful conversions
def to_decimal(x):
    """Safe conversion to Decimal"""
    try:
        return D(str(x))  # Via string!
    except:
        return D(0)
```

**Why Decimal?**
- float: ~15 digits precision
- Decimal: 200+ digits precision
- Critical for mass inversion (12 orders of magnitude!)

---

### 7.2 Caching & Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def delta_percent_cached(M_str, Lmin_str, Lmax_str):
    """Cached Δ(M) computation"""
    M = D(M_str)
    Lmin = D(Lmin_str)
    Lmax = D(Lmax_str)
    return delta_percent(M, Lmin, Lmax)

# Usage
result = delta_percent_cached(str(M), str(Lmin), str(Lmax))
```

**Speedup:** 10-100× for repeated calculations

---

### 7.3 Vectorization (where possible)

```python
# SLOW: Loop
for i, row in df.iterrows():
    z_seg[i] = predict_redshift(row['M'], row['r'], ...)

# FAST: Vectorized
z_seg = np.vectorize(predict_redshift)(
    df['M'].values,
    df['r'].values,
    ...
)
```

**But:** Careful with Decimal! NumPy works with float64.

---

## 8. Summary: Best Practices

### 8.1 Code Organization

✅ **Modular:** core/ modules for reusability  
✅ **Hierarchical:** scripts/ organized by functionality  
✅ **Documented:** Docstrings for all functions  
✅ **Tested:** 161 automated tests  

### 8.2 Data Flow

✅ **Deterministic:** Fixed seeds, reproducible  
✅ **Validated:** Input checks, error handling  
✅ **Logged:** All steps documented  
✅ **Cached:** Intermediate results stored  

### 8.3 Testing

✅ **Comprehensive:** 116 + 45 Tests  
✅ **Stratified:** Physics (verbose) + Technical (silent)  
✅ **Automated:** run_all_validations.py  
✅ **Continuous:** Cache clearing BEFORE tests  

### 8.4 Platform Support

✅ **Cross-Platform:** Windows, Linux, macOS, WSL  
✅ **UTF-8 Safe:** Explicit encoding everywhere  
✅ **Subprocess-Safe:** stdout/stderr explicitly bound  
✅ **Colab-Ready:** Zero-install notebooks  

---

**© 2025 Carmen Wrede & Lino Casu**  
**License:** ANTI-CAPITALIST SOFTWARE LICENSE v1.4
