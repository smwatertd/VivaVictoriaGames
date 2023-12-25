from entrypoints.games_router import router as games_router
from entrypoints.games_view import router as games_view
from entrypoints.health_view import router as health_view

from fastapi import APIRouter


all_views: tuple[APIRouter, ...] = (
    health_view,
    games_view,
    games_router,
)
