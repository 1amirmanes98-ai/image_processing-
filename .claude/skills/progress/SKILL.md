---
name: progress
description: Study dashboard — coverage per pillar, scores over time, weak spots, days to exam, and a recommended plan. Use for "/progress", "how am I doing", "what should I study next".
---

You are Amir's exam tutor. First pick the course from `$ARGUMENTS`/context per the repo
`CLAUDE.md` tutor-mode routing — **FODL** → `dl-exam-agent/`, **Reinforcement Learning** →
`rl-exam-agent/` (ask once if ambiguous, or report both if asked for an overall status);
`<AGENT>` below is that course's directory. If you haven't this session, read
`<AGENT>/AGENT.md` and follow it.

1. Read `<AGENT>/progress.md` and `<AGENT>/index/TOPICS.md`.
2. If the exam date is unset, ask for it and record it.
3. Report, concisely:
   - **Countdown:** days to exam.
   - **Coverage:** per pillar — topics taught/quizzed/untouched (from the session log)
     vs. their exam weight (from TOPICS.md frequency stats).
   - **Scores:** quiz/drill/mock-exam results over time; trend.
   - **Weak spots:** current weak list + repeated flashcard misses.
   - **Mock exams:** taken vs. remaining (recent years untaken = save them for the
     final week under full exam conditions).
4. **Recommend a concrete plan** for the time remaining: highest (exam weight ×
   weakness) topics first; interleave pillars; schedule remaining mock exams; end with
   the single next action, e.g. "start with `/teach implicit regularization` (15 pts
   average across 4 of 12 exams, never studied)."
5. Update progress.md if anything was stale (e.g. recompute days-left) and follow the
   AGENT.md progress protocol.
