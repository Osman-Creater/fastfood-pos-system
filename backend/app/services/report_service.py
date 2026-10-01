from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from app.seed_data import get_demo_orders


class ReportService:
    async def get_daily_sales_summary(self, location_id: str, report_date: datetime):
        orders = get_demo_orders(location_id)
        total_gross = Decimal("0")
        total_tax = Decimal("0")
        order_count = 0

        for order in orders:
            order_date = datetime.fromisoformat(order["created_at"]).date()
            if order_date == report_date.date():
                total_gross += Decimal(str(order["total_amount"]))
                total_tax += Decimal(str(order["tax_total"]))
                order_count += 1

        net_sales = total_gross - total_tax
        avg_order_value = (total_gross / order_count) if order_count else Decimal("0")

        return {
            "location_id": location_id,
            "report_date": report_date.date().isoformat(),
            "gross_sales": str(total_gross.quantize(Decimal("0.01"))),
            "tax_total": str(total_tax.quantize(Decimal("0.01"))),
            "discount_total": "0.00",
            "refund_total": "0.00",
            "net_sales": str(net_sales.quantize(Decimal("0.01"))),
            "order_count": order_count,
            "average_order_value": str(avg_order_value.quantize(Decimal("0.01"))),
            "cash_sales": "0.00",
            "card_sales": "0.00",
            "wallet_sales": "0.00",
            "delivery_platform_sales": "0.00",
        }

    async def get_food_cost_report(self, location_id: str, start_date: datetime, end_date: datetime):
        items = [
            {"name": "Classic Burger", "sold": 54, "food_cost": "172.40", "sales": "675.00"},
            {"name": "Chicken Wrap", "sold": 46, "food_cost": "144.80", "sales": "483.00"},
            {"name": "Fries", "sold": 72, "food_cost": "86.40", "sales": "324.00"},
            {"name": "Soft Drink", "sold": 82, "food_cost": "41.00", "sales": "225.50"},
        ]

        total_food_cost = sum(Decimal(str(item["food_cost"])) for item in items)
        total_sales = sum(Decimal(str(item["sales"])) for item in items)

        return {
            "location_id": location_id,
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "items": items,
            "total_food_cost": str(total_food_cost.quantize(Decimal("0.01"))),
            "total_sales": str(total_sales.quantize(Decimal("0.01"))),
        }

    async def get_profit_loss_report(self, location_id: str, start_date: datetime, end_date: datetime):
        revenue = {"food_sales": "2450.00", "beverage_sales": "380.00"}
        cost_of_goods_sold = {"food_cost": "710.00"}
        operating_expenses = {"rent": "420.00", "utilities": "160.00", "labor": "840.00"}

        revenue_total = Decimal(revenue["food_sales"]) + Decimal(revenue["beverage_sales"])
        cogs_total = Decimal(cost_of_goods_sold["food_cost"])
        expense_total = sum(Decimal(str(v)) for v in operating_expenses.values())
        net_profit = revenue_total - cogs_total - expense_total

        return {
            "location_id": location_id,
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "revenue": revenue,
            "cost_of_goods_sold": cost_of_goods_sold,
            "operating_expenses": operating_expenses,
            "net_profit": str(net_profit.quantize(Decimal("0.01"))),
        }
