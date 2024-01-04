from typing import TYPE_CHECKING

from core.settings import game_settings


if TYPE_CHECKING:
    from domain.models.captured_field import CapturedField
    from domain.models.marked_field import MarkedField
    from domain.models.player import Player


class Field:
    def __init__(
        self,
        id: int,
        value: int,
        captured: 'CapturedField | None',
        marked_field: 'MarkedField | None',
    ) -> None:
        self._id = id
        self._value = value
        self._captured = captured
        self._marked_field = marked_field

    def __repr__(self) -> str:
        return f'Field(id={self._id})'

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return False
        return self._id == __value._id

    def __hash__(self) -> int:
        return hash(self._id)

    def get_id(self) -> int:
        return self._id

    def get_value(self) -> int:
        return self._value

    def mark_as_base(self) -> None:
        self._value = game_settings.base_field_value

    def on_capture(self) -> None:
        self._value += 1

    def is_captured(self) -> bool:
        return self._captured is not None

    def get_owner(self) -> 'Player':
        if self._captured is None:
            raise ValueError('Cannot get owner without captured')
        return self._captured.get_owner()

    def on_defend(self) -> None:
        self._value += 2

    def get_captured_field(self) -> 'CapturedField':
        if self._captured is None:
            raise ValueError('Cannot get captured field without captured')
        return self._captured
