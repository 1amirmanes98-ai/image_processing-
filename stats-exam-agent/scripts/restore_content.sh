#!/usr/bin/env bash
# Restore the Intro to Statistics tutor's content (course materials + generated study
# index) from the content zip that Amir keeps locally (stats-tutor-content.zip).
#
# Usage: bash stats-exam-agent/scripts/restore_content.sh <path-to-stats-tutor-content.zip>
set -euo pipefail
ZIP="${1:?usage: restore_content.sh <stats-tutor-content.zip>}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
unzip -o -q "$ZIP" -d "$DIR"
echo "Restored into $DIR:"
echo "  PDFs:         $(find "$DIR/materials" -name '*.pdf' 2>/dev/null | wc -l) (expect 26)"
echo "  Text mirrors: $(find "$DIR/materials/text" -name '*.txt' 2>/dev/null | wc -l) (expect 26)"
echo "  Index files:  $(find "$DIR/index" \( -name '*.md' -o -name '*.json' \) 2>/dev/null | wc -l) (expect 37)"
