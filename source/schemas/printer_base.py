from datetime import datetime

from schemas.base import BaseSchema
from schemas.device_base import DeviceBaseSchema


class PrinterBaseSchema(DeviceBaseSchema):
    cartridge_model_id: int | None = None


class PrinterBaseSchemaOut(PrinterBaseSchema):
    id: int


class PrinterBaseSchemaIn(PrinterBaseSchema):
    ...
