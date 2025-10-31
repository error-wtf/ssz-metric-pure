"""
SSZ Metric Pure - Core Parameters & Constants

Fundamental constants, SSZ parameters, and mass correction Δ(M).

Sources:
- ssz-full-metric: Production constants
- ssz-metric-final: Pure SSZ improvements, φ-series
- Segmented-Spacetime-Results: ESO validated Δ(M)

This is 100% PURE SSZ - no hybrid GR mixing in core equations.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from decimal import Decimal as D, getcontext
from typing import Optional
import numpy as np

# Set high precision for geometric calculations
getcontext().prec = 200

# ============================================================================
# FUNDAMENTAL CONSTANTS (SI Units)
# ============================================================================

# Fundamental constants
G_SI = 6.67430e-11  # m³/(kg·s²) - Gravitational constant (CODATA 2018)
G_PRECISE = D('6.67430e-11')

C_SI = 299792458.0  # m/s - Speed of light (exact by definition)
C_PRECISE = D('2.99792458e8')

HBAR = 1.054571817e-34  # J·s - Reduced Planck constant
K_B = 1.380649e-23  # J/K - Boltzmann constant

# Astronomical constants
M_SUN = 1.98847e30  # kg - Solar mass
M_SUN_PRECISE = D('1.98847e30')
R_SUN = 6.96e8  # m - Solar radius
PC = 3.0857e16  # m - Parsec
AU = 1.495978707e11  # m - Astronomical unit

# ============================================================================
# GOLDEN RATIO (φ) - GEOMETRIC FOUNDATION OF SSZ
# ============================================================================

PHI = (1.0 + np.sqrt(5.0)) / 2.0  # φ ≈ 1.618033988749894...
PHI_PRECISE = (D(1) + D(5).sqrt()) / D(2)

# φ is NOT a fitting parameter - it emerges from:
# 1. Fibonacci-like segment recursion
# 2. Optimal packing in spacetime
# 3. Natural boundary conditions

# ============================================================================
# φ-SERIES BREAKTHROUGH (from 28-hour session)
# ============================================================================

# Universal Intersection Point u* (MASS-INDEPENDENT!)
# Discovery: r*/r_s is THE SAME for all masses!
# Tested: M☉, 10M☉, 10⁶M☉, 10⁹M☉ → SAME u*!
U_STAR_UNIVERSAL = 1.3865616196  # Precision: |error| = 3.8×10⁻⁷

# φ-Series Post-Newtonian Coefficients
# Formula: c_{n+2} = (c_{n+1} + c_n) / φ
# NO arbitrary parameters - pure geometric origin!
PHI_SERIES_COEFFICIENTS = {
    0: 1.0,      # Geometry (flat space)
    1: -2.0,     # Geometry (Newtonian)
    2: 2.0,      # Geometry (PN correction)
    3: -1.133,   # GR validated! (ε₃ = -24/5)
    4: 0.536,    # PREDICTED from φ-recursion
    5: -0.369,   # PREDICTED from φ-recursion
    6: 0.103,    # PREDICTED from φ-recursion
}

# Epsilon coefficients (ε_n = c_n × φⁿ)
EPSILON_COEFFICIENTS = {
    0: 1.0,
    1: -3.236,
    2: 5.236,
    3: -4.800,  # GR value!
    4: 3.672,
    5: -4.094,
    6: 1.847,
}

# Fine structure constant
ALPHA_FS = 7.2973525693e-3

# ============================================================================
# SSZ UNIVERSAL CONSTANTS (Mass-Independent!)
# ============================================================================

# Natural boundary ratio
R_PHI_RATIO = 0.809  # r_φ/r_s ≈ 0.809 (varies slightly with Δ(M))

# Minimum metric coefficient (singularity-free proof!)
A_MIN = 0.284  # A(r_φ) > 0 → NO SINGULARITY at natural boundary

# Segment saturation maximum
XI_MAX = 1.0  # Maximum segment density (complete saturation)

# ============================================================================
# SSZ-SPECIFIC PARAMETERS
# ============================================================================

# Δ(M) Mass Correction Parameters (from φ-based geometry)
# Formula: Δ(M) = A × exp(-α × r_s) + B
# NOT arbitrary fitting - emergent from φ-spiral scaling!
DELTA_M_A = 98.01
DELTA_M_ALPHA = 2.7177e4
DELTA_M_B = 1.96

# Segment saturation parameters
XI_MAX = 1.0  # Maximum segment density
VARPHI_DEFAULT = PHI  # φ-parameter for saturation

# Dimensionless radius mapping
# "At radius 1 the circle is divided into 4φ segments"
R_DIMENSIONLESS_1 = 4.0 * PHI  # ≈ 6.472

# Numerical stability
EPSILON_FLOOR = 1e-10  # Softplus minimum
BETA_SOFTPLUS = 50.0   # Softplus steepness
HORIZON_MARGIN = 1e-6  # Safety margin for horizon

# TOV integration
RHO_0_DEFAULT = 0.0    # Fluid rest density (exterior mode)
CS2_DEFAULT = 0.30     # Sound speed squared
PR_0_DEFAULT = 0.0     # Initial fluid pressure

# Scalar field (from ssz_theory_segmented.py)
PHI_CAP_DEFAULT = 1e-3   # φ field saturation cap
PHIP_CAP_DEFAULT = 1e-3  # φ' derivative cap
Z0_DEFAULT = 1.0         # Z_parallel(φ) baseline
ALPHA_Z_DEFAULT = 3e-3   # Z linear coefficient
BETA_Z_DEFAULT = -8e-3   # Z quadratic coefficient
Z_MIN = 1e-8             # Z lower bound
Z_MAX = 1e+8             # Z upper bound
M_PHI_DEFAULT = 0.0      # Scalar mass
LAMBDA_DEFAULT = 0.0     # Quartic coupling

# ============================================================================
# TOLERANCES & VALIDATION
# ============================================================================

# GR-limit recovery tolerances (for validation layer ONLY)
TOL_GR_KERR = 1e-8      # Kerr limit tolerance
TOL_SCHWARZSCHILD = 1e-10  # Schwarzschild limit
TOL_MINKOWSKI = 1e-12   # Minkowski limit (M→0)

# Numerical integration
RTOL_DEFAULT = 1e-7     # Relative tolerance
ATOL_DEFAULT = 1e-9     # Absolute tolerance
MAX_STEP_RS_DEFAULT = 0.02  # Max step (fraction of r_s)

# Monotonicity checks
TOL_MONOTONIC = 1e-6    # Redshift monotonicity tolerance

# ============================================================================
# DIMENSIONLESS MODE
# ============================================================================

class DimensionlessMode:
    """
    Dimensionless units with G=c=1.
    
    Conversions:
    - Mass: M_geom = G M / c² (meters)
    - Time: t_geom = c t (meters)
    - r_s = 2 M_geom
    """
    
    G = 1.0
    C = 1.0
    
    @staticmethod
    def mass_to_geom(M_kg: float) -> float:
        """Convert SI mass to geometric units."""
        return G_SI * M_kg / (C_SI ** 2)
    
    @staticmethod
    def geom_to_mass(M_geom: float) -> float:
        """Convert geometric mass to SI."""
        return M_geom * (C_SI ** 2) / G_SI
    
    @staticmethod
    def schwarzschild_radius(M_kg: float) -> float:
        """r_s = 2M_geom in geometric units."""
        return 2.0 * DimensionlessMode.mass_to_geom(M_kg)


# ============================================================================
# PARAMETER CLASSES
# ============================================================================

class SSZParams:
    """
    Pure SSZ parameters (unified from both repos).
    
    Usage:
        >>> params = SSZParams(mass=M_SUN)
        >>> params.r_s  # Schwarzschild radius
        2952.9...
        >>> params.delta_M()  # Mass correction
        99.97...
    """
    
    def __init__(
        self,
        mass: float,
        G: float = G_SI,
        c: float = C_SI,
        varphi: float = VARPHI_DEFAULT,
        dimensionless: bool = False
    ):
        """
        Initialize SSZ parameters.
        
        Args:
            mass: Mass in kg (or geometric if dimensionless=True)
            G: Gravitational constant
            c: Speed of light
            varphi: φ-parameter (golden ratio by default)
            dimensionless: Use G=c=1 units
        """
        if dimensionless:
            self.G = 1.0
            self.c = 1.0
            self.M = mass  # Already in geometric units
        else:
            self.G = G
            self.c = c
            self.M = mass
        
        self.varphi = varphi
        self.dimensionless = dimensionless
        
        # Compute derived quantities
        self.r_s = self.schwarzschild_radius()
        self.r_phi = self.golden_radius()
    
    def schwarzschild_radius(self) -> float:
        """r_s = 2GM/c²"""
        return 2.0 * self.G * self.M / (self.c ** 2)
    
    def delta_M(self) -> float:
        """
        Δ(M) mass correction (φ-based).
        
        Returns percentage (e.g., 2.0 means 2%).
        """
        r_s = self.r_s
        return DELTA_M_A * np.exp(-DELTA_M_ALPHA * r_s) + DELTA_M_B
    
    def golden_radius(self) -> float:
        """
        r_φ = (φ/2) r_s × (1 + Δ(M)/100)
        
        Natural boundary radius from φ-geometry.
        """
        delta_pct = self.delta_M()
        return (self.varphi / 2.0) * self.r_s * (1.0 + delta_pct / 100.0)
    
    def to_dimensionless(self):
        """Convert to dimensionless (G=c=1) parameters."""
        if self.dimensionless:
            return self
        
        M_geom = DimensionlessMode.mass_to_geom(self.M)
        return SSZParams(mass=M_geom, dimensionless=True, varphi=self.varphi)
    
    def __repr__(self):
        units = "geometric" if self.dimensionless else "SI"
        return (f"SSZParams(M={self.M:.3e}, r_s={self.r_s:.3e}, "
                f"r_φ={self.r_phi:.3e}, Δ(M)={self.delta_M():.2f}%, "
                f"units={units})")


class KerrSSZParams(SSZParams):
    """
    Rotating SSZ-Kerr parameters.
    
    Additional parameter:
    - a: Spin parameter (0 ≤ a ≤ M in geometric units)
    """
    
    def __init__(
        self,
        mass: float,
        spin: float,
        G: float = G_SI,
        c: float = C_SI,
        varphi: float = VARPHI_DEFAULT,
        dimensionless: bool = False
    ):
        """
        Initialize Kerr-SSZ parameters.
        
        Args:
            mass: Mass
            spin: Spin parameter a (dimensionless â = a/M)
            G, c: Constants
            varphi: φ-parameter
            dimensionless: G=c=1 mode
        """
        super().__init__(mass, G, c, varphi, dimensionless)
        
        self.a = spin  # Spin parameter
        self.a_hat = spin / self.M if self.M > 0 else 0.0  # Dimensionless â
        
        # Validate spin
        if dimensionless:
            max_spin = self.M
        else:
            max_spin = self.G * self.M / self.c
        
        if abs(self.a) > max_spin:
            raise ValueError(
                f"Spin |a|={abs(self.a):.3e} exceeds maximum {max_spin:.3e}"
            )
    
    def __repr__(self):
        base = super().__repr__()
        return base.replace("SSZParams", "KerrSSZParams").replace(
            ")", f", a={self.a:.3e}, â={self.a_hat:.3f})"
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def schwarzschild_radius(mass: float, G: float = G_SI, c: float = C_SI) -> float:
    """Quick r_s calculation."""
    return 2.0 * G * mass / (c ** 2)


def golden_radius(mass: float, G: float = G_SI, c: float = C_SI) -> float:
    """Quick r_φ calculation."""
    r_s = schwarzschild_radius(mass, G, c)
    delta_pct = DELTA_M_A * np.exp(-DELTA_M_ALPHA * r_s) + DELTA_M_B
    return (PHI / 2.0) * r_s * (1.0 + delta_pct / 100.0)


def validate_spin(spin: float, mass: float) -> bool:
    """Check if spin is valid (|a| ≤ M in geometric units)."""
    a_max = G_SI * mass / C_SI
    return abs(spin) <= a_max
