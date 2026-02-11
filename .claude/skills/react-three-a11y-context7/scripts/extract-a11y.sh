#!/bin/bash
set -euo pipefail

# Extract accessibility patterns from documentation
# Usage: extract-a11y.sh <topic>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic>" >&2
    exit 1
fi

# Read local accessibility patterns reference
REF_FILE="${SCRIPT_DIR}/../references/screen-reader-guide.md"

if [[ -f "$REF_FILE" ]]; then
    # Search for topic in a11y file
    grep -i -A 30 "$TOPIC" "$REF_FILE" 2>/dev/null | head -60 || \
    cat "$REF_FILE" | head -100
else
    echo "Screen reader guide reference not found"
fi
