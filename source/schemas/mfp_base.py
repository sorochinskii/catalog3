from datetime import datetime

from schemas.base import BaseSchema


class MFPBaseSchema(BaseSchema):
    serial: str


class MFPBaseSchemaOut(MFPBaseSchema):
    id: int
    type: str
    created: datetime
    updated: datetime
