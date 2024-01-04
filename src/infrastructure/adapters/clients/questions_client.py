from domain.value_objects import Question, QuestionAnswer

from infrastructure.ports.clients import HTTPClient


class QuestionsClient:
    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    async def random_by_category(self, category_id: int) -> Question:
        response = await self._client.get_random_question_by_category(category_id)
        answers = [QuestionAnswer(id=answer.id, body=answer.body) for answer in response.answers]
        [correct_answer] = [
            QuestionAnswer(id=answer.id, body=answer.body) for answer in response.answers if answer.is_correct
        ]
        return Question(id=response.id, body=response.body, answers=answers, correct_answer=correct_answer)

    async def get_correct_answer(self, question_id: int) -> int:
        response = await self._client.get_question(question_id)
        return next(answer.id for answer in response.answers if answer.is_correct)
