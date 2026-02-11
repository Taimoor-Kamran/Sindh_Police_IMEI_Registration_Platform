# CRUD Operations with SQLModel

## Table of Contents
- [Create](#create)
- [Read](#read)
- [Update](#update)
- [Delete](#delete)
- [Repository Pattern](#repository-pattern)

## Create

```python
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_hero(session: AsyncSession, hero: HeroCreate) -> Hero:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero
```

## Read

```python
# Get by ID
async def get_hero(session: AsyncSession, hero_id: int) -> Hero | None:
    return await session.get(Hero, hero_id)

# Get all with pagination
async def get_heroes(
    session: AsyncSession,
    offset: int = 0,
    limit: int = 100
) -> list[Hero]:
    statement = select(Hero).offset(offset).limit(limit)
    result = await session.exec(statement)
    return result.all()

# Filter
async def get_heroes_by_team(session: AsyncSession, team_id: int) -> list[Hero]:
    statement = select(Hero).where(Hero.team_id == team_id)
    result = await session.exec(statement)
    return result.all()
```

## Update

```python
async def update_hero(
    session: AsyncSession,
    hero_id: int,
    hero_update: HeroUpdate
) -> Hero | None:
    db_hero = await session.get(Hero, hero_id)
    if not db_hero:
        return None

    hero_data = hero_update.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)

    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero
```

## Delete

```python
async def delete_hero(session: AsyncSession, hero_id: int) -> bool:
    hero = await session.get(Hero, hero_id)
    if not hero:
        return False

    await session.delete(hero)
    await session.commit()
    return True
```

## Repository Pattern

```python
# app/repositories/hero.py
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

class HeroRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, hero: HeroCreate) -> Hero:
        db_hero = Hero.model_validate(hero)
        self.session.add(db_hero)
        await self.session.commit()
        await self.session.refresh(db_hero)
        return db_hero

    async def get(self, hero_id: int) -> Hero | None:
        return await self.session.get(Hero, hero_id)

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Hero]:
        statement = select(Hero).offset(offset).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def update(self, hero_id: int, hero_update: HeroUpdate) -> Hero | None:
        db_hero = await self.get(hero_id)
        if not db_hero:
            return None
        db_hero.sqlmodel_update(hero_update.model_dump(exclude_unset=True))
        self.session.add(db_hero)
        await self.session.commit()
        await self.session.refresh(db_hero)
        return db_hero

    async def delete(self, hero_id: int) -> bool:
        hero = await self.get(hero_id)
        if not hero:
            return False
        await self.session.delete(hero)
        await self.session.commit()
        return True
```
