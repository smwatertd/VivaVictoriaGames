from abc import ABC, abstractmethod

from domain.models import Field

from infrastructure.ports.repositories.repository import Repository


class FieldsRepository(Repository, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.seen: set[Field]

    @abstractmethod
    async def get(self, id: int) -> Field:
        pass
