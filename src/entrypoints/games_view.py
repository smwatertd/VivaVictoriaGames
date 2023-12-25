from typing import Any

from core.container import container

from entrypoints import schemas

from fastapi import APIRouter

from infrastructure import adapters

from services import commands

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket


router = APIRouter(
    tags=['Games'],
)


class BaseGamesWebSocketEndpoint(WebSocketEndpoint):
    layer: adapters.ChannelLayer
    encoding = 'json'

    async def on_connect(self, websocket: WebSocket) -> None:
        await super().on_connect(websocket)
        self._get_websocket_data(websocket)
        await self.layer.group_add(
            self.data.game_pk,
            adapters.Channel(
                self.data.user_pk,
                adapters.StarletteWebSocketConnection(websocket),
                container.chat_message_consumer(),
            ),
        )

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await super().on_disconnect(websocket, close_code)
        await self.layer.group_discard(self.data.game_pk, self.data.user_pk)

    async def on_receive(self, websocket: WebSocket, data: Any) -> None:
        action, data = self._parse_message(data)
        # TODO: add allowed actions
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
        self.data = schemas.GamesConnectionSchema(game_pk=int(game), user_pk=int(user_pk), username=username)


class GamesWebSocketEndpoint(BaseGamesWebSocketEndpoint):
    layer = container.channel_layer()

    async def on_connect(self, websocket: WebSocket) -> None:
        await super().on_connect(websocket)
        await self._handler_command(
            commands.AddUser(
                game_pk=self.data.game_pk,
                user_pk=self.data.user_pk,
                username=self.data.username,
            ),
        )

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await super().on_disconnect(websocket, close_code)
        await self._handler_command(
            commands.RemoveUser(
                game_pk=self.data.game_pk,
                user_pk=self.data.user_pk,
                username=self.data.username,
            ),
        )

    async def attack_field(self, websocket: WebSocket, data: dict[str, str | int]) -> None:
        await self._handler_command(
            commands.AttackField(
                game_pk=self.data.game_pk,
                attacker_pk=self.data.user_pk,
                field_pk=int(data.get('field_pk', 0)),
            ),
        )

    async def send_answer(self, websocket: WebSocket, data: dict[str, str | int]) -> None:
        await self._handler_command(
            commands.SendAnswer(
                game_pk=self.data.game_pk,
                player_pk=self.data.user_pk,
                answer_pk=int(data.get('answer_pk', 0)),
            ),
        )

    async def _handler_command(self, command: commands.Command) -> None:
        await container.messagebus().handle(command)


router.add_websocket_route('/ws', GamesWebSocketEndpoint)
