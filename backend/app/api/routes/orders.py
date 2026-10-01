from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.deps import get_current_user

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

    subtotal = Decimal("0")
    for item in payload.items:
        subtotal += Decimal("12.50") * Decimal(item.quantity)

    tax_total = subtotal * Decimal("0.10")
    discount_total = Decimal("0")
    total_amount = subtotal + tax_total - discount_total

    order = {
        "id": str(uuid4()),
        "location_id": payload.location_id,
        "order_type": payload.order_type,
        "status": "open",
        "subtotal": str(subtotal),
        "tax_total": str(tax_total),
        "discount_total": str(discount_total),
        "total_amount": str(total_amount),
        "payment_status": "unpaid",
        "items": payload.items,
    }

    return {"success": True, "data": order}


@router.post("/{order_id}/payments")
async def finalize_order(order_id: str, payload: PaymentInput, current_user=Depends(get_current_user)):
    if "cashier" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Forbidden")

    return {
        "success": True,
        "data": {
            "order_id": order_id,
            "payment_method": payload.payment_method,
            "amount": str(payload.amount),
            "status": "paid",
        },
    }
