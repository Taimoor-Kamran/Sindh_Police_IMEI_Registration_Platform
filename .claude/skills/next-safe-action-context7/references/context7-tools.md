# Context7 MCP Tools

*2 tools available*

## `resolve-library-id`

Resolves a package/product name to a Context7-compatible library ID and returns matching libraries.

You MUST call this function before 'query-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

### Selection Process

1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
   - Name similarity to the query (exact matches prioritized)
   - Description relevance to the query's intent
   - Documentation coverage (prioritize libraries with higher Code Snippet counts)
   - Source reputation (consider libraries with High or Medium reputation more authoritative)
   - Benchmark Score: Quality indicator (100 is the highest score)

### Parameters

- **`query`** (`string`) *(required)*: The user's original question or task
- **`libraryName`** (`string`) *(required)*: Library name to search for and retrieve a Context7-compatible library ID

### Response Format

Returns a list of matching libraries with:
- Title
- Context7-compatible library ID (e.g., `/theedoran/next-safe-action`)
- Code Snippets count
- Source Reputation (High/Medium/Low)
- Benchmark Score
- Description

### Examples

```bash
# Find Next Safe Action library
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t resolve-library-id \
  -p '{"query": "Type safe server actions Next.js", "libraryName": "next-safe-action"}'
```

<details>
<summary>Full Schema</summary>

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The user's original question or task."
    },
    "libraryName": {
      "type": "string",
      "description": "Library name to search for and retrieve a Context7-compatible library ID."
    }
  },
  "required": ["query", "libraryName"]
}
```
</details>

## `query-docs`

Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework.

You must call 'resolve-library-id' first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

### Parameters

- **`libraryId`** (`string`) *(required)*: Exact Context7-compatible library ID (e.g., '/theedoran/next-safe-action') retrieved from 'resolve-library-id'

- **`query`** (`string`) *(required)*: The question or task you need help with. Be specific and include relevant details.

### Examples

```bash
# Get Next Safe Action server action documentation
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/theedoran/next-safe-action", "query": "create server action with zod validation"}'

# Get useAction hook examples
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/theedoran/next-safe-action", "query": "useAction hook client side"}'

# Get error handling patterns
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/theedoran/next-safe-action", "query": "returnValidationErrors error handling"}'
```

<details>
<summary>Full Schema</summary>

```json
{
  "type": "object",
  "properties": {
    "libraryId": {
      "type": "string",
      "description": "Exact Context7-compatible library ID retrieved from 'resolve-library-id'."
    },
    "query": {
      "type": "string",
      "description": "The question or task you need help with."
    }
  },
  "required": ["libraryId", "query"]
}
```
</details>

## Usage Patterns

### Pattern 1: Unknown Library

When you don't know the exact library ID:

```bash
# Step 1: Resolve library name
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t resolve-library-id -p '{"query": "Type safe server actions", "libraryName": "next-safe-action"}'

# Step 2: Use returned ID to fetch docs
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/theedoran/next-safe-action", "query": "server action validation"}'
```

### Pattern 2: Known Library ID

When you know the library ID:

```bash
# Direct fetch (skip resolve step)
python3 scripts/mcp-client.py call -s "npx -y @upstash/context7-mcp" \
  -t query-docs \
  -p '{"libraryId": "/theedoran/next-safe-action", "query": "useOptimisticAction hook"}'
```

## Next Safe Action Library IDs

Quick reference:

| Library | Context7 ID |
|---------|-------------|
| Next Safe Action | `/theedoran/next-safe-action` |
| Next Safe Action (Website) | `/websites/next-safe-action_dev` |

## Tips

1. **Library Resolution**: Always use `resolve-library-id` first unless you have the exact ID
2. **Query Specificity**: More specific queries yield better results
3. **Fallback**: If no results, try broader or different phrasing
