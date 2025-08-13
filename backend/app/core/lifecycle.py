from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # inicializações (cache/httpx/telemetria) poderiam entrar aqui
    yield
    # finalizações/cleanup
