from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from app.services.inventory_service import InventoryService
from app.services.journal_service import JournalService


class OrderService:
    def __init__(self):
        self.inventory_service = InventoryService()
        self.journal_service = JournalService()

    def create_order(self, payload: dict) -> dict:
        subtotal = Decimal("0")
        tax_rate = Decimal("0.10")

        for item in payload["items"]:
            unit_price = Decimal("12.50")
            subtotal += unit_price * Decimal(str(item["quantity"]))

        tax_total = subtotal * tax_rate
        discount_total = Decimal("0")
        total_amount = subtotal + tax_total - discount_total

        order = {
            "id": str(uuid4()),
            "location_id": payload["location_id"],
            "terminal_id": payload.get("terminal_id"),
            "shift_id": payload.get("shift_id"),
            "cashier_user_id": payload["cashier_user_id"],
            "customer_id": payload.get("customer_id"),
            "order_number": f"ORD-{uuid4().hex[:8].upper()}",
            "order_type": payload.get("order_type", "dine_in"),
            "status": "open",
            "subtotal": str(subtotal),
            "tax_total": str(tax_total),
            "discount_total": str(discount_total),
            "total_amount": str(total_amount),
            "payment_status": "unpaid",
            "items": payload["items"],
        }
        return order

    def finalize_order(self, order: dict, payment_method: str, payment_amount: Decimal) -> dict:
        if payment_amount < Decimal(order["total_amount"]):
            raise ValueError("Insufficient payment amount")

        inventory_tx = self.inventory_service.deduct_for_order(order)
        journal = self.journal_service.create_sale_journal(
            order=order,
            payment_method=payment_method,
            payment_amount=payment_amount,
            tax_total=Decimal(order["tax_total"]),
        )

        order["status"] = "completed"
        order["payment_status"] = "paid"
        return {
            "order": order,
            "payment": {
                "order_id": order["id"],
                "payment_method": payment_method,
                "amount": str(payment_amount),
                "status": "paid",
            },
            "inventory_transactions": inventory_tx,
            "journal": journal,
        }
