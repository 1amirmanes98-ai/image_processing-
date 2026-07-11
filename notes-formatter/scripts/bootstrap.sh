#!/usr/bin/env bash
# bootstrap.sh — idempotent environment check/setup for the notes formatter.
# Ensures: poppler-utils (pdftoppm), Chromium, Node 22, and vendored assets.
# Running as root (no sudo). Safe to re-run; a second run is a clean no-op.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$ROOT/vendor"
CHROME="${CHROME_BIN:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
NODE="/opt/node22/bin/node"

fail=0
note() { printf '  %s\n' "$*"; }
ok()   { printf 'OK   %s\n' "$*"; }
bad()  { printf 'FAIL %s\n' "$*"; fail=1; }

echo "== notes-formatter bootstrap =="

# 1) poppler-utils / pdftoppm ------------------------------------------------
if command -v pdftoppm >/dev/null 2>&1; then
  ok "pdftoppm present ($(command -v pdftoppm))"
else
  note "pdftoppm missing — installing poppler-utils via apt-get ..."
  apt-get update -qq >/dev/null 2>&1
  if apt-get install -y -qq poppler-utils >/dev/null 2>&1 && command -v pdftoppm >/dev/null 2>&1; then
    ok "installed poppler-utils ($(command -v pdftoppm))"
  else
    bad "could not install poppler-utils"
    note "fallback: 'pip install pymupdf' and rasterize via fitz (see README)"
  fi
fi

# 2) Chromium ----------------------------------------------------------------
if [ -x "$CHROME" ]; then
  ok "chromium present ($CHROME)"
else
  bad "chromium not found/executable at $CHROME (set CHROME_BIN to override)"
fi

# 3) Node 22 -----------------------------------------------------------------
if [ -x "$NODE" ]; then
  ok "node present ($("$NODE" --version 2>/dev/null))"
else
  bad "node not found at $NODE"
fi

# 4) Vendored assets ---------------------------------------------------------
if [ -f "$VENDOR/katex/katex.min.css" ] && [ -f "$VENDOR/katex/katex.min.js" ]; then
  ok "KaTeX vendored ($(find "$VENDOR/katex/fonts" -name '*.woff2' 2>/dev/null | wc -l) woff2 fonts)"
else
  bad "KaTeX assets missing under $VENDOR/katex/"
fi

if ls "$VENDOR"/fonts/DavidLibre-*.ttf >/dev/null 2>&1; then
  ok "David Libre vendored ($(ls "$VENDOR"/fonts/DavidLibre-*.ttf | wc -l) weights)"
else
  bad "David Libre fonts missing under $VENDOR/fonts/"
fi

echo "==============================="
if [ "$fail" -ne 0 ]; then
  echo "bootstrap: FAILED — see messages above" >&2
  exit 1
fi
echo "bootstrap: OK"
