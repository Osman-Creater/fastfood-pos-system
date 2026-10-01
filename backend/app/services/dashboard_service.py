from __future__ import annotations

from datetime import datetime
from decimal import Decimal


class DashboardService:
    async def get_summary(self, location_id: str, date: str) -> dict:
        return {
            "location_id": location_id,
            "date": date,
            "kpis": [
                {"label": "Gross Sales", "value": "0.00"},
                {"label": "Net Sales", "value": "0.00"},
                {"label": "Orders", "value": "0"},
                {"label": "Refunds", "value": "0.00"},
            ],
            "top_items": [],
            "payment_mix": [],
            "low_stock_alerts": [],
        }
