from domain.models import Answer, Question

from infrastructure.ports.clients import HTTPClient


class QuestionsClient:
    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    async def random_by_category(self, category_id: int) -> Question:
        response = await self._client.get_random_question_by_category(category_id)
        return Question(
            id=response.id,
            answers=[Answer(id=answer.id, is_correct=answer.is_correct) for answer in response.answers],
        )
