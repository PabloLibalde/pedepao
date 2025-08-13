from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Time, Boolean, String
from app.db.base import Base

class Window(Base):
    __tablename__ = "windows"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    cutoff_time: Mapped[str] = mapped_column(String(8), default="13:00")  # HH:MM (local)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
