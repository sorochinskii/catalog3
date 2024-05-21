from typing import Optional

from apps.utils import EmailSender, RenderMessage
from config import settings
from db.models.users import User
from exceptions.http_exceptions import HTTPObjectNotExist
from exceptions.smtp_exception_handler import SmtpErrorHandler
from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin, InvalidPasswordException
from schemas.users_base import UserBaseSchemaIn


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
            protocol=settings.HTTP_PROTOCOL,
            port=settings.HTTP_PORT,
            host=settings.HOST,
            api_v=settings.V1,
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
