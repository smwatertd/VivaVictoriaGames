import json

from infrastructure.ports import Message, MessageType


class RedisMessage(Message):
    def __init__(self, body: dict[str, str | bytes]) -> None:
        self._payload = json.loads(body.get('data', ''))

    def __repr__(self) -> str:
        return f'RedisMessage(payload={self._payload})'

    def get_message_type(self) -> MessageType:
        return MessageType.EVENT

    def get_payload_type(self) -> str:
        return self._payload.get('event_type', 'unknown')

    def get_payload(self) -> dict:
        return self._payload
