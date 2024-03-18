from typing import TYPE_CHECKING

from db.models.base import BaseCommon
from db.models.rooms import Room
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.rooms import Room


class Building(BaseCommon):
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    rooms: Mapped[list["Room"] | None] = relationship(
        back_populates="building", cascade="all, delete")
