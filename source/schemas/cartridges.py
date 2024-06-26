from .cartridges_base import CartridgeBaseSchemaOut, ModelBaseSchemaOut
from .printer_base import PrinterBaseSchemaOut
from .vendors_base import VendorBaseSchemaOut


class ModelSchemaOut(ModelBaseSchemaOut):
    vendor: VendorBaseSchemaOut
    alternatives: list[ModelBaseSchemaOut]
    cartridges: list[CartridgeBaseSchemaOut]


class CartridgeSchemaOut(CartridgeBaseSchemaOut):
    model: ModelBaseSchemaOut
    printers: list[PrinterBaseSchemaOut]
