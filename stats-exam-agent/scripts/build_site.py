#!/usr/bin/env python3
"""Build the Intro to Statistics Study Hub single-file site from the study index.

Usage: python3 build_site.py <index_dir> <libs_dir> <template.html> <out.html> [docs_out.html]

e.g. python3 stats-exam-agent/scripts/build_site.py stats-exam-agent/index /tmp/site-libs \
       stats-exam-agent/scripts/site_template.html /tmp/stats-study-hub.html docs/stats/index.html

Parses index/exams/*.md, index/lectures/*.md, index/TOPICS.md, index/EXAM_MAP.md,
index/CHEATSHEET.md and generated_exams/*.md into JSON, inlines KaTeX/marked (fonts
as data URIs), and injects everything into the template's placeholders: __DATA__,
__KATEX_CSS__, __KATEX_JS__, __AUTORENDER_JS__, __MARKED_JS__.

Libs (KaTeX 0.16.11 + marked 12.0.2 + woff2 fonts) are fetched per the README:
stats-exam-agent/README.md § "The Study Hub website".
"""
import base64
import json
import re
import sys
from collections import Counter
from pathlib import Path

# The four course pillars (weeks 1-4 / 5-6 / 7-8 / 9-11).
PILLAR_CANON = {
    "descriptive": "Descriptive",
    "estimation": "Estimation",
    "testing": "Testing",
    "twosample": "TwoSample",
    "two-sample": "TwoSample",
    "two sample": "TwoSample",
    "categorical": "TwoSample",
    "nonparametric": "TwoSample",
    "paired": "TwoSample",
}


def canon_pillar(raw: str) -> str:
    raw = (raw or "").strip().lower()
    for k, v in PILLAR_CANON.items():
        if k in raw:
            return v
    return "Practices"


def parse_exam(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    exam_id = path.stem.replace("stats_exam_", "")
    head = text.split("\n## ", 1)[0]

    def meta(pattern):
        m = re.search(pattern, head, re.IGNORECASE)
        return m.group(1).strip() if m else ""

    exam = {
        "id": exam_id,
        "title": text.splitlines()[0].lstrip("# ").strip(),
        "date": meta(r"\*\*Date\s*/\s*semester:\*\*\s*(.+)"),
        "total": meta(r"\*\*Total points:\*\*\s*(\d+)"),
        "questions": [],
    }
    # question blocks start with "## Q"
    for block in re.split(r"\n(?=## Q)", text):
        m = re.match(r"## Q(\d+)\s*\((\d+)\s*pts?\)\s*[—-]\s*(.+)", block)
        if not m:
            continue
        qnum, pts, title = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        topics_m = re.search(r"\*\*Topics:\*\*\s*(.+?)(?:\||\n)", block)
        pillar_m = re.search(r"\*\*Pillar:\*\*\s*([A-Za-z/ -]+)", block)
        diff_m = re.search(r"\*\*Difficulty:\*\*\s*(\d)", block)
        maps_m = re.search(r"\*\*Maps to:\*\*\s*(.+)", block)
        stmt, sketch = "", ""
        sm = re.search(
            r"\*\*Statement[^:]*:\*\*\s*\n(.*?)(?=\n\*\*Solution sketch|\Z)",
            block, re.DOTALL)
        if sm:
            stmt = sm.group(1).strip()
        km = re.search(r"\*\*Solution sketch[^:]*:\*\*\s*\n(.*)", block, re.DOTALL)
        if km:
            sketch = km.group(1).strip()
        exam["questions"].append({
            "n": qnum,
            "pts": pts,
            "title": title,
            "topics": [t.strip() for t in topics_m.group(1).split(",")] if topics_m else [],
            "pillar": canon_pillar(pillar_m.group(1) if pillar_m else ""),
            "difficulty": int(diff_m.group(1)) if diff_m else 0,
            "maps_to": maps_m.group(1).strip() if maps_m else "",
            "statement": stmt,
            "sketch": sketch,
        })
    return exam


CARD_ITEM_RE = re.compile(
    r"^(?:[-*]\s*)?\*\*\s*(Def|Definition|Thm|Theorem|Lem|Lemma|Prop|Proposition|Cor|Corollary)\b",
    re.IGNORECASE)


def split_items(section: str) -> list:
    """Split a Key definitions / Key theorems section into items that each start
    with a bold Def/Thm/... marker line."""
    items, cur = [], []
    for line in section.splitlines():
        if CARD_ITEM_RE.match(line.strip()):
            if cur:
                items.append("\n".join(cur).strip())
            cur = [line]
        elif cur:
            cur.append(line)
    if cur:
        items.append("\n".join(cur).strip())
    return [i for i in items if len(i) > 20]


def note_sort_key(path: Path):
    """week_01..week_10 first (course order), then slides_07..slides_11."""
    m = re.match(r"(week|slides)_(\d+)", path.stem)
    if not m:
        return (2, 0, path.stem)
    return (0 if m.group(1) == "week" else 1, int(m.group(2)), path.stem)


def parse_lecture(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    name = path.stem
    title = text.splitlines()[0].lstrip("# ").strip()
    pm = re.search(r"\*\*Pillar:\*\*\s*([A-Za-z/ -]+)", text)
    pillar = canon_pillar(pm.group(1) if pm else "")
    sections = {}
    for m in re.finditer(r"\n## +(.+?)\n(.*?)(?=\n## |\Z)", text, re.DOTALL):
        sections[m.group(1).strip().lower()] = m.group(2)
    cards = []
    for sec_key, kind in ((("key definitions",), "def"),
                          (("key theorems & results", "key theorems"), "thm")):
        sec = ""
        for k in sec_key:
            for name_l, body in sections.items():
                if name_l.startswith(k):
                    sec = body
                    break
            if sec:
                break
        for item in split_items(sec):
            # front = the bold lead (name); back = the whole item
            fm = re.match(r"(?:[-*]\s*)?\*\*(.+?)\*\*", item)
            front = fm.group(1).strip().rstrip(".") if fm else item[:80]
            cards.append({
                "kind": kind,
                "front": front,
                "back": item,
                "lecture": name,
                "lecture_title": title,
                "pillar": pillar,
            })
    return {"name": name, "title": title, "pillar": pillar, "cards": cards}


def read_note(path: Path) -> dict:
    """Read a full index note (week chapter / slide deck) into titled sections."""
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    pm = re.search(r"\*\*Pillar:\*\*\s*([A-Za-z/ -]+)", text)
    head = text.split("\n## ", 1)[0]
    intro = "\n".join(l for l in head.splitlines()[1:] if l.strip())
    sections = [{"h": "About", "b": intro}] if intro else []
    for m in re.finditer(r"\n## +(.+?)\n(.*?)(?=\n## |\Z)", text, re.DOTALL):
        sections.append({"h": m.group(1).strip(), "b": m.group(2).strip()})
    kind = "slides" if path.stem.startswith("slides") else "week"
    return {"name": path.stem, "kind": kind, "title": title,
            "pillar": canon_pillar(pm.group(1) if pm else ""), "sections": sections}


def resolve_refs(taught: str, note_names: list) -> list:
    """Map the free-text 'taught in' column to actual note file names
    (week_01..week_10, slides_07..slides_11; tolerate 'week 5' style)."""
    refs, low = [], taught.lower()
    for name in note_names:
        m = re.match(r"(week|slides)_(\d+)", name)
        if not m:
            if name in low:
                refs.append(name)
            continue
        kind, num = m.group(1), int(m.group(2))
        if re.search(rf"{kind}[_ ]0*{num}\b", low):
            refs.append(name)
    return refs


def parse_exam_refs(examined: str) -> list:
    """Parse 'a2025_Q1, b2013_Q3' style refs into [examId, qnum] pairs."""
    out = []
    for m in re.finditer(r"\b([ab])[_ ]?(\d{4})[_ ]?Q(\d)", examined):
        out.append([f"{m.group(1)}_{m.group(2)}", int(m.group(3))])
    return out


def parse_topics(path: Path, note_names: list) -> list:
    """Parse TOPICS.md pillar tables into topic rows with machine-readable refs."""
    text = path.read_text(encoding="utf-8")
    out = []
    for pm in re.finditer(r"\n## Pillar \d+ — (\w+).*?\n(.*?)(?=\n## |\Z)", text, re.DOTALL):
        pillar = canon_pillar(pm.group(1))
        for row in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(🔴|🟠|🟡)\s*\|",
                               pm.group(2), re.MULTILINE):
            topic, taught, examined, prio = (row.group(i).strip() for i in range(1, 5))
            if topic.lower() == "topic" or set(topic) <= {"-", " ", ":"}:
                continue
            out.append({"pillar": pillar, "topic": topic, "taught": taught,
                        "examined": examined,
                        "taught_refs": resolve_refs(taught, note_names),
                        "exam_refs": parse_exam_refs(examined),
                        "priority": {"🔴": "core", "🟠": "frequent", "🟡": "seen"}[prio]})
    return out


def parse_archetypes(path: Path, exams: list) -> list:
    """Parse the numbered archetype list in EXAM_MAP.md. Each archetype's pillar =
    majority pillar of the exam questions it references."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"## Recurring question archetypes.*?\n(.*?)(?=\n## |\nNote|\Z)", text, re.DOTALL)
    if not m:
        return []
    qpillar = {(e["id"], q["n"]): q["pillar"] for e in exams for q in e["questions"]}
    out = []
    for im in re.finditer(r"^\d+\.\s+(.*?)(?=^\d+\.|\Z)", m.group(1), re.DOTALL | re.MULTILINE):
        item = " ".join(im.group(1).split())
        name_m = re.match(r"\*\*(.+?)\*\*", item)
        refs = parse_exam_refs(item)
        pillars = Counter(qpillar.get((eid, qn)) for eid, qn in refs if qpillar.get((eid, qn)))
        out.append({
            "name": name_m.group(1) if name_m else item[:60],
            "desc": item,
            "count": len(refs),
            "pillar": pillars.most_common(1)[0][0] if pillars else "Practices",
        })
    return out


MOCK_Q_RE = re.compile(r"^## Q(?:uestion)?\s*(\d+)\s*\((\d+)\s*pts?\)\s*[—-]\s*(.+)$",
                       re.MULTILINE)


def parse_mock(path: Path) -> dict:
    """Parse a generated mock exam (stats-exam-agent/generated_exams/mock_exam_NN.md).

    Format contract: questions start with '## Question N (P pts) — Title'; the body
    may carry a '**Topics:** ... | **Pillar:** X | ...' meta line (recommended); the
    sibling file <stem>_solutions.md holds rubric blocks starting '## QN'.
    """
    text = path.read_text(encoding="utf-8")
    sol_path = path.with_name(path.stem + "_solutions.md")
    solutions = {}
    if sol_path.exists():
        stext = sol_path.read_text(encoding="utf-8")
        for m in re.finditer(r"^## Q(?:uestion)?\s*(\d+)[^\n]*\n(.*?)(?=^## |\Z)",
                             stext, re.MULTILINE | re.DOTALL):
            solutions[int(m.group(1))] = m.group(2).strip()
    num = re.search(r"(\d+)", path.stem)
    exam = {"id": "mock_" + (num.group(1) if num else path.stem), "mock": True,
            "title": text.splitlines()[0].lstrip("# ").strip(),
            "date": "", "total": "100", "questions": []}
    dm = re.search(r"generated ([0-9-]+)", text)
    if dm:
        exam["date"] = "Generated by your tutor on " + dm.group(1)
    tm = re.search(r"\*\*Total points:\*\*\s*(\d+)", text)
    if tm:
        exam["total"] = tm.group(1)
    heads = list(MOCK_Q_RE.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        qnum = int(m.group(1))
        body = text[m.end():end].strip().strip("-— \n")
        pillar_m = re.search(r"\*\*Pillar:\*\*\s*([A-Za-z/ -]+)", body)
        topics_m = re.search(r"\*\*Topics:\*\*\s*(.+?)(?:\||\n)", body)
        diff_m = re.search(r"\*\*Difficulty:\*\*\s*(\d)", body)
        # strip the meta line from the displayed statement
        body = re.sub(r"^\*\*Topics:\*\*.*$", "", body, count=1, flags=re.MULTILINE).strip()
        exam["questions"].append({
            "n": qnum, "pts": int(m.group(2)), "title": m.group(3).strip(),
            "topics": [t.strip() for t in topics_m.group(1).split(",")] if topics_m else [],
            "pillar": canon_pillar(pillar_m.group(1)) if pillar_m else "Testing",
            "difficulty": int(diff_m.group(1)) if diff_m else 0, "maps_to": "",
            "statement": body, "sketch": solutions.get(qnum, ""),
        })
    return exam


def parse_cheatsheet(path: Path):
    """Parse CHEATSHEET.md (### items with **Statement/Use it when/Seen in/Watch out**)."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    head = text.split("\n## ", 1)[0].splitlines()
    out = {"title": head[0].lstrip("# ").strip(),
           "intro": " ".join(l.strip() for l in head[1:] if l.strip()), "sections": []}
    for m in re.finditer(r"\n## +(.+?)\n(.*?)(?=\n## |\Z)", text, re.DOTALL):
        sec = {"name": m.group(1).strip(), "items": []}
        body = m.group(2)
        for im in re.finditer(r"\n### +(.+?)\n(.*?)(?=\n### |\Z)", "\n" + body, re.DOTALL):
            item = {"name": im.group(1).strip()}
            for key, field in (("Statement", "statement"), ("Use it when", "use"),
                               ("Seen in", "seen"), ("Watch out", "watch")):
                km = re.search(r"\*\*" + key + r":\*\*\s*(.*?)(?=\n\*\*[A-Z]|\Z)",
                               im.group(2), re.DOTALL)
                if km:
                    item[field] = km.group(1).strip()
            if item.get("statement"):
                sec["items"].append(item)
        if sec["items"]:
            out["sections"].append(sec)
    return out


def inline_katex_css(css: str, fonts_dir: Path) -> str:
    """Replace font urls with woff2 data URIs; drop woff/ttf fallbacks."""
    def repl(m):
        fname = m.group(1)
        p = fonts_dir / fname
        if fname.endswith(".woff2") and p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f"url(data:font/woff2;base64,{b64}) format('woff2')"
        return "url(data:,)"  # dead fallback source, woff2 always wins first

    css = re.sub(r"url\(fonts/([^)]+)\)\s*format\(['\"][^'\"]+['\"]\)", repl, css)
    return css


def main():
    index_dir, libs_dir, template_p, out_p = (Path(a) for a in sys.argv[1:5])

    def exam_key(e):
        parts = e["id"].split("_")
        return (parts[1], parts[0]) if len(parts) == 2 else (e["id"], "")

    exams = sorted((parse_exam(p) for p in (index_dir / "exams").glob("*.md")), key=exam_key)
    gen_dir = index_dir.parent / "generated_exams"
    mocks = sorted((parse_mock(p) for p in gen_dir.glob("*.md")
                    if not p.stem.endswith("_solutions")),
                   key=lambda e: e["id"]) if gen_dir.exists() else []
    note_paths = sorted((index_dir / "lectures").glob("*.md"), key=note_sort_key)
    lectures = [parse_lecture(p) for p in note_paths]
    cards = [c for l in lectures for c in l["cards"]]
    notes = [read_note(p) for p in note_paths]
    topics = parse_topics(index_dir / "TOPICS.md", [n["name"] for n in notes])
    archetypes = parse_archetypes(index_dir / "EXAM_MAP.md", exams)

    cheat = parse_cheatsheet(index_dir / "CHEATSHEET.md")
    data = {"exams": exams, "mocks": mocks, "cards": cards, "topics": topics,
            "archetypes": archetypes, "notes": notes, "cheatsheet": cheat,
            "lectures": [{"name": l["name"], "title": l["title"], "pillar": l["pillar"],
                          "n_cards": len(l["cards"])} for l in lectures]}

    html = template_p.read_text(encoding="utf-8")
    kcss = inline_katex_css((libs_dir / "katex.min.css").read_text(encoding="utf-8"),
                            libs_dir / "fonts")
    kjs = (libs_dir / "katex.min.js").read_text(encoding="utf-8")
    # KaTeX hard-refuses to render in quirks mode (page served without a doctype,
    # e.g. the artifact viewer or the raw standalone file). Rendering there is fine
    # in practice — neutralize the guard so math never falls back to raw TeX.
    guard = '"CSS1Compat"!==document.compatMode'
    assert guard in kjs, "KaTeX quirks-mode guard not found — check katex version"
    kjs = kjs.replace(guard, "!1")
    payload = json.dumps(data, ensure_ascii=False)
    # JSON goes inside a <script type="application/json"> tag — escape closers.
    payload = payload.replace("</", "<\\/")
    for k, v in (("__KATEX_CSS__", kcss),
                 ("__KATEX_JS__", kjs),
                 ("__AUTORENDER_JS__", (libs_dir / "auto-render.min.js").read_text(encoding="utf-8")),
                 ("__MARKED_JS__", (libs_dir / "marked.min.js").read_text(encoding="utf-8")),
                 ("__DATA__", payload)):
        assert k in html, f"placeholder {k} missing from template"
        html = html.replace(k, v)
    out_p.write_text(html, encoding="utf-8")
    # Standalone copy for direct sharing: a complete standards-mode document.
    wrapped = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width, initial-scale=1">'
               "</head><body>" + html + "</body></html>")
    standalone = out_p.with_name(out_p.stem + "-standalone.html")
    standalone.write_text(wrapped, encoding="utf-8")
    # Optional 5th arg: also refresh the GitHub Pages copy (docs/stats/index.html) —
    # pushing it (on main) triggers .github/workflows/pages.yml to redeploy the site.
    if len(sys.argv) > 5:
        docs_p = Path(sys.argv[5])
        docs_p.parent.mkdir(parents=True, exist_ok=True)
        docs_p.write_text(wrapped, encoding="utf-8")
    n_q = sum(len(e["questions"]) for e in exams)
    n_refs = sum(len(t["taught_refs"]) for t in topics)
    n_erefs = sum(len(t["exam_refs"]) for t in topics)
    n_cheat = sum(len(s["items"]) for s in cheat["sections"]) if cheat else 0
    print(f"cheatsheet_items={n_cheat}")
    print(f"exams={len(exams)} mocks={len(mocks)} "
          f"mock_questions={sum(len(m['questions']) for m in mocks)} "
          f"questions={n_q} cards={len(cards)} "
          f"topics={len(topics)} taught_refs={n_refs} exam_refs={n_erefs} "
          f"notes={len(notes)} archetypes={len(archetypes)} "
          f"out={out_p} ({out_p.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
