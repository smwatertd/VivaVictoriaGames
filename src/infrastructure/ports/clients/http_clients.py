from abc import ABC, abstractmethod

from infrastructure.ports.clients.schemas import CategorySchema, QuestionSchema


class HTTPClient(ABC):
    @abstractmethod
    async def get_random_question_by_category(self, category_id: int) -> QuestionSchema:
        pass

    @abstractmethod
    async def get_all_categories(self) -> list[CategorySchema]:
        pass

    @abstractmethod
    async def get_question(self, question_id: int) -> QuestionSchema:
        pass
