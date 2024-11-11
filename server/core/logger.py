import logging
from datetime import datetime
from enum import Enum
from logging import FileHandler, Logger, getLogger

from pytz import timezone
from rich.console import Console
from rich.logging import RichHandler

from server.core.settings import settings


class LogStatus(Enum):
    """Class Log Status, to represent enum used for LogConfig settings"""

    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class LogConfig:
    """Class Log Config"""

    def __init__(self) -> None:
        self._default_log_format: str = "%(levelname)s | %(name)s | %(asctime)s | %(message)s"
        self._simple_log_format: str = "%(message)s"
        self._logger_name: str = settings.PROJECT_NAME
        self._logger_level: str = settings.LOG_LEVEL
        self._timezone = timezone(settings.TIMEZONE)
        self.log: Logger
        self.console = Console()

    def _configure_log_level(self) -> int:
        """Function responsible to set a log level based on environment settings.
        Returns:
            int: Return a reference for log, based on logging library.
        """
        level_map = {
            LogStatus.DEBUG.value: logging.DEBUG,
            LogStatus.WARNING.value: logging.WARNING,
            LogStatus.ERROR.value: logging.ERROR,
            LogStatus.CRITICAL.value: logging.CRITICAL,
            LogStatus.INFO.value: logging.INFO,
        }
        return level_map.get(self._logger_level, logging.INFO)

    def _configure_logging(self) -> None:
        """Function responsible to set the log instance"""
        logging.Formatter.converter = lambda *args: datetime.now(tz=self._timezone).timetuple()

        # Rich handler for terminal output
        rich_handler = RichHandler(console=self.console, show_time=False, show_level=True, show_path=False)
        rich_handler.setFormatter(logging.Formatter(self._simple_log_format))

        # File handler for logging to file
        file_handler = FileHandler(f"{settings.BASE_DIR}/logs/app.log")
        file_handler.setFormatter(logging.Formatter(self._default_log_format))

        logging.basicConfig(
            level=self._configure_log_level(), format=self._simple_log_format, handlers=[rich_handler, file_handler]
        )
        self.log = getLogger(self._logger_name)

    def build(self) -> None:
        """Function responsible to construct the entire structure"""
        self._configure_logging()
