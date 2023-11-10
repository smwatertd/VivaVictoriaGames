from typing import Any

from core.container import container

from domain import commands

from entrypoints.schemas import GamesConnectionSchema

from fastapi import APIRouter

from infrastructure.adapters.channel_layers import ChannelLayer
from infrastructure.adapters.consumers import RedisConsumer
from infrastructure.adapters.websocket_connections import StarletteWebSocketConnection

from services.messagebus import MessageBus

from starlette.endpoints import WebSocketEndpoint
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket


router = APIRouter(
    tags=['Games'],
)


class BaseGamesWebSocketEndpoint(WebSocketEndpoint):
    layer: ChannelLayer
    encoding = 'json'

    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        super().__init__(scope, receive, send)
        self.messagebus: MessageBus = container.messagebus()

    async def on_connect(self, websocket: WebSocket) -> None:
        # TODO: Delete Temp Data
        await super().on_connect(websocket)
        self._get_websocket_data(websocket)
        await self.layer.group_add(self.data.game_pk, StarletteWebSocketConnection(websocket))

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await super().on_disconnect(websocket, close_code)
        await self.layer.group_discard(self.data.game_pk, StarletteWebSocketConnection(websocket))

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
        user_pk = username[-1]
        self.data = GamesConnectionSchema(game_pk=int(game), user_pk=int(user_pk), username=username)


class GamesWebSocketEndpoint(BaseGamesWebSocketEndpoint):
    layer: ChannelLayer = container.channel_layer(consumer_factory=RedisConsumer)

    async def on_connect(self, websocket: WebSocket) -> None:
        await super().on_connect(websocket)
        command = commands.AddUser(
            game_pk=self.data.game_pk,
            user_pk=self.data.user_pk,
            username=self.data.username,
        )
        await self.messagebus.handle(command, container.unit_of_work())

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await super().on_disconnect(websocket, close_code)
        command = commands.RemoveUser(
            game_pk=self.data.game_pk,
            user_pk=self.data.user_pk,
            username=self.data.username,
        )
        await self.messagebus.handle(command, container.unit_of_work())

    async def attack_field(self, websocket: WebSocket, data: dict[str, str | int]) -> None:
        command = commands.AttackField(
            game_pk=self.data.game_pk,
            attacker_pk=self.data.user_pk,
            field_pk=data.get('field_pk'),
        )
        await self.messagebus.handle(command, container.unit_of_work())

    async def send_answer(self, websocket: WebSocket, data: dict[str, str | int]) -> None:
        command = commands.SendAnswer(
            game_pk=self.data.game_pk,
            user_pk=self.data.user_pk,
            answer=data.get('answer_pk'),
        )
        await self.messagebus.handle(command, container.unit_of_work())


router.add_websocket_route('/ws', GamesWebSocketEndpoint)
