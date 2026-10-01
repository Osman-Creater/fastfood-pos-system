from __future__ import annotations

from decimal import Decimal


class BankReconciliationService:
    def reconcile_bank_deposit(self, expected_cash: Decimal, actual_bank_deposit: Decimal) -> dict:
        variance = actual_bank_deposit - expected_cash
        return {
            "expected_cash": str(expected_cash),
            "actual_bank_deposit": str(actual_bank_deposit),
            "variance": str(variance),
            "status": "matched" if variance == 0 else "difference_detected",
        }

    def reconcile_card_settlement(self, card_sales_total: Decimal, settlement_amount: Decimal, processing_fees: Decimal) -> dict:
        net_expected = card_sales_total - processing_fees
        variance = settlement_amount - net_expected
        return {
            "card_sales_total": str(card_sales_total),
            "processing_fees": str(processing_fees),
            "settlement_amount": str(settlement_amount),
            "net_expected": str(net_expected),
            "variance": str(variance),
        }
