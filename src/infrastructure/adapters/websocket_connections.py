import json

from infrastructure.ports import WebSocketConnection

from starlette.websockets import WebSocket


class StarletteWebSocketConnection(WebSocketConnection):
    def __init__(self, websocket: WebSocket) -> None:
        super().__init__(websocket)
        self.websocket: WebSocket

    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send_json(json.loads(data))
