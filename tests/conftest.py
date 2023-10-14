from core.app_factory import get_production_app

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return get_production_app()


@pytest.fixture(scope='session')
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='class', autouse=True)
def class_client(request: pytest.FixtureRequest, client: TestClient) -> None:
    request.cls.client = client
