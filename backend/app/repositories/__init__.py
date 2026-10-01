from __future__ import annotations

from sqlalchemy import select

from app.models import InventoryItem, Order, Payment, Shift
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    async def get_all_for_location(self, location_id: str) -> list[Order]:
        stmt = select(Order).where(Order.location_id == location_id).order_by(Order.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_status(self, location_id: str, status: str) -> list[Order]:
        stmt = select(Order).where(Order.location_id == location_id, Order.status == status)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class InventoryRepository(BaseRepository[InventoryItem]):
    async def get_low_stock(self, location_id: str) -> list[InventoryItem]:
        stmt = select(InventoryItem).where(
            InventoryItem.location_id == location_id,
            InventoryItem.is_active.is_(True),
            InventoryItem.current_quantity <= InventoryItem.reorder_level,
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class PaymentRepository(BaseRepository[Payment]):
    async def get_by_order(self, order_id: str) -> list[Payment]:
        stmt = select(Payment).where(Payment.order_id == order_id).order_by(Payment.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ShiftRepository(BaseRepository[Shift]):
    async def get_open_shift_for_user(self, user_id: str) -> Shift | None:
        stmt = select(Shift).where(Shift.cashier_user_id == user_id, Shift.status == "open")
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_open_shift_for_location(self, location_id: str) -> list[Shift]:
        stmt = select(Shift).where(Shift.location_id == location_id, Shift.status == "open")
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


__all__ = [
    "BaseRepository",
    "OrderRepository",
    "InventoryRepository",
    "PaymentRepository",
    "ShiftRepository",
]
