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

## Workflow

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
`Read` the page PNGs in batches of 4–6. Build a mental map of the notebook:
its sections, their order, which items Amir marked important (`#`), his
abbreviations, and any exercises. Do **not** start writing HTML until you've
seen every page.

### 4. Transcribe & author `content.html`
Write `outputs/<slug>/content.html` section by section, re-reading the relevant
page PNGs as you go. Follow `DESIGN.md`. **Fidelity rules (non-negotiable):**
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
`Read` **every** `outputs/<slug>/qa/page-*.png` and check:
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
