---
name: uiux-design-context7
description: Fetch and search UI/UX design documentation from Context7. Use when the user asks about design systems, accessibility, color theory, typography, layout patterns, responsive design, user experience principles, or needs help with CSS/visual implementation best practices.
---

# UI/UX Design Context7 Documentation Skill

Efficiently fetch and search UI/UX design documentation using Context7's API with token-optimized filtering.

## Quick Start

```bash
# Search for specific UI/UX topic
./scripts/fetch-docs.sh "accessibility"

# Get color and typography documentation
./scripts/fetch-docs.sh "color theory" --section="contrast"

# Search for layout patterns
./scripts/fetch-docs.sh "flexbox grid" --verbose
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
# Get CSS examples only
./scripts/extract-css.sh "<topic>"

# Get design principles only
./scripts/extract-principles.sh "<topic>"

# Get accessibility guidelines
./scripts/extract-a11y.sh "<topic>"
```

## Common Topics

### Visual Design
| Topic | Description |
|-------|-------------|
| `color-theory` | Color palettes, harmony, contrast ratios |
| `typography` | Font selection, hierarchy, readability |
| `spacing` | Whitespace, margins, padding systems |
| `layout` | Grid systems, flexbox patterns, composition |
| `visual-hierarchy` | Emphasis, flow, attention guidance |
| `iconography` | Icon design, consistency, sizing |

### User Experience
| Topic | Description |
|-------|-------------|
| `accessibility` | WCAG guidelines, ARIA, screen readers |
| `usability` | Heuristics, user testing, cognitive load |
| `navigation` | Menus, breadcrumbs, wayfinding |
| `forms` | Input design, validation, error handling |
| `feedback` | Loading states, notifications, confirmations |
| `microinteractions` | Animations, transitions, hover states |

### Design Systems
| Topic | Description |
|-------|-------------|
| `design-tokens` | Variables, theming, consistency |
| `components` | Buttons, cards, modals, patterns |
| `responsive` | Breakpoints, fluid design, mobile-first |
| `dark-mode` | Theme switching, color adaptation |

## Output Format

Documentation is returned in structured markdown:

```markdown
## Topic: <searched-topic>

### Summary
Brief explanation of the concept

### Design Principles
- Core principles and guidelines

### Implementation
```css
/* CSS example */
.component {
  /* properties */
}
```

### Accessibility
- A11y considerations for this pattern

### Best Practices
- Do's and don'ts

### Related
- Link to related topics
```

## Design Principles Reference

### The 7 Fundamental Principles

1. **Contrast** - Create visual distinction between elements
2. **Repetition** - Establish consistency through patterns
3. **Alignment** - Create visual connections
4. **Proximity** - Group related elements
5. **Balance** - Distribute visual weight
6. **Hierarchy** - Establish importance order
7. **White Space** - Allow elements to breathe

### Accessibility Essentials

- **Color Contrast**: 4.5:1 for normal text, 3:1 for large text
- **Focus Indicators**: Visible keyboard focus states
- **Alt Text**: Descriptive alternatives for images
- **Semantic HTML**: Proper heading structure, landmarks
- **Touch Targets**: Minimum 44x44px for mobile

### Responsive Breakpoints (Mobile-First)

```css
/* Base: Mobile (0-639px) */
/* sm: 640px+ */
/* md: 768px+ */
/* lg: 1024px+ */
/* xl: 1280px+ */
/* 2xl: 1536px+ */
```

## References

- `references/design-principles.md` - Core design principles and guidelines
- `references/accessibility-guide.md` - WCAG compliance and a11y patterns
- `references/css-patterns.md` - Common CSS patterns and implementations

## Token Efficiency

This skill achieves significant token savings:

| Operation | Traditional | Context7 Efficient |
|-----------|-------------|-------------------|
| Full docs fetch | ~50K tokens | 0 tokens (subprocess) |
| Filtered output | N/A | ~2-5K tokens |
| **Savings** | - | **90-96%** |
