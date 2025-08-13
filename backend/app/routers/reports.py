from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..auth import get_db, require_admin
from ..schemas import ReportFilter
from ..models import Order, Offer, User

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(require_admin)])

@router.post("/summary")
def summary(body: ReportFilter, db: Session = Depends(get_db)):
    q = db.query(Offer.name, func.count(Order.id))\
        .join(Offer, Offer.id == Order.offer_id)\
        .filter(Order.order_date >= body.date_from, Order.order_date <= body.date_to)\
        .group_by(Offer.name).order_by(Offer.name)
    data = [{"offer": name, "qty": qty} for name, qty in q.all()]
    return {"items": data}

@router.post("/detail")
def detail(body: ReportFilter, db: Session = Depends(get_db)):
    q = db.query(Order.order_date, User.full_name, Offer.name)\
        .join(User, User.id == Order.user_id)\
        .join(Offer, Offer.id == Order.offer_id)\
        .filter(Order.order_date >= body.date_from, Order.order_date <= body.date_to)\
        .order_by(Order.order_date, User.full_name)
    data = [{"date": str(d), "user": u, "offer": o} for d, u, o in q.all()]
    return {"items": data}
