#!/bin/bash
set -euo pipefail

# Extract design examples for a specific UX law

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <law-name>" >&2
    echo "Example: $(basename "$0") hicks-law" >&2
    exit 1
fi

# Fetch full docs and extract code/design examples
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    awk '
        /^```/ { in_code = !in_code; print; next }
        in_code { print }
        /^###.*[Ee]xample|^###.*[Cc]ode|^###.*[Ii]mplementation|^###.*CSS|^###.*HTML/ {
            found=1; print
        }
        found && /^##[^#]/ { found=0 }
        found { print }
    ' | head -150

# Extract inline code patterns
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    grep -E '`[^`]+`|min-width|min-height|padding|margin|font-size' 2>/dev/null | head -20
