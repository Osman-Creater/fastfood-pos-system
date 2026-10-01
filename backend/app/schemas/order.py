from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class OrderItemInput(BaseModel):
    menu_item_id: str
    quantity: int = Field(..., gt=0)
    notes: Optional[str] = None
    modifier_ids: list[str] = []


class CreateOrderInput(BaseModel):
    location_id: str
    terminal_id: Optional[str] = None
    shift_id: Optional[str] = None
    cashier_user_id: str
    customer_id: Optional[str] = None
    order_type: str = "dine_in"
    discount_code: Optional[str] = None
    notes: Optional[str] = None
    items: list[OrderItemInput]


class PaymentInput(BaseModel):
    payment_method: str
    payment_provider: Optional[str] = None
    reference_no: Optional[str] = None
    amount: Decimal = Field(..., gt=0)


class DailySalesSummary(BaseModel):
    location_id: str
    report_date: str
    gross_sales: Decimal
    tax_total: Decimal
    discount_total: Decimal
    refund_total: Decimal
    net_sales: Decimal
    order_count: int
    average_order_value: Decimal
    cash_sales: Decimal
    card_sales: Decimal
    wallet_sales: Decimal
    delivery_platform_sales: Decimal
