---
name: quiz
description: Adaptive graded quiz on course topics, one question at a time with points and feedback. Works for both tutored courses (FODL and Intro to Statistics). Use when the user wants to be tested (e.g. "/quiz", "/quiz generalization", "/quiz hypothesis testing", "test me on confidence intervals").
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). Pick the course from the topic/context or the
nearer exam; if genuinely ambiguous, ask once. Below, `<agent>` = the chosen
directory. If you haven't this session, read `<agent>/AGENT.md` and follow it.

Input: `$ARGUMENTS` = optional topic and/or length (e.g. "rademacher", "power and
sample size 8 questions"). Defaults: adaptive topic mix, 6 questions.

## Setup

1. Read `<agent>/index/TOPICS.md` and `<agent>/progress.md`.
2. Choose questions: if a topic was given, stay on it; otherwise weight by
   (exam frequency × current weakness), and prefer topics not quizzed recently.
3. Build a mix of formats calibrated to the real exam style (see `index/exams/`):
   - FODL: state-the-definition/theorem; true/false with justification; short proof
     or computation; "find the bug in this argument".
   - Statistics: true/false claims **with brief justification** (the real Q1 format —
     verdict without justification = 0); short computations (estimator, CI, test
     statistic + decision, power); "which test applies here and why"; reading a
     study design (observational vs experiment, what may be concluded).
   Source questions from `index/exams/` sub-parts or generate variants grounded in
   the index notes. Verify any generated question yourself before asking (AGENT.md
   rule 4 — for numeric answers, a quick python3 check).

## Loop (strictly one question at a time)

For each question: state it with its point value → wait for the answer → grade
(points earned, exactly what's missing/wrong, model answer at full-credit rigor,
source citation) → one-line running score → next question. Offer a hint if the user
stalls (hint ladder from AGENT.md; hints cost ~20% of the sub-part's points, tell them).

## Wrap-up

- Score table: per question — topic, points earned/possible.
- Diagnosis: strongest / weakest, each with a source pointer for review.
- Recommend the next action (`/teach X`, `/drill Y`, `/exam`).
- Update `<agent>/progress.md` (session log + weak/strong lists) and follow the
  AGENT.md progress protocol (commit+push at session end).
