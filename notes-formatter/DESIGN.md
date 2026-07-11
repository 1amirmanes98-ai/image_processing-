# DESIGN.md — the authoring contract for `content.html`

This is the **model-facing spec**. When you transcribe a notebook you write a
single HTML *fragment* (`content.html`) using the classes below. `build_pdf.py`
wraps that fragment in `template/page.html.j2`, inlines `template/notes.css` +
KaTeX, and prints it to A4 via Chromium. You never write `<html>`/`<head>`/
`<body>` — only the content that goes **inside** `<main>`.

- Language/direction: the page is `dir="rtl" lang="he"`. Write Hebrew normally.
- Body font: **David Libre** (serif, Hebrew). Math: **KaTeX**.
- The document **title** is passed on the command line (`--title`) and only feeds
  `<title>` and the printed page footer. The *visible* title is authored by you,
  inside a `.hero` block (see below).

---

## 1. Math (KaTeX) and the bidi rules — READ THIS FIRST

KaTeX auto-render runs over the body. Delimiters:

| kind      | delimiters | example |
|-----------|------------|---------|
| inline    | `\( … \)`  | `לכל \(u,v \in V\) מתקיים…` |
| display   | `\[ … \]`  | `<div class="math">\[ \langle \varphi(v),u\rangle = \langle v,\varphi^*(u)\rangle \]</div>` |

Rules that keep RTL text and LTR math from fighting:

1. **Every display equation goes in `<div class="math"> \[ … \] </div>`.**
   `.math` forces `direction: ltr` and centers the formula.
2. **Inline math is fine inside a Hebrew sentence** — `.katex` is
   `unicode-bidi: isolate`, so it won't reorder the surrounding Hebrew.
3. **Wrap bare Latin / ASCII-symbol runs in `<span dir="ltr">…</span>`** when the
   punctuation around them flips. Examples that need it: variable names like
   `V`, `QR`, `A^t`, set literals `\(\mathbb{F}\in\{\mathbb{R},\mathbb{C}\}\)`,
   or any inline `\( … \)` that sits next to a comma/period. When in doubt,
   wrap it — `span[dir="ltr"]` is also `unicode-bidi: isolate`.
   ```html
   ההעתקה <span dir="ltr">\(\varphi^*: V \to V\)</span> היחידה המקיימת…
   ```
4. Never leave raw `\(`, `\)`, `\[`, `\]` visible — if you see them in the QA
   render, KaTeX failed (usually a LaTeX syntax error inside).

---

## 2. Page-1 header — `.hero`

A graph-paper card holding the eyebrow line, the title (blue underline),
a one-line subtitle, the `.legend`, and the `.abbrev` strip.

```html
<div class="hero">
  <div class="eyebrow">אלגברה לינארית · סיכום הרצאה · 11.07.2026</div>
  <h1>מרחבי מכפלה פנימית</h1>
  <div class="subtitle">העתקה צמודה, אוניטריות ונורמליות — ובדרך אל המשפט הספקטרלי.</div>

  <ul class="legend"> … </ul>       <!-- §7 -->
  <div class="abbrev"> … </div>     <!-- §8 -->
</div>
```

---

## 3. Callout boxes — `.box` + one variant

The **workhorse**. Base class `.box` plus exactly one colour variant. The pill
label is generated automatically from the variant; the box may also carry an
inline bold heading in `<span class="t">…</span>` that sits next to the pill.

| variant  | pill (default) | colour | use for |
|----------|----------------|--------|---------|
| `.def`   | הגדרה   | blue   | definitions |
| `.thm`   | משפט    | green  | theorems, claims, lemmas, corollaries, exercises |
| `.trick` | טריק    | purple | techniques, shortcuts, "how to check…" |
| `.note`  | דגש     | orange | emphasis / intuition the notebook stresses |
| `.warn`  | זהירות  | red    | pitfalls, "only true when…", common mistakes |
| `.bonus` | בונוס   | teal   | **anything you add beyond the notebook** (see §11) |

```html
<div class="box def">
  <span class="t">ההעתקה הצמודה</span>
  <p>ההעתקה <span dir="ltr">\(\varphi^*:V\to V\)</span> היא היחידה המקיימת</p>
  <div class="math">\[ \langle \varphi(v),u\rangle = \langle v,\varphi^*(u)\rangle \]</div>
</div>
```

**Relabelling the green box.** `.thm` defaults to "משפט". For a claim / corollary /
property / exercise, override with `data-label`:
```html
<div class="box thm" data-label="טענה">…</div>
<div class="box thm" data-label="מסקנה">…</div>
<div class="box thm" data-label="תכונות">…</div>
<div class="box thm" data-label="תרגיל">…</div>
```
`data-label` works on any variant, but keep the colour semantics (a warning is
always `.warn`, etc.).

**Modifiers:**
- `.tight` — compact one-liner box (e.g. a short bonus). `<div class="box bonus tight">…</div>`
- `.dashed` — dashed outline (e.g. "חלק חסר – להשלמה").
- `.imp` — flags the box as **important** with a red `#` corner badge (mirrors
  Amir's `#` mark). `<div class="box thm imp" data-label="טענה">…</div>`

---

## 4. Section headers — `.section-chip`

Auto-numbered dark navy badge on the leading (right) edge + bold title.
Numbering is automatic in document order (CSS counter). No manual numbers.

```html
<h2 class="section-chip">ההעתקה הצמודה \(\varphi^*\)</h2>
```
Use `.section-chip.no-num` for an unnumbered header (drops the badge).

---

## 5. Exercises — `.steps`

Numbered, step-by-step. The **final answer** gets `class="result"` (green ✓ badge).

```html
<ol class="steps">
  <li>מציגים את <span dir="ltr">\(\langle u,v\rangle\)</span> דרך ההגדרה…</li>
  <li>מפעילים את הגדרת הצמודה על <span dir="ltr">\(T^{-1}\)</span>…</li>
  <li class="result">לכן <span dir="ltr">\(S\equiv 0\)</span>. <strong>מש"ל.</strong></li>
</ol>
```

---

## 6. Topic map — `.topic-map`

A row of colour-coded column-cards (the "מפת נושא" on page 1). Each `.tm-col`
takes a colour variant (`.def/.thm/.trick/.bonus`) and a `.h` header. Bullets
support `.star` (gold ★) for emphasis and a `.tm-here` "אנחנו כאן" pill.

```html
<div class="topic-map">
  <div class="tm-col def">
    <div class="h">חלק I · יסודות</div>
    <ul>
      <li>אי־שוויון קושי–שוורץ</li>
      <li class="star">טריקי חישוב</li>
    </ul>
  </div>
  <div class="tm-col trick">
    <span class="tm-here">אנחנו כאן</span>
    <div class="h">חלק II · העתקות</div>
    <ul><li>ההעתקה הצמודה</li></ul>
  </div>
  <div class="tm-col thm">
    <div class="h">חלק III · לכסון</div>
    <ul><li class="star">המשפט הספקטרלי</li></ul>
  </div>
</div>
```

---

## 7. Legend — `.legend`

Bordered pills, each a coloured dot + label. Put it in the `.hero` on page 1.
Variant classes set the dot colour: `.def/.thm/.trick/.note/.warn/.bonus`, and
`.imp` renders the amber `#` chip.

```html
<ul class="legend">
  <li class="lg def">הגדרה</li>
  <li class="lg thm">משפט / טענה</li>
  <li class="lg trick">טריק</li>
  <li class="lg note">דגש</li>
  <li class="lg warn">זהירות</li>
  <li class="lg imp">חשוב במיוחד (כמו במחברת)</li>
  <li class="lg bonus">בונוס — תוספת מעבר למחברת</li>
</ul>
```

---

## 8. Abbreviations — `.abbrev`

A muted, middot-separated line. Preserve **Amir's own abbreviations** from the
notebook. `.lead` is the "קיצורים:" label; each `.ab` is one entry; `.t` bolds
the short form.

```html
<div class="abbrev">
  <span class="lead">קיצורים:</span>
  <span class="ab"><span class="t">מ"פ</span> = מכפלה פנימית</span>
  <span class="ab"><span class="t">א"נ</span> = אורתונורמלי</span>
</div>
```

---

## 9. Dictionary / comparison table — `.dict-table`

Dark header row, hairline borders, zebra rows. Use `<th scope="row">` for the
leading (rightmost) label column. Rows never split across pages.

```html
<table class="dict-table">
  <thead>
    <tr><th>המושג</th><th>מעל <span dir="ltr">\(\mathbb{R}\)</span></th><th>מעל <span dir="ltr">\(\mathbb{C}\)</span></th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">משמרת מ"פ</th>
        <td>אורתוגונלית: <span dir="ltr">\(A^{t}A=I\)</span></td>
        <td>אוניטרית: <span dir="ltr">\(A^{\dagger}A=I\)</span></td></tr>
  </tbody>
</table>
```

---

## 10. Formula sheet — `.formula-grid`

A grid of titled cards (default 2 columns; add `.cols-3` for 3). Each `.fcard`
has a colour variant, a `.ft` title, and a `.math` display formula.

```html
<div class="formula-grid">
  <div class="fcard def">
    <div class="ft">הגדרה</div>
    <div class="math">\[ \langle \varphi(v),u\rangle = \langle v,\varphi^*(u)\rangle \]</div>
  </div>
  <div class="fcard trick">
    <div class="ft">היפוך</div>
    <div class="math">\[ (T^{-1})^* = (T^*)^{-1} \]</div>
  </div>
</div>
```

---

## 11. Inline important marker — `.imp`

`<span class="imp">חשוב במיוחד</span>` renders an amber `# חשוב במיוחד` chip
inline in a sentence. Use it (or `.box.imp`) **only where the notebook itself
marks something important** (Amir's `#`).

---

## 12. Unclear handwriting — `.unclear`

When the handwriting is genuinely illegible, emit a **visible** dashed amber box.
**Never silently guess.** Transcribe what you can and flag the doubt.

```html
<div class="unclear">
  כאן במחברת מופיע ביטוי שלא ניתן לפענוח בוודאות — נראה כמו
  <span dir="ltr">\(\varphi^{\dagger}\)</span> אך ייתכן סימון אחר.
</div>
```

---

## Transcription-fidelity rules (non-negotiable)

1. **Preserve structure and order.** Follow the notebook's sequence of topics and
   sections. Don't reorganise into your own outline.
2. **`#` only where the notebook marks it.** Use `.imp` / `.box.imp` exclusively
   for things Amir flagged important — not for whatever *you* think matters.
3. **Additions live in bonus boxes only.** Any content beyond the notebook
   (extra intuition, a missing proof, "טיפים", "תבניות בי־לינאריות") goes in a
   `.box.bonus`, clearly marked as beyond-the-notebook. Never blend your own
   material into the transcribed flow unmarked.
4. **Never silently guess illegible handwriting.** Use `.unclear`. Leaving an
   `.unclear` unresolved is correct; a confident wrong guess is not.
5. **Keep Amir's abbreviations and notation** and surface them in `.abbrev` +
   `.legend`.
6. **Exercises are guided.** Use `.steps`, and highlight the final result with
   `.result`.
```
