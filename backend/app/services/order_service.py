from __future__ import annotations

from typing import Any
from decimal import Decimal
from uuid import uuid4
from datetime import datetime

from app.seed_data import get_menu_item_by_id


class OrderService:
    def __init__(self):
        self.inventory_service = InventoryService()
        self.journal_service = JournalService()

    def create_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        subtotal = Decimal("0")
        tax_rate = Decimal("0.10")
        item_details: list[dict[str, Any]] = []

        for item in payload.get("items", []):
            menu_item = get_menu_item_by_id(item["menu_item_id"], payload.get("location_id"))
            quantity = Decimal(str(item.get("quantity", 1)))
            unit_price = Decimal(str(menu_item["unit_price"])) if menu_item else Decimal("12.50")
            item_subtotal = (unit_price * quantity).quantize(Decimal("0.01"))
            subtotal += item_subtotal

            item_details.append(
                {
                    "menu_item_id": item["menu_item_id"],
                    "menu_item_name": menu_item["name"] if menu_item else "Unknown Item",
                    "quantity": int(quantity),
                    "unit_price": str(unit_price.quantize(Decimal("0.01"))),
                    "cost_price": str(Decimal(str(menu_item.get("cost_price", 0))).quantize(Decimal("0.01"))) if menu_item else "0.00",
                    "subtotal": str(item_subtotal),
                    "notes": item.get("notes"),
                }
            )

        tax_total = (subtotal * tax_rate).quantize(Decimal("0.01"))
        discount_total = Decimal(str(payload.get("discount_total", 0)))
        total_amount = (subtotal + tax_total - discount_total).quantize(Decimal("0.01"))

        return {
            "id": str(uuid4()),
            "location_id": payload["location_id"],
            "terminal_id": payload.get("terminal_id"),
            "shift_id": payload.get("shift_id"),
            "cashier_user_id": payload.get("cashier_user_id"),
            "customer_id": payload.get("customer_id"),
            "order_number": f"ORD-{uuid4().hex[:8].upper()}",
            "order_type": payload.get("order_type", "dine_in"),
            "status": "open",
            "subtotal": str(subtotal.quantize(Decimal("0.01"))),
            "tax_total": str(tax_total),
            "discount_total": str(discount_total.quantize(Decimal("0.01"))),
            "total_amount": str(total_amount),
            "payment_status": "unpaid",
            "items": item_details,
            "notes": payload.get("notes"),
            "created_at": datetime.utcnow().isoformat(),
        }

    def finalize_order(self, order: dict[str, Any], payment_method: str, payment_amount: Decimal) -> dict[str, Any]:
        total = Decimal(str(order["total_amount"]))
        if payment_amount < total:
            raise ValueError(f"Insufficient payment. Required: {total}, provided: {payment_amount}")

        change = (payment_amount - total).quantize(Decimal("0.01"))
        inventory_tx = self.inventory_service.deduct_for_order(order)
        journal = self.journal_service.create_sale_journal(
            order=order,
            payment_method=payment_method,
            payment_amount=payment_amount,
            tax_total=Decimal(str(order.get("tax_total", 0))),
        )

        order["status"] = "completed"
        order["payment_status"] = "paid"
        order["updated_at"] = datetime.utcnow().isoformat()

        return {
            "success": True,
            "order": order,
            "payment": {
                "order_id": order["id"],
                "payment_method": payment_method,
                "amount": str(payment_amount.quantize(Decimal("0.01"))),
                "change": str(change),
                "status": "paid",
                "processed_at": datetime.utcnow().isoformat(),
            },
            "inventory_transactions": inventory_tx,
            "journal": journal,
            "change": str(change),
        }


class InventoryService:
    def __init__(self):
        pass

    def deduct_for_order(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        stock_entries: list[dict[str, Any]] = []
        location_id = order.get("location_id")

        for item in order.get("items", []):
            quantity = Decimal(str(item.get("quantity", 0)))
            if quantity <= 0:
                continue

            menu_item = get_menu_item_by_id(item["menu_item_id"], location_id)
            unit_cost = Decimal(str(menu_item["cost_price"])) if menu_item else Decimal("3.25")
            item_name = menu_item["name"] if menu_item else "Unknown Item"
            cost_total = (unit_cost * quantity).quantize(Decimal("0.01"))

            stock_entries.append(
                {
                    "id": str(uuid4()),
                    "inventory_item_id": item["menu_item_id"],
                    "movement_type": "sale",
                    "quantity": float(-quantity),
                    "unit_cost": str(unit_cost.quantize(Decimal("0.01"))),
                    "cost_total": str(cost_total),
                    "reference_type": "order",
                    "reference_id": order["id"],
                    "notes": f"Order {order.get('order_number', order['id'])} - {item_name}",
                    "created_at": datetime.utcnow().isoformat(),
                }
            )

        return stock_entries

    def get_location_inventory_summary(self, location_id: str) -> dict[str, Any]:
        inventory_items = [
            {"id": "inv-001", "name": "Chicken", "current_quantity": 30, "reorder_level": 12, "unit_cost": 2.10},
            {"id": "inv-002", "name": "Buns", "current_quantity": 100, "reorder_level": 25, "unit_cost": 0.70},
            {"id": "inv-003", "name": "Lettuce", "current_quantity": 18, "reorder_level": 10, "unit_cost": 0.50},
        ]
        low_stock = [item for item in inventory_items if item["current_quantity"] <= item["reorder_level"]]
        return {
            "location_id": location_id,
            "total_items": len(inventory_items),
            "low_stock_count": len(low_stock),
            "items": inventory_items,
            "low_stock_items": low_stock,
        }


class JournalService:
    def create_sale_journal(self, order: dict, payment_method: str, payment_amount: Decimal, tax_total: Decimal) -> dict:
        account_code = {
            "cash": "1000",
            "card": "1020",
            "wallet": "1200",
            "delivery_platform": "1030",
        }.get(payment_method.lower(), "1000")

        food_sales = Decimal(str(order["total_amount"])) - Decimal(str(tax_total))
        payment_amount = Decimal(str(payment_amount))
        tax_total = Decimal(str(tax_total))

        return {
            "id": str(uuid4()),
            "entry_number": f"JE-{uuid4().hex[:6].upper()}",
            "entry_type": "sale",
            "reference_type": "order",
            "reference_id": order.get("id"),
            "description": f"Sale for order {order.get('order_number')}",
            "entry_date": datetime.utcnow().isoformat(),
            "status": "posted",
            "lines": [
                {"account_code": account_code, "account_name": "Cash / Clearing", "debit": str(payment_amount.quantize(Decimal("0.01"))), "credit": "0.00"},
                {"account_code": "3000", "account_name": "Food Sales", "debit": "0.00", "credit": str(food_sales.quantize(Decimal("0.01")))},
                {"account_code": "2000", "account_name": "Sales Tax Payable", "debit": "0.00", "credit": str(tax_total.quantize(Decimal("0.01")))},
            ],
            "created_at": datetime.utcnow().isoformat(),
        }

    def create_shift_reconciliation_journal(self, shift: dict, over_short: Decimal) -> dict:
        over_short = Decimal(str(over_short))
        if over_short >= 0:
            lines = [
                {"account_code": "1000", "account_name": "Cash on Hand", "debit": str(over_short.quantize(Decimal("0.01"))), "credit": "0.00"},
                {"account_code": "6000", "account_name": "Owner Capital", "debit": "0.00", "credit": str(over_short.quantize(Decimal("0.01")))},
            ]
            description = f"Cash overage reconciliation: {over_short}"
        else:
            abs_value = abs(over_short)
            lines = [
                {"account_code": "6000", "account_name": "Owner Capital", "debit": str(abs_value.quantize(Decimal("0.01"))), "credit": "0.00"},
                {"account_code": "1000", "account_name": "Cash on Hand", "debit": "0.00", "credit": str(abs_value.quantize(Decimal("0.01")))},
            ]
            description = f"Cash shortage reconciliation: {abs_value}"

        return {
            "id": str(uuid4()),
            "entry_number": f"JE-{uuid4().hex[:6].upper()}",
            "entry_type": "shift_reconciliation",
            "reference_type": "shift",
            "reference_id": shift.get("id"),
            "description": description,
            "entry_date": datetime.utcnow().isoformat(),
            "status": "posted",
            "lines": lines,
            "created_at": datetime.utcnow().isoformat(),
        }

    def create_inventory_adjustment_journal(self, adjustment: dict) -> dict:
        cost_total = Decimal(str(adjustment.get("cost_total", 0)))
        return {
            "id": str(uuid4()),
            "entry_number": f"JE-{uuid4().hex[:6].upper()}",
            "entry_type": "inventory_adjustment",
            "reference_type": "stock_transaction",
            "reference_id": adjustment.get("id"),
            "description": f"Inventory adjustment: {adjustment.get('notes', 'No description')}",
            "entry_date": datetime.utcnow().isoformat(),
            "status": "posted",
            "lines": [
                {"account_code": "4030", "account_name": "Inventory Wastage", "debit": str(cost_total.quantize(Decimal("0.01"))), "credit": "0.00"},
                {"account_code": "1100", "account_name": "Inventory", "debit": "0.00", "credit": str(cost_total.quantize(Decimal("0.01")))},
            ],
            "created_at": datetime.utcnow().isoformat(),
        }


class ShiftService:
    def __init__(self):
        pass

    def open_shift(self, location_id: str, cashier_user_id: str, opening_cash: Decimal) -> dict:
        return {
            "id": str(uuid4()),
            "location_id": location_id,
            "cashier_user_id": cashier_user_id,
            "opening_cash": str(opening_cash.quantize(Decimal("0.01"))),
            "expected_cash": str(opening_cash.quantize(Decimal("0.01"))),
            "counted_cash": "0.00",
            "over_short": "0.00",
            "status": "open",
            "opened_at": datetime.utcnow().isoformat(),
            "closed_at": None,
            "created_at": datetime.utcnow().isoformat(),
        }

    def close_shift(self, shift: dict, counted_cash: Decimal, orders_summary: dict | None = None) -> tuple[dict, Decimal]:
        expected_cash = Decimal(str(shift.get("opening_cash", 0)))
        if orders_summary:
            expected_cash += Decimal(str(orders_summary.get("total_cash_sales", 0)))

        over_short = Decimal(str(counted_cash)) - expected_cash
        shift_closed = {
            **shift,
            "expected_cash": str(expected_cash.quantize(Decimal("0.01"))),
            "counted_cash": str(Decimal(str(counted_cash)).quantize(Decimal("0.01"))),
            "over_short": str(over_short.quantize(Decimal("0.01"))),
            "status": "closed",
            "closed_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        return shift_closed, over_short

    def get_shift_summary(self, shift: dict, orders: list | None = None) -> dict:
        orders = orders or []
        total_sales = Decimal("0")
        total_tax = Decimal("0")
        payment_breakdown = {
            "cash": Decimal("0"),
            "card": Decimal("0"),
            "wallet": Decimal("0"),
            "delivery_platform": Decimal("0"),
        }

        for order in orders:
            total_sales += Decimal(str(order.get("total_amount", 0)))
            total_tax += Decimal(str(order.get("tax_total", 0)))
            method = str(order.get("payment_method", "cash")).lower()
            if method in payment_breakdown:
                payment_breakdown[method] += Decimal(str(order.get("total_amount", 0)))

        return {
            "shift_id": shift.get("id"),
            "location_id": shift.get("location_id"),
            "cashier_user_id": shift.get("cashier_user_id"),
            "opened_at": shift.get("opened_at"),
            "closed_at": shift.get("closed_at"),
            "total_orders": len(orders),
            "total_sales": str(total_sales.quantize(Decimal("0.01"))),
            "total_tax": str(total_tax.quantize(Decimal("0.01"))),
            "payment_breakdown": {k: str(v.quantize(Decimal("0.01"))) for k, v in payment_breakdown.items()},
            "opening_cash": shift.get("opening_cash"),
            "expected_cash": shift.get("expected_cash"),
            "counted_cash": shift.get("counted_cash"),
            "over_short": shift.get("over_short"),
            "status": shift.get("status"),
        }


class ReportService:
    async def get_daily_sales_summary(self, location_id: str, report_date: datetime):
        from app.seed_data import get_demo_orders

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
