from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/store-summary")
async def store_summary(location_id: str, current_user=Depends(get_current_user)):
    if current_user.get("location_id") and current_user["location_id"] != location_id:
        raise HTTPException(status_code=403, detail="Location access denied")

    service = AnalyticsService()
    return {"success": True, "data": service.get_store_summary(location_id)}


@router.get("/head-office-rollup")
async def head_office_rollup(location_ids: str, current_user=Depends(get_current_user)):
    ids = [item.strip() for item in location_ids.split(",") if item.strip()]
    service = AnalyticsService()
    return {"success": True, "data": service.get_head_office_rollup(ids)}
