from typing import Literal

from pydantic import BaseModel


class HealthSchema(BaseModel):
    status: Literal['ok']


class GamesConnectionSchema(BaseModel):
    game_pk: int
    user_pk: int
    username: str


class CreateGameSchema(BaseModel):
    creator_id: int


class AvailableGame(BaseModel):
    id: int
