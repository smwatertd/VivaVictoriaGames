from typing import TYPE_CHECKING

from domain.models.field import Field


if TYPE_CHECKING:
    from domain.models.player import Player


class CapturedField:
    def __init__(self, field: Field, owner: 'Player', is_base: bool = False) -> None:
        self._field = field
        self._owner = owner
        self._is_base = is_base

    def get_id(self) -> int:
        return self._field.get_id()

    def get_value(self) -> int:
        return self._field.get_value()

    def mark_as_base(self) -> None:
        self._is_base = True
        self._field.mark_as_base()

    def is_base(self) -> bool:
        return self._is_base

    def get_owner(self) -> 'Player':
        return self._owner

    def set_owner(self, owner: 'Player') -> None:
        self._owner = owner
        self._field.on_capture()

    def on_defend(self) -> None:
        self._field.on_defend()
