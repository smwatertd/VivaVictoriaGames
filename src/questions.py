import random

from domain.models import Answer, Question


QUESTIONS = [
    Question(
        id=i,
        answers=[
            Answer(
                id=i * 5 + j,
                is_correct=j == 0,
            )
            for j in range(1, 5)
        ],
    )
    for i in range(1, 10)
]


def get_random_question() -> Question:
    return random.choice(QUESTIONS)


class QuestionsClient:
    async def get_random_question(self) -> Question:
        return get_random_question()
