import random
from dataclasses import dataclass


@dataclass
class Question:
    text: str


QUESTIONS = tuple(
    Question(text=f'Question {i}?')
    for i in range(100)
)


def get_random_question() -> Question:
    return random.choice(QUESTIONS)


class QuestionsClient:
    async def get_random_question(self) -> Question:
        return get_random_question()
