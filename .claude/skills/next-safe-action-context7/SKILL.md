---
name: next-safe-action-context7
description: Token-efficient Next Safe Action documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for type-safe Server Actions in Next.js App Router. Use when users ask about next-safe-action features, need code examples for server actions, input validation with Zod, useAction/useOptimisticAction hooks, middleware, or error handling. Triggers include questions like "How do I create a safe server action", "Show me next-safe-action validation", "useAction hook examples", or any next-safe-action-related documentation request.
---

# Next Safe Action Context7 Documentation Fetcher

Fetch Next Safe Action documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library next-safe-action --query <query>

# Examples:
bash scripts/fetch-docs.sh --library next-safe-action --query "create server action with validation"
bash scripts/fetch-docs.sh --library next-safe-action --query "useAction hook examples"
bash scripts/fetch-docs.sh --library next-safe-action --query "middleware and error handling"
bash scripts/fetch-docs.sh --library next-safe-action --query "optimistic updates"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Next Safe Action documentation request, follow this workflow:

### 1. Identify Query

Extract from user request:
- **Query:** Specific feature or question (server actions, validation, hooks, middleware, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library next-safe-action --query "<query>" --verbose
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
- `--library next-safe-action` - Uses Next Safe Action library
- `--library-id /theedoran/next-safe-action` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--query <query>` - Specific question or feature to focus on
- `--verbose` - Show token savings statistics

## Next Safe Action Library IDs

Use `--library-id` for faster lookup (skips resolution):

```bash
Main:     /theedoran/next-safe-action
Website:  /websites/next-safe-action_dev
```

## Common Queries

| Query | Description |
|-------|-------------|
| `create server action` | Basic action setup and definition |
| `input validation zod` | Zod schema validation patterns |
| `useAction hook` | Client-side action execution hook |
| `useOptimisticAction` | Optimistic UI updates |
| `middleware` | Action middleware and chaining |
| `error handling` | Validation and server errors |
| `returnValidationErrors` | Custom validation error responses |
| `action client setup` | Creating the action client instance |
| `metadata` | Action metadata and context |
| `bind arguments` | Binding arguments to actions |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me how to create a safe server action"

```bash
bash scripts/fetch-docs.sh --library next-safe-action --query "create server action with validation" --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning Next Safe Action

User asks: "How do I get started with next-safe-action?"

```bash
# Step 1: Get setup info
bash scripts/fetch-docs.sh --library next-safe-action --query "getting started setup"

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library next-safe-action --query "basic action examples"
```

### Pattern 3: Specific Feature Lookup

User asks: "How does useOptimisticAction work?"

```bash
bash scripts/fetch-docs.sh --library-id /theedoran/next-safe-action --query "useOptimisticAction hook examples"
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Error Handling

User needs error handling patterns:

```bash
# Validation errors
bash scripts/fetch-docs.sh --library next-safe-action --query "returnValidationErrors usage"

# Server errors
bash scripts/fetch-docs.sh --library next-safe-action --query "error handling server errors"
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

## Next Safe Action Specific Examples

### Basic Server Action

```bash
# Create action with input validation
bash scripts/fetch-docs.sh --library next-safe-action --query "server action zod schema"

# Action client setup
bash scripts/fetch-docs.sh --library next-safe-action --query "createSafeActionClient setup"
```

### Client-Side Hooks

```bash
# useAction hook
bash scripts/fetch-docs.sh --library next-safe-action --query "useAction hook client"

# useOptimisticAction hook
bash scripts/fetch-docs.sh --library next-safe-action --query "useOptimisticAction optimistic updates"

# Action state and callbacks
bash scripts/fetch-docs.sh --library next-safe-action --query "action callbacks onSuccess onError"
```

### Middleware and Context

```bash
# Middleware setup
bash scripts/fetch-docs.sh --library next-safe-action --query "action middleware"

# Authentication middleware
bash scripts/fetch-docs.sh --library next-safe-action --query "auth middleware context"
```

### Error Handling

```bash
# Validation errors
bash scripts/fetch-docs.sh --library next-safe-action --query "returnValidationErrors"

# Server error handling
bash scripts/fetch-docs.sh --library next-safe-action --query "server error handling throw"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Query not found | Try more specific terms or different phrasing |
| No results | Try broader query or different aspect |
| Need more examples | Try related queries for more context |
| Want full context | Add "getting started" or "overview" to query |

## References

For detailed Context7 MCP tool documentation, see:
- [references/context7-tools.md](references/context7-tools.md) - Complete tool reference
- [references/next-safe-action-patterns.md](references/next-safe-action-patterns.md) - Common patterns

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
