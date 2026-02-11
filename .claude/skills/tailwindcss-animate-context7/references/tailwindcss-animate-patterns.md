# Tailwind CSS Animate Common Patterns

Quick reference for common tailwindcss-animate patterns and best practices.

## Installation

### Plugin Setup

```bash
npm install -D tailwindcss-animate
```

```js
// tailwind.config.js
module.exports = {
  plugins: [
    require("tailwindcss-animate"),
  ],
}
```

### Tailwind CSS v4 (CSS-first)

```css
/* app.css */
@import "tailwindcss";
@plugin "tailwindcss-animate";
```

## Entrance Animations

### Basic Fade In

```html
<div class="animate-in fade-in">
  Fades in from 0% opacity
</div>
```

### Fade In with Custom Starting Opacity

```html
<div class="animate-in fade-in-25">
  Fades in starting from 25% opacity
</div>
```

### Slide In from Direction

```html
<!-- Slide in from top -->
<div class="animate-in slide-in-from-top">
  Slides in from top
</div>

<!-- Slide in from bottom with distance -->
<div class="animate-in slide-in-from-bottom-4">
  Slides in from bottom (1rem)
</div>

<!-- Slide in from left -->
<div class="animate-in slide-in-from-left-10">
  Slides in from left (2.5rem)
</div>

<!-- Slide in from right -->
<div class="animate-in slide-in-from-right-full">
  Slides in from right (100%)
</div>
```

### Zoom In

```html
<div class="animate-in zoom-in">
  Zooms in from 0% scale
</div>

<div class="animate-in zoom-in-50">
  Zooms in from 50% scale
</div>

<div class="animate-in zoom-in-95">
  Zooms in from 95% scale (subtle)
</div>
```

### Spin In

```html
<div class="animate-in spin-in">
  Spins in from 0deg
</div>

<div class="animate-in spin-in-90">
  Spins in from 90deg
</div>
```

### Composing Entrance Animations

```html
<!-- Fade + Slide -->
<div class="animate-in fade-in slide-in-from-bottom-4">
  Fades in while sliding up
</div>

<!-- Fade + Zoom -->
<div class="animate-in fade-in-0 zoom-in-95">
  Fades and zooms in (dialog-style)
</div>

<!-- Fade + Slide + Zoom -->
<div class="animate-in fade-in slide-in-from-left-4 zoom-in-95">
  Fades, slides, and zooms in
</div>
```

## Exit Animations

### Basic Fade Out

```html
<div class="animate-out fade-out">
  Fades out to 0% opacity
</div>
```

### Slide Out to Direction

```html
<!-- Slide out to top -->
<div class="animate-out slide-out-to-top">
  Slides out to top
</div>

<!-- Slide out to bottom -->
<div class="animate-out slide-out-to-bottom-4">
  Slides out to bottom
</div>

<!-- Slide out to left -->
<div class="animate-out slide-out-to-left-10">
  Slides out to left
</div>
```

### Zoom Out

```html
<div class="animate-out zoom-out">
  Zooms out to 0% scale
</div>

<div class="animate-out zoom-out-95">
  Zooms out to 95% scale (subtle)
</div>
```

### Composing Exit Animations

```html
<!-- Fade + Slide out -->
<div class="animate-out fade-out slide-out-to-top-4">
  Fades out while sliding up
</div>

<!-- Fade + Zoom out -->
<div class="animate-out fade-out-0 zoom-out-95">
  Fades and zooms out (dialog-style)
</div>
```

## Animation Properties

### Duration

```html
<div class="animate-in fade-in duration-150">150ms</div>
<div class="animate-in fade-in duration-200">200ms</div>
<div class="animate-in fade-in duration-300">300ms (default)</div>
<div class="animate-in fade-in duration-500">500ms</div>
<div class="animate-in fade-in duration-700">700ms</div>
<div class="animate-in fade-in duration-1000">1000ms</div>
```

### Delay

```html
<div class="animate-in fade-in delay-75">75ms delay</div>
<div class="animate-in fade-in delay-100">100ms delay</div>
<div class="animate-in fade-in delay-150">150ms delay</div>
<div class="animate-in fade-in delay-200">200ms delay</div>
<div class="animate-in fade-in delay-300">300ms delay</div>
<div class="animate-in fade-in delay-500">500ms delay</div>
```

### Direction

```html
<div class="animate-in fade-in direction-normal">Normal</div>
<div class="animate-in fade-in direction-reverse">Reverse</div>
<div class="animate-in fade-in direction-alternate">Alternate</div>
<div class="animate-in fade-in direction-alternate-reverse">Alternate Reverse</div>
```

### Fill Mode

```html
<div class="animate-in fade-in fill-mode-none">None</div>
<div class="animate-in fade-in fill-mode-forwards">Forwards</div>
<div class="animate-in fade-in fill-mode-backwards">Backwards</div>
<div class="animate-in fade-in fill-mode-both">Both</div>
```

### Iteration Count

```html
<div class="animate-in fade-in repeat-0">0 times</div>
<div class="animate-in fade-in repeat-1">1 time (default)</div>
<div class="animate-in fade-in repeat-infinite">Infinite</div>
```

### Play State

```html
<div class="animate-in fade-in running">Running</div>
<div class="animate-in fade-in paused">Paused</div>
```

### Timing Function

```html
<div class="animate-in fade-in ease-linear">Linear</div>
<div class="animate-in fade-in ease-in">Ease In</div>
<div class="animate-in fade-in ease-out">Ease Out</div>
<div class="animate-in fade-in ease-in-out">Ease In Out</div>
```

## Common UI Patterns

### Dialog/Modal Animation

```html
<!-- Overlay -->
<div class="animate-in fade-in duration-200">
  <!-- Dialog content -->
  <div class="animate-in fade-in-0 zoom-in-95 slide-in-from-bottom-2 duration-300">
    <h2>Dialog Title</h2>
    <p>Dialog content here</p>
  </div>
</div>
```

### Dropdown Menu

```html
<div class="animate-in fade-in-0 zoom-in-95 slide-in-from-top-2 duration-200">
  <ul>
    <li>Menu Item 1</li>
    <li>Menu Item 2</li>
    <li>Menu Item 3</li>
  </ul>
</div>
```

### Toast Notification

```html
<!-- Slide in from right -->
<div class="animate-in slide-in-from-right-full fade-in duration-300">
  <p>Success! Your changes have been saved.</p>
</div>

<!-- Exit: slide out to right -->
<div class="animate-out slide-out-to-right-full fade-out duration-200">
  <p>Success! Your changes have been saved.</p>
</div>
```

### Staggered List Items

```html
<ul>
  <li class="animate-in fade-in slide-in-from-left-4 duration-300 delay-0">Item 1</li>
  <li class="animate-in fade-in slide-in-from-left-4 duration-300 delay-75">Item 2</li>
  <li class="animate-in fade-in slide-in-from-left-4 duration-300 delay-150">Item 3</li>
  <li class="animate-in fade-in slide-in-from-left-4 duration-300 delay-200">Item 4</li>
</ul>
```

### Page Transition

```html
<!-- Enter -->
<div class="animate-in fade-in slide-in-from-bottom-4 duration-500">
  Page content
</div>

<!-- Exit -->
<div class="animate-out fade-out slide-out-to-top-4 duration-300">
  Page content
</div>
```

### Tooltip

```html
<div class="animate-in fade-in-0 zoom-in-95 duration-150">
  Tooltip text
</div>
```

## Responsive Animations

```html
<!-- Different animations at different breakpoints -->
<div class="animate-in fade-in md:slide-in-from-left-4 lg:zoom-in-95">
  Responsive animation
</div>

<!-- Duration varies by breakpoint -->
<div class="animate-in fade-in duration-200 md:duration-300 lg:duration-500">
  Responsive duration
</div>
```

## Dark Mode Animations

```html
<!-- Tailwind CSS v3+ dark mode support -->
<div class="animate-in fade-in dark:slide-in-from-bottom-4">
  Dark mode aware animation
</div>
```

## Quick Reference

| Utility | Property |
|---------|----------|
| `animate-in` | Base for entrance animations |
| `animate-out` | Base for exit animations |
| `fade-in` / `fade-out` | Opacity animation |
| `slide-in-from-*` / `slide-out-to-*` | Translate animation |
| `zoom-in` / `zoom-out` | Scale animation |
| `spin-in` / `spin-out` | Rotate animation |
| `duration-*` | Animation duration |
| `delay-*` | Animation delay |
| `direction-*` | Animation direction |
| `fill-mode-*` | Animation fill mode |
| `repeat-*` | Animation iteration count |
| `running` / `paused` | Animation play state |
| `ease-*` | Animation timing function |
