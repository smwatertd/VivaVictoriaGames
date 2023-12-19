class Player:
    def __init__(self, id: int, answer_id: int | None) -> None:
        self._id = id
        self._answer_id = answer_id

    def __repr__(self) -> str:
        return f'Player(id={self._id}, answer={self._answer_id})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self._id == other._id

    def get_id(self) -> int:
        return self._id

    def set_answer(self, answer_id: int) -> None:
        self._answer_id = answer_id

    def is_answered(self) -> bool:
        return self._answer_id is not None

    def get_answer_id(self) -> int:
        if self._answer_id is None:
            raise ValueError('Player has not answered yet')
        return self._answer_id

    def reset_answer_id(self) -> None:
        self._answer_id = None
