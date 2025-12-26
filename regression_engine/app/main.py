from logging.config import dictConfig
from app.core.logging import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(title="Regression Engine")

app.include_router(router, prefix="/api")

