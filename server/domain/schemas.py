from datetime import date
from typing import List

from pydantic import BaseModel, field_validator


class StockRequest(BaseModel):
    amount: float


class StockValues(BaseModel):
    open: float
    high: float
    low: float
    close: float


class PerformanceData(BaseModel):
    five_days: float
    one_month: float
    three_months: float
    year_to_date: float
    one_year: float


class MarketCap(BaseModel):
    currency: str
    value: float


class Competitor(BaseModel):
    name: str
    market_cap: MarketCap


class StockModel(BaseModel):
    status: str
    purchased_amount: float
    purchased_status: str
    request_data: date
    company_code: str
    company_name: str
    stock_values: StockValues
    performance_data: PerformanceData
    competitors: List[Competitor]

    @field_validator("request_data", mode="before")
    def convert_date_to_string(cls, v):
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")
        return v

    class Config:
        from_attributes = True
