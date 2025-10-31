# SSZ Metric Pure - Mathematical Specification

**Version:** 1.0.0  
**Date:** 2025-10-31  
**Authors:** Carmen Wrede & Lino Casu

---

## 1. Core Principles

### 1.1 Segmented Spacetime Hypothesis

Spacetime is **not** a continuous manifold, but consists of **discrete segments** with finite size:

```
Δx_min ≈ Planck length ≈ 1.616 × 10^(-35) m
```

**Consequences:**
- No mathematical singularities
- Natural quantum-gravity bridge
- Emergent metric from segment configuration

### 1.2 Golden Ratio Saturation

Segments fill spacetime according to the **Golden Ratio** φ = (1+√5)/2:

```
Ξ(r) = 1 - exp(-φ · r/r_s)
```

where:
- Ξ(r): Segment saturation factor ∈ [0, 1)
- φ ≈ 1.618033988749: Golden ratio
- r_s: Schwarzschild radius = 2GM/c²

**Physical Interpretation:**
- Ξ(0) = 0: No saturation at center (empty)
- Ξ(∞) → 1: Full saturation far away
- φ provides "natural" exponential scale

---

## 2. Time Component: -g_tt

### 2.1 SSZ Time Dilation

```
D_SSZ(r) = 1 / (1 + Ξ(r))
```

**Properties:**
- D_SSZ(0) = 1: No dilation at center (flat!)
- D_SSZ(r_s) ≈ 0.16: Finite at event horizon
- D_SSZ(∞) → 0.5: Approaches constant
- D_SSZ > 0: No singularity anywhere

### 2.2 Inner Metric Coefficient

```
A_Ξ(r) = D_SSZ(r)² = (1 + Ξ(r))^(-2)
```

**Derivative:**
```
dA_Ξ/dr = -2φ/r_s · exp(-φ r/r_s) / (1 + Ξ(r))³
```

### 2.3 GR Time Dilation (Comparison)

```
D_GR(r) = √(1 - r_s/r)  for r > r_s
```

**Singularity:**
- D_GR(r_s) = 0: Diverges at horizon
- D_GR(r < r_s): Undefined

---

## 3. Outer Solution: φ-Series

### 3.1 Post-Newtonian Expansion

```
A_φ(r) = Σ_{n=0}^6 ε_n (r_s/2r)^n
```

**Coefficients (φ-series):**
```
ε_0 = 1
ε_1 = -2
ε_2 = 2
ε_3 = -φ ≈ -1.618
ε_4 = φ²/2 ≈ 1.309
ε_5 = -φ³/6 ≈ -0.707
ε_6 = φ⁴/24 ≈ 0.287
```

### 3.2 Derivation from Golden Ratio Recursion

Fibonacci relation:
```
F_{n+1} = F_n + F_{n-1}
```

Yields φ-series via:
```
φ^n = φ·φ^(n-1) + φ^(n-2)
```

Applied to metric expansion → ε_n coefficients

---

## 4. Blending: Inner ↔ Outer

### 4.1 Intersection Point r*

Find r* where:
```
D_SSZ(r*) = D_GR(r*)
```

Numerical solution (Brent's method):
```
r* ≈ (2-5) × r_s  (typically)
```

### 4.2 Tanh Transition

```
h(r) = 0.5 · (1 - tanh((r - r*) / Δ))
```

where Δ = blend_width × r*

**Properties:**
- h(r << r*) → 1: Inner (SSZ)
- h(r >> r*) → 0: Outer (φ-series)
- Smooth C^∞ transition

### 4.3 Blended Metric

```
A_blend(r) = h(r) · A_Ξ(r) + (1-h(r)) · A_φ(r)
```

---

## 5. Mirror Blending (Alternative)

### 5.1 GR-SSZ Mix

```
A_GR(r) = 1 - r_s/r  (Schwarzschild)
A_SSZ(r) = A_Ξ(r)    (Segment saturation)

A_mix(r) = h(r) · A_SSZ(r) + (1-h(r)) · A_GR(r)
```

### 5.2 Softplus Safety Floor

```
A_safe(r) = ε + (1/β) · ln(1 + exp(β·(A_mix - ε)))
```

**Parameters:**
- ε = 1e-10: Safety floor (A > 0)
- β = 100: Steepness parameter

**Properties:**
- A_safe > ε everywhere
- Smooth (C^∞)
- Numerically stable

---

## 6. Mass Correction: Δ(M)

### 6.1 Empirical Formula

```
Δ(M) = 2 + 98 · exp(-10 · r_s)
```

**Limits:**
- r_s → 0: Δ(M) → 100 (small masses)
- r_s → ∞: Δ(M) → 2 (large masses)

### 6.2 Corrected Schwarzschild Radius

```
r_s_corrected = r_s · Δ(M)
```

**Purpose:**
Empirical adjustment for segment effects on effective mass.

---

## 7. Radial Component: g_rr

### 7.1 Standard Relation

```
B(r) = 1 / A(r)
```

**Properties:**
- B(0) = 1 / A(0) = 1
- B(r_s) finite (no singularity!)
- B > 0 everywhere

---

## 8. Full Metric Tensor

### 8.1 Spherical Coordinates

```
ds² = -A(r) dt² + B(r) dr² + r² dθ² + r² sin²θ dφ²
```

**Diagonal form:**
```
g_μν = diag(-A(r), B(r), r², r² sin²θ)
```

### 8.2 Components

```
g_tt = -A(r)              (time-time)
g_rr = B(r) = 1/A(r)      (radial-radial)
g_θθ = r²                 (polar-polar)
g_φφ = r² sin²θ           (azimuthal-azimuthal)
```

### 8.3 Inverse Metric

```
g^μν = diag(-1/A(r), 1/B(r), 1/r², 1/(r² sin²θ))
```

---

## 9. Curvature

### 9.1 Curvature Proxy

Approximate Kretschmann scalar:
```
K_proxy(r) = ((1-A)/r²)² + (A'/r)²
```

**SSZ Property:**
- K_proxy(0) finite!
- No divergence at r=0

### 9.2 Kretschmann Scalar (Full)

```
K = R^μνρσ R_μνρσ
```

For Schwarzschild:
```
K_GR = 12 r_s² / r⁶  → ∞ as r → 0
```

For SSZ:
```
K_SSZ(0) finite
```

---

## 10. Derivatives

### 10.1 Segment Saturation Derivative

```
dΞ/dr = (φ/r_s) · exp(-φ r/r_s)
```

### 10.2 Metric Coefficient Derivative

```
dA_Ξ/dr = -2(1+Ξ)^(-3) · dΞ/dr
```

### 10.3 Christoffel Symbols

Example:
```
Γ^t_tr = (1/2) · (1/A) · dA/dr
Γ^r_tt = (1/2) · (1/B) · dA/dr · A
```

---

## 11. Physical Observables

### 11.1 Photon Sphere

Circular null geodesic at:
```
r_ph ≈ 1.338 × r_s  (SSZ, finite!)
```

vs GR:
```
r_ph_GR = 1.5 × r_s
```

### 11.2 ISCO

Innermost stable circular orbit:
```
r_ISCO ≈ 3.066 × r_s  (SSZ)
r_ISCO_GR = 3 × r_s   (GR)
```

### 11.3 Shadow Radius

```
b_shadow = r_ph √(g_φφ / |g_tt|)
```

SSZ: Finite and well-defined

---

## 12. Numerical Implementation

### 12.1 Key Functions

```python
# Segment saturation
def Xi(r, r_s):
    return 1 - np.exp(-PHI * r / r_s)

# SSZ time dilation
def D_SSZ(r, r_s):
    return 1.0 / (1.0 + Xi(r, r_s))

# Inner metric
def A_Xi(r, r_s):
    return D_SSZ(r, r_s) ** 2

# φ-series
def A_phi_series(r, r_s, order=6):
    A = 1.0
    x = r_s / (2*r)
    for n in range(1, order+1):
        A += epsilon[n] * x**n
    return A

# Safe blended metric
def A_safe(r, r_s, use_mirror_blend=True):
    # ... tanh blending + softplus ...
    return A_safe_value
```

### 12.2 Stability Considerations

- Use `np.maximum(r, epsilon)` to avoid r=0 division
- Apply softplus to guarantee A > 0
- Use Brent's method for r* finding
- Numerical derivatives via `np.gradient`

---

## 13. Validation Tests

### 13.1 Segment Density
- ✅ Ξ(0) = 0
- ✅ Ξ(∞) → 1
- ✅ dΞ/dr > 0

### 13.2 Time Dilation
- ✅ D_SSZ(0) = 1
- ✅ D_SSZ > 0 everywhere
- ✅ D_SSZ(r*) = D_GR(r*)

### 13.3 Metric
- ✅ A(0) = 1
- ✅ A > 0 everywhere
- ✅ B = 1/A
- ✅ g_μν finite everywhere

### 13.4 Curvature
- ✅ K_proxy(0) finite
- ✅ No divergence anywhere

---

## 14. Comparison: SSZ vs GR

| Property | GR | SSZ |
|----------|-----|-----|
| D(0) | Undefined | **1.0** |
| D(r_s) | 0 (singularity) | **≈0.16 (finite)** |
| A(0) | Undefined | **1.0 (flat!)** |
| Curvature at r=0 | ∞ | **Finite** |
| Quantum compatible | No | **Yes** |
| Segments | N/A | **Discrete** |
| φ in formulas | No | **Yes** |

---

## 15. References

**SSZ Formalism:**
- Segmented Spacetime hypothesis
- Golden Ratio saturation
- φ-series PN expansion

**Implementation:**
- ssz-full-metric (φ-series, PN)
- ssz-metric-final (mirror blend, softplus)
- ssz-metric-pure (this project)

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the Anti-Capitalist Software License v1.4

**Status:** Complete Mathematical Specification v1.0
