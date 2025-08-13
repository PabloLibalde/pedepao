from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Boolean
from app.db.base import Base


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), index=True, nullable=False
    )
    cutoff_time: Mapped[str] = mapped_column(String(8), default="13:00", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
