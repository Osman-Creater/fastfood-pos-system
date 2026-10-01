from __future__ import annotations

from decimal import Decimal


class ReconciliationService:
    def create_shift_reconciliation_journal(self, shift: dict, over_short: Decimal):
        if over_short >= 0:
            journal_entry = {
                "entry_type": "shift_reconciliation",
                "description": "Cash reconciliation overage",
                "location_id": shift.get("location_id"),
            }
            journal_lines = [
                {"account_code": "1000", "debit": str(over_short), "credit": "0.00"},
                {"account_code": "6000", "debit": "0.00", "credit": str(over_short)},
            ]
        else:
            journal_entry = {
                "entry_type": "shift_reconciliation",
                "description": "Cash reconciliation shortage",
                "location_id": shift.get("location_id"),
            }
            journal_lines = [
                {"account_code": "6000", "debit": str(abs(over_short)), "credit": "0.00"},
                {"account_code": "1000", "debit": "0.00", "credit": str(abs(over_short))},
            ]

        return journal_entry, journal_lines
