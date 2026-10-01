from __future__ import annotations

from typing import Any

from app.config import settings


def build_demo_seed() -> dict[str, Any]:
    return {
        "locations": [
            {"id": "loc-001", "name": "Downtown Outlet", "code": "DTW-001", "city": "Nairobi", "country": "Kenya"},
            {"id": "loc-002", "name": "Westview Branch", "code": "WVW-002", "city": "Mombasa", "country": "Kenya"},
        ],
        "users": [
            {"id": "usr-001", "username": "cashier", "first_name": "Jane", "last_name": "Njeri", "roles": ["cashier", "shift_supervisor"], "location_id": "loc-001"},
            {"id": "usr-002", "username": "manager", "first_name": "John", "last_name": "Otieno", "roles": ["manager", "accountant"], "location_id": "loc-001"},
            {"id": "usr-003", "username": "admin", "first_name": "Mary", "last_name": "Wambui", "roles": ["admin"], "location_id": "loc-001"},
        ],
        "menu_items": [
            {"id": "menu-001", "name": "Classic Burger", "unit_price": 12.50, "cost_price": 4.10, "location_id": "loc-001"},
            {"id": "menu-002", "name": "Chicken Wrap", "unit_price": 10.50, "cost_price": 3.80, "location_id": "loc-001"},
            {"id": "menu-003", "name": "Fries", "unit_price": 4.50, "cost_price": 1.20, "location_id": "loc-001"},
        ],
        "inventory": [
            {"id": "inv-001", "name": "Chicken", "current_quantity": 30, "reorder_level": 12, "unit_cost": 2.10, "location_id": "loc-001"},
            {"id": "inv-002", "name": "Buns", "current_quantity": 100, "reorder_level": 25, "unit_cost": 0.70, "location_id": "loc-001"},
            {"id": "inv-003", "name": "Lettuce", "current_quantity": 18, "reorder_level": 10, "unit_cost": 0.50, "location_id": "loc-001"},
        ],
    }


def get_demo_user(username: str | None = None) -> dict[str, Any] | None:
    seed = build_demo_seed()
    for user in seed["users"]:
        if username is None or user["username"] == username:
            return user
    return None


def get_default_api_base_url() -> str:
    return settings.NEXT_PUBLIC_API_URL
