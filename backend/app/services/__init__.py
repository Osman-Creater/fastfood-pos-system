from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.deps import get_current_user
from app.services.journal_service import JournalService

router = APIRouter(prefix="/api/v1/shifts", tags=["shifts"])


class CloseShiftInput(BaseModel):
    counted_cash: Decimal


@router.post("/{shift_id}/close")
async def close_shift(shift_id: str, payload: CloseShiftInput, current_user=Depends(get_current_user)):
    if "shift_supervisor" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Only supervisors can close shifts")

    shift = {
        "id": shift_id,
        "location_id": "loc-001",
        "opening_cash": 250.00,
    }

    expected_cash = Decimal("250.00")
    over_short = Decimal(str(payload.counted_cash)) - expected_cash

    journal_service = JournalService()
    journal_entry = journal_service.create_shift_reconciliation_journal(shift, over_short)

    return {
        "success": True,
        "data": {
            "shift": {
                **shift,
                "expected_cash": str(expected_cash),
                "counted_cash": str(payload.counted_cash),
                "over_short": str(over_short),
                "status": "closed",
            },
            "journal_entry": journal_entry,
        },
    }
