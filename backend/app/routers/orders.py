from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import zoneinfo

from ..auth import get_db, get_current_user
from ..models import Order, OfferWindow
from ..config import settings

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("")
def place_order(offer_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    tz = zoneinfo.ZoneInfo(settings.TZ)
    now = datetime.now(tz)
    today = now.date()
    # valida janela no dia e weekday
    win = db.query(OfferWindow).filter(
        OfferWindow.offer_id == offer_id,
        OfferWindow.start_date <= today,
        OfferWindow.end_date >= today
    ).first()
    if not win:
        raise HTTPException(400, "Oferta não disponível hoje")
    if str(now.isoweekday()) not in win.weekdays.split(","):
        raise HTTPException(400, "Oferta não disponível neste dia da semana")

    # cutoff
    try:
        hh, mm = map(int, win.cutoff_local_time.split(":"))
    except Exception:
        raise HTTPException(500, "Configuração de cutoff inválida")
    cutoff_dt = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if now > cutoff_dt:
        raise HTTPException(400, f"Hora-limite {win.cutoff_local_time} já passou")

    # um pedido por usuário/dia
    exists = db.query(Order).filter(Order.user_id == user.id, Order.order_date == today).first()
    if exists:
        raise HTTPException(400, "Você já realizou um pedido hoje")

    # grava
    o = Order(user_id=user.id, offer_id=offer_id, order_date=today)
    db.add(o); db.commit()
    return {"ok": True}
