# Intro to Statistics Exam Tutor 🎓

A personal exam-prep agent for **Intro to Statistics** (TAU 0365.1813, Prof. Ruth
Heller), built from the course's written summary (weeks 1–10), the lecture slide
decks (7–11), and **19 past finals (2012–2025)** — all indexed, translated, and
tagged by topic. Five of the exams include official solutions.

## How to use it

Open a Claude Code session on this repo (claude.ai/code, the app, or the CLI) and just
talk, or use the skills (shared with the FODL tutor — they detect the course):

| Command | What it does |
|---|---|
| `/progress` | Dashboard: days to exam, coverage, weak spots, and a study plan. **Start here** — it will ask for your exam date. |
| `/teach <topic>` | Interactive lesson: intuition → precise definitions/formulas → mini-checks → where it appeared in past exams. |
| `/quiz [topic]` | Adaptive graded quiz, one question at a time, real point values. |
| `/exam past a_2024` | Take a real past exam under exam conditions, strictly graded /100. |
| `/exam new` | A freshly generated mock exam in the exact real format. |
| `/solve b_2023 2` | Socratic walkthrough of a specific past-exam question. |
| `/drill <topic>` | Brand-new exam-style exercises on a topic (novel variants of past patterns). |
| `/flashcards [topic]` | Rapid-fire definitions/formulas drill (feeds your two allowed formula pages). |

Free-form works too: *"when do I use Wilson instead of Wald?"*, *"test me on power
calculations"*, *"מה ההבדל בין מבחן וילקוקסון למבחן פרמוטציות?"* — the tutor answers
from the course materials and cites the week/exam it came from.

## What's inside

```
stats-exam-agent/
├── AGENT.md          # the tutor's operating manual (persona, rules, protocols)
├── progress.md       # your study memory: scores, weak spots, exams taken
├── index/            # the tutor's brain — generated from the PDFs
│   ├── TOPICS.md     #   topic map with exam-frequency stats
│   ├── EXAM_MAP.md   #   every past-exam question: points, topics, difficulty + archetypes
│   ├── CHEATSHEET.md #   the ~50 items that belong on your two formula pages
│   ├── exams/        #   full English translations + solution sketches per exam
│   └── lectures/     #   per-week notes (week_*) + slide-deck notes (slides_*)
├── generated_exams/  # tutor-generated mock exams + sealed rubrics (tracked in git)
└── materials/        # original course PDFs (ground truth) + text mirrors
```

Progress persists because the tutor commits `progress.md` at the end of each study
session — so every new session knows where you left off.

## ⚠️ First thing in every new session: restore the content

By your choice, the course PDFs and the generated `index/` are **not stored on GitHub**
(the repo is public). Keep **`stats-tutor-content.zip`** (Claude sent it to you on
2026-07-07) somewhere safe. When you start a fresh session:

1. Attach `stats-tutor-content.zip` to the chat.
2. Say "restore my statistics study content" — the tutor runs
   `bash stats-exam-agent/scripts/restore_content.sh <zip>` and you're ready to go.

(If you ever make the repo private, tell the tutor "commit the course content" once —
then you can drop the zip ritual forever. The `.gitignore` entries for
`stats-exam-agent/materials/` and `stats-exam-agent/index/` are the only thing to
remove.)

## The Study Hub website

A single-file interactive study site (dashboard with the exam template, topic map with
inline past-exam questions, all 19 exams with sealed solution sketches, flashcards,
quiz, memorization cheat sheet, and full-site search) is published at:

**https://1amirmanes98-ai.github.io/image_processing-/stats/**

To rebuild it after the index changes (needs restored content + internet for the
KaTeX/marked libs):

```bash
L=/tmp/site-libs; mkdir -p $L/fonts
for f in katex.min.js katex.min.css contrib/auto-render.min.js; do
  curl -sL "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/$f" -o "$L/$(basename $f)"; done
curl -sL "https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js" -o "$L/marked.min.js"
# fonts: KaTeX_{Main-{Regular,Bold,Italic,BoldItalic},Math-{Italic,BoldItalic},Size{1..4}-Regular,AMS-Regular,Caligraphic-Regular,Typewriter-Regular}.woff2
python3 stats-exam-agent/scripts/build_site.py stats-exam-agent/index $L \
  stats-exam-agent/scripts/site_template.html /tmp/stats-study-hub.html docs/stats/index.html
```

Then commit + push `docs/stats/index.html` — `.github/workflows/pages.yml` redeploys
the site automatically (deploys run from `main`; side-branch pushes need a merge to
`main` first).

Site progress (flashcard/quiz stats, memorize checkboxes, exam date) lives in each
browser's localStorage — separate from the tutor's `progress.md`.
