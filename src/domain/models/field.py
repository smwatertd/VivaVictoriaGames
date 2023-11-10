from domain import exceptions
from domain.models.model import Model
from domain.models.player import Player


class Field(Model):
    def __init__(
        self,
        pk: int,
        owner: Player | None = None,
    ) -> None:
        super().__init__(pk)
        self._owner = owner

    def __repr__(self) -> str:
        return f'Field(pk={self._pk}, owner={self._owner})'

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return False
        return self._pk == __value._pk

    def is_captured(self) -> bool:
        return self._owner is not None

    def ensure_can_capture(self, capturer: Player) -> None:
        if self._owner == capturer:
            raise exceptions.AlreadyOwned

    def get_owner(self) -> Player:
        assert self._owner
        return self._owner

    def set_owner(self, new_owner: Player) -> None:
        self._owner = new_owner
