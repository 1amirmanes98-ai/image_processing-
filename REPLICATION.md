# Replicating this exam-prep system for another course — the cheap way

This playbook exists because the first naive replication attempt burned ~2M tokens.
Followed exactly, a replication should cost **roughly 400–800k tokens**, almost all of
it on the one irreducible task: reading YOUR course's PDFs. Everything else is
copying, not creating.

**The golden rule: COPY the code, GENERATE only the content.**
`dl-exam-agent/scripts/build_site.py`, `scripts/site_template.html`,
`scripts/restore_content.sh`, and `.github/workflows/pages.yml` are
**course-agnostic — copy them byte-for-byte and do not edit them.** All
course-specific values live in one small file you write: `index/SITE_CONFIG.json`.
If you find yourself editing the template HTML or the build script, you are doing
it wrong (exception: a genuinely new feature).

## Phase 0 — Setup (≈5k tokens)

1. Clone the template read-only: `git clone https://github.com/1amirmanes98-ai/image_processing- /tmp/template`
2. Copy verbatim into your repo: `dl-exam-agent/scripts/` (3 files),
   `.github/workflows/pages.yml`, and the `.gitignore` entries for
   `dl-exam-agent/materials/` and `dl-exam-agent/index/`.
3. Unzip the user's materials into `dl-exam-agent/materials/{lectures,recitations,homework,exams}/`
   with clean snake_case names; run `pdftotext -layout` into `materials/text/...`
   mirrors (`apt-get install poppler-utils`).
4. **Decide with the user NOW**: is course content allowed on their (public?) repo?
   Default: keep `materials/` + `index/` gitignored; ship content via a zip +
   `restore_content.sh` (like the template), and publish only `docs/index.html`.

## Phase 1 — Index the course (the expensive part; ≈250–500k tokens)

Fan out parallel agents (3–4 files each). **Give every agent the exact output
format** below — inventing formats is where replicas waste tokens. Copy the agent
prompts from the template's index files' structure:

- `index/lectures/<name>.md` — format: title/File/Pillar/summary header, then
  `## Outline`, `## Key definitions` (items start `**Def (name).**`),
  `## Key theorems & results` (items start `**Thm/Lem/Prop (name).**`, each with
  "Proof idea:" and "Exam relevance:"), `## Techniques & tricks`,
  `## Exam-relevant nuggets`. Flashcards are auto-extracted from the Def/Thm items.
- `index/exams/<name>.md` — per question: `## Q<n> (<pts> pts) — <title>`, then a
  `**Topics:** ... | **Pillar:** ... | **Difficulty:** ...` line, `**Maps to:**`,
  `**Statement (English translation):**`, `**Solution sketch:**`. Statements must
  be complete enough to re-administer.
- `index/recitations/<name>.md`, `index/homework/<name>.md` — see template files.
- `index/TOPICS.md` — pillar tables `| topic | taught | examined | 🔴/🟠/🟡 |` under
  `## Pillar N — <SlotName>` headings; exam refs formatted `a2023_Q2`-style.
- `index/EXAM_MAP.md` — master table + `## Recurring question archetypes`
  numbered list (the site parses the refs out of the archetype text).

**Cost controls:**
- Typeset English PDFs → agents read the **text mirrors** (cheap); use visual PDF
  reads ONLY for scanned/Hebrew/garbled files or to double-check a formula.
- Instruct agents to **write each file as soon as it's done** (crash resilience).
- Skip homework indexing in v1 if budget-tight; add later.

## Phase 2 — Config + build + verify (≈30k tokens)

1. Write `index/SITE_CONFIG.json` (copy the template's and edit): courseName,
   subtitle, heroTitle/heroSub, examFormatLine, `slots` (up to 4 **single-word**
   category names — they become CSS classes), slotKeywords (lowercase keyword →
   slot, used to classify index content), slotRoles, mockSlotByQ,
   askSuggestions, and **`"figures": false`** (the built-in figures are
   FODL-specific; write new ones only as a later phase).
2. Fetch libs once (KaTeX 0.16.11 min js/css + contrib/auto-render + marked 12 +
   the 13 woff2 fonts — exact list in `dl-exam-agent/README.md`).
3. Build: `python3 dl-exam-agent/scripts/build_site.py dl-exam-agent/index <libs> \
   dl-exam-agent/scripts/site_template.html /tmp/site.html docs/index.html`
4. Verify ONCE in headless Chromium (Playwright, executablePath
   `/opt/pw-browsers/chromium`): zero console errors; KaTeX count > 0 on an exam
   page; **test the raw fragment (quirks mode) — the build already patches KaTeX's
   quirks-mode guard, just confirm**; no horizontal scroll at 390px; localStorage
   survives reload. Do NOT iterate visual polish beyond this.

## Phase 3 — Agent + skills (≈15k tokens)

Copy the template's `CLAUDE.md`, `dl-exam-agent/AGENT.md`, `progress.md`, and
`.claude/skills/*` and substitute course facts (name, exam format, file counts).
Do not redesign them.

## Phase 4 — Publish (≈10k tokens)

Commit `docs/index.html` + workflow, push, PR to main, user merges. Known gotcha:
first Pages deploy may fail "Resource not accessible" → user sets Settings → Pages
→ Source: **GitHub Actions**, then re-runs the workflow. Deploys only run from main.

## Phase 5 — Optional extras (defer until the user asks)

Mock exams (generate ONE, solve-first, numeric sanity-check — ≈40k each);
cheat sheet (compile from index with per-item source check — ≈80k); figures
(write per-course, computed not drawn); full adversarial audit (≈150–300k —
worth it, but run ONE audit pass at the end, not after every phase).

## Phase 6 — Hebrew-language course (do this ONLY when one actually exists)

Hebrew **content** already works: index files may be written in Hebrew (math stays
LTR inside KaTeX automatically), and the Ask tokenizer understands Hebrew words
(with a Hebrew stopword list and definite-article stripping). Keep the *structural*
markers of the index format in English (`**Def (…).**`, `## Q1 (40 pts) — …`,
`**Statement:**`) — the parsers key on them; only the prose goes Hebrew.

A Hebrew **UI** (RTL) is a one-session template upgrade. Checklist:
1. Add to SITE_CONFIG.json: `"dir": "rtl"`, `"lang": "he"`, and a `"ui"` strings
   object; template boot sets `document.documentElement.dir/lang` from config and
   reads every UI string via `CONFIG.ui.<key>` with English fallbacks.
2. CSS: convert physical properties to logical ones — `border-left` →
   `border-inline-start` (the colored card stripes: `.qhead`, `.hit`, `.memoitem`,
   `.topicrow .stripe`), `text-align:left` → `start`, `margin/padding-left/right` →
   `-inline-start/-end`. Flex/grid mirror automatically.
3. Force LTR islands: `.katex, .katex-display, code, pre { direction: ltr;
   unicode-bidi: isolate; }` — and verify mixed Hebrew-text + inline-math
   paragraphs visually (this is most of the verification work).
4. Verify RTL in headless Chromium at desktop + 390px widths; check the bottom
   mobile nav order and that `overflow-x` didn't flip.

Ready-made Hebrew UI strings pack (translate-once, copy into `"ui"`):
nav: סקירה · נושאים · חיפוש · מבחנים · לשינון · כרטיסיות · בוחן;
buttons: גלה את הפתרון · ידעתי ✓ · כמעט ◐ · פספסתי ✗ · דלג לשאלה אחרת ·
חזרה · ערבב לי · הצג במבחן המלא; headings: החומר מהשיעור ·
שאלות מבחן בנושא הזה · סקיצת פתרון — נסו לבד קודם · ידוע לי (מעקב שינון) ·
תבנית המבחן · דפוסי שאלות חוזרים; misc: נקודות · קושי · הופיע ב־ ·
נבנה מחדש בכל טעינה · ימים למבחן.

## Anti-patterns that burned tokens the first time

- Rewriting/adapting `site_template.html` instead of using SITE_CONFIG. (Biggest sink.)
- Re-reading whole PDFs visually when text mirrors sufficed.
- Re-verifying with screenshots after every tiny edit — verify once per phase.
- Auditing everything at maximum depth repeatedly — one adversarial pass at the end.
- Agents batching all writes to the end, then dying (rate limits) — write-as-you-go.
- Debugging LaTeX/quirks/Pages issues from scratch — they're already solved here;
  read this file and the commit history instead.
