from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Text, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Offer(Base):
    __tablename__ = "offers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class OfferWindow(Base):
    __tablename__ = "offer_windows"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    weekdays = Column(ARRAY(Integer), nullable=False)   # [1..7] (Seg..Dom)
    cutoff_local_time = Column(String, nullable=False)  # "HH:MM"
    active = Column(Boolean, default=True, index=True)  # <--- GARANTA ESTE CAMPO

    offer = relationship("Offer", back_populates="windows")

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        UniqueConstraint("user_id", "order_date", name="uq_user_orderdate"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id", ondelete="CASCADE"))
    order_date: Mapped[date] = mapped_column(Date)
    chosen_at_utc: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
