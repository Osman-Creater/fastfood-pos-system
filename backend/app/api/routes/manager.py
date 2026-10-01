from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user
from app.services.manager_report_service import ManagerReportService

router = APIRouter(prefix="/api/v1/manager", tags=["manager"])


@router.get("/summary")
async def manager_summary(location_id: str, current_user=Depends(get_current_user)):
    if "store_manager" not in current_user.get("roles", []) and "head_office_admin" not in current_user.get("roles", []):
        return {"success": False, "detail": "Forbidden"}

    service = ManagerReportService()
    return {"success": True, "data": service.get_location_summary(location_id)}


@router.get("/rollup")
async def head_office_rollup(current_user=Depends(get_current_user)):
    if "head_office_admin" not in current_user.get("roles", []):
        return {"success": False, "detail": "Forbidden"}

    service = ManagerReportService()
    return {"success": True, "data": service.get_head_office_rollup(["loc-001", "loc-002", "loc-003"])}


@router.get("/profit-loss")
async def profit_loss(location_id: str, current_user=Depends(get_current_user)):
    if "accountant" not in current_user.get("roles", []) and "head_office_admin" not in current_user.get("roles", []):
        return {"success": False, "detail": "Forbidden"}

    service = ManagerReportService()
    return {"success": True, "data": service.get_profit_loss_summary(location_id)}
