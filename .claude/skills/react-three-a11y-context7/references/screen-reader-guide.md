# Screen Reader Integration Guide for @react-three/a11y

## Overview

Making 3D WebGL content accessible to screen reader users requires providing text alternatives, meaningful descriptions, and dynamic announcements. This guide covers screen reader integration patterns for React Three Fiber applications.

---

## How Screen Readers See 3D Content

WebGL canvases are inherently inaccessible - screen readers cannot interpret pixel data. @react-three/a11y bridges this gap by:

1. Creating invisible DOM elements that mirror 3D objects
2. Positioning these elements to match 3D object locations
3. Managing ARIA attributes and live regions
4. Announcing changes via the A11yAnnouncer component

```
┌─────────────────────────────────────────┐
│  Visual Canvas (WebGL)                  │
│  ┌─────┐  ┌─────┐  ┌─────┐            │
│  │Cube1│  │Cube2│  │Cube3│            │
│  └─────┘  └─────┘  └─────┘            │
└─────────────────────────────────────────┘
            ↓ A11y maps to ↓
┌─────────────────────────────────────────┐
│  Accessible DOM Layer (invisible)       │
│  <button aria-label="Cube1">            │
│  <button aria-label="Cube2">            │
│  <button aria-label="Cube3">            │
└─────────────────────────────────────────┘
```

---

## Providing Descriptions

### Basic Description

```tsx
<A11y
  role="button"
  description="Blue cube - click to change color"
>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial color="blue" />
  </mesh>
</A11y>
```

### Dynamic Descriptions

Update descriptions based on state:

```tsx
function ColorCube() {
  const [color, setColor] = useState('blue')

  return (
    <A11y
      role="button"
      description={`${color} cube - click to change color`}
      actionCall={() => setColor(color === 'blue' ? 'red' : 'blue')}
    >
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color={color} />
      </mesh>
    </A11y>
  )
}
```

### Detailed Descriptions with aria-describedby

For complex descriptions, reference external content:

```tsx
function DataVisualization({ data }) {
  return (
    <>
      <A11y
        role="content"
        description="Sales chart"
        aria-describedby="chart-description"
      >
        <Chart3D data={data} />
      </A11y>

      {/* Hidden description outside Canvas */}
      <div id="chart-description" className="sr-only">
        Bar chart showing monthly sales from January to December.
        Highest sales in December at $150,000.
        Lowest sales in February at $45,000.
        Average monthly sales: $87,000.
      </div>
    </>
  )
}
```

---

## Writing Effective Descriptions

### Good Description Practices

```tsx
// BAD: Vague, doesn't convey purpose
<A11y description="cube">

// GOOD: Describes purpose and action
<A11y description="Volume control slider, currently at 75%">

// BAD: Too technical
<A11y description="BoxGeometry mesh with MeshStandardMaterial">

// GOOD: User-focused
<A11y description="Product image - Nike Air Max sneakers">

// BAD: Missing state information
<A11y description="Toggle button">

// GOOD: Includes current state
<A11y description="Sound toggle, currently muted" pressed={false}>
```

### Description Templates

| Element Type | Description Template |
|--------------|---------------------|
| Navigation | "[Destination] link" |
| Action button | "[Action] button" |
| Toggle | "[Feature] toggle, currently [state]" |
| Data display | "[Data type] showing [summary]" |
| Image/model | "[Subject] - [brief description]" |
| Interactive | "[Object] - [how to interact]" |

---

## Live Announcements

### Setting Up Announcements

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

### Making Announcements

```tsx
function InteractiveScene() {
  const { announce } = useA11y()

  const handleItemCollected = (item) => {
    // Polite announcement - doesn't interrupt
    announce(`Collected ${item.name}`, 'polite')
  }

  const handleDangerAlert = () => {
    // Assertive announcement - interrupts immediately
    announce('Warning: Obstacle ahead!', 'assertive')
  }

  return (
    <group>
      <CollectibleItems onCollect={handleItemCollected} />
      <DangerZone onEnter={handleDangerAlert} />
    </group>
  )
}
```

### When to Use Each Priority

| Priority | Use For | Example |
|----------|---------|---------|
| `polite` | Status updates, confirmations | "Item added to cart" |
| `assertive` | Errors, warnings, time-sensitive | "Session expiring in 1 minute" |

### Announcement Patterns

```tsx
// Loading states
announce('Loading 3D model, please wait', 'polite')
announce('Model loaded successfully', 'polite')

// User actions
announce('Rotated view 90 degrees', 'polite')
announce('Zoomed in to 150%', 'polite')

// Errors
announce('Error: Could not load texture', 'assertive')
announce('Connection lost, attempting to reconnect', 'assertive')

// Navigation
announce('Now viewing: Kitchen section', 'polite')
announce('Exited fullscreen mode', 'polite')

// Game-like interactions
announce('Level 2 complete! Score: 1500', 'polite')
announce('Game over', 'assertive')
```

---

## ARIA Roles and Attributes

### Supported Roles

| Role | Use Case | Keyboard |
|------|----------|----------|
| `button` | Clickable actions | Enter, Space |
| `link` | Navigation | Enter |
| `content` | Static information | N/A (readable) |
| `togglebutton` | On/off controls | Enter, Space |

### Additional ARIA Attributes

```tsx
<A11y
  role="button"
  description="Main action"

  // Additional ARIA
  aria-label="Submit form"
  aria-describedby="form-instructions"
  aria-disabled={isDisabled}
  aria-expanded={isExpanded}
  aria-pressed={isPressed}
>
  <ButtonMesh />
</A11y>
```

### Hiding Decorative Elements

```tsx
// Decorative elements should be hidden from screen readers
<A11y
  role="content"
  aria-hidden={true}
>
  <DecorativeParticles />
</A11y>

// Or simply don't wrap decorative elements
<Particles /> {/* Not wrapped = not announced */}
```

---

## Complex Content Patterns

### Data Tables in 3D

For 3D data visualizations, provide text alternatives:

```tsx
function BarChart3D({ data }) {
  const { announce } = useA11y()

  return (
    <group>
      {/* Overall chart description */}
      <A11y
        role="content"
        description={`Bar chart with ${data.length} data points.
          Range: ${Math.min(...data.map(d => d.value))} to
          ${Math.max(...data.map(d => d.value))}.`}
      >
        <ChartBackground />
      </A11y>

      {/* Individual bars are focusable */}
      {data.map((item, index) => (
        <A11y
          key={item.label}
          role="content"
          description={`${item.label}: ${item.value}`}
          focusCall={() => announce(`${item.label}: ${item.value}`)}
          tabIndex={0}
        >
          <Bar height={item.value} position={[index * 2, 0, 0]} />
        </A11y>
      ))}
    </group>
  )
}
```

### Interactive 3D Models

```tsx
function ProductViewer({ product }) {
  const { announce } = useA11y()
  const [angle, setAngle] = useState(0)

  const rotate = (direction) => {
    const newAngle = angle + (direction * 45)
    setAngle(newAngle)
    announce(`Rotated to ${newAngle} degrees`, 'polite')
  }

  return (
    <>
      <A11y
        role="content"
        description={`3D view of ${product.name}.
          Use arrow buttons to rotate.
          Currently showing: front view.`}
      >
        <ProductModel rotation={[0, angle * Math.PI / 180, 0]} />
      </A11y>

      <A11y
        role="button"
        description="Rotate left"
        actionCall={() => rotate(-1)}
      >
        <RotateLeftButton />
      </A11y>

      <A11y
        role="button"
        description="Rotate right"
        actionCall={() => rotate(1)}
      >
        <RotateRightButton />
      </A11y>
    </>
  )
}
```

### Virtual Reality / Immersive Content

For VR content, provide alternative experiences:

```tsx
function VRScene() {
  const { announce } = useA11y()

  return (
    <>
      {/* Announce VR content limitations */}
      <A11y
        role="content"
        description="Virtual reality experience.
          For non-VR users: This scene shows a virtual art gallery
          with 12 paintings arranged in a circular room."
      >
        <VRGallery />
      </A11y>

      {/* Provide text-based alternative */}
      <Html>
        <details className="sr-only focus:not-sr-only">
          <summary>View gallery as text list</summary>
          <ul>
            <li>Painting 1: Starry Night by Van Gogh</li>
            <li>Painting 2: Mona Lisa by Da Vinci</li>
            {/* ... */}
          </ul>
        </details>
      </Html>
    </>
  )
}
```

---

## Testing with Screen Readers

### Manual Testing

Test with multiple screen readers:

| OS | Screen Reader | Browser |
|----|---------------|---------|
| macOS | VoiceOver | Safari, Chrome |
| Windows | NVDA | Firefox, Chrome |
| Windows | JAWS | Chrome, Edge |
| iOS | VoiceOver | Safari |
| Android | TalkBack | Chrome |

### Testing Checklist

- [ ] All interactive elements are announced
- [ ] Descriptions accurately describe content
- [ ] State changes are announced
- [ ] Focus order is logical
- [ ] No content is skipped
- [ ] Dynamic content is announced appropriately
- [ ] Error messages are announced immediately

### Common Screen Reader Commands

| Action | VoiceOver (Mac) | NVDA (Windows) |
|--------|-----------------|----------------|
| Next item | VO + Right | Down |
| Previous item | VO + Left | Up |
| Activate | VO + Space | Enter |
| Read all | VO + A | NVDA + Down |
| Stop reading | Ctrl | Ctrl |
| List headings | VO + U | H |
| List buttons | VO + U | B |

---

## Debugging Screen Reader Issues

### Enable Debug Mode

```tsx
<A11y
  role="button"
  description="Debug me"
  debug={true} // Shows bounding box
>
  <Mesh />
</A11y>
```

### Inspect Generated HTML

The A11y component creates DOM elements you can inspect:

```javascript
// In browser console
document.querySelectorAll('[data-a11y]')
```

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Element not announced | Missing A11y wrapper | Wrap with `<A11y>` |
| Wrong role announced | Incorrect role prop | Use appropriate role |
| Stale description | Static description | Make description dynamic |
| Missing state | No pressed/expanded | Add state props |
| Double announcements | Redundant descriptions | Consolidate text |
| No focus indicator | Missing visual feedback | Add focus styles |

---

## Performance Considerations

### Optimize for Many Objects

```tsx
// BAD: Every particle is accessible
{particles.map(p => (
  <A11y key={p.id} description={`Particle ${p.id}`}>
    <Particle />
  </A11y>
))}

// GOOD: Group with single description
<A11y
  role="content"
  description="Particle effect with 1000 particles"
>
  <ParticleSystem count={1000} />
</A11y>
```

### Debounce Announcements

```tsx
const { announce } = useA11y()
const announceDebounced = useMemo(
  () => debounce((msg) => announce(msg, 'polite'), 300),
  [announce]
)

useFrame(() => {
  // Frequent updates - debounce announcements
  if (positionChanged) {
    announceDebounced(`Position: ${x}, ${y}`)
  }
})
```
