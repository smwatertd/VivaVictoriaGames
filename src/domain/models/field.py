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

    def is_captured(self) -> bool:
        return self._owner is not None

    def can_be_attacked(self, attacker: Player) -> bool:
        return self._owner is None or self._owner == attacker

    def __repr__(self) -> str:
        return f'Field(pk={self._pk}, owner={self._owner})'
