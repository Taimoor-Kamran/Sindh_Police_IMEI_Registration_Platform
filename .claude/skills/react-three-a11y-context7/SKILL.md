---
name: react-three-a11y-context7
description: Fetch and search React Three A11y (@react-three/a11y) documentation from Context7. Use when the user asks about making 3D scenes accessible, keyboard navigation in Three.js/R3F, screen reader support for WebGL content, focus management in 3D, or ARIA patterns for react-three-fiber applications.
---

# React Three A11y Context7 Documentation Skill

Efficiently fetch and search @react-three/a11y documentation using Context7's API with token-optimized filtering.

## Quick Start

```bash
# Search for specific accessibility topic
./scripts/fetch-docs.sh "A11y component"

# Get keyboard navigation documentation
./scripts/fetch-docs.sh "keyboard" --section="focus"

# Search for screen reader patterns
./scripts/fetch-docs.sh "screen reader" --verbose
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
# Get component documentation
./scripts/extract-components.sh "<component-name>"

# Get accessibility patterns only
./scripts/extract-a11y.sh "<topic>"

# Get code examples only
./scripts/extract-examples.sh "<topic>"
```

## Common Topics

### Core Components
| Topic | Description |
|-------|-------------|
| `A11y` | Main accessibility wrapper component |
| `A11yAnnouncer` | Screen reader announcement system |
| `A11ySection` | Grouping related 3D objects |
| `A11yUserPreferences` | User preference context |

### Accessibility Features
| Topic | Description |
|-------|-------------|
| `keyboard-navigation` | Tab order, focus management in 3D |
| `screen-reader` | ARIA labels, live regions, descriptions |
| `focus-indicators` | Visual focus states for 3D objects |
| `role-mapping` | Mapping 3D elements to ARIA roles |
| `announcements` | Dynamic content announcements |

### Interaction Patterns
| Topic | Description |
|-------|-------------|
| `focusable` | Making 3D objects keyboard focusable |
| `actionable` | Click/Enter handlers for 3D |
| `describedby` | Associating descriptions with 3D objects |
| `tabindex` | Custom focus order in 3D scenes |

### Integration
| Topic | Description |
|-------|-------------|
| `react-three-fiber` | Integration with R3F |
| `drei` | Using with @react-three/drei helpers |
| `gestures` | Accessible touch/pointer interactions |
| `testing` | Testing 3D accessibility |

## Output Format

Documentation is returned in structured markdown:

```markdown
## Topic: <searched-topic>

### Summary
Brief explanation of the concept

### API Signatures
```typescript
interface A11yProps {
  role?: 'button' | 'link' | 'content' | 'togglebutton';
  description?: string;
  actionCall?: () => void;
  // ...
}
```

### Examples
```tsx
// Usage example
<A11y role="button" description="Open settings" actionCall={handleClick}>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</A11y>
```

### Best Practices
- Recommended patterns and guidelines

### Related
- Link to related topics
```

## Key Concepts

### Making 3D Objects Accessible

```tsx
import { A11y } from '@react-three/a11y'

function AccessibleCube() {
  return (
    <A11y
      role="button"
      description="Interactive cube - click to rotate"
      actionCall={() => console.log('Cube clicked')}
    >
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="hotpink" />
      </mesh>
    </A11y>
  )
}
```

### Screen Reader Announcements

```tsx
import { A11yAnnouncer, useA11y } from '@react-three/a11y'

function App() {
  return (
    <>
      <Canvas>
        <Scene />
      </Canvas>
      <A11yAnnouncer />
    </>
  )
}
```

### Keyboard Focus Management

```tsx
<A11y
  role="button"
  tabIndex={0}
  description="Press Enter to activate"
  focusCall={() => setHovered(true)}
  blurCall={() => setHovered(false)}
  actionCall={() => handleAction()}
>
  <InteractiveMesh />
</A11y>
```

## A11y Component Roles

| Role | Use Case | Keyboard Behavior |
|------|----------|-------------------|
| `button` | Clickable 3D objects | Enter/Space activates |
| `link` | Navigation elements | Enter activates |
| `content` | Informational, non-interactive | Tab skips, readable |
| `togglebutton` | On/off states | Enter/Space toggles |

## Accessibility Checklist for 3D Scenes

- [ ] All interactive objects wrapped with `<A11y>`
- [ ] Descriptive `description` props for screen readers
- [ ] Logical tab order through `tabIndex`
- [ ] Visual focus indicators for keyboard users
- [ ] `<A11yAnnouncer>` for dynamic announcements
- [ ] Reduced motion support via `useA11y` preferences
- [ ] Color contrast for any 2D overlays
- [ ] Alternative content for complex visualizations

## References

- `references/a11y-components.md` - Complete component API reference
- `references/keyboard-patterns.md` - Keyboard navigation patterns
- `references/screen-reader-guide.md` - Screen reader integration guide

## Token Efficiency

This skill achieves significant token savings:

| Operation | Traditional | Context7 Efficient |
|-----------|-------------|-------------------|
| Full docs fetch | ~50K tokens | 0 tokens (subprocess) |
| Filtered output | N/A | ~2-5K tokens |
| **Savings** | - | **90-96%** |
