from __future__ import annotations

from typing import Any


class RoleAccessService:
    def can_access_location(self, roles: list[str], location_id: str, user_location_id: str | None) -> bool:
        if "head_office_admin" in roles:
            return True
        if user_location_id is None:
            return False
        return user_location_id == location_id or "store_manager" in roles

    def can_approve_refund(self, roles: list[str]) -> bool:
        return "shift_supervisor" in roles or "store_manager" in roles or "head_office_admin" in roles

    def can_manage_inventory(self, roles: list[str]) -> bool:
        return "inventory_officer" in roles or "store_manager" in roles or "head_office_admin" in roles

    def can_view_financials(self, roles: list[str]) -> bool:
        return "accountant" in roles or "head_office_admin" in roles
