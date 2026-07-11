#!/usr/bin/env python3
"""Render a solution HTML to PDF (WeasyPrint) and rasterize pages for visual QA.

Usage:
    python3 scripts/render.py solution.html "פתרון_מבחן.pdf" [--qa-pages 1,2,3]

After running, OPEN the generated qa/page-*.png images and visually verify:
RTL direction, formula integrity, no overflow, boxes/tables not broken.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from weasyprint import HTML


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="input solution HTML (uses templates CSS with fonts/ paths)")
    ap.add_argument("pdf", help="output PDF path (Hebrew filename is fine)")
    ap.add_argument("--qa-pages", default="1,2", help="comma list of pages to rasterize for QA")
    ap.add_argument("--dpi", type=int, default=80)
    args = ap.parse_args()

    html_path = Path(args.html).resolve()
    pdf_path = Path(args.pdf).resolve()

    # base_url = project root so that url('fonts/DavidLibre-*.ttf') resolves.
    base = html_path.parent
    HTML(filename=str(html_path), base_url=str(base)).write_pdf(str(pdf_path))

    info = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
    pages = next((l.split()[-1] for l in info.stdout.splitlines() if l.startswith("Pages")), "?")
    print(f"Rendered {pdf_path.name}: {pages} pages")

    qa_dir = pdf_path.parent / "qa"
    qa_dir.mkdir(exist_ok=True)
    for p in args.qa_pages.split(","):
        p = p.strip()
        if not p:
            continue
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(args.dpi), "-f", p, "-l", p,
             str(pdf_path), str(qa_dir / f"page-{p}")],
            check=True,
        )
    print(f"QA rasters in {qa_dir}/ — VIEW THEM before delivering.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
