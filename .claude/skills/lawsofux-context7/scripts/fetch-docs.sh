#!/bin/bash
set -euo pipefail

# Laws of UX Context7 Documentation Fetcher
# Fetches and filters Laws of UX documentation with token efficiency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT7_BASE_URL="https://context7.com/api/v1"
LIBRARY_ID="lawsofux"

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
Usage: $(basename "$0") <law-name> [options]

Fetch Laws of UX documentation from Context7 with token-efficient filtering.

Arguments:
    law-name            The UX law to search for

Options:
    --section=<name>    Filter to specific section
    --verbose           Enable verbose output
    --help              Show this help message

Examples:
    $(basename "$0") "fitts law"
    $(basename "$0") "hicks law" --section="examples"
    $(basename "$0") "millers law" --verbose

Laws:
    Cognitive: millers-law, hicks-law, cognitive-load
    Motor: fitts-law, doherty-threshold, goal-gradient-effect
    Gestalt: proximity, similarity, common-region, pragnanz
    Psychology: jakobs-law, aesthetic-usability, peak-end-rule
    Principles: teslers-law, postels-law, occams-razor, pareto
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
    error "Law name is required. Use --help for usage information."
fi

log "Fetching documentation for: $TOPIC"

# Normalize topic for API query
NORMALIZED_TOPIC=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed "s/'s/-/g")

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

# Function to get law from local references
get_local_law() {
    local law_name="$1"
    local laws_file="${SCRIPT_DIR}/../references/laws-complete.md"

    if [[ -f "$laws_file" ]]; then
        # Extract section for the specific law
        awk -v law="$law_name" '
            BEGIN { IGNORECASE=1; found=0 }
            /^##/ {
                if (found) exit
                if (tolower($0) ~ tolower(law)) found=1
            }
            found { print }
        ' "$laws_file"
    fi
}

# Function to filter and format documentation
filter_docs() {
    local raw_docs="$1"
    local section_filter="$2"

    # Check for errors
    if echo "$raw_docs" | grep -q '"error"'; then
        # Fallback to local reference files
        log "API unavailable, using local references"

        local local_content
        local_content=$(get_local_law "$TOPIC")

        if [[ -n "$local_content" ]]; then
            echo "$local_content"
        else
            cat "${SCRIPT_DIR}/../references/laws-complete.md" 2>/dev/null || echo "No local references available"
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
## Law: ${topic}

${content}

---
*Fetched from Context7 Laws of UX documentation*
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
