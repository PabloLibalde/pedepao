from __future__ import annotations

from pydantic import BaseModel, Field


class OfferBase(BaseModel):
    product_id: int
    cutoff_time: str = Field(pattern=r"^\d{2}:\d{2}$", description="HH:MM de 00:00 a 23:59")
    is_active: bool = True


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    product_id: int | None = None
    cutoff_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    is_active: bool | None = None


class OfferRead(BaseModel):
    id: int
    product_id: int
    product_name: str
    cutoff_time: str
    is_active: bool
