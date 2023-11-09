from typing import Literal

from pydantic import BaseModel


class HealthSchema(BaseModel):
    status: Literal['ok']


class GamesConnectionSchema(BaseModel):
    game_pk: int
    user_pk: int
    username: str
