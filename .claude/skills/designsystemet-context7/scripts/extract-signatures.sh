#!/bin/bash
# Extract API signatures and prop definitions from content
# Usage: echo "$content" | ./extract-signatures.sh [max_signatures]

set -euo pipefail

MAX_SIGS="${1:-3}"

awk -v max="$MAX_SIGS" '
BEGIN {
    count = 0
}

# Match TypeScript/React component signatures
/^(export )?(const|function|interface|type) [A-Z][a-zA-Z]*/ {
    if (count < max) {
        print $0
        count++
    }
}

# Match prop type definitions
/Props\s*[=:]/ {
    if (count < max) {
        print $0
        count++
    }
}

# Match interface definitions
/^interface [A-Z]/ {
    if (count < max) {
        print $0
        count++
    }
}

# Match React component definitions with generics
/<[A-Z][a-zA-Z]*Props>/ {
    if (count < max) {
        print $0
        count++
    }
}
'
