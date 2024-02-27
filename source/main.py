import logging
import sys

from api.v1.app import app as app_v1
from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('API is starting up')

app = FastAPI(title='Catalog')

app.mount('/v1', app_v1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8846)
