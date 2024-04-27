from pydantic import EmailStr
from schemas.base import BaseSchema


class UserBaseSchema(BaseSchema):
    email: EmailStr
    name: str


class UserBaseSchemaOut(UserBaseSchema):
    id: int
