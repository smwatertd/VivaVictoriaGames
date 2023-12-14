from domain.models.answer import Answer


class Player:
    def __init__(self, id: int, answer: Answer | None) -> None:
        self.id = id
        self._answer = answer

    def __repr__(self) -> str:
        return f'Player(id={self.id}, answer={self._answer})'

    def __hash__(self) -> int:
        return hash(self.id)

    def set_answer(self, answer: Answer) -> None:
        self._answer = answer

    def is_answered(self) -> bool:
        return self._answer is not None
