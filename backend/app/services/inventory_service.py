from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

class InventoryService:
    def __init__(self):
        pass

    def deduct_for_order(self, order: dict) -> list[dict]:
        stock_entries: list[dict] = []
        for item in order.get("items", []):
            quantity = Decimal(str(item["quantity"]))
            unit_cost = Decimal("3.25")
            stock_entries.append(
                {
                    "id": str(uuid4()),
                    "inventory_item_id": item["menu_item_id"],
                    "movement_type": "sale",
                    "quantity": float(-quantity),
                    "unit_cost": float(unit_cost),
                    "notes": f"Order {order['id']} item deduction",
                }
            )
        return stock_entries
