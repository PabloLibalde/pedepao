from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OfferCreate(BaseModel):
    name: str
    description: str | None = None
    active: bool = True
    
class OfferUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    active: bool | None = None

class OfferWindowCreate(BaseModel):
    offer_id: int
    start_date: date
    end_date: date
    weekdays: list[int] = Field(default_factory=lambda: [1,2,3,4,5])
    cutoff_local_time: str = "13:00"

class ReportFilter(BaseModel):
    date_from: date
    date_to: date
