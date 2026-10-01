from __future__ import annotations

from decimal import Decimal


class FoodCostService:
    def calculate_menu_item_food_cost(self, item_name: str, recipe_items: list[dict], inventory_costs: dict) -> dict:
        food_cost = Decimal("0")
        for ingredient in recipe_items:
            ingredient_cost = Decimal(str(inventory_costs.get(ingredient["inventory_item_id"], 0)))
            food_cost += ingredient_cost * Decimal(str(ingredient["quantity"]))

        return {
            "item_name": item_name,
            "food_cost": str(food_cost),
            "gross_margin": str(Decimal("0.00")),
        }
