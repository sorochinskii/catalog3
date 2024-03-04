from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.db.base import BaseCommon


class Building(BaseCommon):
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    rooms: Mapped[list["Room"] | None] = relationship(
        back_populates="building")
