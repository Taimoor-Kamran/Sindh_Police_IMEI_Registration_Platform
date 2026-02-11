# Alembic Migrations with SQLModel

## Table of Contents
- [Setup](#setup)
- [Configure env.py](#configure-envpy)
- [Create Migrations](#create-migrations)
- [Run Migrations](#run-migrations)

## Setup

```bash
uv add alembic
alembic init alembic
```

## Configure env.py

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from alembic import context

# Import all models for metadata
from app.models import *  # noqa
from app.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Create Migrations

```bash
# Auto-generate migration
alembic revision --autogenerate -m "Add hero table"

# Create empty migration
alembic revision -m "Custom migration"
```

## Run Migrations

```bash
# Apply all pending
alembic upgrade head

# Apply specific revision
alembic upgrade +1

# Rollback
alembic downgrade -1

# Show current revision
alembic current

# Show history
alembic history
```
