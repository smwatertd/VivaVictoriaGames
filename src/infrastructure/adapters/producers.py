import json

import aioredis

from infrastructure.adapters.messages import Message
from infrastructure.ports.producers import Producer

import pika


class RedisProducer(Producer):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        encoding: str,
    ) -> None:
        self._redis = aioredis.Redis(
            host=host,
            port=port,
            db=db,
            encoding=encoding,
        )

    async def publish(self, group: str, message: Message) -> None:
        await self._redis.publish(
            group,
            json.dumps(
                {
                    'type': message.type.value,
                    'payload_type': message.payload_type,
                    'payload': message.payload,
                },
            ),
        )


class RabbitMQProducer(Producer):
    def __init__(self, host: str, port: int, virtual_host: str, exchange: str) -> None:
        self._exchange = exchange
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=virtual_host,
            ),
        )
        self._channel = self._connection.channel()

    async def publish(self, group: str, message: Message) -> None:
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=group,
            body=json.dumps(message.payload),
            properties=pika.BasicProperties(
                headers={
                    'type': message.type.value,
                    'payload_type': message.payload_type,
                },
            ),
        )
