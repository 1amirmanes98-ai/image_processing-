---
name: drill
description: Generate fresh exam-style exercises (novel variants of past-exam patterns) on a topic and coach through them. Works for both tutored courses (FODL and Intro to Statistics). Use for "/drill matrix factorization", "/drill power calculations hard", "give me new exercises on chi-square tests".
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). Pick the course from the topic/context; if
genuinely ambiguous, ask once. Below, `<agent>` = the chosen directory. If you
haven't this session, read `<agent>/AGENT.md` and follow it.

Input: `$ARGUMENTS` = topic + optional difficulty (easy/exam-level/hard). Default:
exam-level, topic chosen from weak spots in `<agent>/progress.md`.

## Generating a good drill (quality bar is high)

1. Read the topic's entry in `index/TOPICS.md`, the mapped index notes, and every
   past-exam question with that tag (via `index/EXAM_MAP.md` → `index/exams/*.md`).
2. Design a **novel** exercise that reuses the *pattern* but not the instance — change
   the ingredients the way the course itself varies them across years (FODL: hypothesis
   class / matrix structure / loss; Statistics: the distribution family / the dataset
   story / the tested parameter / one- vs two-sided / which CI method or test applies).
3. Structure it like the real thing: setup paragraph, then 2–4 sub-parts with point
   values matching real-exam scale, difficulty escalating, hints where the real exams
   would give them. For Statistics, make numbers calculator-friendly and provide the
   normal-table values the student would have.
4. **Solve it fully yourself before presenting** (scratch, not shown). If your solution
   requires anything outside course scope, redesign. Numerically sanity-check
   computational claims with python3 (numpy/scipy) where applicable.

## Coaching loop

Present the exercise → user attempts sub-part by sub-part → grade with points and
precise feedback → hint ladder on request (hints cost ~20%, say so) → full model
solution after each sub-part is resolved. One sub-part at a time.

## Wrap-up

Score, technique recap with citations, and — if they struggled — the matching `/teach`
or `/solve` follow-up. Update `<agent>/progress.md` per AGENT.md protocol.
