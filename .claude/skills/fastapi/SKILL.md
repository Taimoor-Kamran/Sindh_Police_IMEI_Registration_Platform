---
name: fastapi
description: Scaffold and develop FastAPI projects using uv for package management. Use when users want to create new FastAPI applications, add API endpoints, implement authentication, set up database connections, or follow FastAPI best practices. Triggers on requests like "create a FastAPI project", "add an endpoint", "set up JWT auth", or any FastAPI development task.
---

# FastAPI Development

Scaffold and build FastAPI applications using uv for package management.

## Quick Start: New Project

Run the scaffold script to create a new project:

```bash
python scripts/scaffold.py <project-name> [options]
```

**Options:**
- `--db postgres|sqlite|none` - Database setup (default: none)
- `--auth` - Include JWT authentication
- `--docker` - Include Dockerfile and docker-compose.yml

**Examples:**
```bash
# Basic API
python scripts/scaffold.py myapi

# Full-featured with Postgres, auth, and Docker
python scripts/scaffold.py myapi --db postgres --auth --docker

# SQLite with auth (good for development)
python scripts/scaffold.py myapi --db sqlite --auth
```

**After scaffolding:**
```bash
cd myapi
uv sync                              # Install dependencies
cp .env.example .env                 # Configure environment
uv run uvicorn app.main:app --reload # Start dev server
```

API docs available at: http://localhost:8000/docs

## Project Structure

```
project/
├── app/
│   ├── main.py              # FastAPI app + lifespan
│   ├── api/v1/              # API routes (versioned)
│   ├── core/
│   │   ├── config.py        # Settings (pydantic-settings)
│   │   ├── database.py      # DB engine/session
│   │   ├── dependencies.py  # Shared deps
│   │   └── security.py      # JWT/password utils
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── repositories/        # Data access
├── tests/
└── pyproject.toml
```

## Common Tasks

### Add New Endpoint

1. Create schema in `app/schemas/`:
```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float

class Item(ItemCreate):
    id: int
    model_config = {"from_attributes": True}
```

2. Create router in `app/api/v1/`:
```python
from fastapi import APIRouter, Depends
from app.schemas.item import Item, ItemCreate

router = APIRouter()

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    ...

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    ...
```

3. Register in `app/api/v1/__init__.py`:
```python
router.include_router(items.router, prefix="/items", tags=["items"])
```

### Add Database Model

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
```

### Add Dependency

```python
from typing import Annotated
from fastapi import Depends

# In core/dependencies.py
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    ...

# Usage with Annotated (recommended)
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/me")
async def get_me(user: CurrentUser):
    return user
```

## Common uv Commands

```bash
uv sync                              # Install dependencies
uv add <package>                     # Add dependency
uv add --dev <package>               # Add dev dependency
uv run uvicorn app.main:app --reload # Run dev server
uv run pytest                        # Run tests
uv run ruff check .                  # Lint
uv run ruff format .                 # Format
```

## References

- **[references/patterns.md](references/patterns.md)** - Detailed patterns for dependency injection, database, auth, testing, background tasks
- **[references/uv-commands.md](references/uv-commands.md)** - Complete uv command reference
