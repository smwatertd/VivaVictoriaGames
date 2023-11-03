from typing import Literal

from pydantic import BaseModel


class HealthSchema(BaseModel):
    status: Literal['ok']


class GamesConnectionSchema(BaseModel):
    game_id: int
    user_id: int
    username: str
