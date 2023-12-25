from core.settings import game_settings

from domain.models import Duel, Field, Game, Player

from infrastructure.ports.repositories import GamesRepository

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SQLAlchemyGamesRepository(GamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def get(self, id: int) -> Game:
        result = await self._session.execute(
            select(Game)
            .where(Game._id == id)
            .options(
                joinedload(Game._players).joinedload(Player._fields),
                joinedload(Game._fields),
                joinedload(Game._duel).joinedload(Duel._attacker),
                joinedload(Game._duel).joinedload(Duel._defender),
                joinedload(Game._player_order),
            ),
        )
        game = result.scalars().first()
        if game is None:
            # TODO: replace with proper exception
            raise ValueError(f'Game {id} not found')
        self.seen.add(game)
        return game

    async def create(self, creator_id: int) -> None:
        result = await self._session.execute(insert(Game).values(creator_id=creator_id).returning(Game._id))
        game_id = result.scalar_one()
        await self._create_fields(game_settings.fields_count, game_id)
        await self._create_duel(game_id)

    async def _create_fields(self, fields_count: int, game_id: int) -> None:
        for _ in range(fields_count):
            await self._create_field(game_id)

    async def _create_field(self, game_id: int) -> None:
        await self._session.execute(insert(Field).values(game_id=game_id))

    async def _create_duel(self, game_id: int) -> None:
        await self._session.execute(insert(Duel).values(game_id=game_id))
