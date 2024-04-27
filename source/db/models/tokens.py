from datetime import datetime
from uuid import UUID

from db.models.base import BaseCommon
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Token(BaseCommon):
    token: Mapped[UUID] = mapped_column(
        nullable=False, server_default=text("gen_random_uuid()"), unique=True)
    expires: Mapped[datetime]
    user: Mapped['User'] = relationship(back_populates='token')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
