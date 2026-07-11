# notes-formatter

Turn scans of handwritten Hebrew lecture notes into a **beautiful typed PDF**
(RTL, David Libre, KaTeX math) plus a **self-contained HTML** copy.

The design system is calibrated against a reference summary
(`innerproductsummary.pdf`): colour-coded callout boxes, dark numbered section
chips, a page-1 topic map + legend, guided exercises, and a quick formula sheet.

This directory is a **tool**, not exam-prep content. Outputs are personal course
material and are **never committed** — they live under `outputs/` (gitignored)
and are delivered to the user in chat.

---

## Pipeline

```
scan (PDF/images)
  └─ rasterize.sh ──▶ outputs/<slug>/pages/page-NN.png   (read the pages)
        │
        └─ (you transcribe → outputs/<slug>/content.html per ../DESIGN.md)
              │
              └─ build_pdf.py ─┬─▶ rendered.html   (print copy, file:// assets)
                               ├─▶ <slug>.html     (self-contained deliverable)
                               ├─ print_pdf.mjs (Chromium CDP) ─▶ <slug>.pdf
                               └─ --qa: pdftoppm ─▶ outputs/<slug>/qa/page-NN.png
```

Two HTML flavors come out of `build_pdf.py`:

- **`rendered.html`** — used only for the local print step; references the
  vendored KaTeX/fonts by absolute `file://` URLs (fast, no inlining).
- **`<slug>.html`** — the deliverable; **every** asset (David Libre TTF, KaTeX
  CSS + woff2 + JS) is inlined as `data:` URIs / inline `<script>`, so it opens
  in any browser with **no network**.

---

## Usage

```bash
# 0) one-time / idempotent environment check (installs poppler-utils if missing)
notes-formatter/scripts/bootstrap.sh

# 1) rasterize the input so you can read it
notes-formatter/scripts/rasterize.sh outputs/my-notes/pages  path/to/scan.pdf
#   or a set of images:
notes-formatter/scripts/rasterize.sh outputs/my-notes/pages  p1.jpg p2.jpg ...

# 2) author outputs/my-notes/content.html following ../DESIGN.md

# 3) build the PDF (+ QA rasters)
python3 notes-formatter/scripts/build_pdf.py \
    outputs/my-notes/content.html \
    --title "אלגברה לינארית — סיכום ההרצאה" \
    --meta  "נבנה מתוך סיכום ההרצאה · 11.07.2026" \
    -o outputs/my-notes/my-notes.pdf \
    --qa

# 4) read every outputs/my-notes/qa/page-*.png and iterate content.html until clean
#    (first build: all pages; later iterations: only affected pages + last page)

# 5) append a run line to notes-formatter/RUNLOG.md (date, slug, pages, iters,
#    wall time, lesson) — this is how the tool gets faster across sessions
```

### `build_pdf.py`

```
build_pdf.py <content.html> --title T [--footer F] [--meta M] -o out.pdf [--qa]
```
- `--title` — document title; feeds `<title>` and the page footer.
- `--footer` — footer text override (defaults to `--title`).
- `--meta` — optional closing line rendered at the end of the document.
- `--qa` — rasterize the produced PDF to `<outdir>/qa/page-NN.png` (~110 DPI).

### `print_pdf.mjs`

```
node print_pdf.mjs <input.html> <output.pdf> [--footer "text"]
```
Dependency-free Chrome DevTools Protocol driver (Node 22 built-in
`WebSocket`/`fetch`). Launches headless Chromium, waits for
`window.__RENDER_DONE__` (KaTeX rendered + `document.fonts.ready`), then
`Page.printToPDF` at A4 with an RTL `עמוד X מתוך Y` footer.

### `rasterize.sh`

```
rasterize.sh <outdir> <input.pdf | image ...>
```
PDFs → `pdftoppm -r 160 -png`. Images are copied/normalized to `page-NN.<ext>`
in order (no pdftoppm needed; `Read` renders png/jpg directly).

---

## Environment

| tool | path | notes |
|------|------|-------|
| Chromium 141 | `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` | override with `CHROME_BIN` |
| Node 22 | `/opt/node22/bin/node` | built-in `fetch`/`WebSocket` |
| Python 3.11 | system | needs `jinja2` (installed) |
| poppler-utils | installed by `bootstrap.sh` | provides `pdftoppm` |

Vendored under `vendor/` (committed — ~0.6 MB of tool assets, not personal
content):
- `vendor/katex/` — KaTeX 0.16.22 (`katex.min.css/js`, `contrib/auto-render.min.js`, 20 woff2 fonts)
- `vendor/fonts/` — David Libre `Regular` / `Medium` / `Bold` (TTF)

---

## Troubleshooting & fallbacks

- **`pdftoppm: not found`** → run `scripts/bootstrap.sh`. If apt is unavailable,
  fall back to PyMuPDF: `pip install pymupdf`, then rasterize in Python
  (`fitz.open(pdf); page.get_pixmap(dpi=160).save(...)`).
- **PDF has no footer / `printToPDF` empty footer** → Chromium renders header/
  footer in an isolated context with **no webfonts**; the footer is
  intentionally `DejaVu Sans` (same known limitation as the reference). The
  footer only shows if the bottom margin is large enough (we use 0.63in).
- **`__RENDER_DONE__ not set within 30s`** → usually a KaTeX syntax error in the
  content (check the QA render for raw `\( \]`). The driver prints anyway; fix
  the LaTeX and rebuild.
- **CDP driver breaks on a Chromium update** → fallback A: `npm i playwright-core`
  (browsers already on disk; `PLAYWRIGHT_BROWSERS_PATH` is set) and drive via
  its CDP session. Fallback B: `chrome --headless --print-to-pdf=out.pdf
  --no-pdf-header-footer file://…` (loses the Hebrew page-counter footer).
- **Hebrew shows a fallback (sans) font** → the David Libre `@font-face`
  `url()`s didn't resolve; confirm `vendor/fonts/DavidLibre-*.ttf` exist and
  re-run `build_pdf.py` (it rewrites those paths at build time).
- **A box splits across a page** → boxes are `break-inside: avoid`; if one box
  is taller than a page, split its content into two boxes in `content.html`.

---

## Layout

```
notes-formatter/
├── README.md            # this file (human docs)
├── RUNLOG.md            # per-run history + process lessons (the tool's cross-session memory)
├── DESIGN.md            # the authoring contract (model-facing: every class + rules)
├── template/
│   ├── page.html.j2     # RTL jinja2 shell; renderMathInElement → __RENDER_DONE__
│   └── notes.css        # the full design system + print CSS
├── scripts/
│   ├── bootstrap.sh     # idempotent env check/setup
│   ├── rasterize.sh     # PDF/images → page-NN.png
│   ├── build_pdf.py     # jinja2 wrap → 2 HTML flavors → print_pdf.mjs → (--qa) rasters
│   └── print_pdf.mjs    # dependency-free Chromium CDP → A4 PDF with RTL footer
└── vendor/              # KaTeX + David Libre (committed tool assets)
```
