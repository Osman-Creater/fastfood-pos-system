from __future__ import annotations

from decimal import Decimal


class ShiftService:
    def close_shift(self, shift: dict, counted_cash: Decimal):
        expected_cash = Decimal(str(shift["opening_cash"]))
        over_short = Decimal(str(counted_cash)) - expected_cash
        shift["expected_cash"] = str(expected_cash)
        shift["counted_cash"] = str(counted_cash)
        shift["over_short"] = str(over_short)
        shift["status"] = "closed"
        return shift, over_short
