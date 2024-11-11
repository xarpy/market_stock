import secrets
import warnings
from pathlib import Path
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import AnyUrl, PostgresDsn, RedisDsn, computed_field, field_validator, model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)
    PROJECT_NAME: str = "stock-api"
    API_URI: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    LOG_LEVEL: Literal["DEBUG", "ERROR", "INFO", "WARNING", "CRITICAL"] = "DEBUG"
    TIMEZONE: str = "America/Sao_Paulo"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: Annotated[Union[List[AnyUrl], str], field_validator("BACKEND_CORS_ORIGINS")] = []
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432
    DB_DEBUG: bool = False
    REDIS_DB: int = 0
    REDIS_HOST: str = "localhost"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_PORT: int = 6379
    POLYGON_API_KEY: str
    POLYGON_API_URI: str = "https://api.polygon.io/v1/open-close"
    MARKETWATCH_URI: str = "https://www.marketwatch.com/investing/stock"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_DSN(self) -> RedisDsn:
        redis_url = f"redis://"
        if self.REDIS_PASSWORD:
            redis_url += f"{self.REDIS_PASSWORD}@"
        redis_url += f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return RedisDsn(redis_url)

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", ' "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @field_validator("BACKEND_CORS_ORIGINS")
    def parse_cors(cls, values: Union[str, List[str]]) -> List[str]:
        if isinstance(values, str):
            if values.startswith("["):
                return eval(values)
            else:
                return [i.strip() for i in values.split(",")]
        elif isinstance(values, list):
            return values
        raise ValueError(f"Invalid value for BACKEND_CORS_ORIGINS: {v}")

    @model_validator(mode="before")
    def parse_value(cls, values: Dict[Any, Any]) -> Dict[Any, Any]:
        if values.get("REDIS_PORT") and isinstance(values["REDIS_PORT"], str):
            values["REDIS_PORT"] = int(values["REDIS_PORT"])
        if values.get("POSTGRES_PORT") and isinstance(values["POSTGRES_PORT"], str):
            values["POSTGRES_PORT"] = int(values["POSTGRES_PORT"])
        if values.get("DB_DEBUG") and isinstance(values["DB_DEBUG"], str):
            db_debug = int(values["DB_DEBUG"])
            values["DB_DEBUG"] = bool(db_debug)
        return values

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        checklist = [
            "SECRET_KEY",
            "POSTGRES_PASSWORD",
            "POSTGRES_HOST",
            "POSTGRES_USER",
            "REDIS_HOST",
            "POLYGON_API_KEY",
        ]
        for key in checklist:
            self._check_default_secret(key, getattr(self, key))
        return self


settings = Settings()  # type: ignore
