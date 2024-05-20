from unittest.mock import Mock

from fastapi import status
from httpx import AsyncClient

from source.schemas.users_base import BaseUserCreate, OptionalBaseUser


async def test_user_create(test_client: AsyncClient,
                           credits: BaseUserCreate,
                           user_info: OptionalBaseUser):
    user_create = await test_client.post(
        '/v1/users/auth/register', json=credits.model_dump())
    assert user_create.status_code == status.HTTP_201_CREATED
    user_info.update(user_create.json())


async def test_verify_user(mocker: Mock,
                           test_client: AsyncClient,
                           user_info: OptionalBaseUser):
    smtp_module = "source.apps.utils.smtplib.SMTP_SSL"
    mock_smtp = mocker.MagicMock(name=smtp_module)
    mocker.patch(smtp_module, new=mock_smtp)
    send_message = "apps.users.RenderMessage.message"
    mock_send = mocker.MagicMock(name=send_message)
    mocker.patch(send_message, new=mock_send)

    verify_data = {'email': user_info.email}
    response_verify_token = await test_client.post(
        '/v1/users/request-verify-token',
        json=verify_data)
    assert response_verify_token.status_code == status.HTTP_202_ACCEPTED

    token = mock_send.call_args.kwargs
    response_verified = await test_client.post('/v1/users/verify',
                                               json=token)
    assert response_verified.json().get('is_verified') == True


async def test_user_login(test_client: AsyncClient,
                          credits: BaseUserCreate,
                          user_info: dict):
    login_data = {'username': credits.model_dump().get('email'),
                  'password': credits.model_dump().get('password')}
    get_access_token = await test_client.post('/v1/users/auth/jwt/login',
                                              data=login_data)
    assert get_access_token.status_code == status.HTTP_200_OK
