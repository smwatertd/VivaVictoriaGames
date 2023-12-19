from core.settings import questions_settings

import httpx

from infrastructure.ports.clients import AnswerSchema, HTTPClient, QuestionSchema
from infrastructure.ports.clients.schemas import CategorySchema


class HTTPXClient(HTTPClient):
    async def get_random_question_by_category(self, category_id: int) -> QuestionSchema:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{questions_settings.url}/random?category_id={category_id}')
            data = response.json()
            answers = [
                AnswerSchema(id=answer['id'], body=answer['body'], is_correct=answer['is_correct'])
                for answer in data['answers']
            ]
            return QuestionSchema(id=data['id'], body=data['body'], answers=answers)

    async def get_all_categories(self) -> list[CategorySchema]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{questions_settings.url}/categories')
            data = response.json()
            return [CategorySchema(id=category['id'], name=category['name']) for category in data]
