#!/usr/bin/env bash
# Restore the Reinforcement Learning tutor's content (course materials + generated
# study index) from the content zip that Amir keeps locally (rl-tutor-content.zip).
#
# Usage: bash rl-exam-agent/scripts/restore_content.sh <path-to-rl-tutor-content.zip>
set -euo pipefail
ZIP="${1:?usage: restore_content.sh <rl-tutor-content.zip>}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
unzip -o -q "$ZIP" -d "$DIR"
echo "Restored into $DIR:"
echo "  PDFs:         $(find "$DIR/materials" -name '*.pdf' 2>/dev/null | wc -l) (expect 35)"
echo "  Slide decks:  $(find "$DIR/materials" -name '*.pptx' 2>/dev/null | wc -l) (expect 12)"
echo "  Text mirrors: $(find "$DIR/materials/text" -name '*.txt' 2>/dev/null | wc -l) (expect 47)"
echo "  Index files:  $(find "$DIR/index" \( -name '*.md' -o -name '*.json' \) 2>/dev/null | wc -l)"
