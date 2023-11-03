from domain.models import Game

from infrastructure.ports.repositories import GamesRepository


class InMemoryGamesRepository(GamesRepository):
    games = {
        1: Game(1),
        2: Game(2),
    }

    async def get(self, pk: int) -> Game:
        self.seen.add(self.games[pk])
        return self.games[pk]
