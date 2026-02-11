# Next.js 15 App Router Patterns

## File Conventions

| File | Purpose |
|------|---------|
| `layout.tsx` | Shared UI, wraps children |
| `page.tsx` | Unique route UI |
| `loading.tsx` | Loading skeleton |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 page |
| `route.ts` | API endpoint |
| `template.tsx` | Re-renders on navigation |

## Layouts

### Root Layout (Required)
```tsx
// src/app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Nested Layout
```tsx
// src/app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <Sidebar />
      <main>{children}</main>
    </div>
  );
}
```

## Route Groups

### Group without URL segment
```
src/app/
├── (marketing)/
│   ├── about/page.tsx      # /about
│   └── contact/page.tsx    # /contact
├── (dashboard)/
│   ├── settings/page.tsx   # /settings
│   └── profile/page.tsx    # /profile
└── layout.tsx
```

### Multiple Root Layouts
```
src/app/
├── (auth)/
│   ├── layout.tsx          # Auth layout
│   ├── login/page.tsx
│   └── register/page.tsx
└── (main)/
    ├── layout.tsx          # Main layout
    └── dashboard/page.tsx
```

## Dynamic Routes

### Single Parameter
```tsx
// src/app/blog/[slug]/page.tsx
export default function BlogPost({
  params,
}: {
  params: { slug: string };
}) {
  return <h1>Post: {params.slug}</h1>;
}
```

### Catch-all Segments
```tsx
// src/app/docs/[...slug]/page.tsx
// Matches /docs/a, /docs/a/b, /docs/a/b/c
export default function Docs({
  params,
}: {
  params: { slug: string[] };
}) {
  return <p>Path: {params.slug.join("/")}</p>;
}
```

### Optional Catch-all
```tsx
// src/app/shop/[[...categories]]/page.tsx
// Matches /shop, /shop/a, /shop/a/b
```

## Server vs Client Components

### Server Component (Default)
```tsx
// No "use client" directive - runs on server
async function ServerComponent() {
  const data = await fetch("https://api.example.com/data");
  return <div>{/* render data */}</div>;
}
```

### Client Component
```tsx
"use client";

import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Composition Pattern
```tsx
// Server Component wrapping Client Component
import { ClientComponent } from "./client";

export default async function Page() {
  const data = await fetchData();
  return <ClientComponent initialData={data} />;
}
```

## Data Fetching

### Server Component Fetch
```tsx
async function Page() {
  const res = await fetch("https://api.example.com/data", {
    cache: "force-cache",      // Default: cached
    // cache: "no-store",      // No caching
    // next: { revalidate: 60 } // Revalidate every 60s
  });
  const data = await res.json();
  return <div>{data.title}</div>;
}
```

### Parallel Data Fetching
```tsx
async function Page() {
  const [users, posts] = await Promise.all([
    fetch("/api/users").then((r) => r.json()),
    fetch("/api/posts").then((r) => r.json()),
  ]);
  return <div>{/* render */}</div>;
}
```

## API Routes

### Route Handler
```tsx
// src/app/api/users/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  const users = await getUsers();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await createUser(body);
  return NextResponse.json(user, { status: 201 });
}
```

### Dynamic API Route
```tsx
// src/app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await getUser(params.id);
  return NextResponse.json(user);
}
```

## Metadata

### Static Metadata
```tsx
export const metadata = {
  title: "My Page",
  description: "Page description",
};
```

### Dynamic Metadata
```tsx
export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
  };
}
```

## Loading States

### Streaming with Suspense
```tsx
import { Suspense } from "react";

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Loading />}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

## Error Handling

### Error Boundary
```tsx
"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

## Middleware

```tsx
// middleware.ts (root level)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Redirect, rewrite, or modify headers
  if (request.nextUrl.pathname.startsWith("/admin")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};
```

## Server Actions

```tsx
// actions.ts
"use server";

export async function createPost(formData: FormData) {
  const title = formData.get("title");
  await db.post.create({ data: { title } });
  revalidatePath("/posts");
}

// page.tsx
import { createPost } from "./actions";

export default function Page() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  );
}
```
