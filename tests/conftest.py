import asyncio
import os
from typing import AsyncIterator, Generator

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from source.config import ENVIRONMENT, settings
from source.main import app

postgres = PostgresContainer('postgres:15.6-alpine3.19',
                             driver='asyncpg').with_bind_ports(5432, 47000)


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
