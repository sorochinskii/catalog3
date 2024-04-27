from datetime import datetime

from pydantic import UUID4, Field, validator
from schemas.users_base import UserBaseSchemaOut

from .base import BaseSchema


class TokenBase(BaseSchema):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: str | None = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class UserSchemaOut(UserBaseSchemaOut):
    token: TokenBase = {}
