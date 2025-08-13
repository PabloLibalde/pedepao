from __future__ import annotations

from datetime import date
from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    user_id: str
    product_id: int


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    order_date: date
    model_config = ConfigDict(from_attributes=True)
