from datetime import datetime

from schemas.base import BaseSchema


class DeviceBaseSchema(BaseSchema):
    serial: str
    type: str


class MFPBaseSchemaOut(DeviceBaseSchema):
    id: int
    created: datetime
    updated: datetime
