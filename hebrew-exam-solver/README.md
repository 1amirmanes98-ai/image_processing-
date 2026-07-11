# hebrew-exam-solver — Claude Code agent for solving Hebrew math/stats exams

Turns an exam/homework PDF (Hebrew, RTL) into a polished, fully-explained
solution PDF with per-question insight boxes (💡).

## Install as a Claude Code skill

```bash
mkdir -p ~/.claude/skills
cp -r exam-solver ~/.claude/skills/hebrew-exam-solver
```
(or drop it into `.claude/skills/` inside a project). Claude Code reads
`SKILL.md` automatically when the task matches its description.

Alternative: paste SKILL.md's body into the project's `CLAUDE.md` if you prefer
a project-level agent instead of a skill.

## Usage

```
claude "solve the exam in ./exams/moedB.pdf, output a Hebrew solution PDF"
```
First run per machine: the agent runs `scripts/setup.sh` (WeasyPrint + David
Libre fonts + poppler). Everything is offline afterwards except the one-time
font download from github.com/google/fonts.

## Layout

```
SKILL.md               the agent prompt (the important file)
scripts/setup.sh       env setup + RTL smoke test
scripts/render.py      HTML -> PDF + QA page rasters
scripts/verify.py      numeric verification helpers (exact sign/Wilcoxon/McNemar,
                       paired t, CI, sample merging, chi-square, r from Var(X-Y))
                       — run `python3 scripts/verify.py` for self-tests
templates/template.html  the tuned RTL stylesheet + document skeleton
examples/input/        3 real Hebrew inputs (exam, theory sheet, homework)
examples/output/       the corresponding gold solutions (HTML sources + PDFs)
```

## The 4-phase pipeline the prompt enforces

1. **Read** — assume the PDF text layer garbles RTL tables; verify with
   consistency checks (totals, mean-of-diffs = diff-of-means).
2. **Solve** — everything first, every number verified in Python
   (exact tests for small n; scripts/verify.py).
3. **Write** — template.html structure: stmt → steps → final → 💡 insight,
   ending with a conclusions table + recurring-tricks summary.
4. **Render & QA** — WeasyPrint, then actually LOOK at rasterized pages.

## Extending

- New course conventions (plotting positions, table usage): add a bullet under
  Phase 2 in SKILL.md.
- New question types: add a verified helper to scripts/verify.py **with a
  self-test**, and ideally a gold example pair under examples/.
