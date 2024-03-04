from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.db.base import BaseCommon


class Person(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
