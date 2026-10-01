from __future__ import annotations

from decimal import Decimal
from datetime import datetime


class ReportService:
    async def get_daily_sales_summary(self, location_id: str, report_date: datetime):
        return {
            "location_id": location_id,
            "report_date": report_date.date().isoformat(),
            "gross_sales": str(Decimal("0")),
            "tax_total": str(Decimal("0")),
            "discount_total": str(Decimal("0")),
            "refund_total": str(Decimal("0")),
            "net_sales": str(Decimal("0")),
            "order_count": 0,
            "average_order_value": str(Decimal("0")),
            "cash_sales": str(Decimal("0")),
            "card_sales": str(Decimal("0")),
            "wallet_sales": str(Decimal("0")),
            "delivery_platform_sales": str(Decimal("0")),
        }

    async def get_food_cost_report(self, location_id: str, start_date: datetime, end_date: datetime):
        return {"location_id": location_id, "items": []}

    async def get_profit_loss_report(self, location_id: str, start_date: datetime, end_date: datetime):
        return {
            "location_id": location_id,
            "revenue": {"food_sales": "0.00", "beverage_sales": "0.00"},
            "cost_of_goods_sold": {"food_cost": "0.00"},
            "operating_expenses": {"rent": "0.00"},
            "net_profit": "0.00",
        }
