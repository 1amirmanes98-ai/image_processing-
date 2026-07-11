#!/usr/bin/env bash
# rasterize.sh — turn a scanned PDF or a set of images into page-NN.png files.
#
#   rasterize.sh <outdir> <input.pdf>
#   rasterize.sh <outdir> <img1.png> [img2.jpg ...]
#
# PDFs are rendered at 160 DPI with pdftoppm. Image inputs are copied/normalized
# in order to <outdir>/page-NN.<ext> (no pdftoppm needed; Read renders png/jpg).
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: rasterize.sh <outdir> <input.pdf | image ...>" >&2
  exit 2
fi

outdir="$1"; shift
mkdir -p "$outdir"

# Single PDF input -> pdftoppm
if [ "$#" -eq 1 ] && [ "${1##*.}" = "pdf" -o "${1##*.}" = "PDF" ]; then
  if ! command -v pdftoppm >/dev/null 2>&1; then
    echo "rasterize: pdftoppm not found — run scripts/bootstrap.sh first" >&2
    exit 1
  fi
  pdftoppm -r 160 -png "$1" "$outdir/page"
  n=$(find "$outdir" -maxdepth 1 -name 'page-*.png' | wc -l)
  echo "rasterize: wrote $n page(s) from PDF to $outdir"
  exit 0
fi

# Otherwise treat every argument as an image, in order.
i=0
for img in "$@"; do
  if [ ! -f "$img" ]; then echo "rasterize: no such file: $img" >&2; exit 1; fi
  i=$((i + 1))
  ext="${img##*.}"
  ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
  dest="$(printf '%s/page-%02d.%s' "$outdir" "$i" "$ext")"
  cp -f "$img" "$dest"
done
echo "rasterize: normalized $i image(s) to $outdir/page-NN.*"
