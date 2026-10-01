from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class StoreSummary:
    location_id: str
    gross_sales: float = 0.0
    net_sales: float = 0.0
    orders: int = 0
    refunds: float = 0.0
    cash_variance: float = 0.0
    food_cost: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "location_id": self.location_id,
            "gross_sales": round(self.gross_sales, 2),
            "net_sales": round(self.net_sales, 2),
            "orders": self.orders,
            "refunds": round(self.refunds, 2),
            "cash_variance": round(self.cash_variance, 2),
            "food_cost": round(self.food_cost, 2),
        }


class AnalyticsService:
    def get_store_summary(self, location_id: str) -> dict[str, Any]:
        summary = StoreSummary(
            location_id=location_id,
            gross_sales=2450.00,
            net_sales=2325.00,
            orders=87,
            refunds=120.00,
            cash_variance=25.50,
            food_cost=710.00,
        )
        return summary.as_dict()

    def get_head_office_rollup(self, location_ids: list[str]) -> dict[str, Any]:
        totals = [self.get_store_summary(location_id) for location_id in location_ids]
        return {
            "locations": totals,
            "total_gross_sales": round(sum(item["gross_sales"] for item in totals), 2),
            "total_net_sales": round(sum(item["net_sales"] for item in totals), 2),
            "total_orders": sum(item["orders"] for item in totals),
        }
