---
name: nextjs
description: Scaffold and develop Next.js 15 App Router projects with TypeScript and Tailwind CSS. Use when users want to create new Next.js applications, add pages/routes, implement layouts, create API routes, or follow Next.js best practices. Triggers on requests like "create a Next.js app", "add a page", "create API route", or any Next.js development task.
---

# Next.js 15 App Router

Scaffold and develop Next.js 15 applications with App Router, TypeScript, and Tailwind CSS.

## Quick Start: New Project

```bash
python scripts/scaffold.py my-app --path /target/directory
```

Creates:
```
my-app/
├── src/
│   ├── app/
│   │   ├── api/hello/route.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │   └── not-found.tsx
│   ├── components/
│   │   ├── ui/
│   │   └── layout/
│   ├── lib/
│   ├── hooks/
│   └── styles/
├── package.json
├── next.config.ts
└── tailwind.config.ts
```

## File Conventions

| File | Purpose |
|------|---------|
| `layout.tsx` | Shared UI wrapper |
| `page.tsx` | Route page |
| `loading.tsx` | Loading skeleton |
| `error.tsx` | Error boundary |
| `route.ts` | API endpoint |

## Core Patterns

### Server Component (Default)
```tsx
async function Page() {
  const data = await fetch("https://api.example.com/data");
  return <div>{/* render */}</div>;
}
```

### Client Component
```tsx
"use client";
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### API Route
```tsx
// src/app/api/users/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Hello!" });
}
```

### Dynamic Route
```tsx
// src/app/blog/[slug]/page.tsx
export default function Post({ params }: { params: { slug: string } }) {
  return <h1>Post: {params.slug}</h1>;
}
```

## Commands

| Task | Command |
|------|---------|
| Install deps | `npm install` |
| Dev server | `npm run dev` |
| Build | `npm run build` |
| Lint | `npm run lint` |
| Type check | `npm run typecheck` |

## References

- **Patterns**: See [references/patterns.md](references/patterns.md) for layouts, routes, data fetching, server actions
- **Config**: See [references/api_reference.md](references/api_reference.md) for next.config, env vars, deployment
