import uvicorn
from fastapi import FastAPI

from app.api.views import router as wallet_router

app = FastAPI()

app.include_router(wallet_router)
