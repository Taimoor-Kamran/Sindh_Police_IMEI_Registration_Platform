#!/bin/bash
set -euo pipefail

# Extract TypeScript type signatures from documentation
# Returns only type definitions for minimal token usage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic>"
    echo "Example: $(basename "$0") utility-types"
    exit 1
fi

# Fetch docs and extract only type signatures
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    awk '
        /^```typescript/ { in_code=1; next }
        /^```$/ { in_code=0; next }
        in_code && /^(type|interface|enum|class|function|const|declare)/ { print }
    ' | \
    sort -u

echo ""
echo "---"
echo "*Type signatures for: ${TOPIC}*"
