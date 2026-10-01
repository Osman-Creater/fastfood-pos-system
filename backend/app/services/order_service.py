from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import uuid4

from app.seed_data import get_inventory_item_by_id


class InventoryService:
    def __init__(self):
        pass

    def deduct_for_order(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        stock_entries: list[dict[str, Any]] = []
        location_id = order.get("location_id")

        for item in order.get("items", []):
            quantity = Decimal(str(item.get("quantity", 0)))
            if quantity <= 0:
                continue

            inventory_item = get_inventory_item_by_id("inv-001", location_id)
            if inventory_item is None:
                inventory_item = {"id": "inv-001", "name": "Default Inventory", "unit_cost": 3.25, "location_id": location_id}

            stock_entries.append(
                {
                    "id": str(uuid4()),
                    "inventory_item_id": inventory_item["id"],
                    "movement_type": "sale",
                    "quantity": float(-quantity),
                    "unit_cost": float(Decimal(str(inventory_item.get("unit_cost", 3.25))),
                    "notes": f"Order {order['id']} item deduction",
                }
            )
        return stock_entries
