from db.models.base import BaseCommon
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable[int], BaseCommon):
    ...
