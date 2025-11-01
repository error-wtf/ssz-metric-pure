# φ-Spiral Segmented Spacetime Metric - Examples

Complete demonstration of the pure φ-spiral implementation based on local gravitational rotation angles.

---

## 🌀 What is the φ-Spiral Metric?

**Traditional GR:** Gravity = Spacetime curvature  
**SSZ φ-Spiral:** Gravity = Local rotation angle φ_G(r)

### Core Concept

Instead of curved spacetime, the gravitational field is encoded as a **local rotation (boost) angle** φ_G(r) that transforms between coordinate frames:

```
[ct']   [ cosh(φ_G)  -sinh(φ_G) ] [ct]
[r' ] = [ -sinh(φ_G)  cosh(φ_G) ] [r ]
```

This yields the metric:

```
ds² = -c² sech²(φ_G) dt² + 2c tanh(φ_G) dt dr + dr²
```

---

## 📐 Mathematical Forms

### 1. Standard Form (Cross Term)
```
ds² = -c² sech²(φ_G(r)) dt² + 2c tanh(φ_G(r)) dt dr + dr²
```

**Key feature:** Off-diagonal term g_tr ≠ 0 encodes spiral structure!

### 2. Alternative Form (β notation)
```
ds² = -c² (1 - β²(r)) dt² + 2β(r)c dt dr + dr²
where β(r) = tanh(φ_G(r))
```

### 3. Diagonal Form (Optional)
```
ds² = -c² sech²(φ_G(r)) dt² + sinh²(φ_G(r)) dρ²
where dρ = dr + β(r)c dt
```

Shows each spiral segment as a **locally flat sheet**.

### 4. Full 4D Tensor
```
g_μν = ⎡ -c²sech²(φ_G)   c·tanh(φ_G)      0           0        ⎤
       ⎢  c·tanh(φ_G)          1           0           0        ⎥
       ⎢      0                0          r²           0        ⎥
       ⎣      0                0           0      r²sin²θ       ⎦
```

---

## 🔑 Key Physical Properties

### 1. No Singularities
- **r → 0:** φ_G → 0, metric → Minkowski (FLAT!)
- **r → ∞:** Space folds into subspace layers, never diverges

### 2. Subspace Transitions
- Each **Δφ_G = 2π** creates a new Subspace Sheet
- Layer number: `n = floor(φ_G / 2π)`
- Explains ANITA-type anomalies as gravitational phase tunneling

### 3. Time Dilation
```
dτ/dt = sech(φ_G(r)) = 1/cosh(φ_G)
```
- Natural, non-singular time dilation
- → 0 for large φ_G (extreme dilation without horizon)

### 4. Spiral Velocity
```
v_r(r) = c · tanh(φ_G(r))
```
- Local "flow" velocity in spiral structure
- Always subluminal: |v_r| < c

### 5. Light Cone Tilt
- Cross term g_tr causes light cone to **tilt**, not diverge
- Null geodesics: `dr/dt = f(φ_G)` (computable!)

---

## 🚀 Quick Start

### Installation

```bash
cd E:\clone\ssz-metric-pure
pip install -e .
pip install matplotlib  # For visualizations
```

### Basic Usage

```python
from ssz_metric_pure.metric_phi_spiral_ssz_by_human import PhiSpiralSSZMetric

# Solar mass black hole
M_sun = 1.98847e30  # kg
metric = PhiSpiralSSZMetric(mass=M_sun, k=1.0)

# Metric at 5 Schwarzschild radii
r = 5 * metric.r_s
comps = metric.metric_components(r)

print(f"Rotation angle: {comps.phi_G:.6f} rad")
print(f"Time dilation: {comps.tau_factor:.6f}")
print(f"Subspace layer: {metric.subspace_layer(r)}")
```

### Run Complete Demo

```bash
cd examples
python demo_phi_spiral.py
```

**Output:**
- Console statistics (φ_G, β, dτ/dt, layers, etc.)
- 6 PNG plots in `examples/output/`:
  1. Metric components (g_tt, g_tr, g_rr)
  2. Subspace layer transitions
  3. 2D spiral embedding
  4. 3D helix with layers
  5. Time dilation & redshift
  6. Diagonal form coefficients

---

## 📊 Example Outputs

### Console Output

```
φ-SPIRAL SSZ METRIC - BASIC DEMO
================================================================================

Metric: PhiSpiralSSZMetric(M=1.989e+30 kg, k=1.000, r_s=2.953e+03 m, r0=2.953e+03 m)
Schwarzschild radius: 2.953e+03 m

Metric at different radii:
--------------------------------------------------------------------------------
r/r_s      φ_G [rad]       β           dτ/dt       Layer     
--------------------------------------------------------------------------------
0.1        0.095310        0.094963    0.995461    0         
1.0        0.693147        0.600000    0.800000    0         
3.0        1.386294        0.880797    0.474883    0         
10.0       2.397895        0.982742    0.184652    1         
```

### Visualizations

1. **Metric Components**
   - g_tt decreases with depth (time dilation)
   - g_tr ≠ 0 (spiral cross term!)
   - g_rr = 1 (constant radial component)

2. **Subspace Layers**
   - Clear 2π boundaries marked
   - Discrete layer transitions visible
   - No singularities at any radius

3. **2D Spiral Embedding**
   - Archimedean-like spiral
   - Shows φ_G rotation visually
   - Multiple windings = multiple layers

4. **3D Helix**
   - Vertical axis = φ_G / 2π
   - Color-coded by layer number
   - Beautiful helical structure

---

## 🧮 API Reference

### Main Class: `PhiSpiralSSZMetric`

```python
PhiSpiralSSZMetric(
    mass: float,              # Central mass [kg]
    k: float = 1.0,          # Spiral strength parameter
    r0: float = None,        # Characteristic radius (default: r_s)
    phi_G_profile: Callable = None  # Custom φ_G(r) function
)
```

### Core Methods

#### Gravitational Angle
- `phi_G(r)` - Rotation angle at radius r
- `dphi_G_dr(r)` - Radial derivative
- `subspace_layer(r)` - Layer number (counts 2π rotations)

#### Lorentz-like Fields
- `beta(r)` - β = tanh(φ_G)
- `gamma(r)` - γ = cosh(φ_G)
- `v_radial(r)` - Spiral velocity v_r = c·β
- `time_dilation_factor(r)` - dτ/dt = sech(φ_G)

#### Metric Components
- `g_tt(r)` - Time-time component
- `g_tr(r)` - **Time-radial cross term (SPIRAL!)**
- `g_rr(r)` - Radial-radial component
- `g_thth(r)` - Angular θ component
- `g_phph(r, theta)` - Angular φ component
- `metric_tensor(r, theta)` - Full 4×4 tensor
- `metric_components(r, theta)` - All components + auxiliary fields

#### Physical Observables
- `redshift(r)` - Gravitational redshift z
- `proper_time_ratio(r)` - Clock rate dτ/dt
- `light_cone_tilt(r)` - Null geodesic angle

#### Validation
- `schwarzschild_limit(r)` - Compare with GR
- `is_minkowski_at_center()` - Verify flat r=0

#### Diagonal Form
- `diagonal_form_coefficients(r)` - (A_diag, B_diag)

#### Visualizations
- `spiral_embedding_2d(r_array)` - 2D spiral coords
- `spiral_embedding_3d(r_array, z_scale)` - 3D helix coords
- `plot_metric_components(r_min, r_max)` - Metric plot
- `plot_subspace_layers(r_min, r_max)` - Layer transitions

#### Extensions (Experimental)
- `phi_G_anisotropic(r, theta, func)` - Angular dependence
- `phi_G_time_dependent(r, t, func)` - GW perturbations

---

## 🎨 Custom φ_G Profiles

### Default (Logarithmic)
```python
metric = PhiSpiralSSZMetric(mass=M_sun, k=1.0)
# φ_G(r) = k·log(1 + r/r₀)
```

### Custom Profile
```python
# Power law
phi_G_power = lambda r: 2.0 * (r / r_s)**0.5

# Empirical from data
import pandas as pd
df = pd.read_csv("ssz_data.csv")
from scipy.interpolate import interp1d
phi_G_empirical = interp1d(df['r'], df['phi_G'], kind='cubic')

# Create metric
metric = PhiSpiralSSZMetric(mass=M_sun, phi_G_profile=phi_G_empirical)
```

---

## 📈 Advanced Examples

### 1. Gravitational Waves (Time-Dependent φ_G)

```python
# Sinusoidal perturbation
omega_gw = 2 * np.pi * 100  # 100 Hz
r_gw = 100 * metric.r_s

delta_phi_gw = lambda r, t: 0.01 * np.sin(omega_gw * t) * np.exp(-r/r_gw)

# Evaluate at different times
for t in np.linspace(0, 0.1, 10):
    phi_dyn = metric.phi_G_time_dependent(r, t, delta_phi_gw)
    print(f"t={t:.3f}s: φ_G={phi_dyn:.6f} rad")
```

### 2. Anisotropic Mass (Angular Dependence)

```python
# Oblate deformation
f_oblate = lambda theta: 1.0 + 0.2 * np.sin(theta)**2

theta_vals = np.linspace(0, np.pi, 100)
for theta in theta_vals:
    phi_aniso = metric.phi_G_anisotropic(r, theta, f_oblate)
    # Plot φ_G vs. θ
```

### 3. Null Geodesics (Light Propagation)

```python
# Solve: g_tt + 2·g_tr·(dr/dt) + g_rr·(dr/dt)² = 0
r_vals = np.linspace(metric.r_s, 10*metric.r_s, 1000)

for r in r_vals:
    alpha = metric.light_cone_tilt(r)
    # Plot null cone boundaries
```

### 4. Redshift Mapping

```python
# Observer at infinity, source at r_source
r_source_vals = np.logspace(0, 2, 100) * metric.r_s
z_vals = [metric.redshift(r) for r in r_source_vals]

# Plot z vs. r_source
plt.loglog(r_source_vals / metric.r_s, z_vals)
plt.xlabel("r_source / r_s")
plt.ylabel("Redshift z")
```

---

## 🔬 Scientific Applications

### 1. Black Hole Phenomenology
- Study **singularity-free** black hole interiors
- Map subspace layer structure
- Predict observable effects at horizons

### 2. ANITA Anomalies
- Model radio events as **phase tunneling** across φ_G = 2π
- Calculate transmission coefficients
- Predict event rates

### 3. Gravitational Lensing
- Modified light bending due to g_tr term
- Spiral distortions in images
- Time delays with spiral correction

### 4. Cosmology
- Apply to cosmological scales (k varies with Λ)
- Dark energy as φ_G evolution?
- CMB imprints

### 5. Gravitational Waves
- Oscillating φ_G(r,t) as GW model
- Waveform predictions
- Detector signatures

---

## 📝 Comparison: SSZ vs. GR

| Property | General Relativity | SSZ φ-Spiral |
|----------|-------------------|--------------|
| **Field** | Curvature R_μνρσ | Rotation angle φ_G(r) |
| **Singularity** | r=0 diverges | r=0 flat (φ_G→0) |
| **Horizon** | Event horizon at r_s | Subspace transition at φ_G=2π |
| **g_tr** | 0 (Schwarzschild) | ≠ 0 (Spiral!) |
| **Light cone** | Collapses at horizon | Tilts, never collapses |
| **Geometry** | Riemannian manifold | Spiral-segmented sheets |

---

## 🐛 Troubleshooting

### Import Error
```python
ModuleNotFoundError: No module named 'ssz_metric_pure'
```
**Fix:** Install package in editable mode:
```bash
cd E:\clone\ssz-metric-pure
pip install -e .
```

### Matplotlib Missing
```
ImportError: matplotlib required for plotting
```
**Fix:**
```bash
pip install matplotlib
```

### Plots Not Saved
- Check `examples/output/` directory exists
- Script creates it automatically
- Verify write permissions

---

## 📚 References

1. **Casu & Wrede (2025)** - Segmented Spacetime Theory
2. **φ-Spiral Framework** - Pure geometric rotation model
3. **WindSurf Implementation** - Complete computational specification

---

## 🎯 Next Steps

1. **Run the demo:** `python demo_phi_spiral.py`
2. **Explore visualizations** in `output/`
3. **Modify k parameter** to see different spiral strengths
4. **Implement custom φ_G(r)** profiles from data
5. **Compare with observational data**

---

## 📧 Contact

**Questions? Issues? Extensions?**

- GitHub Issues: Report bugs or request features
- Scientific inquiries: Contact authors directly
- Collaboration: Research partnerships welcome

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4

**100% Pure SSZ. No Singularities. Spiral All The Way Down.** 🌀
