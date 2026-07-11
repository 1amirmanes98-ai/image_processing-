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

## Notes formatter (`/format-notes`)

A Claude Code skill that turns scans of handwritten Hebrew lecture notes into a
styled typed **PDF + self-contained HTML** — RTL, David Libre, KaTeX math,
colour-coded callout boxes, a topic map, guided exercises, and a formula sheet.

Pipeline: **scan → rasterize → Claude transcribes → HTML → Chromium print-to-PDF.**

Lives in `.claude/skills/format-notes/` (the skill) and `notes-formatter/`
(templates, scripts, vendored KaTeX + fonts). Generated summaries go to
`outputs/`, which is gitignored — they are personal course content, delivered in
chat and never committed. See [`notes-formatter/README.md`](notes-formatter/README.md)
for setup and usage, and [`notes-formatter/DESIGN.md`](notes-formatter/DESIGN.md)
for the authoring contract.

---

_The exam-prep tutors that previously lived here (Foundations of Deep Learning,
Reinforcement Learning) have moved to their canonical home:
[`1amirmanes98-ai/exam-prep-agent`](https://github.com/1amirmanes98-ai/exam-prep-agent)._
