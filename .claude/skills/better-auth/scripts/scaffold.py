#!/usr/bin/env python3
"""Scaffold a Better Auth project with Next.js integration."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: str, cwd: Path | None = None) -> bool:
    """Run a shell command and return success status."""
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    return result.returncode == 0


def create_env_file(project_path: Path, db: str) -> None:
    """Create .env.example with required variables."""
    db_urls = {
        "postgres": "postgresql://user:password@localhost:5432/mydb",
        "sqlite": "file:./dev.db",
        "mysql": "mysql://user:password@localhost:3306/mydb",
    }

    content = f"""# Better Auth Configuration
BETTER_AUTH_SECRET="{os.urandom(32).hex()}"
BETTER_AUTH_URL="http://localhost:3000"

# Database
DATABASE_URL="{db_urls.get(db, db_urls['sqlite'])}"

# Social Providers (optional)
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
"""
    (project_path / ".env.example").write_text(content)
    (project_path / ".env").write_text(content)


def create_auth_config(project_path: Path, db: str, social: bool, two_factor: bool) -> None:
    """Create auth.ts configuration file."""
    lib_path = project_path / "lib"
    lib_path.mkdir(parents=True, exist_ok=True)

    imports = ['import { betterAuth } from "better-auth"']
    plugins = []

    if db == "postgres":
        imports.append('import { Pool } from "pg"')
    elif db == "sqlite":
        imports.append('import Database from "better-sqlite3"')
    elif db == "mysql":
        imports.append('import mysql from "mysql2/promise"')

    if two_factor:
        imports.append('import { twoFactor } from "better-auth/plugins"')
        plugins.append("twoFactor()")

    db_configs = {
        "postgres": '''new Pool({
    connectionString: process.env.DATABASE_URL,
  })''',
        "sqlite": 'new Database("./sqlite.db")',
        "mysql": '''await mysql.createConnection({
    uri: process.env.DATABASE_URL,
  })''',
    }

    social_config = ""
    if social:
        social_config = """
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    },
  },"""

    plugins_config = ""
    if plugins:
        plugins_config = f"\n  plugins: [{', '.join(plugins)}],"

    content = f'''{chr(10).join(imports)}

export const auth = betterAuth({{
  database: {db_configs.get(db, db_configs['sqlite'])},
  emailAndPassword: {{
    enabled: true,
  }},{social_config}{plugins_config}
}})
'''
    (lib_path / "auth.ts").write_text(content)


def create_auth_client(project_path: Path, two_factor: bool) -> None:
    """Create auth-client.ts for client-side auth."""
    lib_path = project_path / "lib"
    lib_path.mkdir(parents=True, exist_ok=True)

    imports = ['import { createAuthClient } from "better-auth/react"']
    plugins = []

    if two_factor:
        imports.append('import { twoFactorClient } from "better-auth/client/plugins"')
        plugins.append("twoFactorClient()")

    plugins_config = ""
    if plugins:
        plugins_config = f"\n  plugins: [{', '.join(plugins)}],"

    content = f'''{chr(10).join(imports)}

export const authClient = createAuthClient({{
  baseURL: process.env.BETTER_AUTH_URL,{plugins_config}
}})

export const {{ signIn, signUp, signOut, useSession }} = authClient
'''
    (lib_path / "auth-client.ts").write_text(content)


def create_api_route(project_path: Path) -> None:
    """Create Next.js API route handler."""
    api_path = project_path / "app" / "api" / "auth" / "[...all]"
    api_path.mkdir(parents=True, exist_ok=True)

    content = '''import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth.handler)
'''
    (api_path / "route.ts").write_text(content)


def create_middleware(project_path: Path) -> None:
    """Create Next.js middleware for auth protection."""
    content = '''import { NextRequest, NextResponse } from "next/server"
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
  matcher: ["/dashboard/:path*", "/profile/:path*"],
}
'''
    (project_path / "middleware.ts").write_text(content)


def scaffold_project(
    name: str,
    db: str = "sqlite",
    social: bool = False,
    two_factor: bool = False,
    output_dir: Path | None = None,
) -> None:
    """Scaffold a complete Better Auth + Next.js project."""
    project_path = (output_dir or Path.cwd()) / name

    print(f"🚀 Creating Better Auth project: {name}")

    # Create Next.js project
    if not run_cmd(f"npx create-next-app@latest {name} --typescript --tailwind --eslint --app --src-dir=false --import-alias='@/*' --use-npm", cwd=output_dir or Path.cwd()):
        print("❌ Failed to create Next.js project")
        sys.exit(1)

    # Install dependencies
    deps = ["better-auth"]
    if db == "postgres":
        deps.append("pg")
    elif db == "sqlite":
        deps.append("better-sqlite3")
    elif db == "mysql":
        deps.append("mysql2")

    print(f"📦 Installing dependencies: {', '.join(deps)}")
    if not run_cmd(f"npm install {' '.join(deps)}", cwd=project_path):
        print("❌ Failed to install dependencies")
        sys.exit(1)

    # Create configuration files
    print("📝 Creating auth configuration...")
    create_env_file(project_path, db)
    create_auth_config(project_path, db, social, two_factor)
    create_auth_client(project_path, two_factor)
    create_api_route(project_path)
    create_middleware(project_path)

    print(f"""
✅ Better Auth project created successfully!

Next steps:
  cd {name}

  # Configure environment
  cp .env.example .env
  # Edit .env with your database URL and social provider credentials

  # Generate database schema
  npx @better-auth/cli generate

  # Run migrations (if using Prisma/Drizzle)
  npx @better-auth/cli migrate

  # Start development server
  npm run dev

📚 Documentation: https://better-auth.com/docs
""")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a Better Auth + Next.js project"
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--db",
        choices=["postgres", "sqlite", "mysql"],
        default="sqlite",
        help="Database type (default: sqlite)",
    )
    parser.add_argument(
        "--social",
        action="store_true",
        help="Include social provider configuration (GitHub, Google)",
    )
    parser.add_argument(
        "--2fa",
        dest="two_factor",
        action="store_true",
        help="Include two-factor authentication plugin",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory (default: current directory)",
    )

    args = parser.parse_args()
    scaffold_project(
        name=args.name,
        db=args.db,
        social=args.social,
        two_factor=args.two_factor,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()
