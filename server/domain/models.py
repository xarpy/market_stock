from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from server.domain import Base


class Stock(Base):
    """Stock database model"""

    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    purchased_amount = Column(Float)
    purchased_status = Column(String)
    request_data = Column(Date)
    company_code = Column(String, index=True)
    company_name = Column(String)
    stock_values = Column(JSONB)
    performance_data = Column(JSONB)
    competitors = Column(JSONB)
