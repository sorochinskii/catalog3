from schemas.vendors_base import VendorBaseSchema

from .device_base import DeviceBaseSchemaOut


class VendorSchema(VendorBaseSchema):
    ...


class VendorSchemaOut(VendorSchema):
    id: int
    devices: list[DeviceBaseSchemaOut]
