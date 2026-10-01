from __future__ import annotations

from fastapi import APIRouter

from app.services.food_cost_service import FoodCostService

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/menu-profitability")
async def menu_profitability():
    service = FoodCostService()
    recipe_items = [
        {"inventory_item_id": "inv-1", "quantity": 1},
        {"inventory_item_id": "inv-2", "quantity": 1},
        {"inventory_item_id": "inv-3", "quantity": 0.5},
    ]
    inventory_costs = {
        "inv-1": 4.25,
        "inv-2": 0.85,
        "inv-3": 0.65,
    }
    return {
        "success": True,
        "data": service.calculate_menu_item_food_cost("Classic Burger", recipe_items, inventory_costs),
    }
