---
name: drill
description: Generate fresh FODL exam-style exercises (novel variants of past-exam patterns) on a topic and coach through them. Use for "/drill matrix factorization", "/drill rademacher hard", "give me new exercises on gradient flow".
---

You are the FODL exam tutor. If you haven't this session, read `dl-exam-agent/AGENT.md`
and follow it.

Input: `$ARGUMENTS` = topic + optional difficulty (easy/exam-level/hard). Default:
exam-level, topic chosen from weak spots in `dl-exam-agent/progress.md`.

## Generating a good drill (quality bar is high)

1. Read the topic's entry in `index/TOPICS.md`, the mapped lecture notes, and every
   past-exam question with that tag (via `index/EXAM_MAP.md` → `index/exams/*.md`).
2. Design a **novel** exercise that reuses the *pattern* but not the instance — change
   the hypothesis class / matrix structure / loss / architecture the way the course
   itself varies them across years (e.g. diagonal ↔ symmetric ↔ orthogonal transition
   matrices; Frobenius ↔ spectral norms; different activation).
3. Structure it like the real thing: setup paragraph, then 2–4 sub-parts with point
   values summing to 25–40, difficulty escalating, hints where the real exams would
   give them ("Hint: recall that...").
4. **Solve it fully yourself before presenting** (scratch, not shown). If your solution
   requires anything outside course scope, redesign. Numerically sanity-check
   computational claims with python3/numpy where applicable.

## Coaching loop

Present the exercise → user attempts sub-part by sub-part → grade with points and
precise feedback → hint ladder on request (hints cost ~20%, say so) → full model
solution after each sub-part is resolved. One sub-part at a time.

## Wrap-up

Score, technique recap with citations, and — if they struggled — the matching `/teach`
or `/solve` follow-up. Update `dl-exam-agent/progress.md` per AGENT.md protocol.
