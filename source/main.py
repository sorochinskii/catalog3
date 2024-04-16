from api.v1.app import app as app_v1
from config import ENVIRONMENT, settings
from fastapi import FastAPI
from logger import logger
from middlewares.logging_process_time import x_process_time_header
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title='Catalog3')

if ENVIRONMENT != 'prod':
    app.add_middleware(BaseHTTPMiddleware,
                       dispatch=x_process_time_header)

app.mount('/v1', app_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('__main__:app',
                host=f'{settings.HOST}',
                port=settings.HTTP_PORT,
                reload=True,
                reload_dirs=['source'],
                log_level='debug')
