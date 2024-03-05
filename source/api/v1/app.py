from fastapi import FastAPI

from .endpoints.buildings import router_buildings

app = FastAPI()

app.include_router(router_buildings)
