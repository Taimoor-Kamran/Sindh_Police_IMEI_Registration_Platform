---
name: tailwindcss
description: Scaffold and develop Tailwind CSS v4 projects with CSS-first configuration. Use when users want to create new Tailwind projects, configure custom themes with @theme directive, add component styles, or follow Tailwind CSS v4 best practices. Triggers on requests like "create a Tailwind project", "add custom colors", "configure theme", or any Tailwind CSS development task.
---

# Tailwind CSS v4

Scaffold and develop Tailwind CSS v4 projects with CSS-first configuration.

## Quick Start: New Project

```bash
# Vite mode (recommended)
python scripts/scaffold.py my-app --path /target/directory

# PostCSS mode
python scripts/scaffold.py my-app --mode postcss
```

Creates:
```
my-app/
├── src/
│   ├── styles/
│   │   └── main.css        # @theme + @layer config
│   └── components/
├── dist/
├── index.html
├── vite.config.js          # or postcss.config.mjs
└── package.json
```

## Key v4 Changes

| v3 | v4 |
|----|-----|
| `tailwind.config.js` | `@theme { }` in CSS |
| JS configuration | CSS-first configuration |
| `@tailwind base` | `@import "tailwindcss"` |

## @theme Directive

```css
@import "tailwindcss";

@theme {
  /* Colors → bg-primary, text-primary */
  --color-primary: oklch(0.7 0.15 250);
  --color-secondary: oklch(0.6 0.12 300);

  /* Fonts → font-sans, font-mono */
  --font-sans: "Inter", system-ui, sans-serif;

  /* Spacing → p-18, m-18, gap-18 */
  --spacing-18: 4.5rem;
}
```

## @layer Directive

```css
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium;
  }

  .card {
    @apply bg-white rounded-xl shadow-md p-6;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

## Commands

| Mode | Dev | Build |
|------|-----|-------|
| Vite | `npm run dev` | `npm run build` |
| PostCSS | `npm run watch:css` | `npm run build:css` |

## Installation (Manual)

```bash
# Vite
npm install tailwindcss @tailwindcss/vite

# PostCSS
npm install tailwindcss @tailwindcss/postcss postcss
```

## References

- **Patterns**: See [references/patterns.md](references/patterns.md) for @theme, @layer, dark mode, animations
- **Config**: See [references/api_reference.md](references/api_reference.md) for installation, directives, plugins
