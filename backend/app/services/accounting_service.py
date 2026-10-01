from __future__ import annotations

from datetime import datetime
from decimal import Decimal


class AccountingService:
    async def create_sale_journal(self, order: dict, payment_method: str, total_amount: Decimal, tax_total: Decimal):
        if payment_method == "cash":
            account_code = "1000"
        elif payment_method == "card":
            account_code = "1020"
        else:
            account_code = "1030"

        return {
            "entry_type": "sale",
            "description": f"Sale for order {order.get('id')}",
            "entry_date": datetime.utcnow().isoformat(),
            "lines": [
                {"account_code": account_code, "debit": str(total_amount), "credit": "0.00"},
                {"account_code": "3000", "debit": "0.00", "credit": str(Decimal(str(total_amount)) - tax_total)},
                {"account_code": "2000", "debit": "0.00", "credit": str(tax_total)},
            ],
        }
