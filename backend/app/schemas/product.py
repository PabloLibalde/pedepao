from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    is_active: bool = True

class ProductRead(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = {"from_attributes": True}
