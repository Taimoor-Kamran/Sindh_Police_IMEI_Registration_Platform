# Async PostgreSQL Database Setup

## Table of Contents
- [Dependencies](#dependencies)
- [Database Configuration](#database-configuration)
- [Async Engine Setup](#async-engine-setup)
- [Session Dependency](#session-dependency)
- [Create Tables](#create-tables)

## Dependencies

```toml
# pyproject.toml
dependencies = [
    "sqlmodel>=0.0.22",
    "asyncpg>=0.30.0",
    "greenlet>=3.0.0",  # Required for async SQLAlchemy
]
```

## Database Configuration

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dbname"

    model_config = {"env_file": ".env"}

settings = Settings()
```

## Async Engine Setup

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set True for SQL logging
    pool_pre_ping=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

## Session Dependency

```python
# app/core/dependencies.py
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
```

## Create Tables

```python
# app/core/database.py (add to existing)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
```
