from buildings_base import BuildingBaseSchemaOut
from rooms_base import RoomBaseSchema, RoomBaseSchemaOut


class RoomSchema(RoomBaseSchema):
    ...


class RoomSchemaCreatedOut(RoomBaseSchema):
    building: BuildingBaseSchemaOut | None


class RoomSchemaUpdateOut(RoomSchemaCreatedOut):
    ...


class RoomSchemaOut(RoomBaseSchemaOut):
    building: BuildingBaseSchemaOut | None
