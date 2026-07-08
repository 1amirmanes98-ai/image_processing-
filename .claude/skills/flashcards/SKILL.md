---
name: flashcards
description: Rapid-fire drill of definitions, theorem statements, and key formulas. Works for both tutored courses (FODL and Intro to Statistics). Use for "/flashcards", "/flashcards generalization", "/flashcards confidence intervals", "drill me on definitions".
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). Pick the course from the topic/context; if
genuinely ambiguous, ask once. Below, `<agent>` = the chosen directory. If you
haven't this session, read `<agent>/AGENT.md` and follow it.

Input: `$ARGUMENTS` = optional topic/pillar and count (default: 10 cards, mixed, biased
toward `progress.md` weak topics and past flashcard misses).

## Deck

Build cards from the **Key definitions** and **Key theorems & results** sections of
`<agent>/index/lectures/*.md` (FODL: plus recitation formulas; Statistics: plus the
`index/CHEATSHEET.md` items). Card fronts:
- "State the definition of X (with all conditions)."
- "State the formula for Y precisely. When is it valid?" (e.g. the Wilson CI; the
  chi-square statistic and its degrees of freedom; the Wilcoxon null mean/variance)
- "Complete: for L-smooth f and step size η ≤ …, GD guarantees …"
- Reverse cards: "Which tool gives you X? What breaks without assumption Z?"

FODL allows **no formula sheet** — exact statements with all conditions are the bar.
Statistics allows two self-made formula pages — the drill's goal is that the sheet is
written correctly and everything on it is understood; "roughly right" is still a miss.

## Loop

One card at a time: prompt → their answer → verdict ✓/✗/half + the exact statement
(cited) + what they dropped (a missing quantifier or condition = half at best) → next.
Keep the pace snappy — this is recall training, minimal prose.

## Wrap-up

Misses list with source pointers; append misses to the flashcard-misses section in
`<agent>/progress.md` (they get re-drawn next time); commit+push per AGENT.md
protocol. Suggest `/teach` for anything missed twice.
