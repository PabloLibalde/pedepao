from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    # todos opcionais para PUT/PATCH sem obrigar reenvio
    name: str | None = Field(default=None, min_length=1, max_length=120)
    is_active: bool | None = None


class ProductRead(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
