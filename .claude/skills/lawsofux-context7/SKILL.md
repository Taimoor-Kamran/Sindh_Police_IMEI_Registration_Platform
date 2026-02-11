---
name: lawsofux-context7
description: Fetch and search Laws of UX documentation from Context7. Use when the user asks about UX laws, design psychology, cognitive principles, Fitts's Law, Hick's Law, Jakob's Law, Miller's Law, or needs help applying psychological principles to interface design.
---

# Laws of UX Context7 Documentation Skill

Efficiently fetch and search Laws of UX documentation using Context7's API with token-optimized filtering.

## Quick Start

```bash
# Search for specific UX law
./scripts/fetch-docs.sh "fitts law"

# Get cognitive psychology principles
./scripts/fetch-docs.sh "miller's law" --section="working-memory"

# Search for decision-making laws
./scripts/fetch-docs.sh "hicks law" --verbose
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
./scripts/fetch-docs.sh "<law-name>"

# With section filter
./scripts/fetch-docs.sh "<law-name>" --section="<section-name>"

# Verbose mode for debugging
./scripts/fetch-docs.sh "<law-name>" --verbose
```

### Extract Specific Patterns
```bash
# Get practical applications only
./scripts/extract-applications.sh "<law-name>"

# Get psychological principles only
./scripts/extract-psychology.sh "<law-name>"

# Get design examples
./scripts/extract-examples.sh "<law-name>"
```

## Laws of UX Reference

### Cognitive Load & Memory

| Law | Description |
|-----|-------------|
| `millers-law` | Average person can hold 7±2 items in working memory |
| `hicks-law` | Decision time increases with number and complexity of choices |
| `cognitive-load` | Minimize mental effort required to use an interface |

### Motor & Interaction

| Law | Description |
|-----|-------------|
| `fitts-law` | Time to acquire target relates to distance and target size |
| `doherty-threshold` | Productivity increases when response time is <400ms |
| `goal-gradient-effect` | People accelerate behavior as they approach a goal |

### Perception & Gestalt

| Law | Description |
|-----|-------------|
| `law-of-proximity` | Objects close together are perceived as related |
| `law-of-similarity` | Similar elements are perceived as being related |
| `law-of-common-region` | Elements in same bounded area perceived as related |
| `law-of-pragnanz` | Users interpret complex images in simplest form |
| `law-of-uniform-connectedness` | Connected elements perceived as more related |

### Psychology & Behavior

| Law | Description |
|-----|-------------|
| `jakobs-law` | Users prefer sites that work like others they know |
| `aesthetic-usability-effect` | Aesthetically pleasing designs perceived as more usable |
| `peak-end-rule` | Experiences judged by peaks and endings |
| `von-restorff-effect` | Distinctive items are more likely to be remembered |
| `serial-position-effect` | Users recall first and last items best |
| `zeigarnik-effect` | Incomplete tasks remembered better than completed ones |

### Design Principles

| Law | Description |
|-----|-------------|
| `teslers-law` | Every system has irreducible complexity |
| `postels-law` | Be conservative in output, liberal in input |
| `occams-razor` | The simplest solution is usually the best |
| `pareto-principle` | 80% of effects come from 20% of causes |
| `parkinsons-law` | Work expands to fill the time available |

## Output Format

Documentation is returned in structured markdown:

```markdown
## Law: <law-name>

### Definition
Brief explanation of the law

### Psychological Basis
- Why this works from a cognitive perspective

### Key Takeaways
- Actionable design implications

### Implementation
```css
/* CSS/Design example */
.target-button {
  min-width: 44px;
  min-height: 44px;
}
```

### Examples
- Real-world applications

### Related Laws
- Link to related laws
```

## Quick Reference Card

### Touch Target Sizes (Fitts's Law)
- **Minimum**: 44x44px (Apple), 48x48dp (Material Design)
- **Recommended**: 48x48px for primary actions
- **Spacing**: 8px minimum between targets

### Choice Limits (Hick's Law)
- **Navigation**: 5-7 main menu items
- **Forms**: Progressive disclosure for complex forms
- **Options**: Chunk into categories when >7 choices

### Response Times (Doherty Threshold)
- **Instant**: <100ms (feels immediate)
- **Optimal**: <400ms (maintains flow)
- **Maximum**: <1000ms (before feedback needed)

### Memory Chunks (Miller's Law)
- **Phone numbers**: Groups of 3-4 digits
- **Credit cards**: Groups of 4 digits
- **Content**: 5-9 items per group

### Visual Hierarchy (Von Restorff)
- **CTAs**: Make primary action visually distinct
- **Notifications**: Use contrast for important alerts
- **Pricing**: Highlight recommended option

## References

- `references/laws-complete.md` - Complete laws reference with examples
- `references/psychology-principles.md` - Underlying cognitive psychology
- `references/design-patterns.md` - Implementation patterns for each law

## Token Efficiency

This skill achieves significant token savings:

| Operation | Traditional | Context7 Efficient |
|-----------|-------------|-------------------|
| Full docs fetch | ~50K tokens | 0 tokens (subprocess) |
| Filtered output | N/A | ~2-5K tokens |
| **Savings** | - | **90-96%** |
