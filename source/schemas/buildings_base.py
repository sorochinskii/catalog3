from source.apps.schemas import BaseSchema


class BuildingBaseSchema(BaseSchema):
    name: str


class BuildingBaseSchemaOut(BuildingBaseSchema):
    id: int
