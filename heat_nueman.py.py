"""
heat_neumann_all_methods.py

Solve the 2D heat equation

    I_t = ΔI

with homogeneous Neumann (zero-flux) boundary conditions, using:

1. Finite differences (explicit time stepping)
2. Fourier / cosine transform (DCT) – spectral solution
3. Green's function (impulse response) + convolution

All functions accept anything array-like (lists, nested lists, NumPy arrays)
and internally convert to float NumPy arrays.
"""

import numpy as np
from scipy.fft import dctn, idctn   # cosine transforms (for Neumann BC)
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt


# ============================================================
# 1. Finite difference method: I_t = ΔI with Neumann boundary
# ============================================================

def laplacian_neumann(I):
    """
    Discrete 2D Laplacian with Neumann (zero-flux) boundary conditions.

    We implement Neumann BC (∂I/∂n = 0) by mirroring the image values at
    the boundary using 'reflect' padding, then applying the standard 5-point
    Laplacian stencil on the padded image.

    Parameters
    ----------
    I : array-like, shape (N, M)
        Current image / function values.

    Returns
    -------
    L : ndarray, shape (N, M)
        Discrete Laplacian ΔI with Neumann BC.
    """
    I = np.asarray(I, dtype=float)

    # Reflective padding adds a 1-pixel border that mirrors the image
    Ip = np.pad(I, pad_width=1, mode="reflect")

    # 5-point stencil: up + down + left + right - 4 * center
    L = (
        Ip[2:, 1:-1] + Ip[0:-2, 1:-1] +   # down + up
        Ip[1:-1, 2:] + Ip[1:-1, 0:-2] -   # right + left
        4.0 * Ip[1:-1, 1:-1]              # center
    )

    return L


def heat_fd_neumann(I0, dt=0.1, n_steps=10):
    """
    Explicit finite-difference solution of

        I_t = ΔI    with Neumann boundary conditions.

    Time-stepping scheme:
        I^{n+1} = I^n + dt * ΔI^n

    Parameters
    ----------
    I0      : array-like, shape (N, M)
        Initial image at time t = 0.
    dt      : float
        Time step size (for h = 1, a safe choice is dt <= 0.25).
    n_steps : int
        Number of time steps to perform.

    Returns
    -------
    I : ndarray, shape (N, M)
        Approximate solution at time t = n_steps * dt.
    """
    I = np.asarray(I0, dtype=float).copy()

    for _ in range(n_steps):
        I = I + dt * laplacian_neumann(I)

    return I


# ============================================================
# 2. Fourier (DCT) method: diagonalizing Neumann Laplacian
# ============================================================

def heat_fourier_neumann(I0, t):
    """
    Solve I_t = ΔI with homogeneous Neumann boundary conditions
    using the 2D discrete cosine transform (DCT).

    The Neumann Laplacian is diagonal in the cosine basis, with eigenvalues

        λ_k = -4 sin^2(π k / (2N)),  k = 0,...,N-1
        μ_l = -4 sin^2(π l / (2M)),  l = 0,...,M-1

    and Λ_{k,l} = λ_k + μ_l.

    Each cosine mode decays in time as e^{Λ_{k,l} t}.

    Parameters
    ----------
    I0 : array-like, shape (N, M)
        Initial image at t = 0.
    t  : float
        Time at which we want the solution.

    Returns
    -------
    I_t : ndarray, shape (N, M)
        Solution at time t.
    """
    I0 = np.asarray(I0, dtype=float)
    N, M = I0.shape

    # 2D DCT-II (orthonormal) of initial image
    I_hat0 = dctn(I0, type=2, norm="ortho")

    # Eigenvalues of 1D Neumann Laplacian in x and y
    k = np.arange(N)
    l = np.arange(M)
    lam_x = -4.0 * np.sin(np.pi * k / (2.0 * N))**2
    lam_y = -4.0 * np.sin(np.pi * l / (2.0 * M))**2

    # 2D grid of eigenvalues Λ_{k,l} = λ_k + μ_l
    Lam = lam_x[:, None] + lam_y[None, :]

    # Evolve each mode in time: I_hat_t = exp(Λ t) * I_hat0
    I_hat_t = np.exp(Lam * t) * I_hat0

    # Inverse DCT (type III) to return to spatial domain
    I_t = idctn(I_hat_t, type=3, norm="ortho")
    return I_t


# ============================================================
# 3. Green's function (impulse response) + convolution
# ============================================================

def green_function_neumann(shape, t):
    """
    Compute the discrete Green's function (impulse response) for the
    Neumann heat equation on a grid of given shape at time t, using
    the same cosine basis as in `heat_fourier_neumann`.

    We take a discrete delta (impulse) at the center, evolve it in time
    in the DCT domain, then invert back to get G(i, j, t).

    Parameters
    ----------
    shape : tuple (N, M)
        Size of the grid.
    t     : float
        Time.

    Returns
    -------
    G : ndarray, shape (N, M)
        Green's function G(i, j; t) corresponding to an impulse at the center.
    """
    N, M = shape

    # Discrete delta at the center
    delta = np.zeros((N, M), dtype=float)
    i0, j0 = N // 2, M // 2
    delta[i0, j0] = 1.0

    # DCT of delta
    delta_hat = dctn(delta, type=2, norm="ortho")

    # Same eigenvalues as in the Fourier Neumann solver
    k = np.arange(N)
    l = np.arange(M)
    lam_x = -4.0 * np.sin(np.pi * k / (2.0 * N))**2
    lam_y = -4.0 * np.sin(np.pi * l / (2.0 * M))**2
    Lam = lam_x[:, None] + lam_y[None, :]

    # Time evolution of the impulse
    G_hat = np.exp(Lam * t) * delta_hat

    # Inverse DCT gives Green's function in space
    G = idctn(G_hat, type=3, norm="ortho")
    return G


def heat_green_neumann(I0, t):
    """
    Approximate solution of I_t = ΔI with Neumann BC using Green's function.

    In continuous infinite space, the solution can be written as

        I(t) = G(t) * I0,

    where G is the heat kernel (Green's function). On a finite domain with
    Neumann boundary conditions, the operator is not strictly shift-invariant,
    but we can still illustrate the Green's-function idea by convolving an
    approximate Neumann heat kernel G(t) with I0.

    Parameters
    ----------
    I0 : array-like, shape (N, M)
        Initial image.
    t  : float
        Time.

    Returns
    -------
    I_t : ndarray, shape (N, M)
        Approximate solution at time t.
    """
    I0 = np.asarray(I0, dtype=float)
    N, M = I0.shape

    G = green_function_neumann((N, M), t)
    I_t = fftconvolve(I0, G, mode="same")

    return I_t