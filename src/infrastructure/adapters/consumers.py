import json
from typing import AsyncIterator

import aioredis

from infrastructure.adapters.message_types import MessageType
from infrastructure.adapters.messages import Message
from infrastructure.ports import ChatMessageConsumer, MessageConsumer

import pika


class RedisChatMessageConsumer(ChatMessageConsumer):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        encoding: str,
        ignore_subscribe_messages: bool,
    ) -> None:
        self._redis = aioredis.Redis(host=host, port=port, db=db, encoding=encoding)
        self._pubsub = self._redis.pubsub(ignore_subscribe_messages=ignore_subscribe_messages)

    async def subscribe(self, group: str) -> None:
        await self._pubsub.subscribe(group)

    async def unsubscribe(self, group: str) -> None:
        await self._pubsub.unsubscribe(group)

    async def listen(self) -> AsyncIterator[Message]:
        # TODO: fix. When exception raises nothing does because async task. Can add add_done_callback. Change ensure
        # future to create task
        async for message in self._pubsub.listen():
            decoded_data = json.loads(message['data'])
            yield Message(
                type=MessageType(decoded_data['type']),
                payload_type=decoded_data['payload_type'],
                payload=decoded_data['payload'],
            )


class RabbitMQMessageConsumer(MessageConsumer):
    def __init__(
        self,
        host: str,
        port: int,
        virtual_host: str,
    ) -> None:
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=virtual_host,
            ),
        )
        self._channel = self._connection.channel()
        self._delivery_tag = None

    async def listen(self, group: str) -> AsyncIterator[Message]:
        for deliver, properties, body in self._channel.consume(queue=group, auto_ack=False):
            self._delivery_tag = deliver.delivery_tag
            yield Message(
                type=MessageType(properties.headers.get('type', 'unknown')),
                payload_type=properties.headers['payload_type'],
                payload=json.loads(body),
            )

    async def commit(self) -> None:
        if self._delivery_tag is not None:
            self._channel.basic_ack(delivery_tag=self._delivery_tag)
