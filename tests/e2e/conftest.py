from typing import Generator

from core.app_factory import get_test_app

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from tests.e2e.api_client import APIClient


@pytest.fixture
def app() -> Generator[FastAPI, None, None]:
    with get_test_app(is_start_mappers=True) as app:
        yield app


@pytest.fixture
def client(app: FastAPI) -> APIClient:
    return APIClient(client=TestClient(app))
