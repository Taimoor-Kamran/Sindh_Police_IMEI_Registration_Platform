#!/bin/bash
# Extract important notes, warnings, and tips from content
# Usage: echo "$content" | ./extract-notes.sh [max_notes]

set -euo pipefail

MAX_NOTES="${1:-3}"

grep -iE '(note:|warning:|important:|tip:|caution:|accessibility:|a11y:|wcag)' | \
    head -n "$MAX_NOTES" | \
    sed 's/^[[:space:]]*/- /'
