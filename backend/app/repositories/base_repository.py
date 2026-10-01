from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get_by_id(self, model: type[T], entity_id: str) -> T | None:
        return await self.session.get(model, entity_id)

    async def list(self, model: type[T], **filters: Any) -> list[T]:
        stmt = select(model)
        for key, value in filters.items():
            if value is None:
                continue
            stmt = stmt.where(getattr(model, key) == value)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, entity: T) -> T:
        await self.session.flush()
        return entity

    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.flush()


__all__ = ["BaseRepository"]
