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
    # IMPORTANTE no SQLAlchemy 2.x: anotação usa o tipo Python (date), não o tipo SA
    order_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
