from infrastructure.ports import UnitOfWork

from services import dto


async def get_available_games(uow: UnitOfWork) -> list[dto.AvailableGameDTO]:
    async with uow:
        available_games = await uow.games.get_available_games()
        return [dto.AvailableGameDTO(id=game.get_id()) for game in available_games]
