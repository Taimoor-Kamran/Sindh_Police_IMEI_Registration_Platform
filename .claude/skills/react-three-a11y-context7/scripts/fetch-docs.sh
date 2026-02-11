#!/bin/bash
set -euo pipefail

# React Three A11y Context7 Documentation Fetcher
# Fetches and filters @react-three/a11y documentation with token efficiency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT7_BASE_URL="https://context7.com/api/v1"
LIBRARY_ID="pmndrs/react-three-a11y"

# Default values
VERBOSE=false
SECTION=""
TOPIC=""

# Colors for output (disabled in non-interactive mode)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    BLUE=''
    NC=''
fi

usage() {
    cat << EOF
Usage: $(basename "$0") <topic> [options]

Fetch React Three A11y documentation from Context7 with token-efficient filtering.

Arguments:
    topic               The @react-three/a11y topic to search for

Options:
    --section=<name>    Filter to specific section
    --verbose           Enable verbose output
    --help              Show this help message

Examples:
    $(basename "$0") "A11y component"
    $(basename "$0") "keyboard" --section="focus"
    $(basename "$0") "screen reader" --verbose

Topics:
    A11y, A11yAnnouncer, A11ySection, A11yUserPreferences,
    keyboard-navigation, screen-reader, focus-indicators,
    role-mapping, announcements, focusable, actionable,
    react-three-fiber, drei, gestures, testing
EOF
    exit 0
}

log() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[INFO]${NC} $1" >&2
    fi
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --section=*)
            SECTION="${1#*=}"
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            usage
            ;;
        -*)
            error "Unknown option: $1"
            ;;
        *)
            if [[ -z "$TOPIC" ]]; then
                TOPIC="$1"
            fi
            shift
            ;;
    esac
done

# Validate input
if [[ -z "$TOPIC" ]]; then
    error "Topic is required. Use --help for usage information."
fi

log "Fetching documentation for: $TOPIC"

# Normalize topic for API query
NORMALIZED_TOPIC=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Function to fetch from Context7 API
fetch_context7() {
    local query="$1"
    local url="${CONTEXT7_BASE_URL}/docs/${LIBRARY_ID}/search?q=${query}"

    log "Requesting: $url"

    # Fetch raw response - stays in subprocess, not in LLM context
    local response
    response=$(curl -s -f "$url" 2>/dev/null || echo '{"error": "fetch_failed"}')

    echo "$response"
}

# Function to filter and format documentation
filter_docs() {
    local raw_docs="$1"
    local section_filter="$2"

    # Check for errors
    if echo "$raw_docs" | grep -q '"error"'; then
        # Fallback to local reference files
        log "API unavailable, using local references"

        # Try to find relevant local reference
        local ref_file=""
        case "$NORMALIZED_TOPIC" in
            *a11y*|*component*|*role*|*props*)
                ref_file="${SCRIPT_DIR}/../references/a11y-components.md"
                ;;
            *keyboard*|*focus*|*tab*|*navigation*)
                ref_file="${SCRIPT_DIR}/../references/keyboard-patterns.md"
                ;;
            *screen*|*reader*|*aria*|*announce*)
                ref_file="${SCRIPT_DIR}/../references/screen-reader-guide.md"
                ;;
            *)
                ref_file="${SCRIPT_DIR}/../references/a11y-components.md"
                ;;
        esac

        if [[ -f "$ref_file" ]]; then
            cat "$ref_file"
        else
            echo "No local references available for: $TOPIC"
        fi
        return
    fi

    # Extract relevant sections using jq if available, otherwise awk
    if command -v jq &> /dev/null; then
        if [[ -n "$section_filter" ]]; then
            echo "$raw_docs" | jq -r --arg section "$section_filter" '
                .results[]? |
                select(.title | ascii_downcase | contains($section | ascii_downcase)) |
                "## \(.title)\n\n\(.content)\n"
            ' 2>/dev/null || echo "$raw_docs"
        else
            echo "$raw_docs" | jq -r '
                .results[]? |
                "## \(.title)\n\n\(.content)\n"
            ' 2>/dev/null || echo "$raw_docs"
        fi
    else
        # Fallback: basic grep filtering
        if [[ -n "$section_filter" ]]; then
            echo "$raw_docs" | grep -i -A 50 "$section_filter" | head -100
        else
            echo "$raw_docs" | head -200
        fi
    fi
}

# Function to format output as markdown
format_output() {
    local content="$1"
    local topic="$2"

    cat << EOF
## Topic: ${topic}

${content}

---
*Fetched from Context7 @react-three/a11y documentation*
EOF
}

# Main execution
main() {
    log "Starting documentation fetch..."

    # Step 1: Fetch raw docs (subprocess - 0 LLM tokens)
    RAW_DOCS=$(fetch_context7 "$NORMALIZED_TOPIC")

    log "Raw response received, filtering..."

    # Step 2: Filter with shell tools (0 LLM tokens)
    FILTERED_DOCS=$(filter_docs "$RAW_DOCS" "$SECTION")

    # Step 3: Format and return minimal output
    format_output "$FILTERED_DOCS" "$TOPIC"

    log "Done!"
}

main
