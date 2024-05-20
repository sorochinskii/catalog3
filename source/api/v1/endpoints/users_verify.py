from apps.users import (
    auth_backend,
    current_active_user,
    fastapi_users,
    get_user_manager,
)
from db.models.users import User
from exceptions.http_exceptions import HttpExceptionsHandler
from fastapi import APIRouter, Body, Depends, Request, exceptions, status
from fastapi_users import BaseUserManager, models, schemas
from fastapi_users.router.common import ErrorCode, ErrorModel
from pydantic import EmailStr
from schemas.users_base import UserBaseSchemaIn, UserBaseSchemaOut, UserBaseSchemaUpdate

router_verify = APIRouter(prefix='/users')


@router_verify.post(
    "/request-verify-token",
    status_code=status.HTTP_202_ACCEPTED,
    name="verify:request-token",
    tags=["verify"]
)
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP,
                                  models.ID] = Depends(get_user_manager),
) -> None:
    with HttpExceptionsHandler():
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user, request)


@router_verify.post(
    "/verify",
    response_model=UserBaseSchemaOut,
    name="verify:verify",
    tags=["verify"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.VERIFY_USER_BAD_TOKEN: {
                            "summary": "Bad token, not existing user or"
                            "not the e-mail currently set for the user.",
                            "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                        },
                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                            "summary": "The user is already verified.",
                            "value": {
                                "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                            },
                        },
                    }
                }
            },
        }
    },
)
async def verify(
    request: Request,
    token: str = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP,
                                  models.ID] = Depends(get_user_manager),
):
    with HttpExceptionsHandler():
        user = await user_manager.verify(token, request)
        return schemas.model_validate(UserBaseSchemaOut, user)
