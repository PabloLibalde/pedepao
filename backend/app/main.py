from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, offers, orders, reports, health
from .config import settings
from sqlalchemy import inspect
from .db import SessionLocal, engine
from .models import User
from .auth import hash_password
from .config import settings

# imports para seed:
from .db import SessionLocal
from .models import User
from .auth import hash_password

app = FastAPI(
    title="PedePao API",
    # opcional: docs_url="/swagger", redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def ensure_default_admin():
    if not settings.AUTO_SEED_ADMIN:
        return
    # Verifica se as tabelas existem (especialmente 'users')
    insp = inspect(engine)
    if not insp.has_table("users"):
        # Migrações ainda não aplicadas — não falha o startup
        return

    db = SessionLocal()
    try:
        u = db.query(User).filter(User.email == settings.DEFAULT_ADMIN_EMAIL).first()
        if not u:
            u = User(
                email=settings.DEFAULT_ADMIN_EMAIL,
                full_name=settings.DEFAULT_ADMIN_FULLNAME,
                password_hash=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
                is_admin=True,
            )
            db.add(u)
            db.commit()
    finally:
        db.close()

app.include_router(health.router)
app.include_router(users.router)
app.include_router(offers.router)
app.include_router(orders.router)
app.include_router(reports.router)
