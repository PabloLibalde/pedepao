from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, String, ForeignKey
from app.db.base import Base

class Offer(Base):
    __tablename__ = "offers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    cutoff_time: Mapped[str] = mapped_column(String(8), default="13:00")  # HH:MM (local)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
