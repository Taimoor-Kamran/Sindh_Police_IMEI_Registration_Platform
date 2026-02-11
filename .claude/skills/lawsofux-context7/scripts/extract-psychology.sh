#!/bin/bash
set -euo pipefail

# Extract psychological principles for a specific UX law

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <law-name>" >&2
    echo "Example: $(basename "$0") millers-law" >&2
    exit 1
fi

# Fetch full docs and extract psychology/cognitive section
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    awk '
        /^###.*[Pp]sycholog|^###.*[Cc]ognitive|^###.*[Bb]asis|^###.*[Oo]rigin|^###.*[Rr]esearch/ { found=1 }
        /^##[^#]/ { if (found) exit }
        found { print }
    ' | head -100

# Also extract key definitions
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    grep -i -B 2 -A 5 "definition\|states that\|suggests that\|principle" 2>/dev/null | head -30
