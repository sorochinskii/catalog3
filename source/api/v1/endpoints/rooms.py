from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

router_buildings = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
)
