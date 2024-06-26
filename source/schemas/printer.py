
from schemas.cartridges_base import ModelBaseSchemaOut
from schemas.printer_base import PrinterBaseSchemaOut


class PrinterSchemaOut(PrinterBaseSchemaOut):
    cartridge_model: ModelBaseSchemaOut
