from entrypoints import all_views

from fastapi import FastAPI

# from infrastructure.adapters.entities import start_mappers


def get_production_app() -> FastAPI:
    app = FastAPI()
    _include_views(app)
    # start_mappers()
    return app


def _include_views(app: FastAPI) -> None:
    for router in all_views:
        app.include_router(router)
