from schemas.buildings_base import BuildingBaseSchemaOut
from schemas.rooms_base import RoomBaseSchemaOut


class BuildingSchemaOut(BuildingBaseSchemaOut):
    rooms: list[RoomBaseSchemaOut] | None = None
