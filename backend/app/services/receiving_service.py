from __future__ import annotations

from datetime import datetime
from decimal import Decimal


class InventoryReceivingService:
    def receive_inventory(self, location_id: str, inventory_item_id: str, quantity: Decimal, unit_cost: Decimal, received_by: str) -> dict:
        return {
            "id": "recv-001",
            "location_id": location_id,
            "inventory_item_id": inventory_item_id,
            "quantity": str(quantity),
            "unit_cost": str(unit_cost),
            "received_by": received_by,
            "received_at": datetime.utcnow().isoformat(),
            "movement_type": "purchase",
        }

    def get_low_stock_alerts(self, stock_items: list[dict]) -> list[dict]:
        alerts = []
        for item in stock_items:
            current = Decimal(str(item.get("current_quantity", 0)))
            reorder = Decimal(str(item.get("reorder_level", 0)))
            if current <= reorder:
                alerts.append({
                    "inventory_item_id": item.get("id"),
                    "name": item.get("name"),
                    "current_quantity": str(current),
                    "reorder_level": str(reorder),
                    "status": "low_stock",
                })
        return alerts

    def calculate_food_cost(self, recipe_items: list[dict], inventory_costs: dict) -> Decimal:
        total_cost = Decimal("0")
        for ingredient in recipe_items:
            ingredient_cost = Decimal(str(inventory_costs.get(ingredient["inventory_item_id"], 0)))
            total_cost += ingredient_cost * Decimal(str(ingredient["quantity"]))
        return total_cost
