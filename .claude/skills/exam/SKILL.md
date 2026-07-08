---
name: exam
description: Full mock exam under exam conditions with strict grading — a real past exam or a freshly generated one. Works for both tutored courses (FODL 3q/~105pts; Intro to Statistics 4q/100pts+bonus). Use for "/exam", "/exam past a_2023", "/exam new", "give me a mock exam".
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). Pick the course from context or the nearer exam;
if genuinely ambiguous, ask once (exam ids like `a_2023` exist in both). Below,
`<agent>` = the chosen directory. If you haven't this session, read
`<agent>/AGENT.md` and follow it.

Input: `$ARGUMENTS` = `past <exam_id>` (e.g. `past a_2023`) | `new` | empty.
If empty: read `<agent>/progress.md` → recommend an untaken recent past exam
(most representative years first; for Statistics, exams with official solutions grade
most reliably) or `new` if all are taken; let the user choose.

## Administering

**Past exam:** load `<agent>/index/exams/<prefix>_<id>.md` (FODL prefix `fodl_exam`,
Statistics prefix `stats_exam`). Present the full translated exam (all questions and
sub-parts with points). Offer the original Hebrew (Read the PDF pages) — practicing
on the Hebrew original is closest to the real thing.

**New exam:** generate one that mirrors the real format exactly (from
`index/EXAM_MAP.md`):
- FODL: 3 multi-part questions, ~105 pts, one per pillar.
- Statistics: 4 questions, 100 pts + a starred bonus sub-part or two: Q1 = ~6
  true/false claims with justification (~24 pts); Q2–Q4 = computational/analysis
  questions covering estimation, testing, and categorical/two-sample topics; provide
  the normal-table values the student would have on the real exam.
Difficulty and phrasing matched to real exams, novel setups (variants of past
patterns, never copies). Solve every part yourself FIRST (scratch, not shown) to
verify solvability and calibrate points; sanity-check any computation numerically
(python3/scipy).

Persist every generated exam so it also appears on the study site:
- `<agent>/generated_exams/mock_exam_NN.md` — first line
  `# <Course> Mock Exam NN (generated YYYY-MM-DD)`; each question starts exactly
  `## Question N (P pts) — Title` (the site build parses this).
- `<agent>/generated_exams/mock_exam_NN_solutions.md` — rubric blocks starting `## QN`;
  the site shows them as the sealed solution fold.
- Commit both (original content — not gitignored), then offer to rebuild + redeploy
  the study site (see `<agent>/scripts/build_site.py` docstring).

**Exam conditions:** record start time (`date`). Real exam = 3 hours; FODL allows no
aids; Statistics allows a calculator + two double-sided formula pages (suggest using
the site's Memorize tab as the sheet). No hints — if they want hints it stops being
exam-simulation (say so, then use the hint ladder with point costs). No solution
reveals until grading.

## Grading

When they submit (or say "done" / "grade it"):
1. Note elapsed time vs 3h.
2. Grade each sub-part against its points: what earns credit, what's missing, where
   an argument breaks. Course-level rigor. For Statistics claims questions: verdict
   without a valid justification = 0, like the real exam. Partial credit per AGENT.md.
3. Full model solution for every sub-part (full-credit quality), with citations.
4. Report: total (FODL /105, Statistics /100 + bonus), per-question and per-pillar
   breakdown, time verdict, top 3 review priorities with source pointers.
5. Update `<agent>/progress.md`: session log, exams-taken checklist, weak/strong
   lists; commit+push per AGENT.md protocol.
