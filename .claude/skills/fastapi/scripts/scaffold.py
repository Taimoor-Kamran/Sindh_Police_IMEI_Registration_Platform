#!/usr/bin/env python3
"""
FastAPI project scaffolding script using uv for package management.

Usage:
    python scaffold.py <project-name> [--db postgres|sqlite|none] [--auth] [--docker]

Examples:
    python scaffold.py myapi
    python scaffold.py myapi --db postgres --auth --docker
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def create_directory(path: Path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    """Write content to file."""
    path.write_text(content)
    print(f"  Created: {path}")


def scaffold_project(
    project_name: str,
    db: str = "none",
    auth: bool = False,
    docker: bool = False,
):
    """Scaffold a FastAPI project with best practices structure."""

    root = Path(project_name)
    if root.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    print(f"Creating FastAPI project: {project_name}")

    # Create directory structure
    dirs = [
        root / "app",
        root / "app" / "api" / "v1",
        root / "app" / "core",
        root / "app" / "models",
        root / "app" / "schemas",
        root / "app" / "services",
        root / "app" / "repositories",
        root / "tests",
        root / "tests" / "api",
    ]

    for d in dirs:
        create_directory(d)

    # __init__.py files
    init_dirs = [
        root / "app",
        root / "app" / "api",
        root / "app" / "api" / "v1",
        root / "app" / "core",
        root / "app" / "models",
        root / "app" / "schemas",
        root / "app" / "services",
        root / "app" / "repositories",
        root / "tests",
        root / "tests" / "api",
    ]
    for d in init_dirs:
        write_file(d / "__init__.py", "")

    # pyproject.toml
    deps = [
        '"fastapi>=0.115.0"',
        '"uvicorn[standard]>=0.32.0"',
        '"pydantic>=2.0.0"',
        '"pydantic-settings>=2.0.0"',
    ]
    dev_deps = [
        '"pytest>=8.0.0"',
        '"pytest-asyncio>=0.24.0"',
        '"httpx>=0.27.0"',
        '"ruff>=0.8.0"',
    ]

    if db == "postgres":
        deps.extend([
            '"sqlalchemy>=2.0.0"',
            '"asyncpg>=0.30.0"',
            '"alembic>=1.14.0"',
        ])
    elif db == "sqlite":
        deps.extend([
            '"sqlalchemy>=2.0.0"',
            '"aiosqlite>=0.20.0"',
            '"alembic>=1.14.0"',
        ])

    if auth:
        deps.extend([
            '"python-jose[cryptography]>=3.3.0"',
            '"passlib[bcrypt]>=1.7.4"',
            '"python-multipart>=0.0.12"',
        ])

    pyproject = f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "FastAPI application"
requires-python = ">=3.11"
dependencies = [
    {",\n    ".join(deps)}
]

[project.optional-dependencies]
dev = [
    {",\n    ".join(dev_deps)}
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
'''
    write_file(root / "pyproject.toml", pyproject)

    # .python-version
    write_file(root / ".python-version", "3.11\n")

    # app/main.py
    main_py = '''"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import router as api_v1_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
'''
    write_file(root / "app" / "main.py", main_py)

    # app/core/config.py
    config_py = '''"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = False
'''

    if db in ["postgres", "sqlite"]:
        if db == "postgres":
            config_py += '''
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"
'''
        else:
            config_py += '''
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
'''

    if auth:
        config_py += '''
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
'''

    config_py += '''

settings = Settings()
'''
    write_file(root / "app" / "core" / "config.py", config_py)

    # app/core/dependencies.py
    deps_py = '''"""Shared dependencies for dependency injection."""
'''

    if db in ["postgres", "sqlite"]:
        deps_py += '''from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session_maker() as session:
        yield session
'''

    write_file(root / "app" / "core" / "dependencies.py", deps_py)

    # Database setup if needed
    if db in ["postgres", "sqlite"]:
        database_py = '''"""Database configuration."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
'''
        write_file(root / "app" / "core" / "database.py", database_py)

    # Auth setup if needed
    if auth:
        security_py = '''"""Security utilities for authentication."""
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict | None:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
'''
        write_file(root / "app" / "core" / "security.py", security_py)

    # app/api/v1/__init__.py with router
    api_init = '''"""API v1 router."""
from fastapi import APIRouter

from app.api.v1 import items

router = APIRouter()

router.include_router(items.router, prefix="/items", tags=["items"])
'''
    write_file(root / "app" / "api" / "v1" / "__init__.py", api_init)

    # app/api/v1/items.py - Example endpoint
    items_py = '''"""Items API endpoints."""
from fastapi import APIRouter, HTTPException

from app.schemas.item import Item, ItemCreate

router = APIRouter()

# In-memory storage for demo (replace with database in production)
items_db: dict[int, Item] = {}
item_counter = 0


@router.get("/", response_model=list[Item])
async def list_items():
    """List all items."""
    return list(items_db.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    global item_counter
    item_counter += 1
    db_item = Item(id=item_counter, **item.model_dump())
    items_db[item_counter] = db_item
    return db_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
'''
    write_file(root / "app" / "api" / "v1" / "items.py", items_py)

    # app/schemas/item.py
    item_schema = '''"""Item schemas."""
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base item schema."""
    name: str
    description: str | None = None
    price: float


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class Item(ItemBase):
    """Schema for item response."""
    id: int

    model_config = {"from_attributes": True}
'''
    write_file(root / "app" / "schemas" / "item.py", item_schema)
    write_file(root / "app" / "schemas" / "__init__.py", 'from app.schemas.item import Item, ItemCreate\n')

    # tests/conftest.py
    conftest = '''"""Test configuration and fixtures."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    """Create async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
'''
    write_file(root / "tests" / "conftest.py", conftest)

    # tests/api/test_items.py
    test_items = '''"""Tests for items API."""
import pytest


@pytest.mark.asyncio
async def test_create_item(client):
    """Test creating an item."""
    response = await client.post(
        "/api/v1/items/",
        json={"name": "Test Item", "price": 10.99},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.99
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items(client):
    """Test listing items."""
    response = await client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
'''
    write_file(root / "tests" / "api" / "test_items.py", test_items)

    # .env.example
    env_example = '''# Application settings
DEBUG=false
PROJECT_NAME="My FastAPI App"
'''
    if db in ["postgres", "sqlite"]:
        if db == "postgres":
            env_example += 'DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"\n'
        else:
            env_example += 'DATABASE_URL="sqlite+aiosqlite:///./app.db"\n'

    if auth:
        env_example += '''SECRET_KEY="your-super-secret-key-change-this"
ACCESS_TOKEN_EXPIRE_MINUTES=30
'''
    write_file(root / ".env.example", env_example)

    # .gitignore
    gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/

# uv
.uv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution
dist/
build/
*.egg-info/
'''
    write_file(root / ".gitignore", gitignore)

    # Docker files if requested
    if docker:
        dockerfile = '''FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .
COPY .python-version .

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY app/ app/

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        write_file(root / "Dockerfile", dockerfile)

        compose = f'''services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
'''
        if db == "postgres":
            compose += '''    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
'''
        write_file(root / "docker-compose.yml", compose)

    print(f"\n{'='*50}")
    print(f"Project '{project_name}' created successfully!")
    print(f"{'='*50}")
    print("\nNext steps:")
    print(f"  cd {project_name}")
    print("  uv sync                    # Install dependencies")
    print("  cp .env.example .env       # Configure environment")
    print("  uv run uvicorn app.main:app --reload  # Start dev server")
    print("\nUseful commands:")
    print("  uv run pytest              # Run tests")
    print("  uv run ruff check .        # Lint code")
    print("  uv run ruff format .       # Format code")
    if docker:
        print("  docker-compose up          # Start with Docker")
    print(f"\nAPI docs: http://localhost:8000/docs")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a FastAPI project with best practices"
    )
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument(
        "--db",
        choices=["postgres", "sqlite", "none"],
        default="none",
        help="Database to use (default: none)",
    )
    parser.add_argument(
        "--auth",
        action="store_true",
        help="Include JWT authentication setup",
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="Include Dockerfile and docker-compose.yml",
    )

    args = parser.parse_args()
    scaffold_project(
        args.project_name,
        db=args.db,
        auth=args.auth,
        docker=args.docker,
    )


if __name__ == "__main__":
    main()
