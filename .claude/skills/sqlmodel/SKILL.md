---
name: sqlmodel
description: SQLModel integration for FastAPI projects with PostgreSQL. Use when building FastAPI applications that need database models, when converting existing SQLAlchemy/Pydantic projects to SQLModel, when creating CRUD endpoints with database operations, or when setting up async PostgreSQL connections. Triggers on requests involving database models, ORM setup, Pydantic schemas that map to database tables, or unified model definitions.
---

# SQLModel for FastAPI + PostgreSQL

SQLModel combines SQLAlchemy and Pydantic into unified models that serve as both database tables and API schemas.

## Quick Start

### Add dependencies

```bash
uv add sqlmodel asyncpg greenlet
```

### Define unified models

```python
from sqlmodel import SQLModel, Field

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255, index=True)
    completed: bool = False

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: str | None = None
    completed: bool | None = None
```

Key: `table=True` makes it a database table. Without it, it's just a Pydantic schema.

## Workflow

### Adding SQLModel to existing FastAPI project

1. Add dependencies: `uv add sqlmodel asyncpg greenlet`
2. Replace SQLAlchemy Base with SQLModel (see [database.md](references/database.md))
3. Convert models to SQLModel pattern (see [models.md](references/models.md))
4. Update imports from `sqlalchemy` to `sqlmodel` where applicable
5. Consolidate duplicate Pydantic schemas into SQLModel inheritance

### Creating new models

1. Define base model with shared fields (no `table=True`)
2. Create table model inheriting base with `table=True` and `id` field
3. Create schemas: `Create` (inherits base), `Update` (all optional), `Public` (with id)

See [models.md](references/models.md) for field configuration and patterns.

### Database operations

Use async session with `session.exec()` for queries:

```python
from sqlmodel import select

async def get_todos(session: AsyncSession) -> list[Todo]:
    result = await session.exec(select(Todo))
    return result.all()
```

See [crud.md](references/crud.md) for full CRUD patterns and repository pattern.

### Relationships

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")
```

See [relationships.md](references/relationships.md) for one-to-many, many-to-many, and async loading.

### Migrations

Use Alembic with async configuration. See [migrations.md](references/migrations.md) for setup.

## References

| File | Use when |
|------|----------|
| [models.md](references/models.md) | Defining models, fields, timestamps, enums |
| [database.md](references/database.md) | Setting up async PostgreSQL connection |
| [crud.md](references/crud.md) | Implementing create/read/update/delete operations |
| [relationships.md](references/relationships.md) | Adding foreign keys and relationships |
| [migrations.md](references/migrations.md) | Setting up Alembic for schema migrations |
