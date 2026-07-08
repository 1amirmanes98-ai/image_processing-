---
name: progress
description: Study dashboard — coverage per pillar, scores over time, weak spots, days to exam, and a recommended plan. Works for both tutored courses (FODL and Intro to Statistics). Use for "/progress", "how am I doing", "what should I study next".
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). If the user names a course (or only one has an
upcoming exam), report on that one; with no signal, give a compact combined view of
both and lead with the nearer exam. Below, `<agent>` = the chosen directory. If you
haven't this session, read `<agent>/AGENT.md` and follow it.

1. Read `<agent>/progress.md` and `<agent>/index/TOPICS.md`.
2. If the exam date is unset, ask for it and record it.
3. Report, concisely:
   - **Countdown:** days to exam.
   - **Coverage:** per pillar — topics taught/quizzed/untouched (from the session log)
     vs. their exam weight (from TOPICS.md frequency stats).
   - **Scores:** quiz/drill/mock-exam results over time; trend.
   - **Weak spots:** current weak list + repeated flashcard misses.
   - **Mock exams:** taken vs. remaining (recent years untaken = save them for the
     final week under full exam conditions; for Statistics, exams with official
     solutions grade most reliably).
4. **Recommend a concrete plan** for the time remaining: highest (exam weight ×
   weakness) topics first; interleave pillars; schedule remaining mock exams; end with
   the single next action, e.g. "start with `/teach power & sample size` (appears in
   most exams, never studied)."
5. Update progress.md if anything was stale (e.g. recompute days-left) and follow the
   AGENT.md progress protocol.
