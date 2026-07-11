# Repo guide

Numerical / image-processing coursework scripts (Python, NumPy/SciPy/Matplotlib):
classical image restoration and PDE-based image evolution.

- `algo_pictue.py` — frequency-domain Wiener filter (FFT deconvolution).
- `div_grad_pde_fd.py` — finite-difference `I_t = div(grad(Î))` solver (Neumann BC).
- `heat_nueman.py.py` — 2D heat equation (finite differences / DCT / Green's function).
- `sfm.py` — numerical interpolation / basis-function fitting.

Work on these normally. Match each script's existing style (NumPy vectorization,
the finite-difference/spectral conventions already in the file).

## Notes formatter (`/format-notes`)

A Claude Code skill that turns scans of handwritten Hebrew lecture notes into a
styled typed **PDF + self-contained HTML** (RTL, David Libre, KaTeX math,
colour-coded boxes, topic map, guided exercises, formula sheet).

- Lives in `.claude/skills/format-notes/` (the skill) and `notes-formatter/`
  (`template/`, `scripts/`, `vendor/`). See `notes-formatter/DESIGN.md` (the
  authoring contract) and `notes-formatter/README.md` (pipeline + usage).
- Generated summaries go to `outputs/` — **gitignored; deliver in chat, never
  commit** (personal course content).
- **Speed defaults (learned from real runs):** run the skill **inline in one
  session** — no planner/executor model split and no single background agent
  doing the whole pipeline (that pattern took ~30 min/run). Parallelize page
  reads and independent verification; targeted QA re-reads after the first full
  pass. Details in the skill's "Speed rules"; per-run history in
  `notes-formatter/RUNLOG.md` — read it before a run, append to it after, and
  fold recurring lessons back into the skill. RUNLOG/SKILL updates are tool
  metadata: committing them is encouraged.

**Note:** the exam-prep tutors (FODL, Reinforcement Learning) that used to live here have
moved to their canonical home, `1amirmanes98-ai/exam-prep-agent`. New exam-prep agents
belong in **that** repo, not here. (The notes formatter above is a document-formatting
tool, not an exam-prep tutor agent, so it stays here deliberately.)
