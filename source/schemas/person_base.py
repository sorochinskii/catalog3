from schemas.base import BaseSchema


class PersonBaseSchema(BaseSchema):
    name: str


class PersonBaseSchemaIn(PersonBaseSchema):
    ...


class PersonBaseSchemaOut(PersonBaseSchema):
    id: int
