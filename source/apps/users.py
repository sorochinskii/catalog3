from typing import Optional

from apps.utils import EmailSender, RenderMessage
from config import settings
from db.db import get_async_session
from db.models.users import User
from exceptions.http_exceptions import HTTPObjectNotExist
from exceptions.smtp_exception_handler import SmtpErrorHandler
from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from schemas.users_base import UserBaseSchemaIn
from sqlalchemy.ext.asyncio import AsyncSession


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def on_after_register(self, user: User,
                                request: Optional[Request] = None):
        ...

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        ...

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        if not token:
            raise HTTPObjectNotExist
        verification_message = RenderMessage(
            templates_dir=settings.TEMPLATES_DIR,
            template=settings.TEMPLATE_VERIFICATION)
        subject = 'Verification message'
        message = verification_message.message(
            subject=subject,
            token=token)

        email = EmailSender(smtp_server=settings.SMTP_SERVER,
                            smtp_port=settings.SMTP_PORT,
                            sender=settings.SENDER_EMAIL,
                            sender_password=settings.SENDER_PASSWORD,
                            recepient=user.email)
        with SmtpErrorHandler():
            email.send(message=message)

    async def validate_password(
        self,
        password: str,
        user: UserBaseSchemaIn,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason='Password should be at least 8 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET,
                       lifetime_seconds=settings.TOKEN_LIFETIME)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase =
                           Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
