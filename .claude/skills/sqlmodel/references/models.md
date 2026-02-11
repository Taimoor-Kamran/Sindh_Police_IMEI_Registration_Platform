# SQLModel Model Patterns

## Table of Contents
- [Base Model Pattern](#base-model-pattern)
- [Table Model](#table-model)
- [API Schemas](#api-schemas)
- [Field Configuration](#field-configuration)
- [Timestamps Pattern](#timestamps-pattern)

## Base Model Pattern

Shared fields between database and API schemas:

```python
from sqlmodel import SQLModel, Field

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
```

## Table Model

Database table with `table=True`:

```python
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

## API Schemas

Create/Update/Read schemas inherit from base:

```python
# For creating (no id)
class HeroCreate(HeroBase):
    pass

# For updating (all optional)
class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

# For reading (includes id and computed fields)
class HeroPublic(HeroBase):
    id: int
```

## Field Configuration

Common field options:

```python
from sqlmodel import Field

# Primary key
id: int | None = Field(default=None, primary_key=True)

# Indexed field
email: str = Field(index=True, unique=True)

# String constraints
name: str = Field(min_length=1, max_length=255)

# Nullable with default
description: str | None = Field(default=None)

# Foreign key
team_id: int | None = Field(default=None, foreign_key="team.id")

# JSON column
metadata: dict = Field(default_factory=dict, sa_type=JSON)

# Enum field
status: Status = Field(default=Status.PENDING)
```

## Timestamps Pattern

Auto-managed timestamps:

```python
from datetime import datetime
from sqlmodel import SQLModel, Field

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

class Todo(TodoBase, TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
```
