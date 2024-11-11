from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from server.api.v1.stocks import router as stock_router
from server.core.logger import LogConfig
from server.core.settings import settings

# Configuração de logs
log_config = LogConfig()
log_config.build()


# Access the logger
logger = log_config.log
logger.info("Started Stock API Challenge!")

app = FastAPI(title=settings.PROJECT_NAME)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Registrando os endpoints
app.include_router(stock_router, prefix=settings.API_URI)
