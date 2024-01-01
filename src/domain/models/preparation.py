from domain.models.field import Field
from domain.models.player import Player


class Preparation:
    def __init__(self, id: int, round_number: int) -> None:
        self._id = id
        self._round_number = round_number

    def start(self) -> None:
        self._round_number = 1

    def get_round_number(self) -> int:
        return self._round_number

    def set_player_base(self, player: Player, field: Field) -> None:
        player.set_base(field)

    def stop_round(self) -> None:
        self._round_number += 1
