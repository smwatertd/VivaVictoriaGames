from domain.models.player import Player


class Field:
    def __init__(self, id: int, owner: Player | None = None) -> None:
        self.id = id
        self._owner = owner

    def __repr__(self) -> str:
        return f'Field(id={self.id}, owner={self._owner})'

    def is_captured(self) -> bool:
        return self._owner is not None

    def get_owner(self) -> Player | None:
        return self._owner

    def set_owner(self, new_owner: Player) -> None:
        self._owner = new_owner
