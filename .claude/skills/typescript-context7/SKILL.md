---
name: typescript-context7
description: Fetch and search TypeScript documentation from Context7. Use when the user asks about TypeScript types, interfaces, generics, utility types, configuration, or needs help with TypeScript-specific syntax and patterns.
---

# TypeScript Context7 Documentation Skill

Efficiently fetch and search TypeScript documentation using Context7's API with token-optimized filtering.

## Quick Start

```bash
# Search for specific TypeScript topic
./scripts/fetch-docs.sh "generics"

# Get type utility documentation
./scripts/fetch-docs.sh "utility types"

# Search for configuration options
./scripts/fetch-docs.sh "tsconfig"
```

## Architecture

This skill uses a token-efficient architecture:

1. **Fetch**: Raw documentation fetched in shell subprocess (stays out of LLM context)
2. **Filter**: Shell tools (awk/grep/sed) filter to relevant sections (0 tokens)
3. **Return**: Only essential, filtered content returned to Claude

```
Context7 API → Shell Fetch → Pipe Filter → Minimal Output
     ↓              ↓             ↓              ↓
  Large JSON    Subprocess    awk/grep/sed   ~10% tokens
```

## Commands

### Fetch Documentation
```bash
# Basic search
./scripts/fetch-docs.sh "<topic>"

# With section filter
./scripts/fetch-docs.sh "<topic>" --section="<section-name>"

# Verbose mode for debugging
./scripts/fetch-docs.sh "<topic>" --verbose
```

### Extract Specific Patterns
```bash
# Get type signatures only
./scripts/extract-types.sh "<topic>"

# Get code examples only
./scripts/extract-examples.sh "<topic>"
```

## Common Topics

| Topic | Description |
|-------|-------------|
| `generics` | Generic types, constraints, inference |
| `utility-types` | Partial, Required, Pick, Omit, etc. |
| `interfaces` | Interface declarations and extends |
| `type-guards` | Type narrowing and guards |
| `tsconfig` | TypeScript configuration options |
| `decorators` | Decorator syntax and usage |
| `modules` | Module systems and imports |
| `enums` | Enum types and const enums |

## Output Format

Documentation is returned in structured markdown:

```markdown
## Topic: <searched-topic>

### Summary
Brief explanation of the concept

### Type Signatures
```typescript
type Example<T> = ...
```

### Examples
```typescript
// Usage example
const example: Example<string> = ...
```

### Related
- Link to related topics
```

## References

- `references/typescript-patterns.md` - Common TypeScript patterns and idioms
- `references/utility-types.md` - Complete utility type reference
- `references/tsconfig-reference.md` - TSConfig options reference

## Token Efficiency

This skill achieves significant token savings:

| Operation | Traditional | Context7 Efficient |
|-----------|-------------|-------------------|
| Full docs fetch | ~50K tokens | 0 tokens (subprocess) |
| Filtered output | N/A | ~2-5K tokens |
| **Savings** | - | **90-96%** |
