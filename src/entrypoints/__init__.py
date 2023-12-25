from entrypoints.games_router import router as games_router
from entrypoints.games_view import router as games_view
from entrypoints.health_router import router as health_router

from fastapi import APIRouter


all_views: tuple[APIRouter, ...] = (
    health_router,
    games_view,
    games_router,
)
