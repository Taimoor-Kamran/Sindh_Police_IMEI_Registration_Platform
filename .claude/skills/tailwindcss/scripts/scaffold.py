#!/usr/bin/env python3
"""Scaffold a Tailwind CSS v4 project with best practices."""

import argparse
from pathlib import Path

# Package.json for Vite + Tailwind
PACKAGE_JSON_VITE = '''{{
  "name": "{name}",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "devDependencies": {{
    "vite": "^6.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0"
  }}
}}
'''

# Package.json for PostCSS + Tailwind (framework-agnostic)
PACKAGE_JSON_POSTCSS = '''{{
  "name": "{name}",
  "private": true,
  "version": "0.1.0",
  "scripts": {{
    "build:css": "postcss src/styles/input.css -o dist/output.css",
    "watch:css": "postcss src/styles/input.css -o dist/output.css --watch"
  }},
  "devDependencies": {{
    "postcss": "^8.4.0",
    "postcss-cli": "^11.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/postcss": "^4.0.0"
  }}
}}
'''

# Vite config
VITE_CONFIG = '''import {{ defineConfig }} from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({{
  plugins: [tailwindcss()],
}});
'''

# PostCSS config
POSTCSS_CONFIG = '''export default {{
  plugins: {{
    "@tailwindcss/postcss": {{}},
  }},
}};
'''

# Main CSS file with Tailwind v4 setup
MAIN_CSS = '''@import "tailwindcss";

/* Custom theme configuration using @theme directive */
@theme {{
  /* Colors */
  --color-primary: oklch(0.7 0.15 250);
  --color-secondary: oklch(0.6 0.12 300);
  --color-accent: oklch(0.8 0.18 80);

  /* Background & Foreground */
  --color-background: oklch(0.98 0 0);
  --color-foreground: oklch(0.15 0 0);

  /* Semantic colors */
  --color-success: oklch(0.7 0.18 145);
  --color-warning: oklch(0.8 0.15 85);
  --color-error: oklch(0.65 0.2 25);

  /* Font families */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  /* Font sizes */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px oklch(0 0 0 / 0.1);
}}

/* Dark mode theme */
@media (prefers-color-scheme: dark) {{
  @theme {{
    --color-background: oklch(0.15 0 0);
    --color-foreground: oklch(0.95 0 0);
  }}
}}

/* Base layer for element defaults */
@layer base {{
  html {{
    font-family: var(--font-sans);
    background-color: var(--color-background);
    color: var(--color-foreground);
  }}

  h1, h2, h3, h4, h5, h6 {{
    font-weight: 600;
    line-height: 1.25;
  }}

  a {{
    color: var(--color-primary);
    text-decoration: none;
  }}

  a:hover {{
    text-decoration: underline;
  }}
}}

/* Component layer for reusable components */
@layer components {{
  .btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-sm) var(--spacing-md);
    font-weight: 500;
    border-radius: var(--radius-md);
    transition: all 0.2s;
    cursor: pointer;
  }}

  .btn-primary {{
    background-color: var(--color-primary);
    color: white;
  }}

  .btn-primary:hover {{
    opacity: 0.9;
  }}

  .btn-secondary {{
    background-color: var(--color-secondary);
    color: white;
  }}

  .card {{
    background-color: var(--color-background);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    padding: var(--spacing-lg);
  }}

  .input {{
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid oklch(0.8 0 0);
    border-radius: var(--radius-md);
    font-size: var(--text-base);
  }}

  .input:focus {{
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }}
}}

/* Utilities layer for custom utilities */
@layer utilities {{
  .text-balance {{
    text-wrap: balance;
  }}

  .animate-fade-in {{
    animation: fade-in 0.3s ease-out;
  }}

  @keyframes fade-in {{
    from {{ opacity: 0; transform: translateY(-10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
}}
'''

# HTML template
INDEX_HTML = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" href="/src/styles/main.css" />
  </head>
  <body class="min-h-screen bg-background text-foreground">
    <div class="container mx-auto px-4 py-8">
      <header class="mb-8">
        <h1 class="text-4xl font-bold text-primary">{title}</h1>
        <p class="mt-2 text-lg text-foreground/70">
          Built with Tailwind CSS v4
        </p>
      </header>

      <main class="space-y-8">
        <!-- Card Example -->
        <section class="card">
          <h2 class="text-2xl font-semibold mb-4">Card Component</h2>
          <p class="text-foreground/80 mb-4">
            This is a card component using custom theme tokens.
          </p>
          <div class="flex gap-4">
            <button class="btn btn-primary">Primary Button</button>
            <button class="btn btn-secondary">Secondary Button</button>
          </div>
        </section>

        <!-- Form Example -->
        <section class="card">
          <h2 class="text-2xl font-semibold mb-4">Form Elements</h2>
          <form class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-1">Email</label>
              <input type="email" class="input" placeholder="you@example.com" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Message</label>
              <textarea class="input" rows="3" placeholder="Your message..."></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </section>

        <!-- Colors Example -->
        <section class="card">
          <h2 class="text-2xl font-semibold mb-4">Theme Colors</h2>
          <div class="flex flex-wrap gap-4">
            <div class="w-20 h-20 rounded-lg bg-primary flex items-center justify-center text-white text-xs">Primary</div>
            <div class="w-20 h-20 rounded-lg bg-secondary flex items-center justify-center text-white text-xs">Secondary</div>
            <div class="w-20 h-20 rounded-lg bg-accent flex items-center justify-center text-xs">Accent</div>
            <div class="w-20 h-20 rounded-lg bg-success flex items-center justify-center text-white text-xs">Success</div>
            <div class="w-20 h-20 rounded-lg bg-warning flex items-center justify-center text-xs">Warning</div>
            <div class="w-20 h-20 rounded-lg bg-error flex items-center justify-center text-white text-xs">Error</div>
          </div>
        </section>
      </main>

      <footer class="mt-12 pt-8 border-t border-foreground/10 text-center text-foreground/60">
        <p>Built with Tailwind CSS v4</p>
      </footer>
    </div>
  </body>
</html>
'''

GITIGNORE = '''# Dependencies
node_modules/

# Build output
dist/

# Environment
.env
.env.local

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
'''


def create_project(name: str, path: Path, mode: str = "vite"):
    """Create Tailwind CSS v4 project with best practices."""
    project_path = path / name
    title = name.replace("-", " ").title()

    # Create directories
    dirs = [
        project_path / "src" / "styles",
        project_path / "src" / "components",
        project_path / "dist",
        project_path / "public",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create config files based on mode
    if mode == "vite":
        (project_path / "package.json").write_text(
            PACKAGE_JSON_VITE.format(name=name)
        )
        (project_path / "vite.config.js").write_text(VITE_CONFIG)
    else:  # postcss
        (project_path / "package.json").write_text(
            PACKAGE_JSON_POSTCSS.format(name=name)
        )
        (project_path / "postcss.config.mjs").write_text(POSTCSS_CONFIG)

    # Create common files
    (project_path / "src" / "styles" / "main.css").write_text(MAIN_CSS)
    (project_path / "index.html").write_text(INDEX_HTML.format(title=title))
    (project_path / ".gitignore").write_text(GITIGNORE)

    print(f"Created Tailwind CSS v4 project: {project_path}")
    print(f"\nMode: {mode.upper()}")
    print(f"\nStructure:")
    print(f"  {name}/")
    print(f"  ├── src/")
    print(f"  │   ├── styles/")
    print(f"  │   │   └── main.css      # Tailwind + @theme config")
    print(f"  │   └── components/")
    print(f"  ├── dist/")
    print(f"  ├── public/")
    print(f"  ├── index.html")
    if mode == "vite":
        print(f"  ├── vite.config.js")
    else:
        print(f"  ├── postcss.config.mjs")
    print(f"  └── package.json")
    print(f"\nNext steps:")
    print(f"  cd {name}")
    print(f"  npm install")
    if mode == "vite":
        print(f"  npm run dev")
    else:
        print(f"  npm run watch:css")


def main():
    parser = argparse.ArgumentParser(description="Scaffold Tailwind CSS v4 project")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    parser.add_argument(
        "--mode",
        choices=["vite", "postcss"],
        default="vite",
        help="Build mode: vite (default) or postcss"
    )

    args = parser.parse_args()
    create_project(args.name, args.path, args.mode)


if __name__ == "__main__":
    main()
