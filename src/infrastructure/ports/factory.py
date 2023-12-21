from abc import ABC
from typing import Any, Type

from pydantic import BaseModel


class Factory(ABC):
    registry: dict[str, Type[BaseModel]] = {}

    def create(self, type: str, **kwargs: Any) -> Any:
        registred_type = self.registry.get(type)
        if registred_type is None:
            raise ValueError(f'Type {type} not registred')
        return registred_type.model_validate(kwargs)
