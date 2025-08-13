from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.order import Order
from app.db.models.offer import Offer


def _today_date():
    """Retorna a data de hoje no fuso configurado."""
    return datetime.now(ZoneInfo(settings.tz)).date()


def _is_before_cutoff(cutoff_time_str: str) -> bool:
    """cutoff_time_str no formato HH:MM (24h)."""
    now = datetime.now(ZoneInfo(settings.tz))
    hh, mm = map(int, cutoff_time_str.split(":"))
    cutoff_dt = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    return now <= cutoff_dt


def get_today_order(db: Session, user_id: str) -> Order | None:
    today = _today_date()
    return (
        db.query(Order)
        .filter(Order.user_id == user_id, Order.order_date == today)
        .one_or_none()
    )


def create_order(db: Session, user_id: str, product_id: int) -> Order:
    """
    Cria pedido para 'hoje'. Se já existir, levanta ValueError.
    (Mantém a regra de 1 pedido/dia.)
    """
    today = _today_date()

    existing = (
        db.query(Order)
        .filter(Order.user_id == user_id, Order.order_date == today)
        .one_or_none()
    )
    if existing:
        raise ValueError("Já existe um pedido hoje")

    new_order = Order(user_id=user_id, product_id=product_id, order_date=today)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def cancel_today_order(db: Session, user_id: str) -> bool:
    """
    Cancela o pedido de hoje (se existir). Retorna True se cancelou, False se não havia.
    """
    order = get_today_order(db, user_id)
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True


def switch_today_order_to_offer(db: Session, user_id: str, offer_id: int) -> Order:
    """
    Troca o produto do pedido de hoje para o produto da oferta informada.
    Só permite se:
      - existir pedido hoje para o user_id
      - a oferta existir e estiver ativa
      - ainda estiver antes do cutoff da oferta
    """
    order = get_today_order(db, user_id)
    if not order:
        raise LookupError("Não há pedido hoje para este usuário")

    offer = db.get(Offer, offer_id)
    if not offer or not offer.is_active:
        raise LookupError("Oferta inválida")

    if not _is_before_cutoff(offer.cutoff_time):
        raise TimeoutError("Cutoff atingido para alteração")

    order.product_id = offer.product_id
    db.commit()
    db.refresh(order)
    return order
