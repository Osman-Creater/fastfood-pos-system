from __future__ import annotations

from fastapi import APIRouter, Query
from datetime import datetime

from app.services.receiving_service import InventoryReceivingService

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


@router.post("/receive")
async def receive_inventory(location_id: str, inventory_item_id: str, quantity: float, unit_cost: float, received_by: str):
    service = InventoryReceivingService()
    return {"success": True, "data": service.receive_inventory(location_id, inventory_item_id, quantity, unit_cost, received_by)}


@router.get("/low-stock")
async def low_stock():
    stock_items = [
        {"id": "inv-1", "name": "Chicken", "current_quantity": 15, "reorder_level": 20},
        {"id": "inv-2", "name": "Bun", "current_quantity": 40, "reorder_level": 25},
        {"id": "inv-3", "name": "Lettuce", "current_quantity": 60, "reorder_level": 10},
    ]
    service = InventoryReceivingService()
    return {"success": True, "data": service.get_low_stock_alerts(stock_items)}
