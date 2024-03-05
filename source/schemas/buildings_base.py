from schemas.base import BaseSchema


class BuildingBaseSchema(BaseSchema):
    name: str


class BuildingBaseSchemaOut(BuildingBaseSchema):
    id: int
