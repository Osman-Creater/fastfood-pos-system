from __future__ import annotations

from typing import Any, TypeVar, Generic

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: Any):
        self.session = session

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get_by_id(self, entity_id: str, model: Any) -> T | None:
        return await self.session.get(model, entity_id)

    async def list(self, model: Any) -> list[T]:
        return list((await self.session.execute(model.__table__.select())).scalars().all())

    async def update(self, entity: T) -> T:
        await self.session.flush()
        return entity

    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.flush()
