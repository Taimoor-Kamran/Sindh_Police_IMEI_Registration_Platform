#!/bin/bash
set -euo pipefail

# Extract practical applications for a specific UX law

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <law-name>" >&2
    echo "Example: $(basename "$0") fitts-law" >&2
    exit 1
fi

# Fetch full docs and extract applications section
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" --section="application" 2>/dev/null | \
    awk '
        /^###.*[Aa]pplication|^###.*[Ee]xample|^###.*[Uu]se [Cc]ase|^###.*[Ii]mplementation/ { found=1 }
        /^##[^#]/ { if (found) exit }
        found { print }
    ' | head -100

# Also include quick tips if available
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    grep -i -A 5 "tip\|best practice\|do:\|don't:" 2>/dev/null | head -30
