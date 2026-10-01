from __future__ import annotations

from fastapi import APIRouter

from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary")
async def dashboard_summary(location_id: str, date: str):
    service = DashboardService()
    return {"success": True, "data": await service.get_summary(location_id, date)}
