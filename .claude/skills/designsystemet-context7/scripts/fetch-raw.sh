#!/bin/bash
# Fetch raw documentation from Context7 MCP
# This is a thin wrapper around mcp-client.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LIBRARY_ID="${1:-}"
TOPIC="${2:-}"
MODE="${3:-code}"
PAGE="${4:-1}"

if [ -z "$LIBRARY_ID" ]; then
  echo "Usage: $0 <library-id> <topic> [mode] [page]" >&2
  exit 1
fi

# Build parameters JSON
PARAMS="{\"context7CompatibleLibraryID\": \"$LIBRARY_ID\""

if [ -n "$TOPIC" ]; then
  PARAMS+=", \"topic\": \"$TOPIC\""
fi

PARAMS+=", \"mode\": \"$MODE\""
PARAMS+=", \"page\": $PAGE"
PARAMS+="}"

# Call MCP client
python3 "$SCRIPT_DIR/mcp-client.py" call \
  -s "npx -y @upstash/context7-mcp" \
  -t get-library-docs \
  -p "$PARAMS"
