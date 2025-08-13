from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.order_by_offer import OrderByOfferCreate
from app.schemas.order_update_by_offer import OrderUpdateByOffer
from app.db.models.order import Order
from app.db.models.offer import Offer
from app.services.order_service import (
    create_order,
    get_today_order,
    cancel_today_order,
    switch_today_order_to_offer,
)
from app.core.config import settings

from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderRead, status_code=201)
def create(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = create_order(db, user_id=data.user_id, product_id=data.product_id)
        return order
    except ValueError as e:
        # já existe pedido hoje
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/today/{user_id}", response_model=list[OrderRead])
def get_today_orders(user_id: str, db: Session = Depends(get_db)):
    today = datetime.now(ZoneInfo(settings.tz)).date()
    q = db.query(Order).filter(Order.user_id == user_id, Order.order_date == today)
    return q.all()


@router.post("/by-offer", response_model=OrderRead, status_code=201)
def create_by_offer(data: OrderByOfferCreate, db: Session = Depends(get_db)):
    offer = db.get(Offer, data.offer_id)
    if not offer or not offer.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta inválida")
    try:
        order = create_order(db, user_id=data.user_id, product_id=offer.product_id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/today/{user_id}", status_code=204)
def delete_today(user_id: str, db: Session = Depends(get_db)):
    deleted = cancel_today_order(db, user_id)
    if not deleted:
        # Não encontrou pedido; idempotente retornar 204 mesmo assim,
        # mas aqui optei por 404 para deixar claro em teste
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum pedido para hoje")
    return None


@router.put("/by-offer", response_model=OrderRead)
def update_today_by_offer(data: OrderUpdateByOffer, db: Session = Depends(get_db)):
    try:
        order = switch_today_order_to_offer(db, user_id=data.user_id, offer_id=data.offer_id)
        return order
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TimeoutError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
