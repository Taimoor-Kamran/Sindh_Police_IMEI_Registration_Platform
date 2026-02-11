# Tailwind CSS v4 Patterns Reference

## @theme Directive

### Define Custom Colors
```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.7 0.15 250);
  --color-secondary: oklch(0.6 0.12 300);
  --color-brand-blue: #3b82f6;
}
```
Generates: `bg-primary`, `text-secondary`, `border-brand-blue`

### Custom Fonts
```css
@theme {
  --font-display: "Cal Sans", sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "Fira Code", monospace;
}
```
Generates: `font-display`, `font-body`, `font-mono`

### Custom Spacing
```css
@theme {
  --spacing-18: 4.5rem;
  --spacing-128: 32rem;
}
```
Generates: `p-18`, `m-128`, `gap-18`, etc.

### Custom Breakpoints
```css
@theme {
  --breakpoint-xs: 30rem;
  --breakpoint-3xl: 120rem;
}
```
Generates: `xs:`, `3xl:` variants

## @layer Directive

### Base Layer
```css
@layer base {
  html {
    font-family: var(--font-body);
    scroll-behavior: smooth;
  }

  h1 { @apply text-4xl font-bold; }
  h2 { @apply text-3xl font-semibold; }
  h3 { @apply text-2xl font-medium; }

  ::selection {
    background-color: var(--color-primary);
    color: white;
  }
}
```

### Components Layer
```css
@layer components {
  .btn {
    @apply inline-flex items-center justify-center
           px-4 py-2 font-medium rounded-lg
           transition-colors duration-200;
  }

  .btn-primary {
    @apply bg-primary text-white hover:bg-primary/90;
  }

  .btn-outline {
    @apply border-2 border-primary text-primary
           hover:bg-primary hover:text-white;
  }

  .card {
    @apply bg-white rounded-xl shadow-md p-6
           dark:bg-gray-800;
  }

  .input {
    @apply w-full px-4 py-2 border rounded-lg
           focus:outline-none focus:ring-2
           focus:ring-primary/50;
  }
}
```

### Utilities Layer
```css
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  .glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
  }
}
```

## @utility Directive

### Custom Utility with Variants
```css
@utility tab-* {
  tab-size: --value(--tab-size-*);
}

@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
  --tab-size-8: 8;
}
```
Generates: `tab-2`, `tab-4`, `tab-8`

### Functional Utility
```css
@utility content-auto {
  content-visibility: auto;
}
```
Works with variants: `hover:content-auto`, `lg:content-auto`

## Dark Mode

### Using prefers-color-scheme
```css
@theme {
  --color-background: white;
  --color-foreground: black;
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: #0a0a0a;
    --color-foreground: #fafafa;
  }
}
```

### Using Class Strategy
```html
<html class="dark">
  <!-- dark mode active -->
</html>
```

```css
.dark {
  --color-background: #0a0a0a;
  --color-foreground: #fafafa;
}
```

## Container Queries

```css
@utility @container {
  container-type: inline-size;
}

/* In HTML */
<div class="@container">
  <div class="@md:flex @lg:grid">
    <!-- Responds to container, not viewport -->
  </div>
</div>
```

## Animation Patterns

### Keyframe Animation
```css
@theme {
  --animate-fade-in: fade-in 0.5s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```
Use: `animate-fade-in`, `animate-slide-up`

### Transition Utilities
```html
<button class="transition-colors duration-200 hover:bg-primary">
  Hover me
</button>

<div class="transition-transform hover:scale-105">
  Scale on hover
</div>
```

## Responsive Patterns

### Mobile-First
```html
<div class="flex flex-col md:flex-row lg:grid lg:grid-cols-3">
  <!-- Stack on mobile, row on tablet, 3-col grid on desktop -->
</div>
```

### Container-Based
```html
<div class="w-full max-w-md mx-auto lg:max-w-4xl">
  <!-- Contained width with responsive max -->
</div>
```

## Common Component Patterns

### Flexbox Centering
```html
<div class="flex items-center justify-center min-h-screen">
  <content />
</div>
```

### Grid Layout
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <card />
  <card />
  <card />
</div>
```

### Sticky Header
```html
<header class="sticky top-0 z-50 bg-white/80 backdrop-blur-sm">
  <nav />
</header>
```

### Aspect Ratio
```html
<div class="aspect-video bg-gray-200">
  <img class="object-cover w-full h-full" />
</div>
```

## @plugin Directive

### Load Legacy Plugin
```css
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
@plugin "@tailwindcss/container-queries";
```

## Arbitrary Values

```html
<!-- Custom values -->
<div class="w-[317px] h-[100dvh] bg-[#1da1f2]">

<!-- CSS variables -->
<div class="bg-[var(--brand-color)]">

<!-- Calc expressions -->
<div class="w-[calc(100%-2rem)]">
```
