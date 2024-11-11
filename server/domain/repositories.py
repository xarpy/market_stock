from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session

from server.domain import BaseRepository
from server.domain.models import Stock


class StockRepository(BaseRepository):
    """StockRepository class"""

    def __init__(self, session: Session) -> None:
        self.model = Stock
        super().__init__(session)

    def get_stock_by_symbol(self, symbol: str) -> Row | None:
        """_summary_

        Args:
            symbol (str): _description_

        Returns:
            Row | None: _description_
        """
        query = select(self.model).where(Stock.company_code == symbol)
        result = self.session.execute(query).first()
        return result

    def create_or_update_stock(self, stock_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """_summary_

        Args:
            stock_data (Dict[Any, Any]): _description_

        Returns:
            Dict[Any, Any]: _description_
        """
        result = {"updated": False}
        stock = self.get_stock_by_symbol(stock_data["company_code"])
        if stock:
            result["updated"] = True
            stock.purchased_amount = stock_data["purchased_amount"]
            stock.purchased_status = stock_data["purchased_status"]
        else:
            stock = self.model(**stock_data)
            self.session.add(stock)
        self.session.commit()
        self.session.refresh(stock)
        result["stock"] = stock
        return result
