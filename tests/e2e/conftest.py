from core.app_factory import get_production_app

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from tests.e2e.api_client import APIClient


@pytest.fixture
def app() -> FastAPI:
    return get_production_app()


@pytest.fixture
def client(app: FastAPI) -> APIClient:
    return APIClient(client=TestClient(app))
