from fastapi import FastAPI
from app.core.lifecycle import lifespan
from app.core.config import settings
from app.api.routes import products, orders, windows

app = FastAPI(title=settings.api_name, lifespan=lifespan)
app.include_router(products.router, prefix=settings.api_base_path)
app.include_router(orders.router, prefix=settings.api_base_path)
app.include_router(windows.router, prefix=settings.api_base_path)

@app.get("/health")
def health():
    return {"status": "ok"}
