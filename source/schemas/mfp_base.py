from datetime import datetime

from schemas.base import BaseSchema
from schemas.printer_base import PrinterBaseSchema


class MFPBaseSchema(PrinterBaseSchema):
    ...


class MFPBaseSchemaOut(MFPBaseSchema):
    id: int
    type: str
    created: datetime


class MFPBaseSchemaIn(MFPBaseSchema):
    ...
