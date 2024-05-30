from db.models.base import BaseCommon
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Vendor(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    devices: Mapped[list['Device'] | None] = relationship(
        'MFP' or 'Cartridge',
        back_populates="vendor")
