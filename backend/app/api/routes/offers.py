from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.offer import Offer
from app.db.models.product import Product
from app.schemas.offer import OfferCreate, OfferRead

router = APIRouter(prefix="/offers", tags=["offers"])

@router.get("", response_model=list[OfferRead])
def list_offers(db: Session = Depends(get_db)):
    # Join para trazer o nome do produto
    stmt = select(Offer, Product.name).join(Product, Product.id == Offer.product_id)
    rows = db.execute(stmt).all()
    result = []
    for offer, product_name in rows:
        result.append({
            "id": offer.id,
            "product_id": offer.product_id,
            "product_name": product_name,
            "cutoff_time": offer.cutoff_time,
            "is_active": offer.is_active
        })
    return result

@router.post("", response_model=OfferRead, status_code=201)
def create_offer(data: OfferCreate, db: Session = Depends(get_db)):
    o = Offer(**data.model_dump())
    db.add(o); db.commit(); db.refresh(o)
    # enriquecer com o nome do produto
    product_name = db.query(Product.name).filter(Product.id == o.product_id).scalar() or ""
    return {
        "id": o.id,
        "product_id": o.product_id,
        "product_name": product_name,
        "cutoff_time": o.cutoff_time,
        "is_active": o.is_active,
    }
