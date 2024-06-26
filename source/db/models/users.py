from enum import Enum

from db.models.base import BaseCommon
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class RolesEnum(Enum):
    SUPERUSER = 'superuser'
    ADMIN = 'admin'


class User(SQLAlchemyBaseUserTable[int], BaseCommon):
    ...
