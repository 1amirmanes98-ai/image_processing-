# image_processing-

Numerical / image-processing coursework scripts — classical image restoration and
PDE-based image evolution in Python (NumPy / SciPy / Matplotlib).

## Scripts

| File | What it does |
|---|---|
| `algo_pictue.py` | Frequency-domain **Wiener filter** for image deblurring/denoising (FFT-based deconvolution given a PSF). |
| `div_grad_pde_fd.py` | Finite-difference solver for **`I_t = div(grad(Î))`** image-evolution PDEs (e.g. anisotropic diffusion) with homogeneous Neumann (zero-flux) boundaries. |
| `heat_nueman.py.py` | 2D **heat equation** `I_t = ΔI` (Neumann BC) solved three ways: explicit finite differences, DCT/spectral, and Green's-function convolution. |
| `sfm.py` | Numerical interpolation / basis-function fitting experiments. |

## Running

Each script is standalone:

```bash
pip install numpy scipy matplotlib
python3 div_grad_pde_fd.py
```

---

_The exam-prep tutors that previously lived here (Foundations of Deep Learning,
Reinforcement Learning) have moved to their canonical home:
[`1amirmanes98-ai/exam-prep-agent`](https://github.com/1amirmanes98-ai/exam-prep-agent)._
