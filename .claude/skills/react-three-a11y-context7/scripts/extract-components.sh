#!/bin/bash
set -euo pipefail

# Extract component documentation
# Usage: extract-components.sh <component-name>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <component-name>" >&2
    exit 1
fi

# Read local components reference
REF_FILE="${SCRIPT_DIR}/../references/a11y-components.md"

if [[ -f "$REF_FILE" ]]; then
    # Search for component in reference file
    grep -i -A 40 "$TOPIC" "$REF_FILE" 2>/dev/null | head -80 || \
    cat "$REF_FILE" | head -100
else
    echo "A11y components reference not found"
fi
