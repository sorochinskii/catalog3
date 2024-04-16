from api.v1.endpoints.vendors import router_vendors
from config import ENVIRONMENT, settings
from fastapi import FastAPI

from .endpoints.buildings import router_buildings

tags_metadata = [
    {
        'name': 'v1',
        "description": "API version 1",
        'externalDocs': {
            'description': 'sub-docs',
            'url': f'http://{settings.HOST}:{settings.HTTP_PORT}/v1/docs'
        }
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router_buildings)
app.include_router(router_vendors)
