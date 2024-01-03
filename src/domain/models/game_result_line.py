from dataclasses import dataclass

from domain.models.player import Player


@dataclass(slots=True, frozen=True)
class GameResultLine:
    place: int
    player: Player
    score: int
