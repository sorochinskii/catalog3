import asyncio
from typing import AsyncIterator, Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi import status
from httpx import AsyncClient
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from source.config import settings
from source.main import app
from source.schemas.users_base import (
    BaseUser,
    BaseUserCreate,
    OptionalBaseUser,
    UserBaseSchemaOut,
)

postgres = PostgresContainer('postgres:15.6-alpine3.19',
                             driver='asyncpg').with_bind_ports(5432, 47000)


class UserCreateFactory(ModelFactory[BaseUserCreate]):
    __model__ = BaseUserCreate


class UserOutFactory(ModelFactory[UserBaseSchemaOut]):
    __model__ = UserBaseSchemaOut


def run_migrations(dsn: str) -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', 'migrations')
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def credits() -> BaseUserCreate:
    credits = UserCreateFactory.build()
    return credits


@pytest.fixture(scope='session')
def user_info() -> OptionalBaseUser:
    user = OptionalBaseUser(
        **{'id': None, 'email': None, 'is_active': None,
           'is_superuser': None, 'is_verified': None})
    return user


@pytest.fixture(scope='session')
async def user_created(test_client: AsyncClient, credits) -> BaseUser:
    user_create = await test_client.post(
        '/v1/users/auth/register', json=credits.model_dump())
    assert user_create.status_code == status.HTTP_201_CREATED
    return BaseUser(**user_create.json())


@pytest.fixture
def test_client_() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
# def pytest_sessionstart(session):


@pytest.fixture(scope='session', autouse=True)
def setup():
    db = postgres.start()
    run_migrations(settings.DB_URL)


# @pytest.fixture
def pytest_sessionfinish(session, exitstatus):
    postgres.stop()
