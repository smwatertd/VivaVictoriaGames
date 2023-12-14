from random import randint, shuffle

from domain.models import Answer, Question

from infrastructure.ports.repositories import QuestionsRepository


class HTTPQuestionsRepository(QuestionsRepository):
    async def random_by_category(self, category_id: int) -> Question:
        corrects = [True, False, False, False]
        shuffle(corrects)
        return Question(
            id=randint(1, 1000),
            answers=[Answer(id=randint(1, 1000), is_correct=is_correct) for is_correct in corrects],
        )
