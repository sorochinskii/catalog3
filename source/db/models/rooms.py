from typing import TYPE_CHECKING

from db.models.base import BaseCommon

# from db.models.buildings import Building
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.buildings import Building
    from db.models.persons import Person


class RoomsPersons(BaseCommon):
    rooms_id = mapped_column("Room", ForeignKey("room.id"), primary_key=True)
    persons_id = mapped_column("Person", ForeignKey("person.id"), primary_key=True)


class Room(BaseCommon):

    __table_args__ = (UniqueConstraint("building_id", "name"),)

    name = mapped_column(String, nullable=False, unique=True)
    building_id = mapped_column(ForeignKey("building.id"))
    building: Mapped["Building"] = relationship(back_populates="rooms", lazy="joined")
    persons: Mapped["Person"] = relationship(
        secondary=RoomsPersons.__tablename__, back_populates="rooms", lazy="joined"
    )
