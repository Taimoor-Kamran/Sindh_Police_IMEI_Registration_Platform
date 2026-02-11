#!/bin/bash
set -euo pipefail

# Extract TypeScript code examples from documentation
# Returns only executable examples for minimal token usage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TOPIC="${1:-}"
MAX_EXAMPLES="${2:-5}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic> [max_examples]"
    echo "Example: $(basename "$0") generics 3"
    exit 1
fi

echo "## Code Examples: ${TOPIC}"
echo ""

# Fetch docs and extract code blocks
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    awk -v max="$MAX_EXAMPLES" '
        BEGIN { count=0 }
        /^```typescript/ {
            in_code=1
            if (count < max) {
                count++
                print "### Example " count
                print "```typescript"
            }
            next
        }
        /^```$/ {
            if (in_code && count <= max) {
                print "```"
                print ""
            }
            in_code=0
            next
        }
        in_code && count <= max { print }
    '

echo "---"
echo "*Examples for: ${TOPIC} (showing up to ${MAX_EXAMPLES})*"
