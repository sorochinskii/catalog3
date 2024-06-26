from db.models.vendors import Vendor
from db.sa_crud import CRUDSA
from fastapi import APIRouter, Depends
from schemas.buildings import BuildingSchemaOut
from schemas.buildings_base import BuildingBaseSchema

router_buildings = APIRouter(
    prefix="/buildings",
    tags=["buildings"]
)
