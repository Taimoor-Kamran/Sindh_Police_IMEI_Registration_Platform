#!/usr/bin/env python3
"""Scaffold a Next.js 15 App Router project with best practices."""

import argparse
import json
from pathlib import Path

PACKAGE_JSON = '''{{
  "name": "{name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit"
  }},
  "dependencies": {{
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  }},
  "devDependencies": {{
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.7.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^15.0.0",
    "prettier": "^3.4.0",
    "@tailwindcss/postcss": "^4.0.0",
    "tailwindcss": "^4.0.0"
  }}
}}
'''

TSCONFIG = '''{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''

NEXT_CONFIG = '''import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Image optimization settings
  images: {
    remotePatterns: [
      // Add allowed image domains here
      // { protocol: "https", hostname: "example.com" },
    ],
  },

  // Experimental features
  experimental: {
    // Enable typed routes
    typedRoutes: true,
  },
};

export default nextConfig;
'''

TAILWIND_CONFIG = '''import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
} satisfies Config;
'''

POSTCSS_CONFIG = '''export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
'''

ESLINT_CONFIG = '''import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

export default eslintConfig;
'''

PRETTIER_CONFIG = '''{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5",
  "plugins": ["prettier-plugin-tailwindcss"]
}
'''

GITIGNORE = '''# Dependencies
node_modules/
.pnp/
.pnp.js

# Next.js
.next/
out/

# Production
build/

# Testing
coverage/

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts
'''

ENV_EXAMPLE = '''# App
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Database (if using)
# DATABASE_URL=postgresql://user:password@localhost:5432/db

# Auth (if using)
# NEXTAUTH_SECRET=your-secret-here
# NEXTAUTH_URL=http://localhost:3000
'''

ROOT_LAYOUT = '''import type {{ Metadata }} from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {{
  title: "{title}",
  description: "{description}",
}};

export default function RootLayout({{
  children,
}}: Readonly<{{
  children: React.ReactNode;
}}>)  {{
  return (
    <html lang="en">
      <body className="bg-background text-foreground antialiased">
        {{children}}
      </body>
    </html>
  );
}}
'''

HOME_PAGE = '''export default function Home() {{
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-4">{title}</h1>
      <p className="text-lg text-gray-600">
        Get started by editing{{" "}}
        <code className="bg-gray-100 px-2 py-1 rounded">src/app/page.tsx</code>
      </p>
    </main>
  );
}}
'''

LOADING = '''export default function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
    </div>
  );
}
'''

ERROR_PAGE = '''"use client";

import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <button
        onClick={() => reset()}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  );
}
'''

NOT_FOUND = '''import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h2 className="text-2xl font-bold mb-4">Page Not Found</h2>
      <p className="text-gray-600 mb-4">Could not find the requested page.</p>
      <Link
        href="/"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Return Home
      </Link>
    </div>
  );
}
'''

GLOBALS_CSS = '''@import "tailwindcss";

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  font-family: Arial, Helvetica, sans-serif;
}
'''

BUTTON_COMPONENT = '''import { ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline";
  size?: "sm" | "md" | "lg";
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = "", variant = "primary", size = "md", ...props }, ref) => {
    const baseStyles = "font-medium rounded-lg transition-colors";

    const variants = {
      primary: "bg-blue-600 text-white hover:bg-blue-700",
      secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
      outline: "border border-gray-300 hover:bg-gray-50",
    };

    const sizes = {
      sm: "px-3 py-1.5 text-sm",
      md: "px-4 py-2 text-base",
      lg: "px-6 py-3 text-lg",
    };

    return (
      <button
        ref={ref}
        className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button };
'''

CN_UTIL = '''import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
'''

API_ROUTE = '''import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Hello from API!" });
}

export async function POST(request: Request) {
  const body = await request.json();
  return NextResponse.json({ received: body });
}
'''


def create_project(name: str, path: Path, description: str = ""):
    """Create Next.js 15 App Router project with best practices."""
    project_path = path / name
    title = name.replace("-", " ").title()
    desc = description or f"A Next.js application: {name}"

    # Create directory structure
    dirs = [
        project_path / "src" / "app" / "api" / "hello",
        project_path / "src" / "components" / "ui",
        project_path / "src" / "components" / "layout",
        project_path / "src" / "lib",
        project_path / "src" / "hooks",
        project_path / "src" / "types",
        project_path / "src" / "styles",
        project_path / "public",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Root config files
    (project_path / "package.json").write_text(
        PACKAGE_JSON.format(name=name)
    )
    (project_path / "tsconfig.json").write_text(TSCONFIG)
    (project_path / "next.config.ts").write_text(NEXT_CONFIG)
    (project_path / "tailwind.config.ts").write_text(TAILWIND_CONFIG)
    (project_path / "postcss.config.mjs").write_text(POSTCSS_CONFIG)
    (project_path / "eslint.config.mjs").write_text(ESLINT_CONFIG)
    (project_path / ".prettierrc").write_text(PRETTIER_CONFIG)
    (project_path / ".gitignore").write_text(GITIGNORE)
    (project_path / ".env.example").write_text(ENV_EXAMPLE)

    # App directory files
    (project_path / "src" / "app" / "layout.tsx").write_text(
        ROOT_LAYOUT.format(title=title, description=desc)
    )
    (project_path / "src" / "app" / "page.tsx").write_text(
        HOME_PAGE.format(title=title)
    )
    (project_path / "src" / "app" / "loading.tsx").write_text(LOADING)
    (project_path / "src" / "app" / "error.tsx").write_text(ERROR_PAGE)
    (project_path / "src" / "app" / "not-found.tsx").write_text(NOT_FOUND)

    # API route
    (project_path / "src" / "app" / "api" / "hello" / "route.ts").write_text(API_ROUTE)

    # Styles
    (project_path / "src" / "styles" / "globals.css").write_text(GLOBALS_CSS)

    # Components
    (project_path / "src" / "components" / "ui" / "button.tsx").write_text(BUTTON_COMPONENT)

    # Lib utilities
    (project_path / "src" / "lib" / "utils.ts").write_text(CN_UTIL)

    # Type definitions
    (project_path / "src" / "types" / "index.ts").write_text(
        '// Add shared TypeScript types here\nexport {};\n'
    )

    # Hooks
    (project_path / "src" / "hooks" / "index.ts").write_text(
        '// Add custom hooks here\nexport {};\n'
    )

    print(f"Created Next.js 15 project: {project_path}")
    print(f"\nStructure:")
    print(f"  {name}/")
    print(f"  ├── src/")
    print(f"  │   ├── app/")
    print(f"  │   │   ├── api/hello/route.ts")
    print(f"  │   │   ├── layout.tsx")
    print(f"  │   │   ├── page.tsx")
    print(f"  │   │   ├── loading.tsx")
    print(f"  │   │   ├── error.tsx")
    print(f"  │   │   └── not-found.tsx")
    print(f"  │   ├── components/")
    print(f"  │   │   ├── ui/")
    print(f"  │   │   └── layout/")
    print(f"  │   ├── lib/")
    print(f"  │   ├── hooks/")
    print(f"  │   ├── types/")
    print(f"  │   └── styles/")
    print(f"  ├── public/")
    print(f"  ├── package.json")
    print(f"  ├── next.config.ts")
    print(f"  └── tailwind.config.ts")
    print(f"\nNext steps:")
    print(f"  cd {name}")
    print(f"  npm install          # or: pnpm install / bun install")
    print(f"  npm run dev          # Start development server")


def main():
    parser = argparse.ArgumentParser(description="Scaffold Next.js 15 App Router project")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    parser.add_argument("--description", default="", help="Project description")

    args = parser.parse_args()
    create_project(args.name, args.path, args.description)


if __name__ == "__main__":
    main()
