from datetime import date
from typing import List

from pydantic import BaseModel, model_validator


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

    @model_validator(mode="before")
    def formatted_fields(cls, values) -> dict:
        if "amount" in values.keys():
            values["purchased_amount"] = values["amount"]
        elif "status" in values.keys():
            values["purchased_status"] = values["status"]
        return values

    class Config:
        from_attributes = True
