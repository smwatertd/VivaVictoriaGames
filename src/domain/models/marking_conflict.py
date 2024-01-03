from dataclasses import dataclass

from domain.models.field import Field
from domain.models.player import Player


@dataclass(frozen=True, slots=True)
class MarkingConflict:
    players: tuple[Player, ...]
    field: Field
