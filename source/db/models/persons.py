from db.models.base import BaseCommon
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Person(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    rooms = relationship(
        "Room", secondary="rooms_persons", back_populates="persons", lazy="joined"
    )
