#!/bin/bash
# Extract API signatures using awk
# Finds function declarations, types, and next-safe-action method chains

set -euo pipefail

MAX_SIGS="${1:-3}"

# Use awk to find common API patterns
awk -v max="$MAX_SIGS" '
  BEGIN { count = 0 }

  # Function declarations
  /^(export )?(async )?(function|const|let|var) [a-zA-Z_$][a-zA-Z0-9_$]*.*\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Interface definitions
  /^(export )?interface [a-zA-Z_$]/ {
    if (count < max) {
      sig = $0
      getline
      while ($0 ~ /^  / && count < max) {
        sig = sig " " $0
        getline
      }
      print "- `" sig "`"
      count++
    }
  }

  # Type definitions
  /^(export )?type [a-zA-Z_$][a-zA-Z0-9_$]* =/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # next-safe-action client method chains
  /actionClient\.(inputSchema|action|metadata|use|bindArgsSchemas)/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Hooks usage
  /use(Action|OptimisticAction|StateAction)\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # createSafeActionClient
  /createSafeActionClient/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # returnValidationErrors
  /returnValidationErrors/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }
'
