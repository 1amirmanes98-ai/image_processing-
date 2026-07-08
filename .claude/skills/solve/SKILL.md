---
name: solve
description: Socratic step-by-step walkthrough of a specific past exam question. Works for both tutored courses (FODL and Intro to Statistics). Use for "/solve a_2024 2", "/solve b_2023 q1", "walk me through question 3 of the 2022 stats exam".
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). Pick the course from context (exam ids exist in
both — if the user says just "a_2023 2", check which course they've been studying, or
ask once). Below, `<agent>` = the chosen directory. If you haven't this session, read
`<agent>/AGENT.md` and follow it.

Input: `$ARGUMENTS` = exam id + question number (e.g. `a_2024 2`). If ambiguous or
empty, list available exams from `<agent>/index/EXAM_MAP.md` with one-line question
summaries and let the user pick.

## Flow

1. Load the question from `<agent>/index/exams/<prefix>_<id>.md` (FODL prefix
   `fodl_exam`, Statistics prefix `stats_exam`). If any wording seems off, verify
   against the PDF (`<agent>/materials/exams/`, Read pages — note some statistics
   solution PDFs are scans, read visually). Present the statement (translated;
   original Hebrew on request) with sub-part points.
2. **Attempt first.** Ask which sub-part to start with and for their attempt or plan.
   - If they attempt: diagnose precisely — what's right, the exact step that fails.
   - If stuck: hint ladder (nudge → key idea → outline → full), one rung at a time.
3. Work sub-part by sub-part, **Socratically**: at each step ask the guiding question
   ("what is the null distribution of this statistic?", "what does convexity give you
   here?") rather than lecturing. Reveal each step only after they've engaged with it.
4. After each sub-part: recap the clean argument at full-credit rigor, name the general
   technique, and cite where it was taught (week/lecture/recitation/slides).
5. At the end: the complete model solution in one block (exam-ready), the techniques
   checklist, and 1–2 "same pattern" questions from other exams (from EXAM_MAP) to try
   next via `/quiz` or another `/solve`.
6. Update `<agent>/progress.md` per AGENT.md protocol.
