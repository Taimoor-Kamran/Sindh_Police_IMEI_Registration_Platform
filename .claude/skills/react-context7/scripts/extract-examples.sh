#!/bin/bash
set -euo pipefail

# Extract code examples from React documentation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic>"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") useState"
    echo "  $(basename "$0") \"render props\""
    echo "  $(basename "$0") context"
    exit 1
fi

# Fetch docs and extract only code blocks
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    awk '
        /^```(tsx?|jsx?|javascript|typescript)?$/ { in_code=1; print; next }
        /^```$/ { in_code=0; print; next }
        in_code { print }
    '
