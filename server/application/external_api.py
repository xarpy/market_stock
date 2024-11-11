import logging
from datetime import date
from typing import Any, Dict, Optional

from requests import Response, exceptions, request

from server.core.settings import Settings, settings

logger = logging.getLogger(__name__)


class PolygonClient:
    def __init__(self, verify_ssl: bool = False, context: Settings = settings) -> None:
        self._context = context
        self._verify_ssl = verify_ssl
        self._api_key = self._context.POLYGON_API_KEY
        self._uri = self._context.POLYGON_API_URI
        self._headers = {"Content-Type": "application/json"}

    def _build_request_information(self, id: str) -> Dict[Any, Any]:
        link = "{}/{}/{}?apiKey={}".format(self._uri, id.upper(), date.today(), self._api_key)
        result = {"url": link, "method": "GET"}
        return result

    def _log_error(self, error: Exception) -> None:
        if isinstance(error, exceptions.HTTPError):
            logger.error(f"HTTP error occurred: {error.response.status_code} - {error.response.text}")
        elif isinstance(error, exceptions.ConnectionError):
            logger.error("Error connecting to the server: %s", error)
        elif isinstance(error, exceptions.Timeout):
            logger.error("Timeout error: %s", error)
        elif isinstance(error, exceptions.RequestException):
            logger.error("An unknown error occurred during the request: %s", error)
        else:
            logger.error("An unexpected error occurred: %s", error)

    def _adjust_data(self, request_data):
        data = {"stock_values": {}}
        for key, value in request_data.items():
            if key in ["open", "high", "low", "close"]:
                data["stock_values"][key] = value
            else:
                data[key] = value
        return data

    def make_request(self, symbol: str) -> Optional[Response]:
        info = self._build_request_information(symbol)
        try:
            result = request(method=info["method"], url=info["url"], headers=self._headers, verify=self._verify_ssl)
            result.raise_for_status()
            return self._adjust_data(result.json())
        except exceptions.RequestException as error:
            self._log_error(error)
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
