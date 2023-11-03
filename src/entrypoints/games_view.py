from typing import Any

from core.container import container

from domain.commands import ConnectUser, DisconnectUser

from entrypoints.schemas import GamesConnectionSchema

from fastapi import APIRouter

from infrastructure.ports import ChannelLayer

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket


router = APIRouter(
    tags=['Games'],
)


class BaseGamesWebSocketEndpoint(WebSocketEndpoint):
    layer: ChannelLayer
    encoding = 'json'
    actions: tuple[str]

    async def on_connect(self, websocket: WebSocket) -> None:
        # TODO: Delete Temp Data
        await super().on_connect(websocket)
        self._get_websocket_data(websocket)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await super().on_disconnect(websocket, close_code)

    async def on_receive(self, websocket: WebSocket, data: Any) -> None:
        action, data = self._parse_message(data)
        handler = getattr(self, action, self.action_not_allowed)
        await handler(websocket, data)

    async def action_not_allowed(self, websocket: WebSocket, data: Any) -> None:
        await websocket.send_json({'status': 'error', 'detail': 'action not allowed'})

    def _parse_message(self, message: dict) -> tuple[str, dict]:
        return message.get('action', ''), message.get('data', {})

    def _get_websocket_data(self, websocket: WebSocket) -> None:
        game = websocket.query_params.get('game', '1')[-1]
        username = websocket.query_params.get('username', 'anonymous')
        user_id = username[-1]
        self.data = GamesConnectionSchema(game_id=int(game), user_id=int(user_id), username=username)


class GamesWebSocketEndpoint(BaseGamesWebSocketEndpoint):
    layer = container.channel_layer()
    actions = ('',)

    async def on_connect(self, websocket: WebSocket) -> None:
        await super().on_connect(websocket)
        await self.layer.group_add(self.data.game_id, websocket)
        command = ConnectUser(game_id=self.data.game_id, user_id=self.data.user_id, username=self.data.username)
        await container.messagebus().handle(command, container.unit_of_work())

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await super().on_disconnect(websocket, close_code)
        await self.layer.group_discard(self.data.game_id, websocket)
        command = DisconnectUser(game_id=self.data.game_id, user_id=self.data.user_id, username=self.data.username)
        await container.messagebus().handle(command, container.unit_of_work())


router.add_websocket_route('/ws', GamesWebSocketEndpoint)
