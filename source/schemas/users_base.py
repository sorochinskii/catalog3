from typing import Generic

from fastapi_users import models
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import ConfigDict, EmailStr
from pydantic.version import VERSION as PYDANTIC_VERSION
from schemas.base import OptionalFieldsMixin

PYDANTIC_V2 = PYDANTIC_VERSION.startswith('2.')


class BaseUser(CreateUpdateDictModel, Generic[models.ID],
               OptionalFieldsMixin):
    '''Base User model.'''

    id: models.ID
    email: EmailStr
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover

        class Config:
            orm_mode = True


class OptionalBaseUser(BaseUser.optional_fields()):
    def update(self, data: dict):
        update = self.model_dump()
        update.update(data)
        for k, v in self.model_validate(update).model_dump(exclude_defaults=True).items():
            setattr(self, k, v)
        return self


class BaseUserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str


class BaseUserUpdate(CreateUpdateDictModel):
    password: str | None = None
    email: EmailStr | None = None


class UserBaseSchemaIn(BaseUserCreate):
    ...


class UserBaseSchemaOut(BaseUser):
    ...


class UserBaseSchemaUpdate(BaseUser):
    ...
