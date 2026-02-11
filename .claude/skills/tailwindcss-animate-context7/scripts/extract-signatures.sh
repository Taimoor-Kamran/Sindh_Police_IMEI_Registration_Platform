#!/bin/bash
# Extract API signatures using awk
# Finds CSS utility classes, Tailwind config patterns, and plugin definitions

set -euo pipefail

MAX_SIGS="${1:-3}"

# Use awk to find common tailwindcss-animate patterns
awk -v max="$MAX_SIGS" '
  BEGIN { count = 0 }

  # CSS class definitions (animate-in, fade-in, etc.)
  /\.(animate-in|animate-out|fade-in|fade-out|slide-in|slide-out|zoom-in|zoom-out|spin-in|spin-out)/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Tailwind utility class patterns in HTML
  /class="[^"]*animate-(in|out)[^"]*"/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Plugin configuration (require/import)
  /require\("tailwindcss-animate"\)/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # CSS @plugin directive (Tailwind v4)
  /@plugin "tailwindcss-animate"/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # CSS @keyframes definitions
  /@keyframes/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # CSS custom properties (animation variables)
  /--tw-.*animation/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Animation property declarations
  /animation:/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Duration/delay/fill-mode utility patterns
  /(duration-|delay-|fill-mode-|direction-|repeat-)/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Tailwind config theme extend for animation
  /animation:.*\{/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }

  # Module exports (plugin definition)
  /module\.exports.*plugin/ {
    if (count < max) {
      print "- `" $0 "`"
      count++
    }
  }
'
