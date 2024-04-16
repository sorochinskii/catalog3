from crud_db_v1.sa_crud import CRUDSA
from crud_router.router_generator import RouterGenerator
from db.models.vendors import Vendor
from fastapi import APIRouter, Depends
from schemas.vendors import VendorSchema
from schemas.vendors_base import VendorBaseSchema, VendorBaseSchemaOut

router_vendors = RouterGenerator(
    prefix='/vendors',
    db_crud=CRUDSA(model=Vendor),
    schema_basic_out=VendorBaseSchemaOut,
    schema_create=VendorBaseSchema,
    schema_update=VendorSchema,
    route_get_all=True,
    route_get_by_id=True,
    route_create=True,
    route_update=True,
    route_delete=True
)
