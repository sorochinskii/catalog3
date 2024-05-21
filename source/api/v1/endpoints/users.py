
from apps.users_dependencies import auth_backend, current_active_user, fastapi_users
from db.models.users import User
from fastapi import APIRouter, Depends
from schemas.users_base import UserBaseSchemaIn, UserBaseSchemaOut, UserBaseSchemaUpdate

router_users = APIRouter(prefix='/users')

router_users.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

router_users.include_router(
    fastapi_users.get_register_router(
        user_schema=UserBaseSchemaOut,
        user_create_schema=UserBaseSchemaIn),
    prefix='/auth',
    tags=['auth'],
)

router_users.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)


router_users.include_router(
    fastapi_users.get_users_router(
        user_schema=UserBaseSchemaOut,
        user_update_schema=UserBaseSchemaUpdate),
    tags=['users'],
)


@router_users.get('/authenticated-route')
async def authenticated_route(user: User = Depends(current_active_user)):
    return {'message': f'Hello {user.email}!'}
