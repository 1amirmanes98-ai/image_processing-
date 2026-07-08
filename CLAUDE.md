# Repo guide

This repo contains a few unrelated things:

1. **Image-processing / numerical scripts** (`*.py` at root) — coursework scripts.
2. **`dl-exam-agent/`** — a personal exam-prep tutor for *Foundations of Deep Learning*
   (TAU 03683080), built from its lectures, recitations, homework, and 12 past exams.
   Study site at `docs/index.html`.
3. **`rl-exam-agent/`** — a personal exam-prep tutor for *Reinforcement Learning*
   (TAU 0368.3075, Prof. Yishay Mansour), built from its 13 lectures, 12 recitations,
   the RL Foundations book, exercise booklet, and all past exams (2018–2023) + a sample
   exam. Study site at `docs/rl/index.html`.

## Tutor mode

Whenever the user wants to study, asks about deep-learning or reinforcement-learning
theory, mentions an exam, or invokes any study skill (`/teach`, `/quiz`, `/exam`,
`/solve`, `/drill`, `/flashcards`, `/progress`):

1. **Pick the course.** The skills are shared by both tutors. Decide from the
   topic/arguments (e.g. "Rademacher", "gradient flow", "NTK" → FODL; "MDP", "Bellman",
   "Q-learning", "policy gradient", "bandit/regret", "value iteration" → RL), from which
   exam is nearer in the two `progress.md` files, or — if genuinely ambiguous — ask once.
2. **Read that tutor's operating manual first**: `dl-exam-agent/AGENT.md` or
   `rl-exam-agent/AGENT.md` (grounding rules, interaction rules, progress protocol). Note
   its "Content bootstrap" section: each agent's `materials/` and `index/` are
   intentionally untracked; in a fresh clone they must be restored from the user's content
   zip (`fodl-tutor-content.zip` / `rl-tutor-content.zip`) via that agent's
   `scripts/restore_content.sh` before any content-grounded tutoring.
3. Ground everything in that agent's `index/` (start at `index/TOPICS.md`); original PDFs
   in its `materials/` are ground truth.
4. Track study state in that agent's `progress.md` and push it at session end.

Course materials in `*/materials/` are university content for personal study — do not copy
them outside this repo or quote them at length in public-facing artifacts. The built sites
(`docs/index.html`, `docs/rl/index.html`) are published deliberately by the owner.

For ordinary coding tasks in this repo, work normally; tutor mode only activates for
study-related requests.
