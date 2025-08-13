from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date, String, ForeignKey
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), index=True, nullable=False
    )
    # tipo Python na anotação, tipo SA no mapped_column
    order_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
