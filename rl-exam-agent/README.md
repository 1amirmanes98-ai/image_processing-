# rl-exam-agent

A personal exam-prep system for **Reinforcement Learning** (TAU 0368.3075, Prof. Yishay
Mansour): a grounded tutor agent + a single-file interactive study website. Sibling of
`dl-exam-agent/`; built by replicating the template per the repo's `REPLICATION.md`.

## Layout

```
rl-exam-agent/
  AGENT.md                 # the tutor's operating manual — read first for study sessions
  progress.md              # study memory between sessions (tracked in git)
  index/                   # the generated study index (gitignored except SITE_CONFIG.json)
    SITE_CONFIG.json       # course-specific site config (tracked; code, not content)
    TOPICS.md              # topic map with per-pillar exam-frequency tables
    EXAM_MAP.md            # master table of all past questions + recurring archetypes
    lectures/*.md          # per-lecture notes (definitions, theorems, techniques, nuggets)
    recitations/*.md       # per-recitation worked problems
    exams/*.md             # every past-exam question, translated, tagged, with solutions
    exercise_bank/*.md     # the RL question booklet, cataloged by topic
  materials/               # original PDFs / slide decks + text mirrors (gitignored)
  generated_exams/         # tutor-generated mock exams (mock_exam_NN.md + _solutions.md)
  scripts/                 # build + restore tooling (copied verbatim from the template)
```

Course pillars (4): **Planning** · **Learning** · **Approximation** · **Bandits**.
The exam template is stable — Q1 Planning (model an MDP), Q3 Approximation (policy
gradient), Q4 Planning (contraction proof) are near-guaranteed; Q2 is the swing
(Learning / a 2nd Planning / Bandits). See `index/TOPICS.md` and `index/EXAM_MAP.md`.

## Content bootstrap (fresh clone)

`materials/` and `index/` are gitignored (course content stays off the public repo). To
restore them from the local content zip:

```bash
bash rl-exam-agent/scripts/restore_content.sh <path-to-rl-tutor-content.zip>
```

It prints counts to verify (expect 35 PDFs, 12 slide decks, 47 text mirrors).
`progress.md` and `index/SITE_CONFIG.json` are tracked, so study memory and the site
config survive without the zip.

## The Study Hub website

A single-file interactive study site (exam browser, topic map, flashcards, quiz, "Ask"
search, mock exams) published to GitHub Pages at `docs/rl/index.html`. To rebuild after
the index changes (needs restored content + internet for the KaTeX/marked libs):

```bash
L=/tmp/site-libs; mkdir -p $L/fonts
for f in katex.min.js katex.min.css contrib/auto-render.min.js; do
  curl -sL "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/$f" -o "$L/$(basename $f)"; done
curl -sL "https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js" -o "$L/marked.min.js"
# fonts: KaTeX_{Main-{Regular,Bold,Italic,BoldItalic},Math-{Italic,BoldItalic},Size{1..4}-Regular,AMS-Regular,Caligraphic-Regular,Typewriter-Regular}.woff2
python3 rl-exam-agent/scripts/build_site.py rl-exam-agent/index $L \
  rl-exam-agent/scripts/site_template.html /tmp/rl-study-hub.html docs/rl/index.html
```

Then verify once in headless Chromium (zero console errors; KaTeX renders in quirks mode;
no console errors on an exam page) and commit the rebuilt `docs/rl/index.html`.
`.github/workflows/pages.yml` redeploys from `main` on any push touching `docs/`.

`scripts/build_site.py` and `scripts/site_template.html` are course-agnostic — all course
specifics live in `index/SITE_CONFIG.json`. The one course-shaped edit made here was
first-class support for a **4th pillar** (the template ships tuned for 3 + a catch-all);
that change is generic and keyed off `CONFIG.slots`, not RL-specific names.

Site progress (flashcard/quiz stats, exam date) lives in each browser's localStorage —
separate from the tutor's `progress.md`.
