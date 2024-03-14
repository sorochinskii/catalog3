from db.models.base import BaseCommon
from sqlalchemy.orm import Mapped, mapped_column


class Vendor(BaseCommon):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
