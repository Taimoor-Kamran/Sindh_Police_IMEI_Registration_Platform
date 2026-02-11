# Keyboard Navigation Patterns for @react-three/a11y

## Overview

Making 3D scenes keyboard accessible requires careful attention to focus management, tab order, and keyboard event handling. This guide covers patterns for implementing keyboard navigation in React Three Fiber applications.

---

## Focus Management Fundamentals

### How Focus Works in 3D

Unlike traditional DOM elements, 3D objects in a canvas don't natively receive focus. @react-three/a11y creates an invisible DOM overlay that:

1. Mirrors the 3D object's position
2. Receives keyboard focus
3. Dispatches events to your 3D components

```tsx
// The A11y component handles focus bridging automatically
<A11y role="button" description="Interactive cube">
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</A11y>
```

### Focus States

```tsx
function FocusAwareMesh() {
  const [state, setState] = useState<'idle' | 'focused' | 'active'>('idle')

  return (
    <A11y
      role="button"
      description="Press Enter to activate"
      focusCall={() => setState('focused')}
      blurCall={() => setState('idle')}
      actionCall={() => {
        setState('active')
        // Return to focused after action
        setTimeout(() => setState('focused'), 100)
      }}
    >
      <mesh>
        <boxGeometry />
        <meshStandardMaterial
          color={
            state === 'active' ? '#00ff00' :
            state === 'focused' ? '#ffff00' :
            '#ffffff'
          }
        />
      </mesh>
    </A11y>
  )
}
```

---

## Tab Order Control

### Default Tab Order

By default, A11y components are focusable in DOM order (order they appear in JSX):

```tsx
function Scene() {
  return (
    <group>
      {/* Focused first */}
      <A11y role="button" description="Button 1">
        <Mesh1 />
      </A11y>

      {/* Focused second */}
      <A11y role="button" description="Button 2">
        <Mesh2 />
      </A11y>

      {/* Focused third */}
      <A11y role="button" description="Button 3">
        <Mesh3 />
      </A11y>
    </group>
  )
}
```

### Custom Tab Order

Use `tabIndex` to control focus order:

```tsx
function CustomOrderScene() {
  return (
    <group>
      {/* Visual order: 1, 2, 3 */}
      {/* Tab order: 2, 3, 1 */}

      <A11y tabIndex={2} role="button" description="Second in tab order">
        <Mesh1 position={[-2, 0, 0]} />
      </A11y>

      <A11y tabIndex={3} role="button" description="Third in tab order">
        <Mesh2 position={[0, 0, 0]} />
      </A11y>

      <A11y tabIndex={1} role="button" description="First in tab order">
        <Mesh3 position={[2, 0, 0]} />
      </A11y>
    </group>
  )
}
```

### Removing from Tab Order

```tsx
// tabIndex={-1} removes from tab order but keeps accessible
<A11y
  tabIndex={-1}
  role="content"
  description="Decorative element, not interactive"
>
  <DecorativeMesh />
</A11y>
```

---

## Keyboard Event Handling

### Standard Keyboard Actions

The A11y component automatically handles:

- **Enter**: Triggers `actionCall` for buttons and links
- **Space**: Triggers `actionCall` for buttons and togglebuttons
- **Tab**: Moves focus to next focusable element
- **Shift+Tab**: Moves focus to previous focusable element

### Custom Key Handlers

For additional keyboard support, handle events at the Canvas level:

```tsx
function Scene() {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    switch (event.key) {
      case 'ArrowUp':
        moveFocusUp()
        break
      case 'ArrowDown':
        moveFocusDown()
        break
      case 'ArrowLeft':
        moveFocusLeft()
        break
      case 'ArrowRight':
        moveFocusRight()
        break
      case 'Escape':
        clearSelection()
        break
    }
  }, [])

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])

  return (
    <group>
      <NavigableGrid />
    </group>
  )
}
```

---

## Focus Patterns

### Grid Navigation

For 2D grids of 3D objects, implement arrow key navigation:

```tsx
function AccessibleGrid({ items, columns }: { items: Item[], columns: number }) {
  const [focusedIndex, setFocusedIndex] = useState(0)

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      let newIndex = focusedIndex

      switch (e.key) {
        case 'ArrowRight':
          newIndex = Math.min(focusedIndex + 1, items.length - 1)
          break
        case 'ArrowLeft':
          newIndex = Math.max(focusedIndex - 1, 0)
          break
        case 'ArrowDown':
          newIndex = Math.min(focusedIndex + columns, items.length - 1)
          break
        case 'ArrowUp':
          newIndex = Math.max(focusedIndex - columns, 0)
          break
      }

      if (newIndex !== focusedIndex) {
        setFocusedIndex(newIndex)
        e.preventDefault()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [focusedIndex, items.length, columns])

  return (
    <group>
      {items.map((item, index) => {
        const row = Math.floor(index / columns)
        const col = index % columns

        return (
          <A11y
            key={item.id}
            role="button"
            description={item.label}
            tabIndex={index === focusedIndex ? 0 : -1}
            focusCall={() => setFocusedIndex(index)}
          >
            <mesh position={[col * 2, -row * 2, 0]}>
              <boxGeometry />
              <meshStandardMaterial
                color={index === focusedIndex ? 'yellow' : 'white'}
              />
            </mesh>
          </A11y>
        )
      })}
    </group>
  )
}
```

### Roving Tabindex

For component groups where only one item should be in the tab order:

```tsx
function RovingTabGroup({ items }: { items: Item[] }) {
  const [activeIndex, setActiveIndex] = useState(0)

  return (
    <group role="toolbar" aria-label="Tools">
      {items.map((item, index) => (
        <A11y
          key={item.id}
          role="button"
          description={item.label}
          // Only active item is in tab order
          tabIndex={index === activeIndex ? 0 : -1}
          focusCall={() => setActiveIndex(index)}
          actionCall={item.action}
        >
          <ToolMesh active={index === activeIndex} />
        </A11y>
      ))}
    </group>
  )
}
```

### Focus Trap for Modals

When showing a 3D modal/dialog, trap focus within it:

```tsx
function Modal3D({ isOpen, onClose, children }) {
  const modalRef = useRef<Group>(null)

  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }

      // Trap Tab within modal
      if (e.key === 'Tab') {
        // Get all focusable elements in modal
        // Cycle focus within them
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <group ref={modalRef}>
      <A11y
        role="button"
        description="Close modal"
        actionCall={onClose}
        tabIndex={1}
      >
        <CloseButton />
      </A11y>

      {children}

      <A11y
        role="button"
        description="Confirm"
        actionCall={() => { /* ... */ }}
        tabIndex={2}
      >
        <ConfirmButton />
      </A11y>
    </group>
  )
}
```

---

## Visual Focus Indicators

### Focus Ring Pattern

```tsx
function FocusRing({ visible, size = 1 }: { visible: boolean, size?: number }) {
  if (!visible) return null

  return (
    <mesh>
      <ringGeometry args={[size * 0.9, size, 32]} />
      <meshBasicMaterial color="#0066ff" side={DoubleSide} />
    </mesh>
  )
}

function FocusableObject() {
  const [focused, setFocused] = useState(false)

  return (
    <A11y
      role="button"
      description="Focusable object"
      focusCall={() => setFocused(true)}
      blurCall={() => setFocused(false)}
    >
      <group>
        <mesh>
          <sphereGeometry args={[0.5, 32, 32]} />
          <meshStandardMaterial />
        </mesh>
        <FocusRing visible={focused} size={0.6} />
      </group>
    </A11y>
  )
}
```

### Outline Effect

```tsx
import { Outline } from '@react-three/postprocessing'

function FocusOutline({ children, focused }) {
  return (
    <group>
      {children}
      {focused && (
        <Outline
          selection={children}
          edgeStrength={3}
          pulseSpeed={0}
          visibleEdgeColor={0x0066ff}
          hiddenEdgeColor={0x0033aa}
        />
      )}
    </group>
  )
}
```

### Scale Animation

```tsx
function ScaleFocus() {
  const [focused, setFocused] = useState(false)
  const meshRef = useRef<Mesh>(null)

  useFrame(() => {
    if (meshRef.current) {
      const targetScale = focused ? 1.1 : 1
      meshRef.current.scale.lerp(
        new Vector3(targetScale, targetScale, targetScale),
        0.1
      )
    }
  })

  return (
    <A11y
      role="button"
      description="Scale on focus"
      focusCall={() => setFocused(true)}
      blurCall={() => setFocused(false)}
    >
      <mesh ref={meshRef}>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>
    </A11y>
  )
}
```

---

## Skip Links for 3D Content

Provide a way to skip past complex 3D scenes:

```tsx
function App() {
  return (
    <>
      {/* Skip link before Canvas */}
      <a
        href="#after-3d"
        className="sr-only focus:not-sr-only"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          zIndex: 1000,
          background: 'white',
          padding: '8px',
        }}
      >
        Skip 3D content
      </a>

      <Canvas>
        <Scene />
      </Canvas>

      {/* Skip target */}
      <div id="after-3d" tabIndex={-1}>
        <h2>Content after 3D scene</h2>
      </div>

      <A11yAnnouncer />
    </>
  )
}
```

---

## Testing Keyboard Navigation

### Manual Testing Checklist

- [ ] Tab moves focus through all interactive elements
- [ ] Shift+Tab moves focus backwards
- [ ] Focus order is logical
- [ ] Focus indicator is always visible
- [ ] Enter/Space activates buttons
- [ ] Escape closes modals/menus
- [ ] Arrow keys work for grids/lists
- [ ] No keyboard traps exist

### Automated Testing

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('keyboard navigation works', async () => {
  render(<AccessibleScene />)

  // Tab to first button
  await userEvent.tab()
  expect(screen.getByRole('button', { name: /first/i })).toHaveFocus()

  // Tab to second button
  await userEvent.tab()
  expect(screen.getByRole('button', { name: /second/i })).toHaveFocus()

  // Activate with Enter
  await userEvent.keyboard('{Enter}')
  expect(mockHandler).toHaveBeenCalled()
})
```
