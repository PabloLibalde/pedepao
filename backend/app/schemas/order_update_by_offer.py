from pydantic import BaseModel

class OrderUpdateByOffer(BaseModel):
    user_id: str
    offer_id: int
