#!/bin/bash
# Fetch raw documentation from Context7 MCP
# Output: JSON response (stays in shell, doesn't enter Claude context)

set -euo pipefail

LIBRARY_ID="${1:?Error: Library ID required}"
QUERY="${2:-}"

# Build parameters JSON
PARAMS=$(cat <<JSON
{
  "libraryId": "$LIBRARY_ID",
  "query": "$QUERY"
}
JSON
)

# Call MCP server (response stays in this subprocess!)
python3 "$(dirname "$0")/mcp-client.py" call \
  -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p "$PARAMS" 2>/dev/null
