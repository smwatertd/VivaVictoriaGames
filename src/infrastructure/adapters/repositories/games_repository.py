from domain.enums import GameState
from domain.models import Field, Game

from infrastructure.ports.repositories import GamesRepository


class InMemoryGamesRepository(GamesRepository):
    games = {
        1: Game(pk=1, players=[], state=GameState.PLAYERS_WAITING, fields=[Field(pk=i) for i in range(1, 10)]),
        # 2: Game(pk=2, players=[], state=GameState.PLAYERS_WAITING, fields=[Field(pk=i) for i in range(10, 20)]),
    }

    async def get(self, pk: int) -> Game:
        self.seen.add(self.games[pk])
        return self.games[pk]
