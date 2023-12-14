from domain.models.answer import Answer


class Question:
    def __init__(self, id: int, answers: list[Answer]) -> None:
        self.id = id
        self._answers = answers

    def __repr__(self) -> str:
        return f'Question(id={self.id}, answers={self._answers})'
