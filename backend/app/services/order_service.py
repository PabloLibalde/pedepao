from datetime import datetime, date
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.core.config import settings
from app.db.models.order import Order

def get_today_local_date() -> date:
    now = datetime.now(ZoneInfo(settings.tz))
    return now.date()

def ensure_cutoff() -> None:
    # Exemplo simples: compara HH:MM como strings; poderia converter para time
    local_now = datetime.now(ZoneInfo(settings.tz)).strftime("%H:%M")
    cutoff = settings.cutoff_default
    if local_now >= cutoff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pedido após o cutoff")

def create_order(db: Session, user_id: str, product_id: int) -> Order:
    ensure_cutoff()
    od = get_today_local_date()
    order = Order(user_id=user_id, product_id=product_id, order_date=od)
    db.add(order)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um pedido hoje")
    db.refresh(order)
    return order
