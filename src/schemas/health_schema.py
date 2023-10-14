from typing import Literal

from pydantic import BaseModel


class HealthSchema(BaseModel):
    status: Literal['ok']
