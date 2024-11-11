from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.application.services import StockService
from server.core.database import get_db
from server.domain.schemas import StockRequest

router = APIRouter()


@router.get("/stock/{stock_symbol}")
def get_stock(stock_symbol: str, session: Session = Depends(get_db)):
    service = StockService(session)
    response = service.get_stock_info(stock_symbol)
    if not response:
        raise HTTPException(status_code=404, detail="Stock data not found")
    return response


@router.post("/stock/{stock_symbol}")
def add_stock_amount(stock_symbol: str, request: StockRequest, session: Session = Depends(get_db)):
    service = StockService(session)
    stock_data = {"company_code": stock_symbol, "purchased_amount": request.amount}
    response = service.update_stock_amount(stock_data)
    if not response:
        raise HTTPException(status_code=404, detail="Stock data not found")
    return response
