from api.v1.endpoints.mfps import router_mfps
from api.v1.endpoints.users import router_users
from api.v1.endpoints.users_verify import router_verify
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
app.include_router(router_users)
app.include_router(router_verify)
app.include_router(router_mfps)
