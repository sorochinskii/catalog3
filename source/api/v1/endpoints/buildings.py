from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from source.schemas.buildings import BuildingSchemaOut
from source.schemas.buildings_base import BuildingBaseSchema

router_buildings = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
)
