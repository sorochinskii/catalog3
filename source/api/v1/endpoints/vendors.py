from crud_db_v1.sqlalchemy import CRUDSA
from crud_router.router_generator import RouterGenerator
from db.models.vendors import Vendor
from fastapi import APIRouter
from schemas.vendors_base import VendorBaseSchemaOut

router_vendors = RouterGenerator(
    prefix='/vendors',
    db_crud=CRUDSA(model=Vendor),
    schema_basic_out=VendorBaseSchemaOut,
    route_get_all=True
)
