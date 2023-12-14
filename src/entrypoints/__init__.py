from entrypoints.games_view import router as games_view
from entrypoints.health_view import router as health_view

from fastapi import APIRouter


all_views: tuple[APIRouter, ...] = (
    health_view,
    games_view,
)
