---
name: react-context7
description: Fetch and search React documentation from Context7. Use when the user asks about React hooks, components, patterns, state management, performance optimization, or needs help with React-specific syntax and best practices.
---

# React Context7 Documentation Skill

Efficiently fetch and search React documentation using Context7's API with token-optimized filtering.

## Quick Start

```bash
# Search for specific React topic
./scripts/fetch-docs.sh "hooks"

# Get component pattern documentation
./scripts/fetch-docs.sh "render props"

# Search for performance patterns
./scripts/fetch-docs.sh "memoization" --section="useMemo"
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
# Get hook signatures only
./scripts/extract-hooks.sh "<hook-name>"

# Get code examples only
./scripts/extract-examples.sh "<topic>"

# Get component patterns
./scripts/extract-patterns.sh "<pattern-name>"
```

## Common Topics

| Topic | Description |
|-------|-------------|
| `hooks` | useState, useEffect, useContext, custom hooks |
| `components` | Functional components, composition patterns |
| `state-management` | Context API, reducers, state lifting |
| `performance` | useMemo, useCallback, React.memo, lazy loading |
| `forms` | Controlled/uncontrolled inputs, form libraries |
| `effects` | Side effects, cleanup, dependencies |
| `refs` | useRef, forwardRef, callback refs |
| `error-boundaries` | Error handling, fallback UI |
| `suspense` | Code splitting, data fetching |
| `server-components` | RSC, streaming, server actions |

## Output Format

Documentation is returned in structured markdown:

```markdown
## Topic: <searched-topic>

### Summary
Brief explanation of the concept

### API Signatures
```typescript
function useHook<T>(initialValue: T): [T, Dispatch<SetStateAction<T>>]
```

### Examples
```tsx
// Usage example
const [state, setState] = useState<string>('');
```

### Best Practices
- Recommended patterns and guidelines

### Related
- Link to related topics
```

## References

- `references/react-patterns.md` - Common React patterns and idioms
- `references/hooks-reference.md` - Complete hooks API reference
- `references/performance-patterns.md` - Performance optimization patterns

## Token Efficiency

This skill achieves significant token savings:

| Operation | Traditional | Context7 Efficient |
|-----------|-------------|-------------------|
| Full docs fetch | ~50K tokens | 0 tokens (subprocess) |
| Filtered output | N/A | ~2-5K tokens |
| **Savings** | - | **90-96%** |
