#!/bin/bash
set -euo pipefail

# Extract code examples from documentation
# Usage: extract-examples.sh <topic>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic>" >&2
    exit 1
fi

# Search across all reference files for examples
REFS_DIR="${SCRIPT_DIR}/../references"

echo "## Code Examples: ${TOPIC}"
echo ""

for ref_file in "${REFS_DIR}"/*.md; do
    if [[ -f "$ref_file" ]]; then
        # Extract code blocks related to topic
        results=$(grep -i -B 2 -A 20 "$TOPIC" "$ref_file" 2>/dev/null | \
                  grep -A 15 '```' | head -60)
        if [[ -n "$results" ]]; then
            echo "### From $(basename "$ref_file")"
            echo ""
            echo "$results"
            echo ""
        fi
    fi
done
