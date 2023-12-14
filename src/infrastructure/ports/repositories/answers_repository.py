from abc import ABC, abstractmethod

from domain.models import Answer


class AnswersRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> Answer:
        pass
