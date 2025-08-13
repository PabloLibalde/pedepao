from datetime import date
from sqlalchemy import Integer, Date, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("user_id", "order_date", name="uq_order_user_day"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(120), index=True)
    product_id: Mapped[int] = mapped_column(Integer, index=True)
    # 👇 tipo Python na anotação + tipo SA no mapped_column
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
