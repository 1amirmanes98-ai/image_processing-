# Repo guide

Numerical / image-processing coursework scripts (Python, NumPy/SciPy/Matplotlib):
classical image restoration and PDE-based image evolution.

- `algo_pictue.py` — frequency-domain Wiener filter (FFT deconvolution).
- `div_grad_pde_fd.py` — finite-difference `I_t = div(grad(Î))` solver (Neumann BC).
- `heat_nueman.py.py` — 2D heat equation (finite differences / DCT / Green's function).
- `sfm.py` — numerical interpolation / basis-function fitting.

Work on these normally. Match each script's existing style (NumPy vectorization,
the finite-difference/spectral conventions already in the file).

**Note:** the exam-prep tutors (FODL, Reinforcement Learning) that used to live here have
moved to their canonical home, `1amirmanes98-ai/exam-prep-agent`. New exam-prep agents
belong in **that** repo, not here.
