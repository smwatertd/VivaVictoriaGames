import json

from infrastructure.ports import Message, MessageType

from pika.spec import Basic, BasicProperties


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


class RabbitMQMessage(Message):
    def __init__(
        self,
        deliver: Basic.Deliver,
        properties: BasicProperties,
        payload: bytes,
    ) -> None:
        self._headers = properties.headers
        self._payload = json.loads(payload)

    def get_message_type(self) -> MessageType:
        return MessageType(self._headers.get('message_type', 'unknown'))

    def get_payload_type(self) -> str:
        return self._headers.get('payload_type', 'unknown')

    def get_payload(self) -> dict:
        return self._payload
