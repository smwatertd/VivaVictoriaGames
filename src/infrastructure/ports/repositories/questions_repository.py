from abc import ABC, abstractmethod

from domain.models import Question


class QuestionsRepository(ABC):
    @abstractmethod
    async def random_by_category(self, category_id: int) -> Question:
        pass
