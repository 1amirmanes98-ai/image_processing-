#!/usr/bin/env python3
"""Build the FODL Study Hub single-file site from the study index.

Usage: python3 build_site.py <index_dir> <libs_dir> <template.html> <out.html>

Parses index/exams/*.md, index/lectures/*.md, index/TOPICS.md, index/EXAM_MAP.md
into JSON, inlines KaTeX/marked (fonts as data URIs), and injects everything into
the template's placeholders: __DATA__, __KATEX_CSS__, __KATEX_JS__,
__AUTORENDER_JS__, __MARKED_JS__.
"""
import base64
import json
import re
import sys
from pathlib import Path

PILLAR_CANON = {
    "expressiveness": "Expressiveness",
    "optimization": "Optimization",
    "generalization": "Generalization",
    "practices": "Practices",
}


def canon_pillar(raw: str) -> str:
    raw = (raw or "").strip().lower()
    for k, v in PILLAR_CANON.items():
        if k in raw:
            return v
    return "Practices"


def parse_exam(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    exam_id = path.stem.replace("fodl_exam_", "")
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
        pillar_m = re.search(r"\*\*Pillar:\*\*\s*([A-Za-z/ ]+)", block)
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


def parse_lecture(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    name = path.stem
    title = text.splitlines()[0].lstrip("# ").strip()
    pm = re.search(r"\*\*Pillar:\*\*\s*([A-Za-z/ ]+)", text)
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


def parse_topics(path: Path) -> list:
    """Parse TOPICS.md pillar tables into topic rows."""
    text = path.read_text(encoding="utf-8")
    out = []
    for pm in re.finditer(r"\n## Pillar \d+ — (\w+).*?\n(.*?)(?=\n## |\Z)", text, re.DOTALL):
        pillar = canon_pillar(pm.group(1))
        for row in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(🔴|🟠|🟡)\s*\|",
                               pm.group(2), re.MULTILINE):
            topic, taught, examined, prio = (row.group(i).strip() for i in range(1, 5))
            if topic.lower() == "topic" or set(topic) <= {"-", " "}:
                continue
            out.append({"pillar": pillar, "topic": topic, "taught": taught,
                        "examined": examined,
                        "priority": {"🔴": "core", "🟠": "frequent", "🟡": "seen"}[prio]})
    return out


def parse_archetypes(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"## Recurring question archetypes.*?\n(.*?)(?=\nNote|\Z)", text, re.DOTALL)
    if not m:
        return []
    out = []
    for im in re.finditer(r"^\d+\.\s+(.*?)(?=^\d+\.|\Z)", m.group(1), re.DOTALL | re.MULTILINE):
        item = " ".join(im.group(1).split())
        name_m = re.match(r"\*\*(.+?)\*\*", item)
        refs = re.findall(r"\b([abc]_?\d{4}|example)[ _]?Q?(\d)?", item)
        out.append({
            "name": name_m.group(1) if name_m else item[:60],
            "desc": item,
            "count": len(re.findall(r"Q\d", item)),
        })
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
    exams = sorted((parse_exam(p) for p in (index_dir / "exams").glob("*.md")),
                   key=lambda e: (e["id"].split("_")[-1], e["id"]))
    lectures = [parse_lecture(p) for p in sorted((index_dir / "lectures").glob("*.md"))]
    cards = [c for l in lectures for c in l["cards"]]
    topics = parse_topics(index_dir / "TOPICS.md")
    archetypes = parse_archetypes(index_dir / "EXAM_MAP.md")

    data = {"exams": exams, "cards": cards, "topics": topics,
            "archetypes": archetypes,
            "lectures": [{"name": l["name"], "title": l["title"], "pillar": l["pillar"],
                          "n_cards": len(l["cards"])} for l in lectures]}

    html = template_p.read_text(encoding="utf-8")
    kcss = inline_katex_css((libs_dir / "katex.min.css").read_text(encoding="utf-8"),
                            libs_dir / "fonts")
    payload = json.dumps(data, ensure_ascii=False)
    # JSON goes inside a <script type="application/json"> tag — escape closers.
    payload = payload.replace("</", "<\\/")
    for k, v in (("__KATEX_CSS__", kcss),
                 ("__KATEX_JS__", (libs_dir / "katex.min.js").read_text(encoding="utf-8")),
                 ("__AUTORENDER_JS__", (libs_dir / "auto-render.min.js").read_text(encoding="utf-8")),
                 ("__MARKED_JS__", (libs_dir / "marked.min.js").read_text(encoding="utf-8")),
                 ("__DATA__", payload)):
        assert k in html, f"placeholder {k} missing from template"
        html = html.replace(k, v)
    out_p.write_text(html, encoding="utf-8")
    n_q = sum(len(e["questions"]) for e in exams)
    print(f"exams={len(exams)} questions={n_q} cards={len(cards)} "
          f"topics={len(topics)} archetypes={len(archetypes)} "
          f"out={out_p} ({out_p.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
