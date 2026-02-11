---
name: designsystemet-context7
description: Token-efficient documentation fetcher for Designsystemet (Digdir's Norwegian Design System) using Context7 MCP. Fetches React components, accessibility patterns, CSS utilities, and design tokens. Use when users ask about Designsystemet components (Button, Alert, Textfield, etc.), accessibility guidelines, theming, or building public sector digital services with WCAG compliance.
---

# Designsystemet Context7 Documentation Fetcher

Fetch Designsystemet documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --topic Button
bash scripts/fetch-docs.sh --topic accessibility
bash scripts/fetch-docs.sh --topic theming
bash scripts/fetch-docs.sh --topic Textfield
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any Designsystemet documentation request:

### 1. Identify Topic

Extract from user query:
- **Component:** Button, Alert, Textfield, Accordion, Tabs, etc.
- **Concept:** Accessibility, theming, tokens, installation, etc.

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --topic <topic> --verbose
```

The `--verbose` flag shows token savings statistics.

### 3. Use Filtered Output

The script automatically:
- Fetches full documentation (stays in subprocess)
- Filters to code examples + API signatures + key notes
- Returns only essential content to Claude

## Parameters

### Basic Usage

```bash
bash scripts/fetch-docs.sh [OPTIONS]
```

**Required:**
- `--topic <topic>` - Component or concept to search for

**Optional:**
- `--mode <code|info>` - code for examples (default), info for concepts
- `--page <1-10>` - Pagination for more results
- `--verbose` - Show token savings statistics

### Mode Selection

**Code Mode (default):** Returns code examples + API signatures
```bash
--mode code
```

**Info Mode:** Returns conceptual explanations + guidelines
```bash
--mode info
```

## Common Topics

### Components
| Component | Description |
|-----------|-------------|
| `Button` | Primary, secondary, and tertiary buttons |
| `Alert` | Info, warning, success, and danger alerts |
| `Textfield` | Text input with labels and validation |
| `Accordion` | Expandable content sections |
| `Tabs` | Tabbed interface navigation |
| `Modal` | Dialog and modal components |
| `Checkbox` | Checkbox input component |
| `Radio` | Radio button component |
| `Select` | Dropdown select component |
| `Table` | Data table component |
| `Tag` | Label/tag component |
| `Tooltip` | Tooltip component |

### Concepts
| Topic | Description |
|-------|-------------|
| `installation` | Getting started, npm packages |
| `theming` | Custom themes, design tokens |
| `accessibility` | WCAG guidelines, a11y patterns |
| `tokens` | Design tokens reference |
| `typography` | Font styles, text patterns |
| `colors` | Color palette, usage |
| `spacing` | Spacing scale, margins |

## Workflow Patterns

### Pattern 1: Quick Component Examples

User asks: "Show me Designsystemet Button examples"

```bash
bash scripts/fetch-docs.sh --topic Button --verbose
```

Returns: Code examples + API signatures + notes (~205 tokens)

### Pattern 2: Accessibility Guidelines

User asks: "How do I make my forms accessible with Designsystemet?"

```bash
# Step 1: Get accessibility overview
bash scripts/fetch-docs.sh --topic accessibility --mode info

# Step 2: Get form component examples
bash scripts/fetch-docs.sh --topic Textfield --mode code
```

### Pattern 3: Installation & Setup

User asks: "How do I get started with Designsystemet?"

```bash
bash scripts/fetch-docs.sh --topic "getting started" --mode info
```

### Pattern 4: Deep Component Exploration

User needs comprehensive component documentation:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --topic Button --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --topic Button --page 2
```

## Token Efficiency

**How it works:**

1. `fetch-docs.sh` calls `fetch-raw.sh` (which uses `mcp-client.py`)
2. Full response stays in subprocess memory
3. Shell filters (awk/grep/sed) extract essentials (0 LLM tokens used)
4. Returns filtered output to Claude

**Savings:**
- Direct MCP: ~934 tokens per query
- This approach: ~205 tokens per query
- **77% reduction**

**Do NOT use `mcp-client.py` directly** - it bypasses filtering and wastes tokens.

## Package Information

Designsystemet packages:
- `@digdir/designsystemet-css` - Core CSS styles
- `@digdir/designsystemet-theme` - Default Digdir theme
- `@digdir/designsystemet-react` - React components

```bash
npm install @digdir/designsystemet-css @digdir/designsystemet-theme @digdir/designsystemet-react
```

## References

- [references/context7-tools.md](references/context7-tools.md) - Context7 MCP tool reference
- [references/designsystemet-components.md](references/designsystemet-components.md) - Component quick reference
- [Designsystemet Documentation](https://designsystemet.no/en/)
- [GitHub Repository](https://github.com/digdir/designsystemet)

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
