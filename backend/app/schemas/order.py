from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: str
    product_id: int

class OrderRead(BaseModel):
    id: int
    user_id: str
    product_id: int
    order_date: str
    model_config = {"from_attributes": True}
