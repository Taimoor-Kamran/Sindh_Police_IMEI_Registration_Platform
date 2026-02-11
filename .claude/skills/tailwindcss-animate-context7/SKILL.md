---
name: tailwindcss-animate-context7
description: Token-efficient Tailwind CSS Animate documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for tailwindcss-animate plugin including entrance/exit animations, fade, slide, zoom, spin utilities, animation duration, delay, direction, fill-mode, iteration count, play state, and timing functions. Use when users ask about tailwindcss-animate features, need code examples for CSS animations with Tailwind, animation utility classes, or configuring the animate plugin. Triggers include questions like "How do I add animations with Tailwind", "Show me tailwindcss-animate examples", "Tailwind fade-in animation", "animate-in slide-out utilities", or any tailwindcss-animate-related documentation request.
---

# Tailwind CSS Animate Context7 Documentation Fetcher

Fetch tailwindcss-animate plugin documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "entrance animations"
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "fade in"
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation duration"
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "exit animations"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any tailwindcss-animate documentation request, follow this workflow:

### 1. Identify Topic

Extract from user query:
- **Topic:** Specific feature (entrance animations, exit animations, duration, delay, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic <topic> --verbose
```

The `--verbose` flag shows token savings statistics.

### 3. Use Filtered Output

The script automatically:
- Fetches full documentation (934 tokens, stays in subprocess)
- Filters to code examples + API signatures + key notes
- Returns only essential content (205 tokens to Claude)

## Parameters

### Basic Usage

```bash
bash scripts/fetch-docs.sh [OPTIONS]
```

**Required (pick one):**
- `--library "tailwindcss-animate"` - Uses tailwindcss-animate library
- `--library-id /jamiebuilds/tailwindcss-animate` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--topic <topic>` - Specific feature to focus on
- `--mode <code|info>` - code for examples (default), info for concepts
- `--page <1-10>` - Pagination for more results
- `--verbose` - Show token savings statistics

### Mode Selection

**Code Mode (default):** Returns code examples + API signatures
```bash
--mode code
```

**Info Mode:** Returns conceptual explanations + fewer examples
```bash
--mode info
```

## Library ID

Use `--library-id` for faster lookup (skips resolution):

```bash
Tailwind CSS Animate:   /jamiebuilds/tailwindcss-animate
```

## Common Topics

| Topic | Description |
|-------|-------------|
| `entrance animations` | animate-in, fade-in, slide-in, zoom-in, spin-in |
| `exit animations` | animate-out, fade-out, slide-out, zoom-out, spin-out |
| `fade` | fade-in, fade-out opacity animations |
| `slide` | slide-in-from-*, slide-out-to-* directional slides |
| `zoom` | zoom-in, zoom-out scale animations |
| `spin` | spin-in, spin-out rotation animations |
| `animation duration` | duration-75, duration-100, duration-*, custom durations |
| `animation delay` | delay-75, delay-100, delay-*, custom delays |
| `animation direction` | direction-normal, direction-reverse, direction-alternate |
| `animation fill mode` | fill-mode-none, fill-mode-forwards, fill-mode-backwards, fill-mode-both |
| `animation iteration count` | repeat-0, repeat-1, repeat-infinite |
| `animation play state` | running, paused animation states |
| `animation timing function` | ease-in, ease-out, ease-in-out timing functions |
| `installation` | Plugin setup with tailwind.config.js |
| `composing animations` | Combining entrance/exit utilities |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me tailwindcss-animate fade-in examples"

```bash
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "fade in" --verbose
```

Returns: Code examples + utility class references + notes (~205 tokens)

### Pattern 2: Learning the Plugin

User asks: "How do I get started with tailwindcss-animate?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "installation" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "entrance animations" --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How do slide animations work in tailwindcss-animate?"

```bash
bash scripts/fetch-docs.sh --library-id /jamiebuilds/tailwindcss-animate --topic "slide"
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Entrance animations
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "entrance animations" --page 1

# Page 2: Exit animations
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "exit animations" --page 2
```

## Token Efficiency

**How it works:**

1. `fetch-docs.sh` calls `fetch-raw.sh` (which uses `mcp-client.py`)
2. Full response (934 tokens) stays in subprocess memory
3. Shell filters (awk/grep/sed) extract essentials (0 LLM tokens used)
4. Returns filtered output (205 tokens) to Claude

**Savings:**
- Direct MCP: 934 tokens per query
- This approach: 205 tokens per query
- **77% reduction**

**Do NOT use `mcp-client.py` directly** - it bypasses filtering and wastes tokens.

## tailwindcss-animate Specific Examples

### Installation & Setup

```bash
# Setup guide
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "installation"

# Configuration
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "configuration"
```

### Entrance Animations

```bash
# All entrance animations
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "entrance animations"

# Fade in
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "fade in"

# Slide in
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "slide in"

# Zoom in
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "zoom in"
```

### Exit Animations

```bash
# All exit animations
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "exit animations"

# Fade out
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "fade out"

# Slide out
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "slide out"

# Zoom out
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "zoom out"
```

### Animation Properties

```bash
# Duration
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation duration"

# Delay
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation delay"

# Direction
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation direction"

# Fill mode
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation fill mode"

# Iteration count
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation iteration count"

# Timing function
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation timing function"
```

### Composing Animations

```bash
# Combining entrance utilities
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "composing animations"

# Complex animation patterns
bash scripts/fetch-docs.sh --library "tailwindcss-animate" --topic "animation examples"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Topic not found | Try name variations or use broader search term |
| No results | Use `--mode info` or broader topic |
| Need more examples | Increase page: `--page 2` |
| Want full context | Use `--mode info` for explanations |

## References

For detailed Context7 MCP tool documentation, see:
- [references/context7-tools.md](references/context7-tools.md) - Complete tool reference
- [references/tailwindcss-animate-patterns.md](references/tailwindcss-animate-patterns.md) - Common animation patterns

## Implementation Notes

**Components (for reference only, use fetch-docs.sh):**
- `mcp-client.py` - Universal MCP client (foundation)
- `fetch-raw.sh` - MCP wrapper
- `extract-code-blocks.sh` - Code example filter (awk)
- `extract-signatures.sh` - API signature filter (awk)
- `extract-notes.sh` - Important notes filter (grep)
- `fetch-docs.sh` - **Main orchestrator (ALWAYS USE THIS)**

**Architecture:**
Shell pipeline processes documentation in subprocess, keeping full response out of Claude's context. Only filtered essentials enter the LLM context, achieving 77% token savings with 100% functionality preserved.

Based on [Anthropic's "Code Execution with MCP" blog post](https://www.anthropic.com/engineering/code-execution-with-mcp).
