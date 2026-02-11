---
name: better-auth
description: Scaffold and develop authentication with Better Auth, a framework-agnostic TypeScript auth library. Use when users want to add authentication to Next.js/React apps, set up email/password login, configure social providers (GitHub, Google), implement two-factor authentication, or follow Better Auth best practices. Triggers on requests like "add authentication", "set up login", "implement 2FA", "add GitHub login", or any Better Auth development task.
---

# Better Auth Development

Scaffold and build authentication systems using Better Auth, a comprehensive TypeScript authentication library.

## Quick Start: New Project

Run the scaffold script to create a new Next.js project with Better Auth:

```bash
python scripts/scaffold.py <project-name> [options]
```

**Options:**
- `--db postgres|sqlite|mysql` - Database type (default: sqlite)
- `--social` - Include GitHub/Google social providers
- `--2fa` - Include two-factor authentication

**Examples:**
```bash
# Basic auth with SQLite
python scripts/scaffold.py myapp

# Full-featured with Postgres, social login, and 2FA
python scripts/scaffold.py myapp --db postgres --social --2fa

# Development setup with SQLite and social
python scripts/scaffold.py myapp --social
```

**After scaffolding:**
```bash
cd myapp

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Generate database schema
npx @better-auth/cli generate

# Start development server
npm run dev
```

## Project Structure

```
project/
├── app/
│   └── api/auth/[...all]/
│       └── route.ts        # API route handler
├── lib/
│   ├── auth.ts             # Server auth config
│   └── auth-client.ts      # Client auth config
├── middleware.ts           # Route protection
└── .env                    # Environment variables
```

## Adding Auth to Existing Project

### 1. Install Dependencies

```bash
npm install better-auth
# Add database driver
npm install better-sqlite3  # or pg, mysql2
```

### 2. Create Server Config

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import Database from "better-sqlite3"

export const auth = betterAuth({
  database: new Database("./sqlite.db"),
  emailAndPassword: {
    enabled: true,
  },
})
```

### 3. Create Client Config

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient()
export const { signIn, signUp, signOut, useSession } = authClient
```

### 4. Add API Route

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth.handler)
```

### 5. Generate Schema

```bash
npx @better-auth/cli generate
```

## Common Tasks

### Add Social Provider

```typescript
// lib/auth.ts
export const auth = betterAuth({
  // ...existing config
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
})
```

Client usage:
```typescript
await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
})
```

### Protect Routes with Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from "next/server"
import { auth } from "@/lib/auth"

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  })

  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*"],
}
```

### Get Session in Components

```typescript
"use client"
import { useSession } from "@/lib/auth-client"

export function UserProfile() {
  const { data: session, isPending } = useSession()

  if (isPending) return <div>Loading...</div>
  if (!session) return <div>Not logged in</div>

  return <div>Welcome, {session.user.name}</div>
}
```

### Get Session in Server Components

```typescript
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export default async function Dashboard() {
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session) redirect("/login")

  return <div>Welcome, {session.user.name}</div>
}
```

## Environment Variables

Required in `.env`:
```bash
BETTER_AUTH_SECRET="<32+ character random string>"
BETTER_AUTH_URL="http://localhost:3000"
DATABASE_URL="<your database connection string>"

# Social providers (if used)
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
```

Generate secret:
```bash
openssl rand -base64 32
```

## CLI Commands

```bash
# Generate schema for your ORM
npx @better-auth/cli generate

# Apply migrations directly
npx @better-auth/cli migrate

# Set up MCP server for Claude Code
npx @better-auth/cli mcp --claude-code
```

## References

- **[references/patterns.md](references/patterns.md)** - Detailed patterns for email/password, social providers, sessions, 2FA, database adapters, and framework integrations
