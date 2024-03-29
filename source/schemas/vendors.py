from schemas.base import BaseSchema
from schemas.vendors_base import VendorBaseSchema


class VendorSchema(VendorBaseSchema):
    ...


class VendorSchemaOut(VendorSchema):
    id: int
