from core.settings import game_settings

from domain import models
from domain.enums import GameState

from infrastructure.ports.repositories import GamesRepository

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SQLAlchemyGamesRepository(GamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def get(self, id: int) -> models.Game:
        result = await self._session.execute(
            select(models.Game)
            .where(models.Game._id == id)
            .options(
                joinedload(models.Game._preparation),
                joinedload(models.Game._capture)
                .joinedload(models.Capture._marked_fields)
                .joinedload(models.MarkedField._players),
                joinedload(models.Game._capture)
                .joinedload(models.Capture._marked_fields)
                .joinedload(models.MarkedField._field),
                joinedload(models.Game._battle).joinedload(models.Battle._duel),
                joinedload(models.Game._players)
                .joinedload(models.Player._fields)
                .joinedload(models.CapturedField._field),
                joinedload(models.Game._players)
                .joinedload(models.Player._marked_field)
                .joinedload(models.MarkedField._field),
                joinedload(models.Game._fields)
                .joinedload(models.Field._captured)
                .joinedload(models.CapturedField._owner),
                joinedload(models.Game._player_order),
            ),
        )
        game = result.scalars().first()
        if game is None:
            # TODO: replace with proper exception
            raise ValueError(f'Game {id} not found')
        self.seen.add(game)
        return game

    async def create(self, creator_id: int) -> None:
        result = await self._session.execute(
            insert(models.Game).values(creator_id=creator_id).returning(models.Game._id),
        )
        game_id = result.scalar_one()
        await self._create_preparation(game_id)
        await self._create_capture(game_id)
        await self._create_battle(game_id)
        await self._create_fields(game_settings.fields_count, game_id)

    async def get_available_games(self) -> list[models.Game]:
        result = await self._session.execute(
            select(models.Game).where(models.Game._state == GameState.PLAYERS_WAITING),
        )
        return list(result.scalars().fetchall())

    async def _create_preparation(self, game_id: int) -> None:
        await self._session.execute(insert(models.Preparation).values(game_id=game_id))

    async def _create_capture(self, game_id: int) -> None:
        await self._session.execute(insert(models.Capture).values(game_id=game_id))

    async def _create_battle(self, game_id: int) -> None:
        result = await self._session.execute(insert(models.Battle).values(game_id=game_id).returning(models.Battle._id))
        battle_id = result.scalar_one()
        await self._create_duel(battle_id)

    async def _create_fields(self, fields_count: int, game_id: int) -> None:
        for _ in range(fields_count):
            await self._create_field(game_id)

    async def _create_duel(self, battle_id: int) -> None:
        await self._session.execute(insert(models.Duel).values(battle_id=battle_id))

    async def _create_field(self, game_id: int) -> None:
        await self._session.execute(insert(models.Field).values(game_id=game_id))
