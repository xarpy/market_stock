import logging
from datetime import timedelta
from functools import wraps
from json import dumps, loads
from typing import Callable, Optional

from redis import AuthenticationError
from redis.client import Redis

from server.core.exceptions import CacheError
from server.core.settings import Settings, settings

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, cache_expire=3600, context: Settings = settings) -> None:
        self.client = Redis
        self._context = context
        self.cache_expire = cache_expire

    def _connect(self) -> Redis:
        try:
            client = self.client.from_url(self._context.REDIS_DSN.unicode_string())
            if client.ping() is True:
                return client
        except AuthenticationError:
            error_msg = "Authentication error while connecting to Redis."
            logger.exception(error_msg)
            raise CacheError(error_msg)

    def get_cache(self, key: str) -> Optional[dict]:
        result = None
        client = self._connect()
        value = client.get(key)
        if value:
            result = loads(value)
        return result

    def set_cache(self, key: str, value: dict) -> bool:
        client = self._connect()
        result = client.setex(key, timedelta(seconds=self.cache_expire), dumps(value))
        return bool(result)

    def cache(self, key: str) -> Callable:
        """Decorator for caching function results."""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                cached_value = self.get_cache(key)
                if cached_value:
                    logger.info(f"Cache hit for key: {key}")
                    return cached_value
                result = func(*args, **kwargs)
                self.set_cache(key, result)
                logger.info(f"Cache miss for key: {key}. Setting cache.")
                return result

            return wrapper

        return decorator
