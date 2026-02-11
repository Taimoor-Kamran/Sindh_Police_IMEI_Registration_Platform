# UI/UX Design Principles

## The 7 Fundamental Visual Design Principles

### 1. Contrast

Create visual distinction between elements to establish hierarchy and focus.

```css
/* High contrast for primary actions */
.btn-primary {
  background: #0066cc;
  color: #ffffff;
  font-weight: 600;
}

/* Low contrast for secondary/disabled */
.btn-secondary {
  background: #f5f5f5;
  color: #666666;
}
```

**Guidelines:**
- Use contrast to draw attention to important elements
- Ensure text contrast meets WCAG standards (4.5:1 minimum)
- Create contrast through color, size, weight, and spacing

### 2. Repetition

Establish consistency through repeated visual patterns.

```css
/* Design tokens for consistency */
:root {
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;

  --font-body: 'Inter', system-ui, sans-serif;
  --font-heading: 'Inter', system-ui, sans-serif;
}
```

**Guidelines:**
- Reuse colors, fonts, and spacing consistently
- Create a component library with consistent patterns
- Use design tokens for systematic consistency

### 3. Alignment

Create visual connections through proper alignment.

```css
/* Grid-based alignment */
.container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--spacing-md);
}

/* Consistent text alignment */
.card-content {
  text-align: left; /* Prefer left-align for readability */
}

.centered-hero {
  text-align: center;
  max-width: 60ch;
  margin-inline: auto;
}
```

**Guidelines:**
- Align elements along invisible lines
- Use a grid system for consistent layout
- Left-align text for readability, center for emphasis

### 4. Proximity

Group related elements together, separate unrelated ones.

```css
/* Group related items */
.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-group label {
  margin-bottom: var(--spacing-xs);
  display: block;
}

.form-group input {
  margin-bottom: var(--spacing-xs);
}

.form-group .helper-text {
  margin-top: var(--spacing-xs);
  font-size: 0.875rem;
  color: var(--color-muted);
}
```

**Guidelines:**
- Place related items close together
- Use whitespace to separate groups
- Proximity implies relationship

### 5. Balance

Distribute visual weight evenly across the design.

```css
/* Symmetric balance */
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

/* Asymmetric balance */
.feature-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-xl);
  align-items: center;
}
```

**Guidelines:**
- Balance can be symmetric or asymmetric
- Consider visual weight of colors and sizes
- Use whitespace as a balancing element

### 6. Hierarchy

Establish importance order to guide the eye.

```css
/* Typography hierarchy */
h1 {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  line-height: 1.3;
}

h3 {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.4;
}

p {
  font-size: 1rem;
  line-height: 1.6;
}

.caption {
  font-size: 0.875rem;
  color: var(--color-muted);
}
```

**Guidelines:**
- Larger = more important
- Bolder = more important
- Darker/more saturated = more important

### 7. White Space

Allow elements to breathe with purposeful empty space.

```css
/* Generous whitespace */
.section {
  padding: var(--spacing-xl) 0;
}

.card {
  padding: var(--spacing-lg);
}

/* Line height for readability */
.prose {
  line-height: 1.7;
  max-width: 65ch;
}

/* Letter spacing for headings */
h1, h2 {
  letter-spacing: -0.02em;
}
```

**Guidelines:**
- More whitespace = more premium feel
- Don't fill every pixel
- Use consistent spacing scale

---

## Color Theory

### Color Relationships

```css
/* Complementary (opposite on wheel) */
.accent { background: #0066cc; } /* Blue */
.highlight { background: #cc6600; } /* Orange */

/* Analogous (adjacent on wheel) */
.primary { background: #0066cc; } /* Blue */
.secondary { background: #0099cc; } /* Cyan */
.tertiary { background: #6600cc; } /* Purple */

/* Triadic (evenly spaced) */
.color-1 { background: #cc0000; } /* Red */
.color-2 { background: #00cc00; } /* Green */
.color-3 { background: #0000cc; } /* Blue */
```

### Color Semantics

```css
:root {
  /* Status colors */
  --color-success: #22c55e;
  --color-warning: #eab308;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Neutral scale */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
}
```

### Contrast Requirements

| Context | Minimum Ratio | Example |
|---------|---------------|---------|
| Normal text | 4.5:1 | #595959 on #ffffff |
| Large text (18px+) | 3:1 | #767676 on #ffffff |
| UI components | 3:1 | Borders, icons |
| Non-essential | No requirement | Decorative elements |

---

## Typography

### Type Scale

```css
:root {
  /* Modular scale: 1.25 (Major Third) */
  --text-xs: 0.64rem;   /* 10.24px */
  --text-sm: 0.8rem;    /* 12.8px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.25rem;   /* 20px */
  --text-xl: 1.563rem;  /* 25px */
  --text-2xl: 1.953rem; /* 31.25px */
  --text-3xl: 2.441rem; /* 39px */
  --text-4xl: 3.052rem; /* 48.8px */
}
```

### Font Pairing Guidelines

```css
/* Sans-serif body + Sans-serif headings (modern) */
body { font-family: 'Inter', system-ui, sans-serif; }
h1, h2, h3 { font-family: 'Inter', system-ui, sans-serif; }

/* Serif headings + Sans-serif body (editorial) */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif; }
body { font-family: 'Source Sans Pro', system-ui, sans-serif; }

/* Monospace for code */
code, pre { font-family: 'JetBrains Mono', 'Fira Code', monospace; }
```

### Readability

```css
/* Optimal line length */
.prose {
  max-width: 65ch; /* 45-75 characters ideal */
}

/* Line height by context */
.body-text { line-height: 1.6; }
.heading { line-height: 1.2; }
.ui-label { line-height: 1.4; }

/* Paragraph spacing */
.prose p + p {
  margin-top: 1.25em;
}
```

---

## Spacing System

### 8-Point Grid

```css
:root {
  /* Base unit: 8px */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-10: 2.5rem;  /* 40px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
  --space-20: 5rem;    /* 80px */
  --space-24: 6rem;    /* 96px */
}
```

### Component Spacing Patterns

```css
/* Card padding */
.card {
  padding: var(--space-6);
}

/* Button padding */
.btn {
  padding: var(--space-2) var(--space-4);
}

/* Form field spacing */
.form-field {
  margin-bottom: var(--space-4);
}

/* Section spacing */
.section {
  padding-block: var(--space-16);
}
```

---

## Layout Patterns

### Container Width

```css
.container {
  width: 100%;
  max-width: 1280px;
  margin-inline: auto;
  padding-inline: var(--space-4);
}

@media (min-width: 640px) {
  .container {
    padding-inline: var(--space-6);
  }
}

@media (min-width: 1024px) {
  .container {
    padding-inline: var(--space-8);
  }
}
```

### Common Grid Patterns

```css
/* 12-column grid */
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6);
}

/* Auto-fit cards */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-6);
}

/* Sidebar layout */
.sidebar-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--space-8);
}

/* Holy grail */
.holy-grail {
  display: grid;
  grid-template:
    "header header header" auto
    "nav    main   aside" 1fr
    "footer footer footer" auto
    / 200px 1fr 200px;
  min-height: 100vh;
}
```

### Flexbox Patterns

```css
/* Center content */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Space between */
.space-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Stack (vertical) */
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Cluster (horizontal wrap) */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}
```

---

## Responsive Design

### Mobile-First Breakpoints

```css
/* Base: Mobile (0-639px) */
.component {
  padding: var(--space-4);
  font-size: var(--text-base);
}

/* sm: 640px+ (Landscape phones, small tablets) */
@media (min-width: 640px) {
  .component {
    padding: var(--space-6);
  }
}

/* md: 768px+ (Tablets) */
@media (min-width: 768px) {
  .component {
    padding: var(--space-8);
  }
}

/* lg: 1024px+ (Laptops) */
@media (min-width: 1024px) {
  .component {
    padding: var(--space-10);
  }
}

/* xl: 1280px+ (Desktops) */
@media (min-width: 1280px) {
  .component {
    padding: var(--space-12);
  }
}

/* 2xl: 1536px+ (Large screens) */
@media (min-width: 1536px) {
  .component {
    max-width: 1440px;
  }
}
```

### Fluid Typography

```css
/* Clamp for fluid scaling */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
}

h2 {
  font-size: clamp(1.5rem, 3vw + 0.75rem, 2.5rem);
}

p {
  font-size: clamp(1rem, 1vw + 0.75rem, 1.125rem);
}
```

---

## Dark Mode

### Theme Implementation

```css
:root {
  /* Light theme (default) */
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --border-color: #e5e7eb;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #111827;
    --bg-secondary: #1f2937;
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --border-color: #374151;
  }
}

/* Manual toggle support */
[data-theme="dark"] {
  --bg-primary: #111827;
  --bg-secondary: #1f2937;
  --text-primary: #f9fafb;
  --text-secondary: #9ca3af;
  --border-color: #374151;
}
```

### Dark Mode Best Practices

- Don't just invert colors (pure white on black is harsh)
- Reduce contrast slightly (use off-white #f9fafb not #ffffff)
- Adjust shadows (use transparency, not gray)
- Consider elevation with lighter backgrounds
- Test all states (hover, focus, active, disabled)
