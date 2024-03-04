from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from source.db.utils import split_and_concatenate


class Base(DeclarativeBase):
    ...


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        result = split_and_concatenate(cls.__name__)
        return result


class BaseCommon(Base, TableNameMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    class Config:
        from_attributes = True
