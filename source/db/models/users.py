from db.models.base import BaseCommon, created_at, updated_at

# from db.models.tokens import Token
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(BaseCommon):
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[bool] = mapped_column(
        nullable=False, default=False)
    token: Mapped['Token'] = relationship(back_populates='user', uselist=False)
