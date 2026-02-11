# Next.js 15 Commands & Configuration

## CLI Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (Turbopack) |
| `npm run build` | Production build |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npx next info` | Print system info |

## Create New Project

```bash
# Official create-next-app
npx create-next-app@latest my-app

# With options
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Or use scaffold script
python scripts/scaffold.py my-app
```

## next.config.ts Options

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Strict mode for React
  reactStrictMode: true,

  // Image optimization
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "example.com" },
    ],
  },

  // Redirects
  async redirects() {
    return [
      { source: "/old", destination: "/new", permanent: true },
    ];
  },

  // Rewrites (proxy)
  async rewrites() {
    return [
      { source: "/api/:path*", destination: "https://api.example.com/:path*" },
    ];
  },

  // Headers
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [{ key: "X-Frame-Options", value: "DENY" }],
      },
    ];
  },

  // Environment variables
  env: {
    CUSTOM_VAR: "value",
  },

  // Experimental features
  experimental: {
    typedRoutes: true,
    serverActions: { bodySizeLimit: "2mb" },
  },
};

export default nextConfig;
```

## Environment Variables

| Variable | Access | Description |
|----------|--------|-------------|
| `NEXT_PUBLIC_*` | Client + Server | Exposed to browser |
| `DATABASE_URL` | Server only | Private secrets |
| `NODE_ENV` | Both | development/production |

### .env Files Priority
1. `.env.$(NODE_ENV).local`
2. `.env.local` (not loaded in test)
3. `.env.$(NODE_ENV)`
4. `.env`

## TypeScript Paths

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"]
    }
  }
}
```

## Import Aliases

```tsx
// Instead of relative imports
import { Button } from "../../../components/ui/button";

// Use path aliases
import { Button } from "@/components/ui/button";
```

## Caching Strategies

| Strategy | Usage |
|----------|-------|
| `cache: "force-cache"` | Default, cached indefinitely |
| `cache: "no-store"` | Never cache |
| `next: { revalidate: N }` | Cache for N seconds |
| `next: { tags: ["tag"] }` | Tag-based revalidation |

```tsx
// Revalidate after 60 seconds
fetch(url, { next: { revalidate: 60 } });

// Revalidate by tag
fetch(url, { next: { tags: ["posts"] } });

// In server action
import { revalidateTag } from "next/cache";
revalidateTag("posts");
```

## Static Generation

```tsx
// Generate static params at build time
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({ slug: post.slug }));
}
```

## Package Manager Commands

| npm | pnpm | bun |
|-----|------|-----|
| `npm install` | `pnpm install` | `bun install` |
| `npm run dev` | `pnpm dev` | `bun dev` |
| `npm run build` | `pnpm build` | `bun build` |
| `npx next` | `pnpm dlx next` | `bunx next` |

## Deployment

### Vercel (Recommended)
```bash
npm i -g vercel
vercel
```

### Docker
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
CMD ["node", "server.js"]
```

### Static Export
```typescript
// next.config.ts
const nextConfig = {
  output: "export",
};
```
