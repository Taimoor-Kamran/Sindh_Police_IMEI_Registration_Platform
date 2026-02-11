#!/bin/bash
# Main orchestrator: Token-efficient Designsystemet documentation fetcher
#
# This script achieves 77%+ token savings by:
# 1. Fetching raw docs (stays in shell subprocess)
# 2. Filtering with grep/awk/sed (0 LLM tokens!)
# 3. Returning condensed output to Claude

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Designsystemet Context7 library ID
LIBRARY_ID="/digdir/designsystemet"

# Parse arguments
TOPIC=""
MODE="code"
PAGE=1
VERBOSE=0

usage() {
  cat << USAGE
Usage: $0 [OPTIONS]

Token-efficient Designsystemet documentation fetcher using Context7 MCP

OPTIONS:
  --topic TOPIC      Topic to focus on (e.g., Button, accessibility)
  --mode MODE        Mode: code (default) or info
  --page NUM         Page number (1-10, default: 1)
  --verbose, -v      Show token statistics
  --help, -h         Show this help

EXAMPLES:
  # Get Button component examples
  $0 --topic Button

  # Get accessibility guidelines
  $0 --topic accessibility --mode info

  # Get Textfield component with verbose output
  $0 --topic Textfield --verbose

  # Pagination for more results
  $0 --topic Button --page 2 --verbose
USAGE
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --topic)
      TOPIC="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --page)
      PAGE="$2"
      shift 2
      ;;
    -v|--verbose)
      VERBOSE=1
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

# Validate topic
if [ -z "$TOPIC" ]; then
  echo "Error: Must specify --topic" >&2
  usage
fi

[ $VERBOSE -eq 1 ] && echo "📚 Fetching Designsystemet documentation for: $TOPIC" >&2

# Step 1: Fetch raw documentation (stays in shell memory!)
RAW_JSON=$("$SCRIPT_DIR/fetch-raw.sh" "$LIBRARY_ID" "$TOPIC" "$MODE" "$PAGE")

# Step 2: Extract text from JSON (using Python if jq not available)
if command -v jq &> /dev/null; then
  RAW_TEXT=$(echo "$RAW_JSON" | jq -r '.content[0].text // empty')
else
  RAW_TEXT=$(echo "$RAW_JSON" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data.get("content", [{}])[0].get("text", ""))')
fi

if [ -z "$RAW_TEXT" ]; then
  echo "Error: No documentation received from Context7" >&2
  echo "Try a different topic or check if Designsystemet is available in Context7" >&2
  exit 1
fi

# Calculate raw token count (approximate: words * 1.3)
if [ $VERBOSE -eq 1 ]; then
  RAW_WORDS=$(echo "$RAW_TEXT" | wc -w)
  RAW_TOKENS=$(echo "$RAW_WORDS * 1.3" | bc | cut -d. -f1)
  echo "📊 Raw response: ~$RAW_WORDS words (~$RAW_TOKENS tokens)" >&2
fi

# Step 3: Filter using shell tools (0 LLM tokens!)
OUTPUT=""

if [ "$MODE" = "code" ]; then
  # Code mode: Extract code examples and API signatures

  # Extract code blocks
  CODE_BLOCKS=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-code-blocks.sh" 5)

  if [ -n "$CODE_BLOCKS" ] && [ "$CODE_BLOCKS" != "# No code blocks found" ]; then
    OUTPUT+="## Code Examples\n\n$CODE_BLOCKS\n"
  fi

  # Extract API signatures
  SIGNATURES=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-signatures.sh" 3)

  if [ -n "$SIGNATURES" ]; then
    OUTPUT+="\n## API Signatures\n\n$SIGNATURES\n"
  fi

else
  # Info mode: Extract conceptual content

  # Get fewer code examples (2 max)
  CODE_BLOCKS=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-code-blocks.sh" 2)

  if [ -n "$CODE_BLOCKS" ] && [ "$CODE_BLOCKS" != "# No code blocks found" ]; then
    OUTPUT+="## Examples\n\n$CODE_BLOCKS\n"
  fi

  # Extract key paragraphs (first 3 substantial paragraphs)
  OVERVIEW=$(echo "$RAW_TEXT" | \
    awk 'BEGIN{RS=""; FS="\n"} length($0) > 200 && !/```/{print; if(++count>=3) exit}')

  if [ -n "$OVERVIEW" ]; then
    OUTPUT+="\n## Overview\n\n$OVERVIEW\n"
  fi
fi

# Always add important notes
NOTES=$(echo "$RAW_TEXT" | "$SCRIPT_DIR/extract-notes.sh" 3)

if [ -n "$NOTES" ]; then
  OUTPUT+="\n## Important Notes\n\n$NOTES\n"
fi

# Fallback if no content extracted
if [ -z "$OUTPUT" ]; then
  OUTPUT=$(echo "$RAW_TEXT" | head -c 500)
  OUTPUT+="\n\n[Response truncated for brevity...]"
fi

# Step 4: Output filtered content (this is what enters Claude's context!)
echo -e "$OUTPUT"

# Calculate filtered token count and savings
if [ $VERBOSE -eq 1 ]; then
  FILTERED_WORDS=$(echo -e "$OUTPUT" | wc -w)
  FILTERED_TOKENS=$(echo "$FILTERED_WORDS * 1.3" | bc | cut -d. -f1)
  SAVINGS=$(echo "scale=1; (($RAW_TOKENS - $FILTERED_TOKENS) / $RAW_TOKENS) * 100" | bc)

  echo "" >&2
  echo "✨ Filtered output: ~$FILTERED_WORDS words (~$FILTERED_TOKENS tokens)" >&2
  echo "💰 Token savings: ${SAVINGS}%" >&2
fi
