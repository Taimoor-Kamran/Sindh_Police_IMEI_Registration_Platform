#!/bin/bash
set -euo pipefail

# UI/UX Design Context7 Documentation Fetcher
# Fetches and filters design documentation with token efficiency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT7_BASE_URL="https://context7.com/api/v1"
# Primary design documentation sources
LIBRARY_IDS=("tailwindcss" "mdn-web" "radix-ui" "shadcn-ui")

# Default values
VERBOSE=false
SECTION=""
TOPIC=""

# Colors for output (disabled in non-interactive mode)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    YELLOW='\033[0;33m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    BLUE=''
    YELLOW=''
    NC=''
fi

usage() {
    cat << EOF
Usage: $(basename "$0") <topic> [options]

Fetch UI/UX design documentation from Context7 with token-efficient filtering.

Arguments:
    topic               The design topic to search for

Options:
    --section=<name>    Filter to specific section
    --verbose           Enable verbose output
    --help              Show this help message

Examples:
    $(basename "$0") "accessibility"
    $(basename "$0") "color contrast" --section="wcag"
    $(basename "$0") "responsive design" --verbose

Topics:
    Visual: color-theory, typography, spacing, layout, iconography
    UX: accessibility, usability, navigation, forms, feedback
    Systems: design-tokens, components, responsive, dark-mode
EOF
    exit 0
}

log() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[INFO]${NC} $1" >&2
    fi
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
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

# Map topics to appropriate reference files
get_reference_file() {
    local topic="$1"
    case "$topic" in
        *accessibility*|*a11y*|*wcag*|*aria*|*screen-reader*)
            echo "${SCRIPT_DIR}/../references/accessibility-guide.md"
            ;;
        *color*|*typography*|*spacing*|*layout*|*hierarchy*|*contrast*)
            echo "${SCRIPT_DIR}/../references/design-principles.md"
            ;;
        *)
            echo "${SCRIPT_DIR}/../references/css-patterns.md"
            ;;
    esac
}

# Function to fetch from Context7 API
fetch_context7() {
    local query="$1"
    local library="$2"
    local url="${CONTEXT7_BASE_URL}/docs/${library}/search?q=${query}"

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
        return 1
    fi

    # Extract relevant sections using jq if available, otherwise awk
    if command -v jq &> /dev/null; then
        if [[ -n "$section_filter" ]]; then
            echo "$raw_docs" | jq -r --arg section "$section_filter" '
                .results[]? |
                select(.title | ascii_downcase | contains($section | ascii_downcase)) |
                "## \(.title)\n\n\(.content)\n"
            ' 2>/dev/null || return 1
        else
            echo "$raw_docs" | jq -r '
                .results[]? |
                "## \(.title)\n\n\(.content)\n"
            ' 2>/dev/null || return 1
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
*Fetched from Context7 UI/UX documentation*
EOF
}

# Main execution
main() {
    log "Starting documentation fetch..."

    local found_docs=false
    local all_docs=""

    # Try fetching from multiple design-related libraries
    for library in "${LIBRARY_IDS[@]}"; do
        log "Trying library: $library"
        RAW_DOCS=$(fetch_context7 "$NORMALIZED_TOPIC" "$library")

        FILTERED=$(filter_docs "$RAW_DOCS" "$SECTION" 2>/dev/null || echo "")

        if [[ -n "$FILTERED" && "$FILTERED" != "" ]]; then
            found_docs=true
            all_docs+="$FILTERED"$'\n\n'
            log "Found docs in: $library"
        fi
    done

    # Fallback to local references if API failed
    if [[ "$found_docs" == "false" ]]; then
        log "API unavailable, using local references"
        local ref_file
        ref_file=$(get_reference_file "$NORMALIZED_TOPIC")

        if [[ -f "$ref_file" ]]; then
            # Filter local reference by topic
            if [[ -n "$SECTION" ]]; then
                all_docs=$(grep -i -A 100 "$SECTION" "$ref_file" | head -150 || cat "$ref_file")
            else
                all_docs=$(grep -i -A 50 "$TOPIC" "$ref_file" | head -150 || cat "$ref_file")
            fi
        else
            all_docs="No documentation available for: $TOPIC. Try: accessibility, color-theory, typography, layout, forms, responsive"
        fi
    fi

    # Format and return minimal output
    format_output "$all_docs" "$TOPIC"

    log "Done!"
}

main
