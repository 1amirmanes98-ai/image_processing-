# Repo guide

This repo contains two unrelated things:

1. **Image-processing / numerical scripts** (`*.py` at root) — coursework scripts.
2. **`dl-exam-agent/`** — a personal exam-prep tutor for the course *Foundations of
   Deep Learning* (TAU 03683080), built from the course lectures, recitations,
   homework, and 12 past exams.

## Tutor mode

Whenever the user wants to study, asks about deep-learning theory, mentions the FODL
exam, or invokes any of the study skills (`/teach`, `/quiz`, `/exam`, `/solve`,
`/drill`, `/flashcards`, `/progress`):

1. **First read `dl-exam-agent/AGENT.md`** — it is the tutor's operating manual
   (grounding rules, interaction rules, progress protocol).
2. Ground everything in `dl-exam-agent/index/` (start at `index/TOPICS.md`); original
   PDFs in `dl-exam-agent/materials/` are ground truth.
3. Track study state in `dl-exam-agent/progress.md` and push it at session end.

The course materials in `dl-exam-agent/materials/` are university course content for
personal study — do not copy them outside this repo or quote them at length in
public-facing artifacts.

For ordinary coding tasks in this repo, work normally; tutor mode only activates for
study-related requests.
