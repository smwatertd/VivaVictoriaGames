from contextlib import contextmanager
from typing import Generator

from entrypoints import all_views

from fastapi import FastAPI

from infrastructure.adapters.entities import start_mappers, stop_mappers


def get_production_app() -> FastAPI:
    app = _get_app()
    start_mappers()
    return app


@contextmanager
def get_test_app(is_start_mappers: bool) -> Generator[FastAPI, None, None]:
    app = _get_app()
    if is_start_mappers:
        start_mappers()
    yield app
    if is_start_mappers:
        stop_mappers()


def _get_app() -> FastAPI:
    app = FastAPI()
    _include_views(app)
    return app


def _include_views(app: FastAPI) -> None:
    for router in all_views:
        app.include_router(router)
