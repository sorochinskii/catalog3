from crud_router.router_generator import RouterGenerator
from db.db import async_session_maker
from db.models.mfp import MFP
from db.sa_crud import CRUDSA
from schemas.mfp_base import MFPBaseSchemaIn, MFPBaseSchemaOut

router_mfps = RouterGenerator(
    prefix='/mfps',
    db_crud=CRUDSA(model=MFP, async_session=async_session_maker),
    db=async_session_maker,
    schema_basic_out=MFPBaseSchemaOut,
    schema_create=MFPBaseSchemaIn,
    route_get_all=True,
    route_get_by_id=True,
    route_create=True,
    route_delete=True
)
