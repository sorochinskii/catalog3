from typing import Generator

import pytest
from source.main import app
from starlette.testclient import TestClient


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
