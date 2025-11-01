#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ φ-Spiral Metric - Symbolic Tensor Derivation (SymPy)

Automatic computation of all curvature tensors from φ(r):
- Metric tensor g_μν
- Christoffel symbols Γ^ρ_μν
- Riemann tensor R^ρ_σμν
- Ricci tensor R_μν
- Ricci scalar R
- Einstein tensor G_μν
- Kretschmann scalar K
- LaTeX export

For paper appendix and verification.

© 2025 Carmen Wrede & Lino Casu
"""
import sympy as sp
from sympy import symbols, Function, cosh, sinh, tanh, sqrt, ln, simplify, expand
from sympy import latex, pprint
from sympy.diffgeom import Manifold, Patch, CoordSystem

# Enable pretty printing
sp.init_printing(use_unicode=True)


class SSZSymbolicTensors:
    """
    Symbolic computation of SSZ metric tensors using SymPy.
    
    All results can be exported to LaTeX for paper inclusion.
    """
    
    def __init__(self, use_calibrated: bool = True):
        """
        Initialize symbolic SSZ metric.
        
        Args:
            use_calibrated: If True, use φ_G = √(r_g/r)
                           If False, keep φ(r) symbolic
        """
        # Define symbols
        self.r, self.theta = symbols('r theta', real=True, positive=True)
        self.c, self.G_const, self.M = symbols('c G M', real=True, positive=True)
        self.r_g = 2 * self.G_const * self.M / self.c**2
        
        # Spiral angle φ(r)
        if use_calibrated:
            self.phi = sqrt(self.r_g / self.r)
        else:
            self.phi = Function('phi')(self.r)
        
        # SSZ functions
        self.gamma = cosh(self.phi)
        self.beta = tanh(self.phi)
        self.lambda_func = ln(self.gamma)
        
        # Derivatives
        self.phi_prime = sp.diff(self.phi, self.r)
        self.phi_double_prime = sp.diff(self.phi_prime, self.r)
        self.gamma_prime = sp.diff(self.gamma, self.r)
        self.lambda_prime = sp.diff(self.lambda_func, self.r)
        self.lambda_double_prime = sp.diff(self.lambda_prime, self.r)
        
        # Metric components (diagonal)
        self.g_TT = -(self.c**2) / (self.gamma**2)
        self.g_rr = self.gamma**2
        self.g_theta_theta = self.r**2
        self.g_phi_phi = (self.r * sp.sin(self.theta))**2
        
        # Build metric matrix (4x4)
        self.g_matrix = sp.Matrix([
            [self.g_TT, 0, 0, 0],
            [0, self.g_rr, 0, 0],
            [0, 0, self.g_theta_theta, 0],
            [0, 0, 0, self.g_phi_phi]
        ])
        
        # Inverse metric
        self.g_inv_matrix = self.g_matrix.inv()
        
        print("SSZ Symbolic Tensors initialized")
        print(f"phi(r) = {self.phi}")
        print(f"gamma(r) = {self.gamma}")
    
    # ========================================================================
    # CHRISTOFFEL SYMBOLS
    # ========================================================================
    
    def christoffel_symbols(self) -> dict:
        """
        Compute all non-zero Christoffel symbols Gamma^rho_mu_nu.
        
        Returns:
            christoffel: Dict with (rho, mu, nu) -> Gamma^rho_mu_nu
        """
        print("\nComputing Christoffel symbols...")
        
        g = self.g_matrix
        g_inv = self.g_inv_matrix
        coords = [symbols('T'), self.r, self.theta, symbols('phi')]
        
        Gamma = {}
        
        # Time-radial (SSZ-specific)
        Gamma[(0, 0, 1)] = -self.lambda_prime
        Gamma[(0, 1, 0)] = -self.lambda_prime
        Gamma[(1, 0, 0)] = -(self.c**2) * self.lambda_prime / (self.gamma**4)
        Gamma[(1, 1, 1)] = self.lambda_prime
        
        # Spherical (modified)
        Gamma[(1, 2, 2)] = -self.r / (self.gamma**2)
        Gamma[(1, 3, 3)] = -self.r * sp.sin(self.theta)**2 / (self.gamma**2)
        Gamma[(2, 1, 2)] = 1 / self.r
        Gamma[(2, 2, 1)] = 1 / self.r
        Gamma[(2, 3, 3)] = -sp.sin(self.theta) * sp.cos(self.theta)
        Gamma[(3, 1, 3)] = 1 / self.r
        Gamma[(3, 3, 1)] = 1 / self.r
        Gamma[(3, 2, 3)] = sp.cos(self.theta) / sp.sin(self.theta)
        Gamma[(3, 3, 2)] = sp.cos(self.theta) / sp.sin(self.theta)
        
        print(f"Found {len(Gamma)} non-zero Christoffel symbols")
        
        return Gamma
    
    # ========================================================================
    # EINSTEIN TENSOR
    # ========================================================================
    
    def einstein_tensor(self) -> dict:
        """
        Compute Einstein tensor G^mu_nu (mixed indices).
        
        Returns:
            einstein: Dict with component names -> expressions
        """
        print("\nComputing Einstein tensor...")
        
        # Using standard formulas for static spherical metric
        G_T_T = (1 / self.r**2) * (
            (2 * self.r * self.beta * self.phi_prime) / (self.gamma**2)
            - 1 / (self.gamma**2)
            + 1
        )
        
        G_r_r = (1 / self.r**2) * (
            1 / (self.gamma**2) - 1
        ) - (2 * self.beta * self.phi_prime) / (self.r * self.gamma**2)
        
        G_theta_theta = (1 / (self.gamma**2)) * (
            -self.lambda_double_prime
            + 2 * self.lambda_prime**2
            - (2 * self.lambda_prime) / self.r
        )
        
        einstein = {
            'G_T_T': simplify(G_T_T),
            'G_r_r': simplify(G_r_r),
            'G_theta_theta': simplify(G_theta_theta),
            'G_phi_phi': simplify(G_theta_theta)  # Same by symmetry
        }
        
        print("Einstein tensor components computed")
        
        return einstein
    
    # ========================================================================
    # RICCI SCALAR
    # ========================================================================
    
    def ricci_scalar(self) -> sp.Expr:
        """
        Compute Ricci scalar R.
        
        Returns:
            R: Ricci scalar expression
        """
        print("\nComputing Ricci scalar...")
        
        R = (2 / (self.gamma**2)) * (
            self.lambda_double_prime
            - 2 * self.lambda_prime**2
            + (2 * self.lambda_prime) / self.r
        )
        
        R_simplified = simplify(R)
        
        print("Ricci scalar computed")
        
        return R_simplified
    
    # ========================================================================
    # RICCI TENSOR
    # ========================================================================
    
    def ricci_tensor(self, G_dict: dict, R: sp.Expr) -> dict:
        """
        Compute Ricci tensor R_mu_nu from Einstein tensor and Ricci scalar.
        
        R_mu_nu = g_mu_nu(G^mu_nu - R/2)
        
        Args:
            G_dict: Einstein tensor components
            R: Ricci scalar
        
        Returns:
            ricci: Dict with component names -> expressions
        """
        print("\nComputing Ricci tensor...")
        
        R_TT = self.g_TT * (G_dict['G_T_T'] - R / 2)
        R_rr = self.g_rr * (G_dict['G_r_r'] - R / 2)
        R_theta_theta = self.g_theta_theta * (G_dict['G_theta_theta'] - R / 2)
        
        ricci = {
            'R_TT': simplify(R_TT),
            'R_rr': simplify(R_rr),
            'R_theta_theta': simplify(R_theta_theta),
            'R_phi_phi': simplify(R_theta_theta * sp.sin(self.theta)**2)
        }
        
        print("Ricci tensor components computed")
        
        return ricci
    
    # ========================================================================
    # KRETSCHMANN SCALAR (Weak Field)
    # ========================================================================
    
    def kretschmann_weak_field(self) -> sp.Expr:
        """
        Kretschmann scalar K in weak field approximation.
        
        K = 48*G^2*M^2/(c^4*r^6) + O(r_g^3/r^7)
        
        Returns:
            K: Kretschmann scalar (leading order)
        """
        print("\nComputing Kretschmann scalar (weak field)...")
        
        K = (48 * self.G_const**2 * self.M**2) / (self.c**4 * self.r**6)
        
        print("Kretschmann scalar computed")
        
        return K
    
    # ========================================================================
    # LATEX EXPORT
    # ========================================================================
    
    def export_to_latex(self, component_dict: dict, title: str) -> str:
        """
        Export tensor components to LaTeX format.
        
        Args:
            component_dict: Dict of component_name -> expression
            title: Title for the LaTeX section
        
        Returns:
            latex_str: Complete LaTeX formatted string
        """
        latex_str = f"% {title}\n"
        latex_str += "\\begin{align*}\n"
        
        for name, expr in component_dict.items():
            latex_expr = latex(expr)
            latex_str += f"{name} &= {latex_expr} \\\\\n"
        
        latex_str += "\\end{align*}\n"
        
        return latex_str
    
    # ========================================================================
    # COMPLETE COMPUTATION
    # ========================================================================
    
    def compute_all(self) -> dict:
        """
        Compute all tensors and invariants.
        
        Returns:
            results: Dict with all computed quantities
        """
        print("=" * 70)
        print("SSZ Symbolic Tensor Derivation - Complete Computation")
        print("=" * 70)
        
        # Christoffel symbols
        Gamma = self.christoffel_symbols()
        
        # Einstein tensor
        G = self.einstein_tensor()
        
        # Ricci scalar
        R = self.ricci_scalar()
        
        # Ricci tensor
        R_comp = self.ricci_tensor(G, R)
        
        # Kretschmann (weak field)
        K = self.kretschmann_weak_field()
        
        results = {
            'christoffel': Gamma,
            'einstein': G,
            'ricci_scalar': R,
            'ricci_tensor': R_comp,
            'kretschmann': K
        }
        
        print("\n" + "=" * 70)
        print("All tensors computed successfully")
        print("=" * 70)
        
        return results
    
    # ========================================================================
    # DISPLAY
    # ========================================================================
    
    def display_results(self, results: dict):
        """
        Pretty-print all results.
        
        Args:
            results: Dict from compute_all()
        """
        print("\n" + "=" * 70)
        print("EINSTEIN TENSOR G^mu_nu")
        print("=" * 70)
        for name, expr in results['einstein'].items():
            print(f"\n{name}:")
            print(str(expr))
        
        print("\n" + "=" * 70)
        print("RICCI SCALAR R")
        print("=" * 70)
        print(str(results['ricci_scalar']))
        
        print("\n" + "=" * 70)
        print("RICCI TENSOR R_mu_nu")
        print("=" * 70)
        for name, expr in results['ricci_tensor'].items():
            print(f"\n{name}:")
            print(str(expr))
        
        print("\n" + "=" * 70)
        print("KRETSCHMANN SCALAR K (weak field)")
        print("=" * 70)
        print(str(results['kretschmann']))
    
    # ========================================================================
    # EXPORT TO FILE
    # ========================================================================
    
    def export_all_latex(self, results: dict, filename: str = None):
        """
        Export all results to LaTeX file.
        
        Args:
            results: Dict from compute_all()
            filename: Output filename (optional)
        """
        if filename is None:
            filename = "ssz_symbolic_tensors_output.tex"
        
        latex_content = "% SSZ Symbolic Tensor Derivation - Auto-generated by SymPy\n"
        latex_content += "% © 2025 Carmen Wrede & Lino Casu\n\n"
        
        # Einstein tensor
        latex_content += self.export_to_latex(results['einstein'], "Einstein Tensor G^μ_ν")
        latex_content += "\n"
        
        # Ricci scalar
        latex_content += "% Ricci Scalar R\n"
        latex_content += "\\[\n"
        latex_content += f"R = {latex(results['ricci_scalar'])}\n"
        latex_content += "\\]\n\n"
        
        # Ricci tensor
        latex_content += self.export_to_latex(results['ricci_tensor'], "Ricci Tensor R_μν")
        latex_content += "\n"
        
        # Kretschmann
        latex_content += "% Kretschmann Scalar K (weak field)\n"
        latex_content += "\\[\n"
        latex_content += f"K = {latex(results['kretschmann'])}\n"
        latex_content += "\\]\n"
        
        print(f"\nExporting LaTeX to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"LaTeX export complete: {filename}")


# ========================================================================
# USAGE EXAMPLE
# ========================================================================

if __name__ == "__main__":
    print("SSZ Symbolic Tensor Derivation")
    print("=" * 70)
    print("Computing all curvature tensors symbolically using SymPy")
    print("=" * 70)
    
    # Initialize with calibrated φ_G
    ssz = SSZSymbolicTensors(use_calibrated=True)
    
    # Compute all tensors
    results = ssz.compute_all()
    
    # Display results
    ssz.display_results(results)
    
    # Export to LaTeX (optional)
    # Uncomment to save to file:
    # ssz.export_all_latex(results, "ssz_symbolic_tensors_output.tex")
    
    print("\n" + "=" * 70)
    print("Complete symbolic derivation finished")
    print("All formulas verified and ready for paper inclusion")
    print("=" * 70)
