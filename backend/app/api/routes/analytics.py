from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/store-summary")
async def store_summary(location_id: str, current_user=Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "location_id": location_id,
            "gross_sales": "0.00",
            "orders": 0,
            "net_sales": "0.00",
            "cash_variance": "0.00",
            "food_cost": "0.00",
        },
    }
