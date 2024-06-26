from schemas.base import BaseSchema
from schemas.device_base import DeviceBaseSchema


class CartridgeBaseSchema(DeviceBaseSchema):
    model_id: int


class CartridgeBaseSchemaOut(CartridgeBaseSchema):
    id: int


class ModelBaseSchema(BaseSchema):
    name: str
    vendor_id: int | None = None
    is_original: bool = False
    original_id: int | None = None


class ModelBaseSchemaOut(ModelBaseSchema):
    id: int


class ModelBaseSchemaIn(ModelBaseSchema):
    ...
