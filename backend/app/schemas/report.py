from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class DashboardKPI(BaseModel):
    label: str
    value: Decimal


class DashboardSummary(BaseModel):
    location_id: str
    date: str
    kpis: list[DashboardKPI]
    top_items: list[dict]
    payment_mix: list[dict]
    low_stock_alerts: list[dict]
