from sqlalchemy.orm import Mapped, mapped_column

from source.db.base import BaseCommon


class Vendor(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
