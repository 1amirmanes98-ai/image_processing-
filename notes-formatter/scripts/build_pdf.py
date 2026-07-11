#!/usr/bin/env python3
"""
build_pdf.py — wrap a content fragment in the notes template and print it to PDF.

Produces two HTML flavors in the output directory:
  * rendered.html    — print copy; vendor assets referenced by absolute file://
                       URLs (fast for the local Chromium print step).
  * <name>.html      — self-contained deliverable; every asset (David Libre TTF,
                       KaTeX CSS + woff2 + JS) inlined as data:/inline <script>,
                       so it opens in any browser with no network.

Then invokes scripts/print_pdf.mjs (Node CDP driver) on rendered.html.
With --qa, rasterizes the resulting PDF to <outdir>/qa/page-NN.png via pdftoppm.

Usage:
  build_pdf.py <content.html> --title T [--footer F] -o out.pdf [--qa]
"""

import argparse
import base64
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                       # notes-formatter/
TEMPLATE_DIR = ROOT / "template"
VENDOR = ROOT / "vendor"
KATEX_DIR = VENDOR / "katex"
NODE = "/opt/node22/bin/node"

URL_RE = re.compile(r"""url\(\s*['"]?([^'")]+?)['"]?\s*\)""")


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "application/octet-stream"
    if path.suffix.lower() == ".woff2":
        mime = "font/woff2"
    elif path.suffix.lower() == ".ttf":
        mime = "font/ttf"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def rewrite_css_urls(css: str, base_dir: Path, mode: str) -> str:
    """Resolve url(...) refs in `css` relative to base_dir.
    mode='file' -> absolute file:// URLs; mode='data' -> inlined data: URIs."""
    def repl(m):
        ref = m.group(1).strip()
        if ref.startswith(("data:", "http:", "https:", "file:", "#")):
            return m.group(0)
        target = (base_dir / ref).resolve()
        if not target.exists():
            return m.group(0)
        if mode == "data":
            return f"url({data_uri(target)})"
        return f"url(file://{target})"
    return URL_RE.sub(repl, css)


def katex_css_block(mode: str) -> Markup:
    css_path = KATEX_DIR / "katex.min.css"
    if mode == "file":
        # Let Chromium resolve KaTeX's own relative font url()s from the file.
        return Markup(f'<link rel="stylesheet" href="file://{css_path}">')
    css = rewrite_css_urls(css_path.read_text(encoding="utf-8"), KATEX_DIR, "data")
    return Markup(f"<style>{css}</style>")


def _script_tag(path: Path, mode: str) -> str:
    if mode == "file":
        return f'<script src="file://{path}"></script>'
    js = path.read_text(encoding="utf-8").replace("</script", "<\\/script")
    return f"<script>{js}</script>"


def katex_js_block(mode: str) -> Markup:
    katex_js = KATEX_DIR / "katex.min.js"
    autorender = KATEX_DIR / "contrib" / "auto-render.min.js"
    return Markup(_script_tag(katex_js, mode) + "\n" + _script_tag(autorender, mode))


def notes_css(mode: str) -> str:
    css = (TEMPLATE_DIR / "notes.css").read_text(encoding="utf-8")
    return rewrite_css_urls(css, TEMPLATE_DIR, mode)


def render(template, *, title, footer_meta, body, mode):
    return template.render(
        title=title,
        footer_meta=footer_meta,
        body=Markup(body),
        notes_css=Markup(notes_css(mode)),
        katex_css_block=katex_css_block(mode),
        katex_js_block=katex_js_block(mode),
    )


def main():
    ap = argparse.ArgumentParser(description="Build a notes PDF from a content fragment.")
    ap.add_argument("content", help="HTML fragment (the <body> content)")
    ap.add_argument("--title", required=True, help="Document title (also used in the footer)")
    ap.add_argument("--footer", default=None, help="Footer text (defaults to --title)")
    ap.add_argument("--meta", default=None, help="Optional sub-title/meta line shown under the title")
    ap.add_argument("-o", "--output", required=True, help="Output PDF path")
    ap.add_argument("--qa", action="store_true", help="Rasterize the PDF to <outdir>/qa/page-NN.png")
    args = ap.parse_args()

    content_path = Path(args.content).resolve()
    if not content_path.exists():
        sys.exit(f"content not found: {content_path}")
    body = content_path.read_text(encoding="utf-8")

    out_pdf = Path(args.output).resolve()
    outdir = out_pdf.parent
    outdir.mkdir(parents=True, exist_ok=True)
    footer = args.footer if args.footer is not None else args.title

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "j2"]),
    )
    template = env.get_template("page.html.j2")

    # print copy (file:// assets) + self-contained deliverable (inlined assets)
    rendered_html = outdir / "rendered.html"
    rendered_html.write_text(
        render(template, title=args.title, footer_meta=args.meta, body=body, mode="file"),
        encoding="utf-8")

    deliverable = outdir / (out_pdf.stem + ".html")
    deliverable.write_text(
        render(template, title=args.title, footer_meta=args.meta, body=body, mode="data"),
        encoding="utf-8")

    # print via the Node CDP driver
    cmd = [NODE, str(HERE / "print_pdf.mjs"), str(rendered_html), str(out_pdf), "--footer", footer]
    print("[build_pdf] " + " ".join(cmd), file=sys.stderr)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(f"print_pdf.mjs failed (exit {r.returncode})")

    print(f"[build_pdf] PDF:         {out_pdf}", file=sys.stderr)
    print(f"[build_pdf] deliverable: {deliverable}", file=sys.stderr)

    if args.qa:
        qa = outdir / "qa"
        qa.mkdir(exist_ok=True)
        qc = subprocess.run(
            ["pdftoppm", "-r", "110", "-png", str(out_pdf), str(qa / "page")],
        )
        if qc.returncode != 0:
            sys.exit("pdftoppm failed — is poppler-utils installed? run bootstrap.sh")
        pages = sorted(qa.glob("page-*.png"))
        print(f"[build_pdf] QA:          {len(pages)} page(s) in {qa}", file=sys.stderr)


if __name__ == "__main__":
    main()
