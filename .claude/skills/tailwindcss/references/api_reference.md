# Tailwind CSS v4 Configuration Reference

## Installation

### Vite (Recommended)
```bash
npm install tailwindcss @tailwindcss/vite
```

```js
// vite.config.js
import tailwindcss from "@tailwindcss/vite";

export default {
  plugins: [tailwindcss()],
};
```

### PostCSS
```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

```js
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

### CLI (Standalone)
```bash
# Download standalone CLI
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss-macos-arm64
mv tailwindcss-macos-arm64 tailwindcss

# Build CSS
./tailwindcss -i input.css -o output.css --watch
```

## CSS Setup

### Minimal Setup
```css
@import "tailwindcss";
```

### With Theme
```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.7 0.15 250);
  --font-sans: "Inter", sans-serif;
}
```

## Directives Reference

| Directive | Purpose |
|-----------|---------|
| `@import "tailwindcss"` | Import Tailwind |
| `@theme { }` | Define design tokens |
| `@layer base { }` | Base/reset styles |
| `@layer components { }` | Component classes |
| `@layer utilities { }` | Custom utilities |
| `@utility name { }` | Single utility with variants |
| `@plugin "name"` | Load legacy JS plugin |
| `@source "path"` | Add content source |
| `@variant name { }` | Custom variant |

## Theme Token Namespaces

| Namespace | Generates |
|-----------|-----------|
| `--color-*` | `bg-*`, `text-*`, `border-*` |
| `--font-*` | `font-*` |
| `--text-*` | `text-*` (sizes) |
| `--spacing-*` | `p-*`, `m-*`, `gap-*`, etc. |
| `--radius-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |
| `--breakpoint-*` | `sm:`, `md:`, etc. |
| `--animate-*` | `animate-*` |
| `--ease-*` | `ease-*` |

## Color Formats

```css
@theme {
  /* OKLCH (recommended for v4) */
  --color-brand: oklch(0.7 0.15 250);

  /* With alpha */
  --color-overlay: oklch(0 0 0 / 0.5);

  /* Hex still works */
  --color-legacy: #3b82f6;

  /* HSL */
  --color-accent: hsl(220 90% 56%);
}
```

## Browser Support

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 111+ |
| Firefox | 128+ |
| Safari | 16.4+ |
| Edge | 111+ |

**Note:** v4 uses `@property` and `color-mix()` which require modern browsers.

## Content Detection

Tailwind v4 auto-detects content. Override with:

```css
@source "../components/**/*.jsx";
@source "../pages/**/*.tsx";
```

## Plugins

### Official Plugins
```css
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
@plugin "@tailwindcss/container-queries";
@plugin "@tailwindcss/aspect-ratio";
```

### Custom Plugin (Legacy)
```js
// plugin.js
export default function({ addUtilities }) {
  addUtilities({
    '.content-auto': {
      'content-visibility': 'auto',
    },
  });
}
```

```css
@plugin "./plugin.js";
```

## Upgrading from v3

```bash
# Run upgrade tool
npx @tailwindcss/upgrade
```

### Key Changes
| v3 | v4 |
|----|-----|
| `tailwind.config.js` | `@theme { }` in CSS |
| `theme.extend.colors` | `--color-*` tokens |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| `darkMode: 'class'` | Use CSS variables |

## Performance

| Metric | v3 | v4 |
|--------|----|----|
| Full build | 1x | 3.5x faster |
| Incremental | 1x | 8x faster |
| No-change rebuild | 1x | 100x faster |

## Commands

| Task | Command |
|------|---------|
| Dev (Vite) | `npm run dev` |
| Build (Vite) | `npm run build` |
| Watch (PostCSS) | `postcss input.css -o output.css --watch` |
| Build (PostCSS) | `postcss input.css -o output.css` |
| Build (CLI) | `tailwindcss -i input.css -o output.css` |

## Framework Integration

### Next.js
```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

### React (Vite)
```bash
npm install tailwindcss @tailwindcss/vite
```

### Vue (Vite)
```bash
npm install tailwindcss @tailwindcss/vite
```

### Svelte
```bash
npm install tailwindcss @tailwindcss/vite
```
