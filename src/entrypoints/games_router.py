from typing import Annotated

from entrypoints import dependencies, schemas

from fastapi import APIRouter, Depends

from services import commands
from services.messagebus import MessageBus


router = APIRouter(
    tags=['Games'],
)


@router.post('/games', status_code=201)
async def create_game(
    create_data: schemas.CreateGameSchema,
    messagebus: Annotated[MessageBus, Depends(dependencies.get_messagebus)],
) -> None:
    await messagebus.handle(commands.CreateGame(creator_id=create_data.creator_id))
