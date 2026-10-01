from __future__ import annotations

from typing import Any

from backend.app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Any]):
    async def get_all_for_location(self, location_id: str) -> list[Any]:
        return []


class InventoryRepository(BaseRepository[Any]):
    async def get_low_stock(self, location_id: str) -> list[Any]:
        return []


class PaymentRepository(BaseRepository[Any]):
    async def get_by_order(self, order_id: str) -> list[Any]:
        return []


class ShiftRepository(BaseRepository[Any]):
    async def get_open_shift_for_user(self, user_id: str) -> Any | None:
        return None
