from core.app_factory import get_test_app

from fastapi import FastAPI

import pytest


@pytest.fixture
def app() -> FastAPI:
    return get_test_app(is_start_mappers=False)
