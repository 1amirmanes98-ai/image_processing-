---
name: format-notes
description: >-
  Transcribe scanned handwritten Hebrew lecture notes into a beautiful typed,
  RTL PDF + self-contained HTML (David Libre, KaTeX math, colour-coded boxes,
  topic map, guided exercises, formula sheet) styled like Amir's reference
  summary. Use when the user uploads a scan/photo of handwritten notes or a
  solved exercise and wants it typed up / formatted / turned into a PDF —
  e.g. "תקליד לי את הסיכום", "תעשה מהמחברת הזאת PDF מסודר",
  "תמלל ותעצב את הפתרון", "format these lecture notes", "type up my notebook".
  Not for exam-prep tutoring — this is a formatting/typesetting tool.
---

# format-notes — handwritten Hebrew notes → typed PDF

You are given `$ARGUMENTS` (a path to a scanned PDF / image(s), or the user
pointed at an upload). Produce a polished RTL summary PDF **and** a
self-contained HTML, and deliver both in chat. Everything lives under
`notes-formatter/` (the tool) and `outputs/<slug>/` (the run — **gitignored,
never committed**).

Read `notes-formatter/DESIGN.md` before you write any HTML — it is the authoring
contract (every CSS class, the RTL/LTR bidi rules, and the fidelity rules).

## Speed rules (learned from real runs — see `notes-formatter/RUNLOG.md`)

These exist because early runs took ~30 min. Apply them; they do not trade off
quality:

- **Run inline, don't delegate wholesale.** If your session model is already the
  strongest available, execute this workflow yourself instead of spawning one
  background agent to do everything — a handoff adds waiting plus duplicated QA.
  Delegate only truly parallel side-work (see next rule) or when your context is
  nearly full.
- **Parallelize page reads.** Issue 4–6 `Read` calls *in a single message* per
  batch. Never read scan pages one call at a time.
- **Single-pass authoring for inputs ≤ ~12 pages.** Author each `content.html`
  section right after reading its page batch. Use a separate scratch transcript
  pass only for bigger inputs.
- **Fan out independent verification.** When correctness-checking a solved exam,
  each question is independent: spawn parallel subagents (one per question,
  structured output) while you author — don't re-derive five problems serially.
- **Targeted QA re-reads.** Full page-by-page QA on the *first* build only.
  After a targeted fix, re-read just the affected page(s) + the last page, and
  sanity-check page count with `pdfinfo`. Don't re-read all N pages per iteration.
- **Log every run.** Append a line to `notes-formatter/RUNLOG.md` (step 8) and
  read it at the start of a run — it is the cross-session memory of this tool.

## Workflow

### 0. Learn from past runs
Read `notes-formatter/RUNLOG.md` (if present) — apply any lessons recorded there.

### 1. Bootstrap
Run `notes-formatter/scripts/bootstrap.sh`. It installs `poppler-utils` if
missing and verifies Chromium, Node 22, and the vendored KaTeX + David Libre
assets. Fix any FAIL before continuing (see the README fallbacks).

### 2. Ingest
Pick a short `<slug>` and make `outputs/<slug>/`. Rasterize the input so you can
read it:
```bash
notes-formatter/scripts/rasterize.sh outputs/<slug>/pages  <input.pdf | images...>
```

### 3. Survey (before transcribing)
`Read` the page PNGs in batches of 4–6 — **all Reads of a batch in one message,
in parallel**. Build a mental map of the notebook: its sections, their order,
which items Amir marked important (`#`), his abbreviations, and any exercises.
Do **not** start writing HTML until you've seen every page.

### 4. Transcribe & author `content.html`
Write `outputs/<slug>/content.html` **section by section as you read** (single
pass; for inputs > ~12 pages you may keep a scratch transcript first), re-reading
a specific page only when ambiguous. Follow `DESIGN.md`.
**Fidelity rules (non-negotiable):**
- **Preserve the notebook's structure and order** — don't reorganise.
- **`#` / `.imp` only where the notebook marks it** — not what you think matters.
- **Anything beyond the notebook goes in a `.box.bonus`**, clearly flagged as an
  addition (e.g. a missing proof, extra intuition, "טיפים", "תבניות בי־לינאריות").
- **Never silently guess illegible handwriting** — emit a visible `.unclear`
  box. An unresolved `.unclear` is correct; a confident wrong guess is not.
- **Keep Amir's abbreviations + notation**; surface them in `.abbrev` + `.legend`.
- **Exercises are guided** — use `.steps` and mark the answer with `.result`.
- Page 1 opens with a `.hero` (title, subtitle, legend, abbreviations) and a
  `.topic-map`.

### 5. Build
```bash
python3 notes-formatter/scripts/build_pdf.py \
    outputs/<slug>/content.html \
    --title "<Hebrew title>" \
    --meta  "<optional closing line>" \
    -o outputs/<slug>/<slug>.pdf \
    --qa
```
This writes `rendered.html`, the self-contained `<slug>.html`, the `<slug>.pdf`,
and `qa/page-NN.png`.

### 6. Mandatory visual QA loop
On the **first build**, `Read` **every** `outputs/<slug>/qa/page-*.png` (in
parallel batches). On rebuilds after a targeted fix, re-read **only the affected
page(s) + the last page** and verify the page count via `pdfinfo`. Check:
- Hebrew renders RTL in **David Libre** (not a sans fallback);
- math renders via KaTeX (no raw `\( \)` / `\[ \]` visible), bidi correct around
  formulas;
- backgrounds/box tints print;
- no box splits across a page; no overflow/clipping;
- the `עמוד X מתוך Y` footer is on every page;
- legend + formula sheet present; every notebook section is present and in order.

Compare against the reference look (`innerproductsummary.pdf`, readable after
bootstrap). **Fix `content.html` and rebuild until clean.** Iterate — do not
deliver a first draft you haven't eyeballed page by page.

### 7. Deliver
Send both files with `SendUserFile`:
```
SendUserFile(files=["outputs/<slug>/<slug>.pdf", "outputs/<slug>/<slug>.html"], status="normal")
```
Outputs are personal course content — **deliver in chat only, never git commit
them** (`outputs/` is gitignored). Report any `.unclear` spots you left for the
user to confirm.

### 8. Log the run (cross-session memory)
Append one line to `notes-formatter/RUNLOG.md`:
```
| YYYY-MM-DD | <slug> | <in pages> | <out pages> | <QA iterations> | <wall time> | <lesson, or "-"> |
```
Keep lessons about **process** (speed, QA, pipeline), never course content.
If a lesson generalizes, also fold it into the "Speed rules" section above —
that is how this skill gets faster over time. Committing RUNLOG.md + SKILL.md
updates is allowed and encouraged (they are tool metadata, not personal content).
