from fastapi import FastAPI

from aleph_balance.db import engine
from aleph_balance.models import Base
from .endpoints.balance import router as balance_router

app = FastAPI()

app.include_router(balance_router)


@app.on_event("startup")
async def startup():
    # Create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
