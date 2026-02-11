---
name: supabase-context7
description: Token-efficient Supabase documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for Supabase Auth, Database, Storage, Edge Functions, and Realtime. Use when users ask about Supabase features, need code examples for authentication, database queries, RLS policies, storage operations, or Edge Functions. Triggers include questions like "How do I set up Supabase auth", "Show me RLS policy examples", "Supabase storage upload", or any Supabase-related documentation request.
---

# Supabase Context7 Documentation Fetcher

Fetch Supabase documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library supabase --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library supabase --topic authentication
bash scripts/fetch-docs.sh --library supabase --topic "row level security"
bash scripts/fetch-docs.sh --library supabase --topic storage
bash scripts/fetch-docs.sh --library supabase --topic "edge functions"
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Supabase documentation request, follow this workflow:

### 1. Identify Topic

Extract from user query:
- **Topic:** Specific feature (auth, database, storage, realtime, edge-functions, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library supabase --topic <topic> --verbose
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
- `--library supabase` - Uses Supabase library
- `--library-id /supabase/supabase` - Direct Context7 ID (faster, skips resolution)

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

## Supabase Library ID

Use `--library-id` for faster lookup (skips resolution):

```bash
Supabase:   /supabase/supabase
```

## Common Supabase Topics

| Topic | Description |
|-------|-------------|
| `authentication` | Sign up, sign in, OAuth, magic links, SSO |
| `database` | PostgreSQL queries, tables, relationships |
| `row level security` | RLS policies, security patterns |
| `storage` | File uploads, downloads, buckets |
| `edge functions` | Deno Edge Functions, deployment |
| `realtime` | Subscriptions, presence, broadcast |
| `postgres functions` | Database functions, triggers |
| `auth hooks` | Custom auth flows, webhooks |
| `migrations` | Database migrations, CLI |
| `client libraries` | JavaScript, Python, Flutter, Swift SDKs |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me Supabase auth sign up examples"

```bash
bash scripts/fetch-docs.sh --library supabase --topic "auth sign up" --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning Supabase Feature

User asks: "How do I get started with Supabase RLS?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library supabase --topic "row level security" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library supabase --topic "rls policies" --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How does Supabase storage work?"

```bash
bash scripts/fetch-docs.sh --library-id /supabase/supabase --topic storage
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --library supabase --topic authentication --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --library supabase --topic authentication --page 2
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

## Supabase-Specific Examples

### Authentication

```bash
# Email/password auth
bash scripts/fetch-docs.sh --library supabase --topic "email auth"

# OAuth providers
bash scripts/fetch-docs.sh --library supabase --topic "oauth google"

# Magic links
bash scripts/fetch-docs.sh --library supabase --topic "magic link"
```

### Database

```bash
# Basic queries
bash scripts/fetch-docs.sh --library supabase --topic "select queries"

# Inserts and updates
bash scripts/fetch-docs.sh --library supabase --topic "insert update"

# Joins and relationships
bash scripts/fetch-docs.sh --library supabase --topic "joins"
```

### Row Level Security

```bash
# RLS basics
bash scripts/fetch-docs.sh --library supabase --topic "rls policies"

# Auth-based policies
bash scripts/fetch-docs.sh --library supabase --topic "auth uid policy"
```

### Storage

```bash
# File uploads
bash scripts/fetch-docs.sh --library supabase --topic "storage upload"

# Signed URLs
bash scripts/fetch-docs.sh --library supabase --topic "signed url"
```

### Edge Functions

```bash
# Creating functions
bash scripts/fetch-docs.sh --library supabase --topic "edge function create"

# Invoking functions
bash scripts/fetch-docs.sh --library supabase --topic "invoke function"
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
- [references/supabase-patterns.md](references/supabase-patterns.md) - Common Supabase patterns

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
