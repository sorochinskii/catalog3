import logging
import os
import sys

from api.v1.app import app as app_v1
from db.models.buildings import Building
from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API is starting up")

app = FastAPI(title="Catalog3")

app.mount("/v1", app_v1)

if __name__ == "__main__":
    path = os.getcwd()
    import uvicorn
    uvicorn.run("__main__:app", host="127.0.0.1", port=8845, reload=True,
                reload_dirs=['source'])
