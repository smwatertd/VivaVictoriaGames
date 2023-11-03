from typing import Any

from infrastructure.ports import WebSocketConnection

from starlette.websockets import WebSocket


class StarletteWebSocketConnection(WebSocketConnection):
    def __init__(self, websocket: WebSocket) -> None:
        super().__init__(websocket)
        self.websocket: WebSocket

    async def send_json(self, data: Any) -> None:
        # TODO: Fix data type annotation
        pass
