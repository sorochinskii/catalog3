from crud_router.router_generator import RouterGenerator
from db.models.printers import Printer
from db.sa_crud import CRUDSA
from schemas.printer import PrinterSchemaOut

router_printers = RouterGenerator(
    prefix='/printers',
    db_crud=CRUDSA(model=Printer),
    schema_basic_out=PrinterSchemaOut,
    route_get_all=True,
    route_get_by_id=True,
)
