from fastapi import APIRouter

from server.api.v1 import stocks

router = APIRouter()
router.include_router(stocks.router, prefix="stock", tags=["stock"])
