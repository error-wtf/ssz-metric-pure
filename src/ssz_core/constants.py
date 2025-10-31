"""
Physical Constants for SSZ Metric

All values in SI units.

© 2025 Carmen Wrede & Lino Casu
"""

import math

# Golden Ratio (φ = (1 + √5) / 2)
PHI = (1.0 + math.sqrt(5.0)) / 2.0  # ≈ 1.618033988749

# Speed of light (m/s)
C = 299792458.0

# Gravitational constant (m³ kg⁻¹ s⁻²)
G = 6.67430e-11

# Solar mass (kg)
M_SUN = 1.98847e30

# Solar radius (m)
R_SUN = 6.96340e8

# Planck constant (J·s)
H_PLANCK = 6.62607015e-34

# Boltzmann constant (J/K)
K_BOLTZMANN = 1.380649e-23

# Reduced Planck constant (ℏ)
HBAR = H_PLANCK / (2.0 * math.pi)
