from api.v1.endpoints.vendors import router_vendors
from fastapi import FastAPI

from .endpoints.buildings import router_buildings

app = FastAPI()

app.include_router(router_buildings)
app.include_router(router_vendors)
