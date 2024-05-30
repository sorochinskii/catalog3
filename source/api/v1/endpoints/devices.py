from crud_db_v1.sa_crud import CRUDSA
from crud_router.router_generator import RouterGenerator
from db.models.devices import Device

# from schemas.devices import VendorSchema
# from schemas.devices_base import VendorBaseSchema, VendorBaseSchemaOut

# router_vendors = RouterGenerator(
#     prefix='/devices',
#     db_crud=CRUDSA(model=Device),
#     schema_basic_out=DeviceBaseSchemaOut,
#     schema_create=DeviceBaseSchema,
#     route_get_all=True,
#     route_get_by_id=True,
#     route_create=True,
#     route_delete=True
# )
