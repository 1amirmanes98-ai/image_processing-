---
name: teach
description: Interactive lesson on a course topic — intuition, formal definitions/theorems, mini-checks, and where it appeared in past exams. Works for both tutored courses (FODL and Intro to Statistics). Use when the user wants to learn or review a topic (e.g. "/teach gradient flow", "/teach confidence intervals", "explain the chi-square test to me").
---

This repo hosts two exam tutors: **FODL** (`dl-exam-agent/`) and **Intro to
Statistics** (`stats-exam-agent/`). Pick the course from the topic (DL theory →
FODL; statistics/inference → Statistics), from context, or by the nearer exam in the
two `progress.md` files; if genuinely ambiguous, ask once. Below, `<agent>` = the
chosen directory. If you haven't this session, read `<agent>/AGENT.md` and follow it
(including its content-bootstrap check).

Input: `$ARGUMENTS` = topic (free text). If empty, read `<agent>/index/TOPICS.md`
and `<agent>/progress.md`, propose the 3 highest-value topics right now (exam
frequency × weakness × not yet covered), and let the user pick.

## Lesson flow

1. **Locate.** Find the topic in `index/TOPICS.md`; read the mapped index notes
   (FODL: `index/lectures|recitations|homework/*.md`; Statistics:
   `index/lectures/week_*.md` and `slides_*.md`). Open the source PDF only if a
   statement you need is unclear in the index.
2. **Orient (short).** Where the topic sits in the course (pillar, week/lecture), why
   it matters for the exam (frequency from TOPICS.md, e.g. "appeared in 14 of 19
   exams").
3. **Teach in layers, interactively.** For each core item (definition → theorem/formula
   → method → example):
   - intuition first, then the precise formal statement (LaTeX, course notation);
   - after each layer, a quick **check question** (one at a time; wait for the answer;
     correct misconceptions immediately);
   - flag common traps and what the exam expects to be stated rigorously (for
     Statistics: conditions for approximations, one- vs two-sided, conclusion phrased
     in context).
4. **Connect to exams.** Show 1–2 concrete past-exam questions on this topic (from
   `index/exams/`), with year/moed/points — don't solve them, just show what mastery
   is asked for. Offer `/solve` for a walkthrough or `/quiz <topic>` to test.
5. **Log.** Append lesson + topic + observed gaps to `<agent>/progress.md`
   (per AGENT.md progress protocol).

Keep each message digestible — this is a conversation, not a textbook dump.
