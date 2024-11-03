#functions final final fianl
import numpy as np
from sympy import symbols, diff, sqrt, pi, tan, cos, sin, evalf
from sympy.functions import asin as arcsin

c = 2.99e11  # Speed of light in mm/s
omega = symbols('omega', real=True, positive=True)

def create_matrix(A, B, C, D, E, F, G, H, I):  # create an ABCDEFGHI matrix
    return np.array([
        [A, B, 0, E],
        [C, D, 0, F],
        [G, H, 1, I],
        [0, 0, 0, 1]], dtype=complex)  # Use complex dtype to handle complex numbers

def lens_matrix(f):
    return create_matrix(1, 0, -1 / f, 1, 0, 0, 0, 0, 0)

def construct_refractive_index(B1, B2, B3, C1, C2, C3):
    lambda_ = 2 * pi * c / omega
    n_squared = 1 + (B1 * lambda_**2 / (lambda_**2 - C1)) + \
                    (B2 * lambda_**2 / (lambda_**2 - C2)) + \
                    (B3 * lambda_**2 / (lambda_**2 - C3))
    n = sqrt(n_squared)
    return n

def dispersive_slab_matrix(L, n_func, v):
    w_val = 2 * pi * v  # Angular frequency from a given frequency v
    n_at_w = n_func.subs(omega, w_val).evalf()
    d_n_d_w = n_func.diff(omega).subs(omega, w_val).evalf()
    vg = c / (w_val * d_n_d_w + n_at_w)
    d_vg_d_v = vg.diff(omega).subs(omega, w_val).evalf()
    z = -d_vg_d_v * (L / vg**2)
    return create_matrix(1, L / n_at_w, 0, 1, 0, 0, 0, 0, z)

def littrow_prism(ψ, n_func, v):
    w_val = 2 * pi * v
    n_at_w = n_func.subs(omega, w_val).evalf()
    m = sqrt(1 - (n_at_w ** 2) * (sin(ψ) ** 2)) / cos(ψ)
    dn_df = 2 * pi * n_func.diff(omega)
    dn_df_at_w = dn_df.subs(omega, w_val).evalf()
    λ_0 = c / v
    return create_matrix(m, 0, 0, 1 / m, 0, -dn_df_at_w * tan(ψ) / m, -dn_df_at_w * tan(ψ) / λ_0, 0, 0)

def prism(ψ, n_func, v):
    w_val = 2 * pi * v
    n_at_w = n_func.subs(omega, w_val).evalf()
    m = sqrt(1 - (n_at_w ** 2) * (sin(ψ) ** 2)) / cos(ψ)
    dn_df = 2 * pi * n_func.diff(omega)
    dn_df_at_w = dn_df.subs(omega, w_val).evalf()
    λ_0 = c / v
    return create_matrix(m, 0, 0, 1 / m, 0, -dn_df_at_w * tan(ψ), -dn_df_at_w * m * tan(ψ) / λ_0, 0, 0)

def grating(ψ, Λ, v):
    λ = c / v
    φ = (pi / 2) - arcsin(sin(pi / 2 - ψ) - λ / Λ)  # First-order diffraction only
    return create_matrix(-(sin(φ) / sin(ψ)), 0, 0, -(sin(ψ) / sin(φ)), 0,
                         (cos(φ) - cos(ψ)) / v * sin(φ), (cos(ψ) - cos(φ)) / c * sin(ψ), 0, 0)

def general_prism(B1, B2, B3, C1, C2, C3, α, θ, d, v):
    n_func = construct_refractive_index(B1, B2, B3, C1, C2, C3)
    w_val = 2 * pi * v
    n_at_w = n_func.subs(omega, w_val).evalf()
    dn_df = 2 * pi * n_func.diff(omega)
    dn_df_at_w = dn_df.subs(omega, w_val).evalf()
    vg = c / (w_val * dn_df / (2 * pi) + n_func)
    vg_at_w = vg.subs(omega, w_val).evalf()
    d_vg_d_v = 2 * pi * vg.diff(omega)
    d_vg_d_v_at_w = d_vg_d_v.subs(omega, w_val).evalf()
    ψ = arcsin(sin(θ) / n_at_w)
    φ = α - ψ
    λ_0 = c / v
    L = d * sin(α) / cos(ψ - α)
    m_φ = sqrt(1 - (n_at_w * sin(φ)) ** 2) / cos(φ)
    m_ψ = cos(ψ) / sqrt(1 - (n_at_w * sin(ψ)) ** 2)
    z = -d_vg_d_v_at_w * (L / vg_at_w ** 2)
    return create_matrix(m_φ * m_ψ, L * m_φ / n_at_w * m_ψ, 0, 1 / m_φ * m_ψ,
                         -dn_df_at_w * L * m_φ * tan(ψ) / n_at_w, -dn_df_at_w * (tan(φ) + tan(ψ)) / m_φ,
                         -dn_df_at_w * m_ψ * (tan(φ) + tan(ψ)) / λ_0,
                         -dn_df_at_w * L * tan(ψ) / (m_ψ * n_at_w * λ_0),
                         ((dn_df_at_w ** 2) * L * tan(ψ) * tan(φ) / (n_at_w * λ_0)) + z)

def free_space(L, v):
    return create_matrix(1, L, 0, 1, 0, 0, 0, 0, 0)
