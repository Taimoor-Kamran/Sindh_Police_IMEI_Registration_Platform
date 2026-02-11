---
name: envconfig-context7
description: Token-efficient Envconfig documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for kelseyhightower/envconfig Go library including struct tags, environment variable parsing, defaults, required fields, custom decoders, and usage generation. Use when users ask about Envconfig features, need code examples for Go configuration from environment variables, struct tag syntax, or custom deserializers. Triggers include questions like "How do I use envconfig", "Show me struct tags for envconfig", "Envconfig default values", or any Go environment configuration request.
---

# Envconfig Context7 Documentation Fetcher

Fetch kelseyhightower/envconfig documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library envconfig --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library envconfig --topic "struct tags"
bash scripts/fetch-docs.sh --library envconfig --topic "default values"
bash scripts/fetch-docs.sh --library envconfig --topic "required fields"
bash scripts/fetch-docs.sh --library envconfig --topic "custom decoder"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Envconfig documentation request, follow this workflow:

### 1. Identify Topic

Extract from user query:
- **Topic:** Specific feature (struct tags, defaults, required, decoder, usage, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library envconfig --topic <topic> --verbose
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
- `--library envconfig` - Uses Envconfig library
- `--library-id /kelseyhightower/envconfig` - Direct Context7 ID (faster, skips resolution)

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

## Envconfig Library ID

Use `--library-id` for faster lookup (skips resolution):

```bash
Envconfig:   /kelseyhightower/envconfig
```

## Common Envconfig Topics

| Topic | Description |
|-------|-------------|
| `struct tags` | envconfig, default, required, split_words, ignored |
| `basic usage` | Process(), MustProcess(), getting started |
| `default values` | Setting defaults with struct tags |
| `required fields` | Making fields required, validation |
| `custom decoder` | Decoder interface, custom types |
| `split words` | CamelCase to SNAKE_CASE conversion |
| `prefix` | Environment variable prefixes |
| `usage` | Generating usage documentation |
| `ignored` | Ignoring fields from processing |
| `nested structs` | Processing nested configurations |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me envconfig struct tag examples"

```bash
bash scripts/fetch-docs.sh --library envconfig --topic "struct tags" --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning Envconfig Feature

User asks: "How do I set default values in envconfig?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library envconfig --topic "default values" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library envconfig --topic "default" --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How do custom decoders work in envconfig?"

```bash
bash scripts/fetch-docs.sh --library-id /kelseyhightower/envconfig --topic "custom decoder"
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --library envconfig --topic "struct tags" --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --library envconfig --topic "struct tags" --page 2
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

## Envconfig-Specific Examples

### Struct Tags

```bash
# Basic struct tags
bash scripts/fetch-docs.sh --library envconfig --topic "struct tags"

# envconfig tag for custom names
bash scripts/fetch-docs.sh --library envconfig --topic "envconfig tag"

# split_words for CamelCase
bash scripts/fetch-docs.sh --library envconfig --topic "split_words"
```

### Default Values

```bash
# Setting defaults
bash scripts/fetch-docs.sh --library envconfig --topic "default"

# Default with complex types
bash scripts/fetch-docs.sh --library envconfig --topic "default values"
```

### Required Fields

```bash
# Required fields
bash scripts/fetch-docs.sh --library envconfig --topic "required"

# Validation patterns
bash scripts/fetch-docs.sh --library envconfig --topic "required fields"
```

### Custom Decoders

```bash
# Decoder interface
bash scripts/fetch-docs.sh --library envconfig --topic "decoder"

# Custom type parsing
bash scripts/fetch-docs.sh --library envconfig --topic "custom decoder"

# Setter interface
bash scripts/fetch-docs.sh --library envconfig --topic "setter"
```

### Usage Generation

```bash
# Usage documentation
bash scripts/fetch-docs.sh --library envconfig --topic "usage"

# Usage format options
bash scripts/fetch-docs.sh --library envconfig --topic "usage generation"
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
- [references/envconfig-patterns.md](references/envconfig-patterns.md) - Common Envconfig patterns

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
