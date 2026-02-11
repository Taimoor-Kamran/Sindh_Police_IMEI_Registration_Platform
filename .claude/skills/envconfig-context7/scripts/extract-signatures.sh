#!/bin/bash
# Extract API signatures using awk
# Finds Go function declarations, interfaces, types, and envconfig patterns

set -euo pipefail

MAX_SIGS="${1:-3}"

# Use awk to find common Go API patterns
awk -v max="$MAX_SIGS" '
  BEGIN { count = 0 }

  # Go function declarations
  /^func [a-zA-Z_][a-zA-Z0-9_]*\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Go method declarations
  /^func \([a-zA-Z_][a-zA-Z0-9_]* \*?[a-zA-Z_][a-zA-Z0-9_]*\) [a-zA-Z_][a-zA-Z0-9_]*\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Go type declarations
  /^type [a-zA-Z_][a-zA-Z0-9_]* (struct|interface|func)/ {
    if (count < max) {
      sig = $0
      getline
      while ($0 ~ /^\t/ && count < max) {
        sig = sig " " $0
        getline
      }
      print "- `" sig "`"
      count++
    }
  }

  # envconfig struct tags
  /`envconfig:/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # envconfig.Process and related functions
  /envconfig\.(Process|MustProcess|Usage|Usagef|CheckDisallowed)/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Go interface implementations
  /Decode\(|Set\(/ {
    if (count < max && /func/) {
      print "- `" $0 "`"
      count++
    }
  }
'
