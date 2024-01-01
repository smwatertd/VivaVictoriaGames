from datetime import datetime

from domain.models.captured_field import CapturedField
from domain.models.field import Field
from domain.models.marked_field import MarkField


class Player:
    def __init__(
        self,
        id: int,
        connected_at: datetime | None,
        answer_id: int | None,
        answered_at: datetime | None,
        fields: list['CapturedField'],
        marked_field: 'MarkField | None',
    ) -> None:
        self._id = id
        self._connected_at = connected_at
        self._answer_id = answer_id
        self._answered_at = answered_at
        self._fields = fields
        self._marked_field = marked_field

    def __repr__(self) -> str:
        return f'Player(id={self._id})'

    def get_id(self) -> int:
        return self._id

    def on_connect(self) -> None:
        self._connected_at = datetime.utcnow()

    def get_connected_at(self) -> datetime:
        assert self._connected_at
        return self._connected_at

    def set_answer(self, answer: int) -> None:
        self._answer_id = answer
        self._answered_at = datetime.utcnow()

    def get_answer(self) -> int:
        assert self._answer_id, 'Player is not answered'
        return self._answer_id

    def clear_answer(self) -> None:
        self._answer_id = None

    def get_answered_at(self) -> datetime:
        assert self._answered_at, 'Player is not answered'
        return self._answered_at

    def set_base(self, field: Field) -> None:
        captured_field = CapturedField(field, self)
        self._fields.append(captured_field)
        captured_field.mark_as_base()

    def mark_field(self, field: Field) -> None:
        self._marked_field = MarkField(field)

    def is_marked_field(self) -> bool:
        return self._marked_field is not None

    def get_marked_field(self) -> MarkField:
        assert self._marked_field
        return self._marked_field

    def clear_marked_field(self) -> None:
        self._marked_field = None

    def is_answered(self) -> bool:
        return self._answer_id is not None

    def capture(self, field: Field) -> None:
        captured_field = CapturedField(field, self)
        self._fields.append(captured_field)

    def get_captured_field(self, field: Field) -> CapturedField:
        for captured_field in self._fields:
            if captured_field.get_field() == field:
                return captured_field
        raise ValueError('Field is not captured')
