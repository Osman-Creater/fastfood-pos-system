from __future__ import annotations

from typing import Any


class ManagerReportService:
    def get_location_summary(self, location_id: str) -> dict[str, Any]:
        return {
            "location_id": location_id,
            "gross_sales": "0.00",
            "net_sales": "0.00",
            "refunds": "0.00",
            "order_count": 0,
            "cash_variance": "0.00",
            "top_item": "Classic Burger",
            "status": "healthy",
        }

    def get_head_office_rollup(self, location_ids: list[str]) -> dict[str, Any]:
        totals = []
        for location_id in location_ids:
            totals.append(self.get_location_summary(location_id))

        return {
            "locations": totals,
            "total_gross_sales": "0.00",
            "total_net_sales": "0.00",
            "total_orders": 0,
        }

    def get_profit_loss_summary(self, location_id: str) -> dict[str, Any]:
        return {
            "location_id": location_id,
            "revenue": {"food_sales": "0.00", "beverage_sales": "0.00"},
            "cogs": {"food_cost": "0.00", "packaging_cost": "0.00"},
            "operating_expenses": {"rent": "0.00", "utilities": "0.00"},
            "net_profit": "0.00",
        }
