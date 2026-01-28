from fastapi import FastAPI
from app.api.routes import router
from app.config import init_store

init_store(capacity=100)

app = FastAPI()

app.include_router(router)