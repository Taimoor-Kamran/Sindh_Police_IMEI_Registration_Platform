---
name: drf-context7
description: Token-efficient Django REST Framework documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for DRF serializers, viewsets, routers, permissions, authentication, filtering, pagination, and throttling. Use when users ask about DRF features, need code examples for REST APIs, serializer validation, viewset actions, or permission classes. Triggers include questions like "How do I create a DRF serializer", "Show me ViewSet examples", "DRF authentication setup", or any Django REST Framework-related documentation request.
---

# Django REST Framework Context7 Documentation Fetcher

Fetch Django REST Framework documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library "django rest framework" --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library "django rest framework" --topic serializers
bash scripts/fetch-docs.sh --library "django rest framework" --topic viewsets
bash scripts/fetch-docs.sh --library "django rest framework" --topic authentication
bash scripts/fetch-docs.sh --library "django rest framework" --topic permissions
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Django REST Framework documentation request, follow this workflow:

### 1. Identify Topic

Extract from user query:
- **Topic:** Specific feature (serializers, viewsets, permissions, authentication, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library "django rest framework" --topic <topic> --verbose
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
- `--library "django rest framework"` - Uses DRF library
- `--library-id /encode/django-rest-framework` - Direct Context7 ID (faster, skips resolution)

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

## DRF Library ID

Use `--library-id` for faster lookup (skips resolution):

```bash
Django REST Framework:   /encode/django-rest-framework
```

## Common DRF Topics

| Topic | Description |
|-------|-------------|
| `serializers` | ModelSerializer, nested serializers, validation |
| `viewsets` | ModelViewSet, custom actions, mixins |
| `routers` | DefaultRouter, SimpleRouter, custom routes |
| `permissions` | Permission classes, custom permissions |
| `authentication` | Token auth, JWT, session auth, custom backends |
| `filtering` | DjangoFilterBackend, SearchFilter, OrderingFilter |
| `pagination` | PageNumberPagination, LimitOffsetPagination |
| `throttling` | Rate limiting, custom throttle classes |
| `validators` | Field validators, object-level validation |
| `generic views` | ListAPIView, CreateAPIView, mixins |
| `requests` | Request parsing, content negotiation |
| `responses` | Response objects, status codes |
| `renderers` | JSON, browsable API, custom renderers |
| `parsers` | JSON parser, multipart, custom parsers |
| `relations` | PrimaryKeyRelatedField, nested relationships |
| `fields` | Custom fields, SerializerMethodField |

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me DRF serializer examples"

```bash
bash scripts/fetch-docs.sh --library "django rest framework" --topic serializers --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning DRF Feature

User asks: "How do I get started with DRF ViewSets?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library "django rest framework" --topic viewsets --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library "django rest framework" --topic viewsets --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How does DRF authentication work?"

```bash
bash scripts/fetch-docs.sh --library-id /encode/django-rest-framework --topic authentication
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --library "django rest framework" --topic serializers --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --library "django rest framework" --topic serializers --page 2
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

## DRF-Specific Examples

### Serializers

```bash
# Basic serializers
bash scripts/fetch-docs.sh --library "django rest framework" --topic "modelserializer"

# Nested serializers
bash scripts/fetch-docs.sh --library "django rest framework" --topic "nested serializers"

# Validation
bash scripts/fetch-docs.sh --library "django rest framework" --topic "serializer validation"
```

### ViewSets

```bash
# Basic viewsets
bash scripts/fetch-docs.sh --library "django rest framework" --topic "modelviewset"

# Custom actions
bash scripts/fetch-docs.sh --library "django rest framework" --topic "viewset actions"

# Mixins
bash scripts/fetch-docs.sh --library "django rest framework" --topic "viewset mixins"
```

### Authentication

```bash
# Token authentication
bash scripts/fetch-docs.sh --library "django rest framework" --topic "token authentication"

# Session authentication
bash scripts/fetch-docs.sh --library "django rest framework" --topic "session authentication"

# Custom authentication
bash scripts/fetch-docs.sh --library "django rest framework" --topic "custom authentication"
```

### Permissions

```bash
# Permission classes
bash scripts/fetch-docs.sh --library "django rest framework" --topic "permission classes"

# Custom permissions
bash scripts/fetch-docs.sh --library "django rest framework" --topic "custom permissions"

# Object-level permissions
bash scripts/fetch-docs.sh --library "django rest framework" --topic "object permissions"
```

### Filtering & Pagination

```bash
# Filtering
bash scripts/fetch-docs.sh --library "django rest framework" --topic "filtering"

# Search
bash scripts/fetch-docs.sh --library "django rest framework" --topic "searchfilter"

# Pagination
bash scripts/fetch-docs.sh --library "django rest framework" --topic "pagination"
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
- [references/drf-patterns.md](references/drf-patterns.md) - Common DRF patterns

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
