# Repo guide

This repo contains three unrelated things:

1. **Image-processing / numerical scripts** (`*.py` at root) — coursework scripts.
2. **`dl-exam-agent/`** — a personal exam-prep tutor for *Foundations of Deep
   Learning* (TAU 03683080), built from the course lectures, recitations, homework,
   and 12 past exams.
3. **`stats-exam-agent/`** — a personal exam-prep tutor for *Intro to Statistics*
   (TAU 0365.1813, Prof. Ruth Heller), built from the course summary, lecture slides,
   and 19 past finals (2012–2025).

## Tutor mode

Whenever the user wants to study, asks about deep-learning or statistics theory,
mentions an exam, or invokes any of the study skills (`/teach`, `/quiz`, `/exam`,
`/solve`, `/drill`, `/flashcards`, `/progress`):

1. **Pick the course.** The skills are shared by both tutors. Decide from the
   topic/arguments (e.g. "Rademacher", "gradient flow" → FODL; "confidence interval",
   "chi-square", "Wilcoxon" → Statistics), from which exam is nearer in the two
   `progress.md` files, or — if genuinely ambiguous — ask once.
2. **Read the tutor's operating manual first**: `dl-exam-agent/AGENT.md` or
   `stats-exam-agent/AGENT.md`. It defines grounding rules, interaction rules, and the
   progress protocol. Note the "Content bootstrap" section: each agent's `materials/`
   and `index/` are intentionally untracked; in a fresh clone they must be restored
   from the user's content zip (`fodl-tutor-content.zip` / `stats-tutor-content.zip`)
   via that agent's `scripts/restore_content.sh` before any content-grounded tutoring.
3. Ground everything in the agent's `index/` (start at `index/TOPICS.md`); original
   PDFs in `materials/` are ground truth.
4. Track study state in that agent's `progress.md` and push it at session end.

The course materials in `dl-exam-agent/materials/` and `stats-exam-agent/materials/`
are university course content for personal study — do not copy them outside this repo
or quote them at length in public-facing artifacts.

## Study sites

Both tutors ship a single-file study site, deployed by `.github/workflows/pages.yml`
from `docs/` on pushes to `main`:

- FODL: `docs/index.html` → https://1amirmanes98-ai.github.io/image_processing-/
  (rebuild: `dl-exam-agent/scripts/build_site.py`)
- Statistics: `docs/stats/index.html` → https://1amirmanes98-ai.github.io/image_processing-/stats/
  (rebuild: `stats-exam-agent/scripts/build_site.py`; see that script's docstring for
  the exact command and where to fetch the KaTeX/marked libs)

For ordinary coding tasks in this repo, work normally; tutor mode only activates for
study-related requests.
