# Better Auth Patterns Reference

## Table of Contents
- [Email/Password Authentication](#emailpassword-authentication)
- [Social Providers](#social-providers)
- [Session Management](#session-management)
- [Two-Factor Authentication](#two-factor-authentication)
- [Database Adapters](#database-adapters)
- [Framework Integrations](#framework-integrations)

---

## Email/Password Authentication

### Server Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: /* your database */,
  emailAndPassword: {
    enabled: true,
    // Optional configurations
    minPasswordLength: 8,        // Default: 8
    maxPasswordLength: 128,      // Default: 128
    requireEmailVerification: true,
  },
})
```

### Client Sign Up

```typescript
import { authClient } from "@/lib/auth-client"

const { data, error } = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe",              // optional
  callbackURL: "/dashboard",     // redirect after signup
})
```

### Client Sign In

```typescript
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
  callbackURL: "/dashboard",
  rememberMe: true,              // optional: extend session
})
```

### Password Reset Flow

```typescript
// Server: Configure password reset
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    sendResetPassword: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        body: `Click here to reset: ${url}`,
      })
    },
  },
})

// Client: Request reset
await authClient.forgetPassword({ email: "user@example.com" })

// Client: Complete reset (after clicking email link)
await authClient.resetPassword({
  newPassword: "newSecurePassword",
  token: tokenFromUrl,
})
```

### Email Verification

```typescript
// Server: Configure email verification
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        body: `Click to verify: ${url}`,
      })
    },
  },
})

// Client: Resend verification
await authClient.sendVerificationEmail({ email: "user@example.com" })
```

---

## Social Providers

### Configuration

```typescript
// lib/auth.ts
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    apple: {
      clientId: process.env.APPLE_CLIENT_ID!,
      clientSecret: process.env.APPLE_CLIENT_SECRET!,
    },
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    },
  },
})
```

### Client Social Sign In

```typescript
await authClient.signIn.social({
  provider: "github",            // "google", "apple", "discord", etc.
  callbackURL: "/dashboard",
  errorCallbackURL: "/login?error=true",
  newUserCallbackURL: "/welcome", // optional: redirect for new users
})
```

### Link Social Account

```typescript
// Link additional social account to existing user
await authClient.linkSocial({ provider: "google" })
```

---

## Session Management

### Get Session (Client)

```typescript
// React hook
const { data: session, isPending } = authClient.useSession()

// One-time fetch
const { data: session } = await authClient.getSession()
```

### Get Session (Server)

```typescript
// Next.js API Route / Server Component
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

const session = await auth.api.getSession({
  headers: await headers(),
})
```

### Session Configuration

```typescript
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7,   // 7 days (default)
    updateAge: 60 * 60 * 24,       // Update every 24 hours
    freshAge: 60 * 60 * 24,        // Fresh for 24 hours

    // Cookie caching (reduces DB queries)
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60,              // 5 minutes
    },
  },
})
```

### Sign Out

```typescript
// Client-side
await authClient.signOut()

// Revoke all sessions
await authClient.revokeOtherSessions()
```

### List Active Sessions

```typescript
const { data: sessions } = await authClient.listSessions()

// Revoke specific session
await authClient.revokeSession({ sessionId: "session-id" })
```

---

## Two-Factor Authentication

### Server Setup

```typescript
import { betterAuth } from "better-auth"
import { twoFactor } from "better-auth/plugins"

export const auth = betterAuth({
  plugins: [
    twoFactor({
      issuer: "MyApp",           // Shows in authenticator app
      otpOptions: {
        sendOTP: async ({ user, otp }) => {
          await sendSMS(user.phone, `Your code: ${otp}`)
        },
      },
    }),
  ],
})
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react"
import { twoFactorClient } from "better-auth/client/plugins"

export const authClient = createAuthClient({
  plugins: [twoFactorClient()],
})
```

### Enable TOTP

```typescript
// Get TOTP URI for QR code
const { data } = await authClient.twoFactor.getTotpUri()
// Display QR code with data.totpURI

// Verify and enable
await authClient.twoFactor.enable({
  password: "currentPassword",
})
```

### Verify TOTP on Sign In

```typescript
const { data, error } = await authClient.twoFactor.verifyTotp({
  code: "123456",
  trustDevice: true,             // Skip 2FA for 30 days on this device
})
```

### Backup Codes

```typescript
// Generate backup codes
const { data } = await authClient.twoFactor.generateBackupCodes()
// Store: data.backupCodes

// Use backup code
await authClient.twoFactor.verifyBackupCode({ code: "backup-code" })
```

---

## Database Adapters

### PostgreSQL

```typescript
import { Pool } from "pg"

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
})
```

### SQLite

```typescript
import Database from "better-sqlite3"

export const auth = betterAuth({
  database: new Database("./sqlite.db"),
})
```

### MySQL

```typescript
import mysql from "mysql2/promise"

export const auth = betterAuth({
  database: await mysql.createConnection({
    uri: process.env.DATABASE_URL,
  }),
})
```

### Drizzle ORM

```typescript
import { drizzleAdapter } from "better-auth/adapters/drizzle"
import { db } from "@/db"

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",              // "mysql", "sqlite"
  }),
})
```

### Prisma

```typescript
import { prismaAdapter } from "better-auth/adapters/prisma"
import { prisma } from "@/db"

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
})
```

---

## Framework Integrations

### Next.js (App Router)

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth.handler)
```

### Next.js Middleware

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

### Express

```typescript
import express from "express"
import { toNodeHandler } from "better-auth/node"
import { auth } from "./auth"

const app = express()
app.all("/api/auth/*", toNodeHandler(auth))
```

### Hono

```typescript
import { Hono } from "hono"
import { auth } from "./auth"

const app = new Hono()
app.on(["GET", "POST"], "/api/auth/*", (c) => auth.handler(c.req.raw))
```

---

## CLI Commands

```bash
# Generate database schema/migrations
npx @better-auth/cli generate

# Apply migrations directly
npx @better-auth/cli migrate

# Set up MCP for Claude Code
npx @better-auth/cli mcp --claude-code
```
