#!/bin/bash
set -euo pipefail

# Extract specific React patterns from reference files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATTERN_NAME="${1:-}"

if [[ -z "$PATTERN_NAME" ]]; then
    echo "Usage: $(basename "$0") <pattern-name>"
    echo ""
    echo "Available patterns:"
    echo "  - compound-components"
    echo "  - render-props"
    echo "  - higher-order-components"
    echo "  - custom-hooks"
    echo "  - controlled-components"
    echo "  - container-presentational"
    echo "  - state-reducer"
    echo "  - prop-getters"
    exit 1
fi

PATTERNS_REF="${SCRIPT_DIR}/../references/react-patterns.md"

if [[ -f "$PATTERNS_REF" ]]; then
    # Extract section for specific pattern
    awk -v pattern="$PATTERN_NAME" '
        BEGIN { found=0; IGNORECASE=1 }
        /^##/ && tolower($0) ~ tolower(pattern) { found=1 }
        /^##/ && found && !(tolower($0) ~ tolower(pattern)) { found=0 }
        found { print }
    ' "$PATTERNS_REF"
else
    echo "Pattern reference file not found"
    exit 1
fi
