from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import zoneinfo

from ..auth import get_db, require_admin, get_current_user
from ..schemas import OfferCreate, OfferWindowCreate, OfferUpdate
from ..models import Offer, OfferWindow
from ..config import settings

router = APIRouter(prefix="/offers", tags=["offers"])

@router.post("", dependencies=[Depends(require_admin)])
def create_offer(body: OfferCreate, db: Session = Depends(get_db)):
    offer = Offer(name=body.name, description=body.description, active=body.active)
    db.add(offer); db.commit()
    return {"id": offer.id}

@router.post("/window", dependencies=[Depends(require_admin)])
def create_window(body: OfferWindowCreate, db: Session = Depends(get_db)):
    if not db.get(Offer, body.offer_id):
        raise HTTPException(404, "Oferta inexistente")
    weekdays = ",".join(map(str, body.weekdays))
    w = OfferWindow(
        offer_id=body.offer_id,
        start_date=body.start_date,
        end_date=body.end_date,
        weekdays=weekdays,
        cutoff_local_time=body.cutoff_local_time,
    )
    db.add(w); db.commit()
    return {"id": w.id}

@router.get("/today")
def today_offers(db: Session = Depends(get_db), user = Depends(get_current_user)):
    tz = zoneinfo.ZoneInfo(settings.TZ)
    now = datetime.now(tz)
    today = now.date()
    weekday = now.isoweekday()  # 1..7
    q = db.query(Offer, OfferWindow).join(OfferWindow, Offer.id == OfferWindow.offer_id)\
        .filter(Offer.active == True)\
        .filter(OfferWindow.start_date <= today, OfferWindow.end_date >= today)
    items = []
    for offer, win in q.all():
        if str(weekday) in win.weekdays.split(","):
            items.append({
                "offer_id": offer.id, "name": offer.name, "description": offer.description,
                "cutoff": win.cutoff_local_time
            })
    return {"date": str(today), "items": items}

@router.get("", dependencies=[Depends(require_admin)])
def list_offers(db: Session = Depends(get_db)):
    rows = db.query(Offer).order_by(Offer.name).all()
    return [
        {"id": o.id, "name": o.name, "description": o.description, "active": o.active}
        for o in rows
    ]
@router.put("/{offer_id}", dependencies=[Depends(require_admin)])
def update_offer(offer_id: int, body: OfferUpdate, db: Session = Depends(get_db)):
    o = db.query(Offer).filter(Offer.id == offer_id).first()
    if not o:
        raise HTTPException(404, "Oferta não encontrada")
    if body.name is not None:
        o.name = body.name
    if body.description is not None:
        o.description = body.description
    if body.active is not None:
        o.active = body.active
    db.commit()
    db.refresh(o)
    return {"id": o.id, "name": o.name, "description": o.description, "active": o.active}