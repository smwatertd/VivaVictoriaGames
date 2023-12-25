from domain.models import Player
from domain.strategies import PlayerTurnSelector


class FakePlayerTurnSelector(PlayerTurnSelector):
    def select(self, round_number: int, players: list[Player]) -> Player:
        return players[0]

    def get_order(self, players: list[Player]) -> list[Player]:
        return players
