# @react-three/a11y Component Reference

## Installation

```bash
npm install @react-three/a11y
# or
yarn add @react-three/a11y
# or
pnpm add @react-three/a11y
```

---

## A11y Component

The main wrapper component that makes 3D objects accessible.

### Props

```typescript
interface A11yProps {
  /** Accessibility role for the wrapped element */
  role?: 'button' | 'link' | 'content' | 'togglebutton';

  /** Description read by screen readers */
  description?: string;

  /** Alternative description for screen readers */
  a11yElStyle?: React.CSSProperties;

  /** Tab order index */
  tabIndex?: number;

  /** Called when Enter/Space pressed or element clicked */
  actionCall?: () => void;

  /** Called when element receives focus */
  focusCall?: () => void;

  /** Called when element loses focus */
  blurCall?: () => void;

  /** For togglebutton role - current pressed state */
  pressed?: boolean;

  /** Activates debug mode showing bounding box */
  debug?: boolean;

  /** Show focus ring (requires CSS) */
  showFocusRing?: boolean;

  /** Additional ARIA attributes */
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-hidden'?: boolean;

  /** Children - 3D objects to make accessible */
  children: React.ReactNode;
}
```

### Basic Usage

```tsx
import { Canvas } from '@react-three/fiber'
import { A11y, A11yAnnouncer } from '@react-three/a11y'

function AccessibleButton() {
  const handleClick = () => {
    console.log('Button activated!')
  }

  return (
    <A11y
      role="button"
      description="A 3D button that opens settings"
      actionCall={handleClick}
    >
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="blue" />
      </mesh>
    </A11y>
  )
}

function App() {
  return (
    <>
      <Canvas>
        <ambientLight />
        <AccessibleButton />
      </Canvas>
      <A11yAnnouncer />
    </>
  )
}
```

### Role Examples

#### Button Role

```tsx
// Interactive button - activated with Enter/Space
<A11y
  role="button"
  description="Submit form"
  actionCall={() => submitForm()}
>
  <SubmitButtonMesh />
</A11y>
```

#### Link Role

```tsx
// Navigation link - activated with Enter
<A11y
  role="link"
  description="Go to home page"
  actionCall={() => navigate('/')}
>
  <HomeIconMesh />
</A11y>
```

#### Content Role

```tsx
// Non-interactive, informational content
<A11y
  role="content"
  description="3D model of a house showing the front exterior"
>
  <HouseModel />
</A11y>
```

#### Toggle Button Role

```tsx
// Toggle with pressed state
const [isOn, setIsOn] = useState(false)

<A11y
  role="togglebutton"
  description={`Sound is ${isOn ? 'on' : 'off'}`}
  pressed={isOn}
  actionCall={() => setIsOn(!isOn)}
>
  <SoundToggleMesh active={isOn} />
</A11y>
```

---

## A11yAnnouncer

Renders a visually hidden live region for screen reader announcements.

### Usage

```tsx
import { A11yAnnouncer } from '@react-three/a11y'

function App() {
  return (
    <>
      <Canvas>
        <Scene />
      </Canvas>
      {/* Place outside Canvas, once per app */}
      <A11yAnnouncer />
    </>
  )
}
```

### Customization

```tsx
<A11yAnnouncer
  // CSS styles for the announcer container
  style={{
    position: 'absolute',
    left: '-10000px',
    width: '1px',
    height: '1px',
    overflow: 'hidden',
  }}
/>
```

---

## A11ySection

Groups related accessible elements for better organization.

### Props

```typescript
interface A11ySectionProps {
  /** Section label for screen readers */
  label: string;

  /** Section description */
  description?: string;

  /** Children - A11y wrapped elements */
  children: React.ReactNode;
}
```

### Usage

```tsx
import { A11ySection, A11y } from '@react-three/a11y'

function NavigationBar() {
  return (
    <A11ySection label="Main navigation" description="Site navigation links">
      <A11y role="link" description="Home" actionCall={() => navigate('/')}>
        <HomeButton />
      </A11y>
      <A11y role="link" description="About" actionCall={() => navigate('/about')}>
        <AboutButton />
      </A11y>
      <A11y role="link" description="Contact" actionCall={() => navigate('/contact')}>
        <ContactButton />
      </A11y>
    </A11ySection>
  )
}
```

---

## A11yUserPreferences

Context provider for user accessibility preferences.

### Props

```typescript
interface A11yUserPreferencesProps {
  /** Respect prefers-reduced-motion */
  reduceMotion?: boolean;

  /** Respect prefers-color-scheme */
  prefersDarkMode?: boolean;

  /** Custom preferences */
  preferences?: {
    highContrast?: boolean;
    largeText?: boolean;
  };

  children: React.ReactNode;
}
```

### Usage

```tsx
import { A11yUserPreferences, useA11y } from '@react-three/a11y'

function App() {
  return (
    <A11yUserPreferences>
      <Canvas>
        <AccessibleScene />
      </Canvas>
    </A11yUserPreferences>
  )
}

function AccessibleScene() {
  const { prefersReducedMotion } = useA11y()

  return (
    <mesh>
      {!prefersReducedMotion && <AnimatedRotation />}
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  )
}
```

---

## useA11y Hook

Access accessibility state and preferences within components.

### Return Values

```typescript
interface UseA11yReturn {
  /** User prefers reduced motion */
  prefersReducedMotion: boolean;

  /** User prefers dark mode */
  prefersDarkMode: boolean;

  /** Announce message to screen readers */
  announce: (message: string, priority?: 'polite' | 'assertive') => void;

  /** Current focus state */
  focused: boolean;

  /** Current hover state */
  hovered: boolean;
}
```

### Usage

```tsx
import { useA11y } from '@react-three/a11y'

function AccessibleMesh() {
  const { focused, hovered, announce, prefersReducedMotion } = useA11y()

  useEffect(() => {
    if (focused) {
      announce('Cube is now focused')
    }
  }, [focused, announce])

  return (
    <mesh scale={focused || hovered ? 1.1 : 1}>
      <boxGeometry />
      <meshStandardMaterial
        color={focused ? 'yellow' : hovered ? 'lightblue' : 'white'}
      />
    </mesh>
  )
}
```

---

## Focus Management

### Visual Focus Indicators

```tsx
function FocusableObject() {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <A11y
      role="button"
      description="Focusable cube"
      focusCall={() => setIsFocused(true)}
      blurCall={() => setIsFocused(false)}
      actionCall={() => console.log('Activated!')}
    >
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color={isFocused ? '#ffff00' : '#ffffff'} />
      </mesh>
      {/* Focus ring */}
      {isFocused && (
        <mesh>
          <boxGeometry args={[1.1, 1.1, 1.1]} />
          <meshBasicMaterial color="#0066ff" wireframe />
        </mesh>
      )}
    </A11y>
  )
}
```

### Tab Order Control

```tsx
function OrderedNavigation() {
  return (
    <group>
      <A11y tabIndex={1} role="button" description="First item">
        <FirstMesh />
      </A11y>
      <A11y tabIndex={2} role="button" description="Second item">
        <SecondMesh />
      </A11y>
      <A11y tabIndex={3} role="button" description="Third item">
        <ThirdMesh />
      </A11y>
    </group>
  )
}
```

---

## Best Practices

### 1. Always Provide Descriptions

```tsx
// Bad - no description
<A11y role="button">
  <Mesh />
</A11y>

// Good - descriptive
<A11y role="button" description="Add item to shopping cart">
  <CartButtonMesh />
</A11y>
```

### 2. Use Appropriate Roles

```tsx
// Use 'button' for actions
<A11y role="button" description="Delete item">...</A11y>

// Use 'link' for navigation
<A11y role="link" description="View product details">...</A11y>

// Use 'content' for informational elements
<A11y role="content" description="Company logo">...</A11y>

// Use 'togglebutton' for on/off states
<A11y role="togglebutton" pressed={isActive}>...</A11y>
```

### 3. Provide Visual Feedback

```tsx
// Always show focus and hover states
<A11y
  role="button"
  focusCall={() => setFocused(true)}
  blurCall={() => setFocused(false)}
>
  <mesh>
    <material color={focused ? 'highlight' : 'default'} />
  </mesh>
</A11y>
```

### 4. Respect User Preferences

```tsx
const { prefersReducedMotion } = useA11y()

// Disable or reduce animations when preferred
useFrame((state) => {
  if (!prefersReducedMotion) {
    mesh.current.rotation.y += 0.01
  }
})
```

### 5. Include A11yAnnouncer

```tsx
// Always include announcer at app level
function App() {
  return (
    <>
      <Canvas>...</Canvas>
      <A11yAnnouncer />
    </>
  )
}
```
