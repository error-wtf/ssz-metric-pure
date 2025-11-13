# SSZ Mathematical Foundations - Complete Formula Collection

**Dokumentation aller mathematischen Grundlagen der Segmented Spacetime Theorie**  
**Datum:** 2025-11-13  
**Quellen:** error-wtf/Segmented-Spacetime-Mass-Projection-Unified-Results, ssz-metric-pure, g79-cygnus-tests

---

## 1. Fundamentale Konstanten

### φ - Der Goldene Schnitt (FUNDAMENTAL!)
```
φ = (1 + √5) / 2 ≈ 1.618033988749...
```

**Rolle:** KEINE fitting parameter, sondern geometrische Grundlage der Raumzeit-Segmentierung!
- φ-Spiral Geometrie für self-similar scaling
- Natürliche Grenze: r_φ = (φ/2)r_s ≈ 1.618 r_s
- Erscheint in ALLEN SSZ-Relationen

### Weitere Konstanten
```python
G = 6.67430e-11        # m³ kg⁻¹ s⁻² (Gravitationskonstante)
c = 2.99792458e8       # m s⁻¹ (Lichtgeschwindigkeit)
α_fs = 7.2973525693e-3 # Fine structure constant
h = 6.62607015e-34     # Js (Planck-Konstante)
M_☉ = 1.98847e30       # kg (Sonnenmasse)
```

---

## 2. SSZ Metrik-Formeln

### 2.1 Diagonal (T,r) Form (Empfohlen für v2.1.0+)
```
ds² = -(c²/γ²(r)) dT² + γ²(r) dr² + r² dΩ²

Wo:
γ(r) = cosh(φ_G(r))
β(r) = tanh(φ_G(r))

2PN Kalibrierung (v2.1.0 - EMPFOHLEN):
φ²_G(r) = 2U(1 + U/3),  U = GM/(rc²)

1PN Kalibrierung (v2.0.0):
φ²_G(r) = 2U
```

**Bedeutung:** 2PN matcht GR bis O(U²) für schnellere Konvergenz

### 2.2 Original (t,r) Form
```
ds² = -c²(1-β²)dt² + 2βc dt dr + dr² + r² dΩ²

Transformation:
dT = dt - (β(r)γ²(r)/c) dr
```

**Physikalisch äquivalent** (bewiesen via kovarianter Transformation)

### 2.3 Schwarzschild-ähnliche Form
```
ds² = -A(r) c² dt² + B(r) dr² + r² dΩ²

A(U) = 1 - 2U + 2U² + ε₃U³
B(r) = 1/A(r)
U = GM/(rc²)
```

**ε₃-Parameter:**
```
ε₃ = -24/5 = -4.8  (Standard-Wert aus PPN-Tests)
```

---

## 3. Segment Density Ξ(r)

### 3.1 Hyperbolische Form (α-abhängig)
```
Ξ(r) = Ξ_max · tanh(α · r_s/r)

α = 1.0  (Standard)
Ξ_max < 1  (Sättigung verhindert Singularitäten)
```

**Eigenschaften:**
- Kontinuierliche Transition
- Keine Crossover bei α=1.0
- SSZ-Korrekturen bei ALLEN Radien

### 3.2 Exponentielle Form (universell)
```
Ξ(r) = Ξ_max(1 - e^(-φr/r_s))
```

**Eigenschaften:**
- **Universeller Crossover bei r* = 1.386562 r_s**
- Massenunabhängig!
- φ-basierte natürliche Skala

---

## 4. Zeit-Dilatation & Emergenz

### 4.1 GR vs SSZ Time Dilation
```
# General Relativity:
D_GR(r) = √(1 - r_s/r)

# SSZ (mit Segment-Dichte):
D_SSZ(r) = √(1 - r_s/r) · √(1 - Ξ(r))

# Am Horizont (r = r_s):
D_GR(r_s) = 0  (Singularität!)
D_SSZ(r_s) = √(1 - Ξ_max) ≈ 0.667  (endlich!)
```

### 4.2 Zeit-Emergenz aus Segmenten
```
Δt(r) = (1 + Ξ(r)) / φ

Zeit entsteht aus φ-basierten Segment-Resonanzen!
```

**Resonanzfrequenz:**
```
ω(r) = φ / (1 + Ξ(r))
ω(∞) = φ = 1.618...  (Asymptotisch)
```

### 4.3 Universeller Intersektionspunkt
```
r* / r_s = 1.386562  (für exponentielle Ξ)
D*(r*) = 0.528007

Bei r* gilt: D_GR(r*) = D_SSZ(r*) (exakt!)
```

---

## 5. Mass-Projection & Δ(M) Korrekturen

### 5.1 Φ-basierte Δ(M) Formel
```
Δ(M) = A · exp(-α · r_s) + B

Wo:
r_s = 2GM/c²
A = 98.01
α = 2.7177e4  (abgeleitet von φ-Spiral Pitch!)
B = 1.96
```

**Wichtig:** α ist NICHT arbiträr, sondern aus φ-Spiral-Geometrie abgeleitet!

### 5.2 Normalisierung
```
L = log₁₀(M)
norm = (L - L_min) / (L_max - L_min)  falls L_max > L_min, sonst 1
Δ_percent(M) = Δ_raw(M) · norm
```

### 5.3 Mass-Radius Beziehung
```
r_φ = (G·φ·M/c²) · (1 + Δ_percent/100)
```

**Mass Inversion** (Newton-Raphson):
```
f(M) = r_φ(M) - r_obs = 0
M_next = M - f(M)/f'(M)
Konvergenz: |res| < 10⁻¹²⁰
```

---

## 6. Gravitational & Special Relativistic Redshift

### 6.1 Gravitational Redshift
```
z_gr(M, r) = 1/√(1 - r_s/r) - 1
```

**Gültigkeit:** r > r_s, sonst NaN

### 6.2 Special Relativistic Redshift
```
β = v_tot/c  (begrenzt auf 0.999999999999)
γ = 1/√(1 - β²)
β_los = v_los/c

z_sr = γ(1 + β_los) - 1
```

### 6.3 Kombinierter Redshift
```
z_combined = (1 + z_gr)(1 + z_sr) - 1
```

### 6.4 SSZ Segment-basierter Redshift
```
# Mit Δ(M) Korrektur:
z_gr_scaled = z_gr · (1 + Δ_percent/100)
z_seg = (1 + z_gr_scaled)(1 + z_sr) - 1
```

---

## 7. PPN (Parametrized Post-Newtonian) Parameter

### 7.1 Weak-Field Expansion
```
A(U) = 1 - 2U + 2U² + O(U³)
B(U) = 1/A(U) = 1 + 2U + O(U²)
```

### 7.2 PPN Parameter
```
β = 1.000000000000  (kein bevorzugtes Bezugssystem)
γ = 1.000000000000  (GR-ähnliche Raum-Krümmung)

Abweichung: |β-1| < 10⁻¹² (Maschinenpräzision!)
```

**Bedeutung:** SSZ matcht GR im Weak-Field-Limit EXAKT!

---

## 8. Duale Geschwindigkeits-Invariante

### 8.1 Fundamentale Dualität
```
v_esc(r) = √(2GM/r)  (Escape velocity)
v_fall(r) = c²/v_esc(r)  (Dual fall velocity)

INVARIANTE: v_esc(r) · v_fall(r) = c²  (exakt!)
```

**Max Abweichung:** 0.000e+00 (Maschinenpräzision)

### 8.2 Lorentz-Faktoren
```
γ_GR(r) = 1/√(1 - r_s/r)
γ_dual(v_fall) = 1/√(1 - (c/v_fall)²)

Konsistenz: γ_GR(r) = γ_dual(v_fall(r))
```

**Physikalisch:** v_fall kann c überschreiten (duales Skalentempo, nicht physikalische Geschwindigkeit!)

---

## 9. Energie-Bedingungen (Energy Conditions)

### 9.1 Effektiver Stress-Energy Tensor
```
T_μν = (c⁴/8πG) G_μν

Aus SSZ-Metrik abgeleitet:
8πρ   = (1-A)/r² - A'/r
8πp_r = A'/r + (A-1)/r²
8πp_t = A''/2 + A'/r
```

**Wichtige Relation:**
```
p_r = -ρc²  (radiale Spannung balanciert Dichte!)
```

### 9.2 Bedingungen
```
WEC (Weak Energy):      ρ ≥ 0 AND ρ + p_t ≥ 0
DEC (Dominant Energy):  ρ ≥ |p_r| AND ρ ≥ |p_t|
SEC (Strong Energy):    ρ + p_r + 2p_t ≥ 0
NEC (Null Energy):      ρ + p_r = 0  (analytisch für SSZ!)
```

**Resultat:**
- WEC/DEC/SEC **erfüllt für r ≥ 5r_s**
- Verletzungen auf r < 5r_s beschränkt (starkes Feld)
- Abweichungen kontrolliert und endlich

---

## 10. Schwarze Loch Stabilität

### 10.1 Energie-Dissipation
```
E_{t+1} = E_t(1 + λ_A - λ_A²K²)

Dämpfungsfaktor: η ≈ 4.9×10³⁷
E_final/E₀ ≈ 10⁻³⁸  (extreme Dissipation!)
```

### 10.2 Segment-Sättigung
```
Ξ_max = 0.802 < 1.0

R(r=0) = 0.503 R₀  (endliche Krümmung am Zentrum!)
D(r_s) = 2/(2+α) ≈ 0.667  (endlich am Horizont!)
```

### 10.3 Stabilitätsschwelle
```
Stabil wenn: λ_A < 1/K²
Chaos wenn: λ_A > 1/K²  (Zeit bricht zusammen!)
```

---

## 11. Observables & Testbare Vorhersagen

### 11.1 Neutron Star Differenzen
```
Δ = (D_SSZ - D_GR) / D_GR × 100%

Bei r = 5r_s:
Δ = -44%  (SSZ vorhersagt langsameren Zeitfluss!)

Observabel: 
- Pulsar-Perioden erscheinen LÄNGER
- Röntgen-Timing zeigt SSZ-Signatur
- Erhöhter Redshift
```

### 11.2 Schwarzes Loch Schatten
```
r_shadow(SSZ) ≈ r_shadow(GR) × 1.02

~2% größer als GR
Testbar mit zukünftiger EHT-Auflösung
```

### 11.3 Gravitationswellen
```
f_QNM(SSZ) ≈ φ · f_QNM(GR)

~5% Frequenzshift
Testbar mit 3G-Detektoren (Cosmic Explorer, Einstein Telescope)
```

---

## 12. Kontinuitäts-Bedingungen

### 12.1 C¹ Kontinuität
```
Segment-Joins prüfen:
|A(r_boundary⁺) - A(r_boundary⁻)| < ε
|A'(r_boundary⁺) - A'(r_boundary⁻)| < ε
```

### 12.2 C² Kontinuität
```
Quintic Hermite Interpolation:
- Wert-Kontinuität
- 1. Ableitung kontinuierlich
- 2. Ableitung kontinuierlich

Curvature Proxy: K ≈ 10⁻¹⁵ – 10⁻¹⁶  (extrem glatt!)
```

**Resultat:** Keine δ-Funktions-Singularitäten im Stress-Energy!

---

## 13. Kosmologische Anwendungen

### 13.1 G79.29+0.46 Temporal Redshift
```
z_temporal = 1 - γ_seg ≈ 0.12  (intrinsischer temporaler Shift)
z_obs ≈ 1.7×10⁻⁵  (beobachteter Residual, Δv ≈ 5 km/s)

Physikalisch:
- 86% des Effekts ist temporal (Metrik-Physik)
- 14% ist klassischer Doppler (Expansions-Kinematik)
```

### 13.2 Temperatur-Beziehung
```
T_obs(r) = γ_seg(r) × T_local

Innerhalb g⁽²⁾: Scheinbare Kühlung (γ_seg < 1)
An Grenze: Temperatur-Sprung ~150 K
Außerhalb g⁽¹⁾: Klassische Temperatur
```

### 13.3 Hot Ring Structure
```
Position: r ~ 0.5 pc
Temperatur: 200-300 K (Peak)
Mechanismus: Temporal metric transition
Status: ✅ Bereits in Spitzer/Herschel-Daten beobachtet!
```

---

## 14. Numerische Methoden & Toleranzen

### 14.1 Newton-Raphson (Mass Inversion)
```
Iterationen: max 200
Konvergenz: |f(M)| < 10⁻¹²⁰
Relative Toleranz: |ΔM/M| < 10⁻¹²⁰
Step Control: wenn |step| > |M|, step *= 0.5
```

### 14.2 Finite Differenzen
```
A'(r) ≈ (A(r+h) - A(r-h))/(2h)
A''(r) ≈ (A(r+h) - 2A(r) + A(r-h))/h²

h = max(10⁻⁶·r, 10⁻³)  (adaptive Schrittweite)
```

### 14.3 Bootstrap Confidence Intervals
```
n_boot = 2000  (Standarditerationen)
CI: [2.5%, 97.5%] Quantile
Verwendet für: Median-Schätzungen mit Unsicherheit
```

---

## 15. Validierungs-Metriken

### 15.1 Paired Test Statistics
```
Binomial-Test (exakt):
p-value = P(X ≥ k | n, p=0.5)

ESO-Daten:
- Wins: 46/47 (97.9%)
- p-value < 0.0001 (hoch signifikant!)
```

### 15.2 Regime-spezifische Performance
```
Photon Sphere (r = 2-3 r_s): 100% (11/11)
Strong Field (r = 3-10 r_s): 97.2% (35/36)
High Velocity (v > 0.05c): 94.4% (17/18)
Weak Field (r > 10 r_s): 37% (erwartet - GR bereits gut)
```

### 15.3 Mass Range Validation
```
Mass range tested: 10⁶ - 10⁹ M_☉ (3 Größenordnungen!)
SAME parameters work across all masses!
→ Beweist: φ-basierte Skalierung ist universal
```

---

## Zusammenfassung: Warum diese Formeln funktionieren

1. **φ ist fundamental** - Kein Fitting-Parameter, sondern geometrische Notwendigkeit
2. **Segment-Sättigung** - Ξ_max < 1 verhindert Singularitäten natürlich
3. **Universelle Skalierung** - Gleiche Formeln für alle Massenskalen
4. **PPN-Kompatibilität** - Matcht GR im Weak-Field (β=γ=1)
5. **Testbare Vorhersagen** - 44% NS-Differenz, 2% BH-Schatten, φ-skalierte GW
6. **Numerisch robust** - Konvergenz zu Maschinenpräzision

---

**© 2025 Carmen Wrede & Lino Casu**  
**Lizenz:** ANTI-CAPITALIST SOFTWARE LICENSE v1.4
