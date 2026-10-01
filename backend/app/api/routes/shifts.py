from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth.deps import get_current_user
from app.services.shift_service import ShiftService
from app.services.reconciliation_service import ReconciliationService

router = APIRouter(prefix="/api/v1/shifts", tags=["shifts"])


class CloseShiftInput(BaseModel):
    counted_cash: Decimal


@router.post("/{shift_id}/close")
async def close_shift(shift_id: str, payload: CloseShiftInput, current_user=Depends(get_current_user)):
    if "shift_supervisor" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Only supervisors can close shifts")

    shift_service = ShiftService()
    shift, over_short = shift_service.close_shift({
        "id": shift_id,
        "location_id": "loc-001",
        "opening_cash": 250.00,
    }, payload.counted_cash)

    reconciliation_service = ReconciliationService()
    journal_entry, journal_lines = reconciliation_service.create_shift_reconciliation_journal(shift, over_short)

    return {
        "success": True,
        "data": {
            "shift": shift,
            "over_short": str(over_short),
            "journal_entry": journal_entry,
            "journal_lines": journal_lines,
        },
    }
