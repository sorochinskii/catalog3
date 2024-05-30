from typing import TYPE_CHECKING

from db.models.base import BaseCommon
from db.models.rooms import RoomsPersons
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.devices import Device
    from db.models.rooms import Room


class Person(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    rooms: Mapped[list['Room']] = relationship(
        secondary=RoomsPersons.tablename())
    devices_responsibility: Mapped[list['Device']] = relationship(
        back_populates='responsible_person')
