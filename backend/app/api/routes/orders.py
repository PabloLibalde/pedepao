from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.order_by_offer import OrderByOfferCreate
from app.db.models.order import Order
from app.db.models.offer import Offer
from app.services.order_service import create_order
from app.core.config import settings

from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderRead, status_code=201)
def create(data: OrderCreate, db: Session = Depends(get_db)):
    order = create_order(db, user_id=data.user_id, product_id=data.product_id)
    return order


@router.get("/today/{user_id}", response_model=list[OrderRead])
def get_today_orders(user_id: str, db: Session = Depends(get_db)):
    today = datetime.now(ZoneInfo(settings.tz)).date()
    q = db.query(Order).filter(Order.user_id == user_id, Order.order_date == today)
    return q.all()


@router.post("/by-offer", response_model=OrderRead, status_code=201)
def create_by_offer(data: OrderByOfferCreate, db: Session = Depends(get_db)):
    offer = db.query(Offer).get(data.offer_id)
    if not offer or not offer.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta inválida")
    order = create_order(db, user_id=data.user_id, product_id=offer.product_id)
    return order
