from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import uuid4


class InventoryService:
    def __init__(self):
        pass

    def deduct_for_order(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        stock_entries: list[dict[str, Any]] = []
        for item in order.get("items", []):
            quantity = Decimal(str(item["quantity"]))
            stock_entries.append(
                {
                    "id": str(uuid4()),
                    "inventory_item_id": item["menu_item_id"],
                    "movement_type": "sale",
                    "quantity": float(-quantity),
                    "unit_cost": float(Decimal("3.25")),
                    "notes": f"Order {order['id']} item deduction",
                }
            )
        return stock_entries
