import os
from sys import stderr

from api.v1.app import app as app_v1
from config import ENVIRONMENT, settings
from fastapi import Depends, FastAPI
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from source.middlewares.logging_process_time import x_process_time_header

app = FastAPI(title="Catalog3")

if ENVIRONMENT != 'prod':
    app.add_middleware(BaseHTTPMiddleware,
                       dispatch=x_process_time_header)

app.mount("/v1", app_v1)

logger.remove()

logger.add(f'{settings.LOG_DIR}/debug/' + '{time:YYYY_MM_DD}',
           filter=lambda record: record["level"].name == "DEBUG", format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}")

logger.add(f'{settings.LOG_DIR}/info/' + '{time:YYYY_MM_DD}',
           filter=lambda record: record["level"].name == "INFO")

logger.add(f'{settings.LOG_DIR}/error/' + '{time:YYYY_MM_DD}',
           filter=lambda record: record["level"].name == "ERROR")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app",
                host="127.0.0.1",
                port=8845,
                reload=True,
                reload_dirs=['source'],
                log_level='debug')
