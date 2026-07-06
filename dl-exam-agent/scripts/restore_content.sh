#!/usr/bin/env bash
# Restore the FODL tutor's content (course materials + generated study index)
# from the content zip that Amir keeps locally (fodl-tutor-content.zip).
#
# Usage: bash dl-exam-agent/scripts/restore_content.sh <path-to-fodl-tutor-content.zip>
set -euo pipefail
ZIP="${1:?usage: restore_content.sh <fodl-tutor-content.zip>}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
unzip -o -q "$ZIP" -d "$DIR"
echo "Restored into $DIR:"
echo "  PDFs:        $(find "$DIR/materials" -name '*.pdf' 2>/dev/null | wc -l) (expect 34)"
echo "  Text mirrors: $(find "$DIR/materials/text" -name '*.txt' 2>/dev/null | wc -l) (expect 34)"
echo "  Index files: $(find "$DIR/index" -name '*.md' 2>/dev/null | wc -l) (expect 36)"
