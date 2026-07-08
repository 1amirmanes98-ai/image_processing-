# image_processing-
An automated image processing framework focused on feature extraction and computer vision. This project leverages deep learning models and traditional CV techniques to automate the detection, segmentation, and classification of visual data. Built for high-performance analysis and real-time application.

## 🎓 FODL Exam Tutor

This repo also hosts a personal exam-prep agent for **Foundations of Deep Learning**
(TAU 03683080) — open a Claude Code session here and run `/progress` to start studying.
See [`dl-exam-agent/README.md`](dl-exam-agent/README.md).

**The study site** (all 12 past exams translated with solution sketches, 4 generated
mock exams, flashcards, quizzes, a 56-item memorization cheat sheet, computed concept
figures, and full-site search): https://1amirmanes98-ai.github.io/image_processing-/

## 📊 Intro to Statistics Exam Tutor

Same framework, second course: a personal exam-prep agent for **Intro to Statistics**
(TAU 0365.1813, Prof. Ruth Heller), built from the course summary, lecture slides, and
**19 past finals (2012–2025)**. See
[`stats-exam-agent/README.md`](stats-exam-agent/README.md).

**The study site**: https://1amirmanes98-ai.github.io/image_processing-/stats/

## 🔁 Build this for YOUR course

**Read [`REPLICATION.md`](REPLICATION.md) first** — it is the exact playbook with
per-phase token budgets and the cost traps to avoid (a naive replication burns ~2M
tokens; the playbook route costs ~400–800k). The scripts are course-agnostic: copy
them verbatim and put all course specifics in `index/SITE_CONFIG.json`.

The short version:

1. **Create your own repo** (don't fork this one — you want your course, not mine).
2. **Open a Claude Code session** on your repo ([claude.ai/code](https://claude.ai/code)),
   and upload two zips: your course materials (lectures/recitations/homework PDFs) and
   your past exams.
3. **Say:** *"Build me an exam-prep agent and study site like
   `1amirmanes98-ai/image_processing-` — read that repo's README, `dl-exam-agent/`
   layout, `scripts/build_site.py` + `scripts/site_template.html`, and
   `.github/workflows/pages.yml`, then replicate the whole pipeline for my course
   from my uploaded materials."*
4. Claude will index your materials (topics, per-exam question maps, solution
   sketches), set up the tutor skills (`/teach`, `/quiz`, `/exam`, …), build the
   single-file study site, and wire GitHub Pages so it publishes on every push.

What makes it work well, in one line each: ground every claim in the actual course
PDFs (never from memory); analyze all past exams for recurring question archetypes;
generate mock exams only after solving them; audit everything adversarially against
the sources; keep raw course content out of git unless you're allowed to publish it
(see `.gitignore` — publish only derived/original content, and check your course's
policy).
