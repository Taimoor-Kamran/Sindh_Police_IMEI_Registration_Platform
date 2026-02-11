#!/bin/bash
# Extract API signatures using awk
# Finds class definitions, function declarations, and DRF-specific patterns

set -euo pipefail

MAX_SIGS="${1:-3}"

# Use awk to find common DRF API patterns
awk -v max="$MAX_SIGS" '
  BEGIN { count = 0 }

  # Python class definitions (serializers, viewsets, etc.)
  /^class [A-Z][a-zA-Z0-9_]*\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Python function/method definitions
  /^(    )?def [a-z_][a-zA-Z0-9_]*\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # DRF serializer field definitions
  /[a-z_]+ = serializers\.[A-Z][a-zA-Z]+\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # DRF model field definitions in Meta class
  /fields = \[/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # ViewSet actions decorator
  /@action\(/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Permission/Authentication class references
  /permission_classes = \[/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  /authentication_classes = \[/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Router registration
  /router\.(register|urls)/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # URL patterns
  /path\(.*ViewSet/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }
'
