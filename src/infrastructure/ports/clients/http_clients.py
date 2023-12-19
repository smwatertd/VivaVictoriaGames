from abc import ABC, abstractmethod

from infrastructure.ports.clients.schemas import QuestionSchema


class HTTPClient(ABC):
    @abstractmethod
    async def get_random_question_by_category(self, category_id: int) -> QuestionSchema:
        pass
