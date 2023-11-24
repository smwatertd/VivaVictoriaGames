from core.settings import db_settings

from infrastructure.adapters import repositories
from infrastructure.ports.producers import Producer
from infrastructure.ports.unit_of_work import UnitOfWork

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


SQLALCHEMY_DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(db_settings.url, echo=db_settings.echo),
    class_=AsyncSession,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        event_producer: Producer,
        session_factory: async_sessionmaker[
            AsyncSession
        ] = SQLALCHEMY_DEFAULT_SESSION_FACTORY,
    ) -> None:
        super().__init__(event_producer)
        self._session_factory = session_factory

    async def __aenter__(self) -> 'SQLAlchemyUnitOfWork':
        self._session = self._session_factory()
        self.games = repositories.SQLAlchemyGamesRepository(self._session)
        self.players = repositories.SQLAlchemyPlayersRepository(self._session)
        self.fields = repositories.SQLAlchemyFieldsRepository(self._session)
        return await super().__aenter__()

    async def __aexit__(self) -> None:
        return await super().__aexit__()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def commit(self) -> None:
        await self._session.commit()
