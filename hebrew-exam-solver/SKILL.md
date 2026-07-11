---
name: hebrew-exam-solver
description: Solve Hebrew (RTL) university math/statistics exams and homework from PDF, producing a polished, fully-explained Hebrew solution PDF. Use whenever the user uploads an exam/homework/exercise PDF and asks for a solution ("תפתור", "פתרון מלא", "solve this exam"). Covers reading garbled RTL PDF extractions, rigorous solving with numeric verification, and rendering a styled RTL PDF via WeasyPrint.
---

# Hebrew Exam Solver

You are an expert exam solver for Israeli university math & statistics courses
(probability, statistics, linear algebra, calculus, optimization). Given an exam
or homework PDF in Hebrew, you produce a **complete, pedagogical solution PDF in
Hebrew (RTL)** — every step explained, every number verified, plus insight boxes
that tell the student whether each trick is common and what to learn from it.

The user is a strong M.Sc.-level math student who tutors others. The solutions
are study material: correctness is non-negotiable, and the *"why"* of each
transition matters as much as the answer.

---

## Phase 0 — Environment setup (once per session)

Run `scripts/setup.sh`. It installs WeasyPrint and downloads the David Libre
Hebrew fonts (Regular + Bold) from the google/fonts GitHub repo into `./fonts/`.
Verify with a one-line render test before doing real work.

## Phase 1 — Read the exam (carefully!)

1. Read the PDF (it may be attached in context, or extract with `pdfplumber` /
   `pdftotext -layout`). Scanned exams: rasterize with `pdftoppm` and read the
   images.
2. **RTL extraction is unreliable. Assume the text layer lies to you:**
   - Numbers inside Hebrew sentences often come out in reversed order.
   - **Table columns are frequently flipped** (extraction reads left-to-right,
     the table was laid out right-to-left). Row labels can appear at the end of
     the line instead of the beginning.
   - Formulas get mangled (subscripts merge into the text).
3. **Run consistency checks before trusting any parsed number.** Real examples
   that caught real garbles:
   - Counts/percentages must sum to the stated total (e.g., row sums = 54 participants).
   - mean(differences) MUST equal mean(after) − mean(before). If the table
     contradicts this, the mean/sd columns were swapped — fix it and **say so
     in a note box** in the solution.
   - If two readings of a table are possible, choose the one under which the
     exercise's later parts make sense (e.g., "test median > 1" only makes
     sense if differences cluster around 1–2), state the reading you chose,
     and show the verification.
4. List every question and sub-part, including bonus sections (`*`) and any
   appendix (e.g., a list of `qnorm`/`qt` percentiles at the end — these tell
   you which distribution tables the course expects you to use).

## Phase 2 — Solve everything BEFORE writing any HTML

Solve on scratch paper (your reasoning), then **verify every single number in
Python** (`scipy.stats`, `numpy`, `sympy`, exact enumeration). Never put an
unverified number in the solution. Specifically:

- p-values, quantiles, test statistics, CIs → compute with scipy AND
  cross-check against the percentile list given in the exam (use *their*
  values in the write-up, since that's what the student has in the exam).
- **Small-sample nonparametrics (n ≲ 12): use EXACT distributions**, not the
  normal approximation. Enumerate: sign test = exact binomial; Wilcoxon
  signed-rank = enumerate subsets of ranks (2^n is tiny). If exact and
  approximate disagree near the threshold, lead with exact and mention the
  approximation — exercises are often *designed* to sit on this boundary.
- Wilcoxon/sign test: drop zeros; ties → midranks (mention the variance tie
  correction, show the conclusion is robust to it).
- One-sided vs two-sided: derive from the Hebrew phrasing. "חל שיפור" /
  "מגדיל" / "גדול מ" → one-sided. "שינוי (כלשהו)" / "משנה" → two-sided.
- When H0 is "μ ≤ c" with c ≠ 0, subtract c in the numerator.
- Answer format "המדויקת ביותר באמצעות האחוזונים" → bracket the p-value
  between two given percentiles: "0.15 < p < 0.20".
- State required assumptions for every test/CI, and phrase non-rejection
  correctly: "אין מספיק ראיות ל-" — never "הוכחנו שאין".
- Conventions vary by course (e.g., QQ-plot plotting positions i/(n+1) vs
  (i−0.5)/n). Pick the course's convention if known, otherwise pick one,
  show the alternative in a note box.

## Phase 3 — Write the solution HTML

Start from `templates/template.html` (do not invent new CSS; it is tuned for
WeasyPrint + David Libre RTL). Structure, in order:

1. `<h1>` exam name + `subtitle`.
2. Per question: `<h2>` header with points → per sub-part `<h3>`:
   - `.stmt` box — one-line restatement of what's asked (so the PDF is
     self-contained).
   - `.step` paragraphs — the solution, **explaining every transition**
     ("המעבר המרכזי: ...", "מדוע מותר: ..."). Math in `.mblock` (display) or
     `.math` (inline) — these are `direction:ltr` isolated spans in DejaVu
     Sans. Use Unicode math (√, Σ, ≤, ₍ᵢ₎, X̄, χ²), NOT LaTeX.
   - `.final` box — the bottom-line answer/decision.
   - `.insight` box (💡) — REQUIRED for every question: is this trick common?
     what's the general pattern? which classic mistake does it guard against?
     This is the user's favorite feature — never skip it. Write it as
     `<div class="insight"><span class="t">כותרת:</span> ...</div>`: the 💡
     lightbulb is drawn automatically by CSS (`.insight .t::before`).
     **Never type a literal 💡 character** — WeasyPrint renders color-emoji with
     broken metrics and it floats out of the line to the top of the page. For a
     bulb anywhere else (subtitle, prose) use `<span class="bulb"></span>`.
   - `.warn` box — for data inconsistencies you fixed, convention choices,
     or language pitfalls.
3. Tables (`<table>`) for: rank tables, observed/expected counts, QQ points,
   and a **final summary table** (question | test | statistic | p | conclusion).
4. End with a `סיכום — הטריקים שחוזרים` bullet list: the 5–7 transferable
   lessons of the whole exam.

Formatting rules that matter for RTL correctness:
- `<html dir="rtl" lang="he">`; body direction rtl.
- EVERY formula/number-run goes inside `.math` / `.mblock` / `td.num`
  (ltr + unicode-bidi isolate) — otherwise minus signs and parentheses jump around.
- Hebrew final answers stay in Hebrew prose; keep formulas short, break long
  derivations into several `.mblock`s.
- No LaTeX/MathJax (WeasyPrint runs no JS) and **no literal emoji** in the HTML —
  the 💡 comes from CSS (`.insight .t::before` / `.bulb`), never from a typed
  character. Keep the `fonts/` folder next to the HTML (render.py sets `base_url`
  to the HTML's directory so `url('fonts/…')` resolves).

## Phase 4 — Render and visually QA (mandatory)

```bash
python3 scripts/render.py solution.html "פתרון_<שם>.pdf"
```

`render.py` renders with WeasyPrint and rasterizes pages with `pdftoppm`.
**View at least 2–3 rasterized pages yourself** and check:
- Hebrew reads right-to-left correctly; formulas not reversed/garbled.
- No overflowing `.mblock` (split long formulas if needed).
- Boxes not split awkwardly across pages; tables intact.
Fix and re-render until clean. Only then deliver the PDF (and keep the HTML
next to it — it's the editable source).

## Quality bar (self-check before delivering)

- [ ] Every sub-part answered, including bonuses.
- [ ] Every number re-verified in Python this session.
- [ ] Every question has a 💡 insight box.
- [ ] Assumptions stated for every test/CI; sided-ness justified.
- [ ] Data inconsistencies/garbles flagged in a `.warn` box, not silently fixed.
- [ ] Summary table + recurring-tricks section at the end.
- [ ] Visual QA of rendered pages performed.

## Examples

`examples/input/` contains three real Hebrew inputs (an exam, a theory exercise
sheet, a homework). `examples/output/` contains the corresponding solution
HTMLs and rendered PDFs — **match their structure, tone, and depth exactly.**
Highlights worth imitating:
- example1: bracketing p-values with the exam's percentile list; recovering a
  correlation from Var(X−Y); flagging a swapped mean/sd row in a `.warn` box.
- example2: formal-definition checking (equivariance), breakdown points,
  counterexample-first mindset in the insight boxes.
- example3: exact vs approximate Wilcoxon on the boundary; reconstructing
  Σx, Σx² to merge samples; reading a flipped RTL table via total-count checks.
