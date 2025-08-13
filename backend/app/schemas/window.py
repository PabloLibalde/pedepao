from pydantic import BaseModel, Field

class WindowCreate(BaseModel):
    name: str
    cutoff_time: str = Field(default="13:00", pattern=r"^\d{2}:\d{2}$")
    is_active: bool = True

class WindowRead(BaseModel):
    id: int
    name: str
    cutoff_time: str
    is_active: bool
    model_config = {"from_attributes": True}
