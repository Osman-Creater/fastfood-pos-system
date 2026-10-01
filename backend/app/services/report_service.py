from __future__ import annotations

from decimal import Decimal
from datetime import datetime


class ReportService:
    async def get_daily_sales_summary(self, location_id: str, report_date: datetime):
        return {
            "location_id": location_id,
            "report_date": report_date.date().isoformat(),
            "gross_sales": "2450.00",
            "tax_total": "220.50",
            "discount_total": "25.00",
            "refund_total": "45.00",
            "net_sales": "2325.50",
            "order_count": 87,
            "average_order_value": "28.22",
            "cash_sales": "1120.00",
            "card_sales": "830.50",
            "wallet_sales": "210.00",
            "delivery_platform_sales": "290.00",
        }

    async def get_food_cost_report(self, location_id: str, start_date: datetime, end_date: datetime):
        return {
            "location_id": location_id,
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "items": [
                {"name": "Classic Burger", "sold": 54, "food_cost": "172.40", "sales": "675.00"},
                {"name": "Chicken Wrap", "sold": 46, "food_cost": "144.80", "sales": "483.00"},
                {"name": "Fries", "sold": 72, "food_cost": "86.40", "sales": "324.00"},
                {"name": "Soft Drink", "sold": 82, "food_cost": "41.00", "sales": "225.50"},
            ],
            "total_food_cost": "444.60",
            "total_sales": "1707.50",
        }

    async def get_profit_loss_report(self, location_id: str, start_date: datetime, end_date: datetime):
        return {
            "location_id": location_id,
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "revenue": {"food_sales": "2450.00", "beverage_sales": "380.00"},
            "cost_of_goods_sold": {"food_cost": "710.00"},
            "operating_expenses": {"rent": "420.00", "utilities": "160.00", "labor": "840.00"},
            "net_profit": "700.00",
        }
