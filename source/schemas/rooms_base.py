from base import BaseSchema


class RoomBaseSchema(BaseSchema):
    name: str
    building_id: int | None = None


class RoomBaseSchemaOut(RoomBaseSchema):
    id: int
