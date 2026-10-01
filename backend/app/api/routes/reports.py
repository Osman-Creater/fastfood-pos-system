from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Query
from app.services.report_service import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/daily-sales")
async def daily_sales(location_id: str, report_date: datetime = Query(...)):
    report = await ReportService().get_daily_sales_summary(location_id, report_date)
    return {"success": True, "data": report}


@router.get("/food-cost")
async def food_cost(location_id: str, start_date: datetime = Query(...), end_date: datetime = Query(...)):
    report = await ReportService().get_food_cost_report(location_id, start_date, end_date)
    return {"success": True, "data": report}


@router.get("/profit-loss")
async def profit_loss(location_id: str, start_date: datetime = Query(...), end_date: datetime = Query(...)):
    report = await ReportService().get_profit_loss_report(location_id, start_date, end_date)
    return {"success": True, "data": report}
