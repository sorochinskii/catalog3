from crud_db_v1.sa_crud import CRUDSA
from crud_router.router_generator import RouterGenerator
from db.models.mfp import MFPNetwork
from schemas.mfp_base import MFPBaseSchema, MFPBaseSchemaOut

router_mfps = RouterGenerator(
    prefix='/mfps',
    db_crud=CRUDSA(model=MFPNetwork),
    schema_basic_out=MFPBaseSchemaOut,
    schema_create=MFPBaseSchema,
    route_get_all=True,
    route_get_by_id=True,
    route_create=True,
    route_delete=True
)
