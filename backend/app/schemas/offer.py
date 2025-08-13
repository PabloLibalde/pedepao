from pydantic import BaseModel, Field

class OfferCreate(BaseModel):
    product_id: int
    cutoff_time: str = Field(default="13:00", pattern=r"^\d{2}:\d{2}$")
    is_active: bool = True

class OfferRead(BaseModel):
    id: int
    product_id: int
    product_name: str
    cutoff_time: str
    is_active: bool
    model_config = {"from_attributes": True}
