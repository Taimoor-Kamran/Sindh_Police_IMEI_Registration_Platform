#!/bin/bash
set -euo pipefail

# Extract design principles from documentation
# Usage: extract-principles.sh <topic>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic>" >&2
    exit 1
fi

# Read local design principles reference
REF_FILE="${SCRIPT_DIR}/../references/design-principles.md"

if [[ -f "$REF_FILE" ]]; then
    # Search for topic in principles file
    grep -i -A 20 "$TOPIC" "$REF_FILE" 2>/dev/null | head -50 || \
    echo "No specific principles found for: $TOPIC"
else
    echo "Design principles reference not found"
fi
