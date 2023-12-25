from typing import Annotated

from entrypoints import dependencies, schemas

from fastapi import APIRouter, Depends

from infrastructure.ports import UnitOfWork

from services import commands, messagebus, views


router = APIRouter(
    tags=['Games'],
)


@router.post('/games', status_code=201)
async def create_game(
    create_data: schemas.CreateGameSchema,
    messagebus: Annotated[messagebus.MessageBus, Depends(dependencies.get_messagebus)],
) -> None:
    await messagebus.handle(commands.CreateGame(creator_id=create_data.creator_id))


@router.get('/games/available', status_code=200)
async def get_available_games(
    unit_of_work: Annotated[UnitOfWork, Depends(dependencies.get_unit_of_work)],
) -> list[schemas.AvailableGame]:
    games = await views.get_available_games(unit_of_work)
    return [schemas.AvailableGame(id=game.id) for game in games]
