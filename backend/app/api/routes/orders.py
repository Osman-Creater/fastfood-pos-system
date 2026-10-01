from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.deps import get_current_user
from app.services.order_service import OrderService

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


class OrderItemInput(BaseModel):
    menu_item_id: str
    quantity: int = 1
    notes: str | None = None
    modifier_ids: list[str] | None = None


class CreateOrderInput(BaseModel):
    location_id: str
    terminal_id: str | None = None
    shift_id: str | None = None
    cashier_user_id: str
    customer_id: str | None = None
    order_type: str = "dine_in"
    discount_code: str | None = None
    notes: str | None = None
    items: list[OrderItemInput]


class PaymentInput(BaseModel):
    payment_method: str
    payment_provider: str | None = None
    reference_no: str | None = None
    amount: Decimal


@router.post("")
async def create_order(payload: CreateOrderInput, current_user=Depends(get_current_user)):
    if "cashier" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Forbidden")

    service = OrderService()
    order = service.create_order(payload.model_dump())
    return {"success": True, "data": order}


@router.post("/{order_id}/payments")
async def finalize_order(order_id: str, payload: PaymentInput, current_user=Depends(get_current_user)):
    if "cashier" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Forbidden")

    service = OrderService()
    derived_order = {
        "id": order_id,
        "order_number": f"ORD-{uuid4().hex[:8].upper()}",
        "location_id": "loc-001",
        "total_amount": str(payload.amount),
        "tax_total": "0.00",
        "items": [{"menu_item_id": "menu-001", "quantity": 1}],
    }

    try:
        result = service.finalize_order(derived_order, payload.payment_method, payload.amount)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {"success": True, "data": result}
