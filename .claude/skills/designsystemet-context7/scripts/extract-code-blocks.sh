#!/bin/bash
# Extract code blocks from markdown content
# Usage: echo "$content" | ./extract-code-blocks.sh [max_blocks]

set -euo pipefail

MAX_BLOCKS="${1:-5}"

awk -v max="$MAX_BLOCKS" '
BEGIN {
    in_block = 0
    block_count = 0
    current_block = ""
    lang = ""
}

/^```/ {
    if (in_block == 0) {
        # Start of code block
        in_block = 1
        lang = substr($0, 4)
        current_block = ""
    } else {
        # End of code block
        in_block = 0
        block_count++

        if (block_count <= max) {
            if (lang != "") {
                print "```" lang
            } else {
                print "```"
            }
            print current_block
            print "```"
            print ""
        }
        current_block = ""
        lang = ""
    }
    next
}

in_block == 1 {
    if (current_block == "") {
        current_block = $0
    } else {
        current_block = current_block "\n" $0
    }
}

END {
    if (block_count == 0) {
        print "# No code blocks found"
    }
}
'
