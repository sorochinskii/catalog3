from schemas.base import BaseSchema


class VendorBaseSchema(BaseSchema):
    name: str


class VendorBaseSchemaOut(VendorBaseSchema):
    id: int
