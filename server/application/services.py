import logging
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from server.application.external_api import PolygonClient
from server.application.scraper import MarketWatchScraper
from server.core.cache import Cache
from server.core.exceptions import CacheError, ServiceError
from server.domain.repositories import StockRepository
from server.domain.schemas import StockModel

logger = logging.getLogger("my_logger")


class StockService:
    def __init__(self, session: Session):
        self._session = session
        self._scraper = MarketWatchScraper(True)
        self._external_client = PolygonClient()
        self._repository = StockRepository(self._session)
        self._cache = Cache()  # Cache de 1 hora (3600 segundos)
        self._cache_key = ""

    def _retrieve_data(self, stock_symbol: str) -> Optional[dict]:
        try:
            data = self._cache.get_cache(self._cache_key)
            if data:
                return data
        except CacheError:
            logger.error(f"Cache data for {stock_symbol} is invalid: {e}")

    def get_stock_info(self, stock_symbol: str) -> Optional[StockModel]:
        self._cache_key = f"stock_data:{stock_symbol}"
        try:
            data = self._retrieve_data(stock_symbol)
            if not data:
                external_data = self._external_client.make_request(stock_symbol)
                scraping_data = self._scraper.run(stock_symbol)
                if external_data and scraping_data:
                    scraping_data.update(**external_data)
                    self._cache.set_cache(self._cache_key, scraping_data)
                    result = self._repository.create_or_update_stock(data)
                    data = result["stock"]
            return data
        except ServiceError as error:
            logger.exception(error)

    def update_stock_amount(self, stock_data: Dict[Any, Any]):
        msg = {"message": ""}
        try:
            result = self._repository.create_or_update_stock(stock_data)
            if result.get("updated"):
                stock = result["stock"]
                msg["message"] = (
                    f"{stock.purchased_amount} units of stock {stock.company_code} were added to your stock record"
                )
            else:
                msg["message"] = "Stock not found"
            return msg
        except Exception as error:
            logger.exception(error)
