# FODL Exam Tutor 🎓

A personal exam-prep agent for **Foundations of Deep Learning** (TAU 03683080,
Dr. Nadav Cohen), built from the course's 9 lectures, 9 recitations, 4 homework sets,
and **12 past exams (2020–2024)** — all indexed, translated, and tagged by topic.

## How to use it

Open a Claude Code session on this repo (claude.ai/code, the app, or the CLI) and just
talk, or use the skills:

| Command | What it does |
|---|---|
| `/progress` | Dashboard: days to exam, coverage, weak spots, and a study plan. **Start here** — it will ask for your exam date. |
| `/teach <topic>` | Interactive lesson: intuition → precise definitions/theorems → mini-checks → where it appeared in past exams. |
| `/quiz [topic]` | Adaptive graded quiz, one question at a time, real point values. |
| `/exam past a_2023` | Take a real past exam under exam conditions, strictly graded /105. |
| `/exam new` | A freshly generated mock exam in the exact real format. |
| `/solve a_2024 2` | Socratic walkthrough of a specific past-exam question. |
| `/drill <topic>` | Brand-new exam-style exercises on a topic (novel variants of past patterns). |
| `/flashcards [topic]` | Rapid-fire definitions/theorems drill (no formula sheet on the exam!). |

Free-form works too: *"why does gradient flow on deep matrix factorization prefer low
rank?"*, *"test me on uniform convergence"*, *"מה ההבדל בין VC ל-Rademacher?"* —
the tutor answers from the course materials and cites the lecture/exam it came from.

## What's inside

```
dl-exam-agent/
├── AGENT.md          # the tutor's operating manual (persona, rules, protocols)
├── progress.md       # your study memory: scores, weak spots, exams taken
├── index/            # the tutor's brain — generated from the PDFs
│   ├── TOPICS.md     #   topic map with exam-frequency stats
│   ├── EXAM_MAP.md   #   every past-exam question: points, topics, difficulty
│   ├── exams/        #   full English translations + solution sketches per exam
│   ├── lectures/     #   per-lecture: definitions, theorems, proof ideas, traps
│   ├── recitations/  #   per-recitation: worked problems and techniques
│   └── homework/     #   homework problem summaries
└── materials/        # original course PDFs (ground truth) + text mirrors
```

Progress persists because the tutor commits `progress.md` at the end of each study
session — so every new session knows where you left off.

## ⚠️ First thing in every new session: restore the content

By your choice, the course PDFs and the generated `index/` are **not stored on GitHub**
(the repo is public). Keep **`fodl-tutor-content.zip`** (Claude sent it to you on
2026-07-06) somewhere safe. When you start a fresh session:

1. Attach `fodl-tutor-content.zip` to the chat.
2. Say "restore my study content" — the tutor runs
   `bash dl-exam-agent/scripts/restore_content.sh <zip>` and you're ready to go.

(If you ever make the repo private, tell the tutor "commit the course content" once —
then you can drop the zip ritual forever. The `.gitignore` entries for
`dl-exam-agent/materials/` and `dl-exam-agent/index/` are the only thing to remove.)
