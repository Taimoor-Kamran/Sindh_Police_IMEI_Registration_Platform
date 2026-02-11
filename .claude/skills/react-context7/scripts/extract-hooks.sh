#!/bin/bash
set -euo pipefail

# Extract React Hook signatures and usage examples

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_NAME="${1:-}"

if [[ -z "$HOOK_NAME" ]]; then
    echo "Usage: $(basename "$0") <hook-name>"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") useState"
    echo "  $(basename "$0") useEffect"
    echo "  $(basename "$0") useCallback"
    exit 1
fi

# Normalize hook name
HOOK_NAME_LOWER=$(echo "$HOOK_NAME" | tr '[:upper:]' '[:lower:]')

# Check local reference first
HOOKS_REF="${SCRIPT_DIR}/../references/hooks-reference.md"

if [[ -f "$HOOKS_REF" ]]; then
    # Extract section for specific hook
    awk -v hook="$HOOK_NAME" '
        BEGIN { found=0; IGNORECASE=1 }
        /^##/ && tolower($0) ~ tolower(hook) { found=1 }
        /^##/ && found && !(tolower($0) ~ tolower(hook)) { found=0 }
        found { print }
    ' "$HOOKS_REF"
else
    # Fallback to fetch script
    "${SCRIPT_DIR}/fetch-docs.sh" "$HOOK_NAME"
fi
