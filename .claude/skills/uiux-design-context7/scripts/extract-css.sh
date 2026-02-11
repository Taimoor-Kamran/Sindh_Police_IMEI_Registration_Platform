#!/bin/bash
set -euo pipefail

# Extract CSS code blocks from documentation
# Usage: extract-css.sh <topic>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $(basename "$0") <topic>" >&2
    exit 1
fi

# Fetch docs and extract CSS blocks
"${SCRIPT_DIR}/fetch-docs.sh" "$TOPIC" 2>/dev/null | \
    awk '
    /^```css/,/^```/ {
        if (/^```css/) { print "/* CSS for: '"$TOPIC"' */"; next }
        if (/^```/) { print ""; next }
        print
    }
    /^```scss/,/^```/ {
        if (/^```scss/) { print "/* SCSS for: '"$TOPIC"' */"; next }
        if (/^```/) { print ""; next }
        print
    }
    /style[:=]/,/[;}]/ { print }
    '
