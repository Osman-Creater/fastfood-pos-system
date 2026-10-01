from __future__ import annotations

from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository):
    async def get_all_for_location(self, location_id: str):
        return []


class InventoryRepository(BaseRepository):
    async def get_low_stock(self, location_id: str):
        return []


class PaymentRepository(BaseRepository):
    async def get_by_order(self, order_id: str):
        return []


class ShiftRepository(BaseRepository):
    async def get_open_shift_for_user(self, user_id: str):
        return None


__all__ = [
    "BaseRepository",
    "OrderRepository",
    "InventoryRepository",
    "PaymentRepository",
    "ShiftRepository",
]
