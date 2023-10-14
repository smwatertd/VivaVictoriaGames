from fastapi import FastAPI

from views import all_views


def get_production_app() -> FastAPI:
    app = FastAPI()
    _include_views(app)
    return app


def _include_views(app: FastAPI) -> None:
    for router in all_views:
        app.include_router(router)
