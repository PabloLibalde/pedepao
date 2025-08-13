from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.window import Window
from app.schemas.window import WindowCreate, WindowRead

router = APIRouter(prefix="/windows", tags=["windows"])

@router.get("", response_model=list[WindowRead])
def list_windows(db: Session = Depends(get_db)):
    return db.query(Window).order_by(Window.name).all()

@router.post("", response_model=WindowRead, status_code=201)
def create_window(data: WindowCreate, db: Session = Depends(get_db)):
    w = Window(**data.model_dump())
    db.add(w); db.commit(); db.refresh(w)
    return w
