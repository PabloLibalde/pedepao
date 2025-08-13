# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..schemas import UserCreate, Token
from ..models import User
from ..auth import (
    get_db,
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_admin,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------- helpers ----------
def _authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

# ---------- LOGIN via FORM (Swagger Authorize) ----------
@router.post("/login", response_model=Token)
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Aceita application/x-www-form-urlencoded (username/password) — usado pelo Swagger Authorize.
    """
    user = _authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

# ---------- LOGIN via JSON (opcional) ----------
class LoginJSON(BaseModel):
    email: EmailStr
    password: str

@router.post("/login_json", response_model=Token)
def login_json(body: LoginJSON, db: Session = Depends(get_db)):
    """
    Aceita JSON: { "email": "...", "password": "..." }.
    """
    user = _authenticate_user(db, body.email, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

# ---------- INFO do usuário ----------
@router.get("/me")
def me(current = Depends(get_current_user)):
    return {"email": current.email, "full_name": current.full_name, "is_admin": current.is_admin}

# ---------- CRIAR USUÁRIO (somente admin) ----------
@router.post("/users", dependencies=[Depends(require_admin)])
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email já cadastrado")
    user = User(
        email=body.email,
        full_name=body.full_name,
        password_hash=hash_password(body.password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    return {"id": user.id}
