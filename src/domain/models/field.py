from domain.models.player import Player


class Field:
    def __init__(self, id: int, value: int, owner: Player | None = None) -> None:
        self._id = id
        self._value = value
        self._owner = owner

    def __repr__(self) -> str:
        return f'Field(id={self._id}, value={self._value}, owner={self._owner})'

    def get_id(self) -> int:
        return self._id

    def is_captured(self) -> bool:
        return self._owner is not None

    def get_owner(self) -> Player | None:
        return self._owner

    def set_owner(self, new_owner: Player) -> None:
        if self._owner is None:
            self._value = 1
        else:
            self._value += 1
        self._owner = new_owner

    def get_value(self) -> int:
        return self._value

    def increase_value(self, value: int) -> None:
        self._value += value
