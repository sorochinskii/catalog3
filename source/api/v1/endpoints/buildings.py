from fastapi import APIRouter, Depends
from schemas.buildings import BuildingSchemaOut
from schemas.buildings_base import BuildingBaseSchema
from sqlalchemy import select
from sqlalchemy.orm import joinedload

router_buildings = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
)
