from buildings_base import BuildingBaseSchemaOut

from source.apps.rooms.schemas_base import RoomBaseSchemaOut


class BuildingSchemaOut(BuildingBaseSchemaOut):
    rooms: list[RoomBaseSchemaOut] | None = None
