
"""
div_grad_pde_fd.py

Finite-difference solver for PDEs of the form

    I_t = div( grad(Î) )

with homogeneous Neumann (zero-flux) boundary conditions.

- I(x, y, t)  : evolving image
- Î(x, y, t)  : some (possibly nonlinear) transform of I, e.g. Î = I

By default, Î = I, so the PDE reduces to the standard heat equation:

    I_t = ΔI.

You can plug any custom "hat_operator" that maps I ↦ Î.
"""

import numpy as np
import matplotlib.pyplot as plt


def grad_neumann(u):
    """
    Compute gradient of u with Neumann (reflective) boundary conditions.

    Parameters
    ----------
    u : array-like, shape (H, W)
        Scalar field (image).

    Returns
    -------
    ux, uy : ndarrays, shape (H, W)
        Approximate partial derivatives du/dx and du/dy.
    """
    u = np.asarray(u, dtype=float)

    # Add a 1-pixel reflective border so that normal derivatives are ~0
    up = np.pad(u, pad_width=1, mode="reflect")

    # Central differences on the padded array
    ux = 0.5 * (up[2:, 1:-1] - up[0:-2, 1:-1])  # d/dx
    uy = 0.5 * (up[1:-1, 2:] - up[1:-1, 0:-2])  # d/dy

    return ux, uy


def div_neumann(px, py):
    """
    Compute divergence of a vector field (px, py) with reflective boundaries.

    Parameters
    ----------
    px, py : array-like, shape (H, W)
        Components of the vector field.

    Returns
    -------
    div : ndarray, shape (H, W)
        Approximation of ∂px/∂x + ∂py/∂y.
    """
    px = np.asarray(px, dtype=float)
    py = np.asarray(py, dtype=float)

    # Reflective padding for each component
    pxp = np.pad(px, pad_width=1, mode="reflect")
    pyp = np.pad(py, pad_width=1, mode="reflect")

    # Central differences
    div_x = 0.5 * (pxp[2:, 1:-1] - pxp[0:-2, 1:-1])
    div_y = 0.5 * (pyp[1:-1, 2:] - pyp[1:-1, 0:-2])

    return div_x + div_y


def evolve_div_grad_hat(I0, dt=0.1, n_steps=10, hat_operator=None):
    """
    Evolve the PDE

        I_t = div( grad(Î) )

    using explicit finite differences with Neumann BC.

    Parameters
    ----------
    I0 : array-like, shape (H, W)
        Initial image at time t = 0.
    dt : float
        Time step size.
    n_steps : int
        Number of time steps to perform.
    hat_operator : callable or None
        A function hat_operator(I) -> Î.
        If None, the identity is used: Î = I (standard heat equation).

    Returns
    -------
    I : ndarray, shape (H, W)
        Approximate solution at time t = n_steps * dt.
    """
    I = np.asarray(I0, dtype=float).copy()

    if hat_operator is None:
        # Default: Î = I  (heat equation)
        def hat_operator(U):
            return U

    for _ in range(n_steps):
        I_hat = hat_operator(I)        # compute Î from current I
        Ix, Iy = grad_neumann(I_hat)   # gradient of Î
        div_term = div_neumann(Ix, Iy) # divergence of that gradient
        I = I + dt * div_term          # explicit Euler update

    return I


def _demo():
    """
    Small demo: start from a binary square and smooth it with I_t = ΔI.

    This corresponds to evolve_div_grad_hat with the default hat_operator,
    i.e. Î = I.
    """
    # Simple test image: white square on black background
    H, W = 64, 64
    I0 = np.zeros((H, W), dtype=float)
    I0[20:44, 20:44] = 1.0

    # PDE parameters
    dt = 0.1
    n_steps = 20

    # Evolve with I_t = div(grad(I)) = ΔI
    I_smooth = evolve_div_grad_hat(I0, dt=dt, n_steps=n_steps)

    # Plot before and after
    fig, axs = plt.subplots(1, 2, figsize=(6, 3))
    axs[0].imshow(I0, cmap="gray")
    axs[0].set_title("Initial")
    axs[0].axis("off")

    axs[1].imshow(I_smooth, cmap="gray")
    axs[1].set_title(f"After {n_steps} steps")
    axs[1].axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    _demo()
