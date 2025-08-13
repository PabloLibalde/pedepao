from pydantic import BaseModel

class OrderByOfferCreate(BaseModel):
    user_id: str
    offer_id: int
