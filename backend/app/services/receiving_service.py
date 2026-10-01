from __future__ import annotations

from datetime import datetime


class ReceivingService:
    async def receive_inventory(self, location_id: str, inventory_item_id: str, quantity: float, unit_cost: float, received_by: str):
        return {
            "location_id": location_id,
            "inventory_item_id": inventory_item_id,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "received_by": received_by,
            "receipt_date": datetime.utcnow().isoformat(),
        }
