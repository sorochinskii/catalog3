from typing import TYPE_CHECKING

from db.models.base import BaseCommon
from db.models.rooms import RoomsPersons
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.rooms import Room


class Person(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    rooms = relationship(
        'Room', secondary=RoomsPersons.__tablename__, lazy='joined'
    )
