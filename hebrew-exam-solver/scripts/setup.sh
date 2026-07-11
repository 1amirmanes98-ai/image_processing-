#!/usr/bin/env bash
# Setup for hebrew-exam-solver: WeasyPrint + David Libre fonts + poppler utils.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/3] Installing Python deps..."
pip install weasyprint scipy numpy sympy pdfplumber --break-system-packages -q || \
pip install weasyprint scipy numpy sympy pdfplumber -q

echo "[2/3] Downloading David Libre fonts..."
mkdir -p fonts
BASE="https://raw.githubusercontent.com/google/fonts/main/ofl/davidlibre"
fetch_font() {  # fetch_font <filename>; skips if already a non-empty file, retries once.
  local f="$1"
  [ -s "fonts/$f" ] && return 0
  curl -fsSL -o "fonts/$f" "$BASE/$f" || curl -fsSL -o "fonts/$f" "$BASE/$f"
  [ -s "fonts/$f" ] || { echo "  ERROR: failed to download $f from $BASE"; return 1; }
}
fetch_font DavidLibre-Regular.ttf
fetch_font DavidLibre-Bold.ttf

echo "[3/3] Checking poppler (pdftoppm/pdftotext) for QA + extraction..."
# `apt-get update` may fail on unrelated third-party PPAs — never let that block
# the install, and never let a poppler failure abort the whole setup (set -e).
if ! command -v pdftoppm >/dev/null; then
  echo "  poppler-utils not found; installing..."
  { command -v sudo >/dev/null && SUDO=sudo || SUDO=; }
  $SUDO apt-get update -qq || echo "  (apt-get update failed — continuing to install anyway)"
  $SUDO apt-get install -y -qq poppler-utils \
    || echo "  WARNING: could not auto-install poppler-utils. Install it manually (needed for QA rasters + scanned-PDF extraction)."
fi
command -v pdftoppm >/dev/null && echo "  poppler OK ($(command -v pdftoppm))" || echo "  poppler MISSING — QA rasterization will not work."

# Smoke test: render one RTL line and make sure it doesn't crash.
python3 - <<'EOF'
from weasyprint import HTML
import os
html = '''<html dir="rtl"><head><meta charset="utf-8"><style>
@font-face { font-family:'David Libre'; src: url('fonts/DavidLibre-Regular.ttf'); }
body { font-family:'David Libre'; direction: rtl; }
</style></head><body><p>בדיקת עברית: השערת האפס נדחית אם t &gt; 1.68.</p></body></html>'''
HTML(string=html, base_url=os.getcwd()).write_pdf('/tmp/rtl_smoke_test.pdf')
print("Smoke test OK -> /tmp/rtl_smoke_test.pdf")
EOF

# Rasterize the smoke test so the agent can immediately LOOK and confirm RTL.
if command -v pdftoppm >/dev/null; then
  pdftoppm -png -r 130 -f 1 -l 1 /tmp/rtl_smoke_test.pdf /tmp/rtl_smoke_test >/dev/null 2>&1 \
    && echo "Smoke raster -> /tmp/rtl_smoke_test-1.png  (OPEN IT: the Hebrew line must read right-to-left, 't > 1.68' not reversed)."
fi
echo "Setup complete."
