# SQLModel Relationships

## Table of Contents
- [One-to-Many](#one-to-many)
- [Many-to-Many](#many-to-many)
- [Async Relationship Loading](#async-relationship-loading)

## One-to-Many

Team has many Heroes:

```python
from sqlmodel import SQLModel, Field, Relationship

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")

    team: Team | None = Relationship(back_populates="heroes")
```

## Many-to-Many

Heroes and Powers with link table:

```python
class HeroPowerLink(SQLModel, table=True):
    hero_id: int = Field(foreign_key="hero.id", primary_key=True)
    power_id: int = Field(foreign_key="power.id", primary_key=True)

class Power(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    heroes: list["Hero"] = Relationship(
        back_populates="powers",
        link_model=HeroPowerLink
    )

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    powers: list[Power] = Relationship(
        back_populates="heroes",
        link_model=HeroPowerLink
    )
```

## Async Relationship Loading

Use `selectinload` for eager loading in async:

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload

async def get_team_with_heroes(session: AsyncSession, team_id: int):
    statement = (
        select(Team)
        .where(Team.id == team_id)
        .options(selectinload(Team.heroes))
    )
    result = await session.exec(statement)
    return result.first()

# For nested relationships
statement = (
    select(Team)
    .options(
        selectinload(Team.heroes).selectinload(Hero.powers)
    )
)
```

### Response Schemas with Relationships

```python
class HeroPublic(SQLModel):
    id: int
    name: str
    team_id: int | None

class TeamPublicWithHeroes(SQLModel):
    id: int
    name: str
    heroes: list[HeroPublic] = []
```
