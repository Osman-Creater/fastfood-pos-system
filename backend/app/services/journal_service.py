from __future__ import annotations

from decimal import Decimal
from datetime import datetime


class JournalService:
    def create_sale_journal(self, order: dict, payment_method: str, payment_amount: Decimal, tax_total: Decimal) -> dict:
        if payment_method == "cash":
            cash_account = "1000"
        elif payment_method == "card":
            cash_account = "1020"
        elif payment_method == "delivery_platform":
            cash_account = "1030"
        else:
            cash_account = "1000"

        food_sales = Decimal(order["total_amount"]) - tax_total

        return {
            "entry_type": "sale",
            "reference_type": "order",
            "reference_id": order["id"],
            "description": f"Sale for order {order['order_number']}",
            "entry_date": datetime.utcnow().isoformat(),
            "lines": [
                {"account_code": cash_account, "debit": str(payment_amount), "credit": "0.00"},
                {"account_code": "3000", "debit": "0.00", "credit": str(food_sales)},
                {"account_code": "2000", "debit": "0.00", "credit": str(tax_total)},
            ],
        }

    def create_shift_reconciliation_journal(self, shift: dict, over_short: Decimal) -> dict:
        if over_short >= 0:
            lines = [
                {"account_code": "1000", "debit": str(over_short), "credit": "0.00"},
                {"account_code": "6000", "debit": "0.00", "credit": str(over_short)},
            ]
            description = "Cash overage reconciliation"
        else:
            lines = [
                {"account_code": "6000", "debit": str(abs(over_short)), "credit": "0.00"},
                {"account_code": "1000", "debit": "0.00", "credit": str(abs(over_short))},
            ]
            description = "Cash shortage reconciliation"

        return {
            "entry_type": "shift_reconciliation",
            "reference_type": "shift",
            "reference_id": shift["id"],
            "description": description,
            "entry_date": datetime.utcnow().isoformat(),
            "lines": lines,
        }
