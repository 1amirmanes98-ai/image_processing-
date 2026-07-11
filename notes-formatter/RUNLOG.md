# RUNLOG — format-notes run history & lessons

Cross-session memory for the `/format-notes` pipeline. One line per run.
Lessons are about **process only** (speed, QA, pipeline) — never course content.
When a lesson generalizes, fold it into the "Speed rules" section of
`.claude/skills/format-notes/SKILL.md`.

| date | slug | in pages | out pages | QA iters | wall time | lesson |
|---|---|---|---|---|---|---|
| 2026-07-11 | inner-product-spaces | 16 | 9 | 2 | ~25 min | Two-pass transcript + full QA re-read each iteration was slow; single background agent = orchestrator waits idle. |
| 2026-07-11 | optimization-exam-x-2023 | 13+5 (questionnaire) | 9 | 2 | ~29 min (84 tool calls, ~267k tokens) | Serial per-question re-derivation dominated; independent questions should be verified by parallel subagents. Full 9-page QA re-read after a 2-line fix wasted ~⅓ of QA time. Orchestrator duplicated QA (5 more page reads) — spot-check ≤3 pages when executor already did full QA. |
| 2026-07-11 | optimization-exam-x-2023 (voice rewrite) | — (rewrite of existing content.html) | 8 | 2 | ~10 min, inline | User feedback: never third-person about the author ("אמיר צדק") — document speaks in the author's voice to students; mistakes → "טעות נפוצה" boxes. Encoded as DESIGN.md "Voice & genre". Also: SVG needs direction:ltr under RTL root; build_pdf.py now clears stale qa/*.png. Inline run + parallel reads + targeted QA re-read ≈ 3x faster than the delegated first pass. |

| 2026-07-11 | kkt-guide | 10 (used 5–9, KKT only) | 6 | 2 | ~8 min, inline | Topic-filtered run (user asked for KKT pages only) — survey-all-pages still required to find the topic boundaries. Long 3-part display equations overflow the page edge → split into stacked `.math` divs at authoring time. Inline + parallel batches + targeted re-read worked as designed. |

## Standing lessons (encoded in SKILL.md "Speed rules")
1. Run inline when the session model is already the executor model — no wholesale delegation.
2. Page reads in parallel batches (4–6 `Read` calls per message).
3. Single-pass authoring for ≤ ~12-page inputs.
4. Fan out independent verification (e.g. per exam question) to parallel subagents.
5. Full visual QA once; targeted re-reads (+`pdfinfo`) on subsequent iterations.
6. Reviewer/orchestrator spot-checks ≤3 pages when the executor already did full-page QA.
