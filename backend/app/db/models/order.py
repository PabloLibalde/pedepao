from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date, String, UniqueConstraint
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        UniqueConstraint("user_id", "order_date", name="uq_order_user_day"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(120), index=True)  # identificador do usuário
    product_id: Mapped[int] = mapped_column(Integer, index=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)  # YYYY-MM-DD (derivado de America/Sao_Paulo)
