# SSZ Metric Pure - Quick Start Guide

**Get started with Pure Segmented Spacetime in 5 minutes!**

---

## Installation

### From Source (Recommended for Development)

```bash
# Clone the repository
cd E:/clone/ssz-metric-pure

# Install in editable mode
pip install -e .

# Verify installation
python -c "import ssz_metric_pure as ssz; print(f'SSZ v{ssz.__version__} installed!')"
```

### Dependencies

Minimal requirements:
```bash
pip install numpy scipy sympy
```

For development:
```bash
pip install pytest pytest-cov black mypy flake8
```

---

## Basic Usage

### 1. Static Black Hole (Schwarzschild-like)

```python
from ssz_metric_pure import SSZParams, StaticSSZMetric, M_SUN

# Create parameters for solar mass black hole
params = SSZParams(mass=M_SUN)

# Initialize metric
metric = StaticSSZMetric(params)

# Schwarzschild radius
print(f"r_s = {metric.r_s:.3e} m")  # → 2.953e+03 m

# Metric coefficient at 3× Schwarzschild radius
A = metric.A_coefficient(3 * metric.r_s)
print(f"A(3r_s) = {A:.6f}")  # → ~0.25 (singularity-free!)

# Gravitational redshift
z = metric.redshift(5 * metric.r_s)
print(f"Redshift at 5r_s: z = {z:.3f}")

# Escape velocity
v_esc = metric.escape_velocity(5 * metric.r_s)
print(f"v_esc = {v_esc:.3e} m/s")  # → < c always!
```

**Key Result:** `A(0) = 1.0` → **NO SINGULARITY at center!**

---

### 2. Rotating Black Hole (Kerr-like)

```python
from ssz_metric_pure import KerrSSZParams, KerrSSZMetric
import numpy as np

# Fast rotating black hole (â = 0.9)
params = KerrSSZParams(mass=1e30, spin=0.9)
kerr = KerrSSZMetric(params)

# Horizons
r_plus, r_minus = kerr.horizons()
print(f"Outer horizon: r_+ = {r_plus/kerr.r_s:.3f} r_s")
print(f"Inner horizon: r_- = {r_minus/kerr.r_s:.3f} r_s")

# Ergosphere at equator
r_ergo = kerr.ergosphere_radius(np.pi / 2)
print(f"Ergosphere: r_ergo = {r_ergo/kerr.r_s:.3f} r_s")

# Frame dragging frequency
omega = kerr.frame_drag_frequency(5*kerr.r_s, np.pi/2)
print(f"Frame drag: ω = {omega:.3e} rad/s")

# Full metric tensor
theta = np.pi / 4  # 45 degrees
components = kerr.metric_tensor(5*kerr.r_s, theta)
print(f"g_tt = {components.g_tt:.6f}")
print(f"g_tφ = {components.g_tph:.6e}")  # Off-diagonal → frame dragging!
```

**Key Features:**
- Frame dragging (g_tφ ≠ 0)
- Ergosphere (g_tt = 0 boundary)
- Inner/outer horizons
- Schwarzschild limit (â=0)

---

### 3. Accessing Constants

```python
from ssz_metric_pure import PHI, G_SI, C_SI, U_STAR_UNIVERSAL

print(f"Golden Ratio: φ = {PHI:.15f}")
print(f"Gravitational constant: G = {G_SI:.3e} m³/(kg·s²)")
print(f"Speed of light: c = {C_SI:.0f} m/s")
print(f"Universal intersection: u* = {U_STAR_UNIVERSAL}")
```

**φ (Phi) is NOT a fitting parameter!**
- Emerges from geometric structure
- Fibonacci-like segment recursion
- Optimal spacetime packing

---

### 4. Segment Density & Time Dilation

```python
from ssz_metric_pure import segment_density_N, time_dilation_SSZ

# Segment density at various radii
r_values = [0.5, 1.0, 2.0, 5.0, 10.0]  # in units of r_s
r_s = 2953  # meters (solar mass)

for r_ratio in r_values:
    r = r_ratio * r_s
    N = segment_density_N(r, r_s)
    D = time_dilation_SSZ(r, r_s)
    print(f"r = {r_ratio:.1f}r_s: N = {N:.6f}, D = {D:.6f}")
```

**Key Property:**
- N(0) = 0 → Flat spacetime at center
- N(∞) → 1 → Bounded saturation
- D = 1/(1+N) → Time dilation factor

---

### 5. Curvature Tensors (Advanced)

```python
from ssz_metric_pure import compute_curvature_at_point
import numpy as np

# Define metric function (4×4 tensor)
def static_metric_func(t, r, theta, phi):
    from ssz_metric_pure import SSZParams, StaticSSZMetric, M_SUN
    params = SSZParams(mass=M_SUN)
    metric = StaticSSZMetric(params)
    
    A = metric.A_coefficient(r)
    B = metric.B_coefficient(r)
    
    g = np.zeros((4, 4))
    g[0, 0] = -A  # g_tt
    g[1, 1] = B   # g_rr
    g[2, 2] = r * r  # g_θθ
    g[3, 3] = (r * np.sin(theta)) ** 2  # g_φφ
    
    return g

# Compute curvature at point
coords = (0, 5*2953, np.pi/2, 0)  # (t, r, θ, φ)
curvature = compute_curvature_at_point(static_metric_func, coords)

print(f"Ricci scalar: R = {curvature['ricci_scalar']:.3e}")
print(f"Einstein tensor computed: {curvature['einstein'].shape}")
```

**Warning:** Full Riemann tensor computation is expensive (256 components)!

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_metric_static.py -v

# With coverage
pytest tests/ --cov=ssz_metric_pure --cov-report=html
```

**Expected:** 18/18 tests PASS (100%)

---

## Examples Directory

See `examples/` for more:
- `basic_usage.py` - Comprehensive examples
- `kerr_rotation.py` - (coming soon) Rotating black holes
- `visualization.py` - (coming soon) Plotting tools

---

## Common Patterns

### Pattern 1: Compare SSZ vs GR

```python
from ssz_metric_pure import SSZParams, StaticSSZMetric, M_SUN

params = SSZParams(mass=M_SUN)
metric = StaticSSZMetric(params)

r = 2 * metric.r_s

# SSZ metric
A_ssz = metric.A_coefficient(r)

# GR Schwarzschild (for comparison)
A_gr = 1 - metric.r_s / r

print(f"SSZ: A({r/metric.r_s:.1f}r_s) = {A_ssz:.6f}")
print(f"GR:  A({r/metric.r_s:.1f}r_s) = {A_gr:.6f}")
print(f"Difference: {abs(A_ssz - A_gr):.3e}")
```

### Pattern 2: Validate Singularity-Free Property

```python
from ssz_metric_pure import SSZParams, StaticSSZMetric, M_SUN
import numpy as np

params = SSZParams(mass=M_SUN)
metric = StaticSSZMetric(params)

# Test from near-center to far field
r_test = np.logspace(
    np.log10(0.1 * metric.r_phi),  # Near natural boundary
    np.log10(100 * metric.r_s),     # Far field
    num=100
)

A_values = [metric.A_coefficient(r) for r in r_test]

print(f"A_min = {min(A_values):.6f}")  # Should be > 0!
print(f"A(0) ≈ {metric.A_coefficient(1e-10):.6f}")  # Should be ≈ 1.0

assert all(A > 0 for A in A_values), "SINGULARITY DETECTED!"
print("✅ Singularity-free validated!")
```

### Pattern 3: Explore Spin Effects

```python
from ssz_metric_pure import KerrSSZParams, KerrSSZMetric

spins = [0.0, 0.3, 0.6, 0.9, 0.99]

for a_hat in spins:
    params = KerrSSZParams(mass=1e30, spin=a_hat)
    kerr = KerrSSZMetric(params)
    
    r_plus, r_minus = kerr.horizons()
    
    if not np.isnan(r_plus):
        print(f"â = {a_hat:.2f}: r_+/r_s = {r_plus/kerr.r_s:.3f}, "
              f"r_-/r_s = {r_minus/kerr.r_s:.3f}")
    else:
        print(f"â = {a_hat:.2f}: NAKED SINGULARITY (unphysical!)")
```

---

## Troubleshooting

### Import Error

```python
# If you get: ModuleNotFoundError: No module named 'ssz_metric_pure'
# Solution: Reinstall in editable mode
pip install -e .
```

### Test Failures

```bash
# Clear pytest cache
rm -rf .pytest_cache __pycache__

# Reinstall package
pip uninstall ssz-metric-pure
pip install -e .

# Run tests again
pytest tests/ -v
```

### Windows Unicode Issues

Some print statements with φ, θ, etc. may fail on Windows cmd.
Solution: Use PowerShell or set environment variable:

```powershell
$env:PYTHONIOENCODING="utf-8"
python your_script.py
```

---

## Next Steps

1. **Read Documentation:**
   - `README.md` - Overview
   - `IMPLEMENTATION_SUMMARY.md` - Detailed guide
   - Function docstrings - Inline help

2. **Explore Examples:**
   - `examples/basic_usage.py`
   - Modify parameters, test your own cases

3. **Run Tests:**
   - Understand validation methods
   - Add your own test cases

4. **Contribute:**
   - Report issues on GitHub
   - Suggest features
   - Submit pull requests

---

## Scientific References

### Key Papers (in `Segmented-Spacetime-Results/papers/`)
- SSZ_Black_Hole_Stability.md
- SSZ_Phi_Series_Discovery.md
- ESO_Validation_Results.md

### External Resources
- Schwarzschild Metric (GR comparison)
- Kerr Metric (rotation reference)
- Boyer-Lindquist coordinates

---

## Getting Help

**Documentation:**
- Inline: `help(SSZParams)`
- README: Complete overview
- Examples: Practical code

**Issues:**
- GitHub Issues (if public repo)
- Contact authors directly

**Community:**
- Research collaborations welcome
- Educational use encouraged
- Anti-capitalist license - read `LICENSE`

---

## License

**ANTI-CAPITALIST SOFTWARE LICENSE v1.4**

- ✅ Free for research
- ✅ Free for education
- ✅ Free for non-commercial use
- ❌ Prohibited for capitalist exploitation

See `LICENSE` file for full terms.

---

## Citation

```bibtex
@software{wrede2025ssz,
  author = {Wrede, Carmen and Casu, Lino},
  title = {SSZ Metric Pure: Pure Segmented Spacetime},
  year = {2025},
  version = {0.1.0},
  url = {https://github.com/error-wtf/ssz-metric-pure}
}
```

---

**Ready to explore singularity-free spacetimes? Let's go!** 🚀🌌

© 2025 Carmen Wrede & Lino Casu
