from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.offer import Offer
from app.db.models.product import Product
from app.schemas.offer import OfferCreate, OfferRead, OfferUpdate

router = APIRouter(prefix="/offers", tags=["offers"])


def _offer_to_read_tuple(db_row: tuple[Offer, str]) -> dict:
    o, pname = db_row
    return {
        "id": o.id,
        "product_id": o.product_id,
        "product_name": pname,
        "cutoff_time": o.cutoff_time,
        "is_active": o.is_active,
    }


@router.get("", response_model=list[OfferRead])
def list_offers(
    db: Session = Depends(get_db),
    active: bool | None = Query(default=None),
    product_id: int | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
):
    stmt = select(Offer, Product.name).join(Product, Product.id == Offer.product_id)
    if active is not None:
        stmt = stmt.where(Offer.is_active == active)
    if product_id is not None:
        stmt = stmt.where(Offer.product_id == product_id)

    stmt = stmt.order_by(Offer.id.asc()).limit(limit).offset(offset)
    rows = db.execute(stmt).all()
    return [_offer_to_read_tuple(r) for r in rows]


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Offer, Product.name)
        .join(Product, Product.id == Offer.product_id)
        .where(Offer.id == offer_id)
    )
    row = db.execute(stmt).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta não encontrada")
    return _offer_to_read_tuple(row)


@router.post("", response_model=OfferRead, status_code=201)
def create_offer(data: OfferCreate, db: Session = Depends(get_db)):
    # checa se produto existe
    if not db.get(Product, data.product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto inválido")

    o = Offer(**data.model_dump())
    db.add(o)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # em geral não há unique aqui; este except cobre FK etc.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflito ao criar oferta")
    db.refresh(o)

    pname = db.query(Product.name).filter(Product.id == o.product_id).scalar() or ""
    return {
        "id": o.id,
        "product_id": o.product_id,
        "product_name": pname,
        "cutoff_time": o.cutoff_time,
        "is_active": o.is_active,
    }


@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(offer_id: int, data: OfferUpdate, db: Session = Depends(get_db)):
    o = db.get(Offer, offer_id)
    if not o:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta não encontrada")

    payload = data.model_dump(exclude_unset=True)

    if "product_id" in payload and payload["product_id"] is not None:
        # valida FK
        if not db.get(Product, payload["product_id"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto inválido")
        o.product_id = payload["product_id"]

    if "cutoff_time" in payload and payload["cutoff_time"] is not None:
        o.cutoff_time = payload["cutoff_time"]

    if "is_active" in payload and payload["is_active"] is not None:
        o.is_active = payload["is_active"]

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflito ao atualizar oferta")

    db.refresh(o)
    pname = db.query(Product.name).filter(Product.id == o.product_id).scalar() or ""
    return {
        "id": o.id,
        "product_id": o.product_id,
        "product_name": pname,
        "cutoff_time": o.cutoff_time,
        "is_active": o.is_active,
    }


@router.delete("/{offer_id}", status_code=204)
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    o = db.get(Offer, offer_id)
    if not o:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta não encontrada")

    db.delete(o)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # se no futuro houver FK (ex.: histórico) com RESTRICT, retornamos 409
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir: oferta referenciada por outros registros",
        )
    return None
