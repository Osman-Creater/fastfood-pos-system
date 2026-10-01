from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user
from app.services.bank_reconciliation_service import BankReconciliationService
from app.services.role_access_service import RoleAccessService

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/access-check")
async def access_check(location_id: str, user_location_id: str | None = None, current_user=Depends(get_current_user)):
    service = RoleAccessService()
    allowed = service.can_access_location(current_user.get("roles", []), location_id, user_location_id)
    return {"success": True, "allowed": allowed}


@router.get("/bank-reconciliation")
async def bank_reconciliation(expected_cash: float, actual_bank_deposit: float, current_user=Depends(get_current_user)):
    if "accountant" not in current_user.get("roles", []) and "head_office_admin" not in current_user.get("roles", []):
        return {"success": False, "detail": "Forbidden"}

    service = BankReconciliationService()
    return {"success": True, "data": service.reconcile_bank_deposit(expected_cash, actual_bank_deposit)}
