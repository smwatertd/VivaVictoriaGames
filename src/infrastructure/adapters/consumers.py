import asyncio
import json
from functools import partial
from typing import Callable

import aio_pika

import aioredis

from infrastructure.adapters.messages import Message, MessageType
from infrastructure.ports import Consumer


class RedisConsumer(Consumer):
    def __init__(self, host: str, port: int, db: int, encoding: str, ignore_subscribe_messages: bool) -> None:
        self._redis = aioredis.Redis(host=host, port=port, db=db, encoding=encoding)
        self._pubsub = self._redis.pubsub(ignore_subscribe_messages=ignore_subscribe_messages)
        self._listen_task: asyncio.Task | None = None

    async def listen(self, group: str, callback: Callable) -> None:
        await self._pubsub.subscribe(group)
        self._listen_task = asyncio.create_task(self._message_process(callback))

    async def stop_listen(self) -> None:
        if self._listen_task is not None:
            self._listen_task.cancel()

    async def _message_process(self, callback: Callable) -> None:
        async for message in self._pubsub.listen():
            parsed_message = self._parse_message(message)
            await callback(parsed_message)

    def _parse_message(self, message: dict) -> Message:
        data = json.loads(message['data'])
        return Message(
            type=MessageType(data.get('type', 'unknown')),
            payload_type=data.get('payload_type', ''),
            payload=data.get('payload', {}),
        )


class RabbitMQConsumer(Consumer):
    def __init__(self, host: str, port: int, virtual_host: str) -> None:
        self._host = host
        self._port = port
        self._virtual_host = virtual_host
        self._listen_task: asyncio.Task | None = None

    async def listen(self, group: str, callback: Callable) -> None:
        self._connection = await aio_pika.connect_robust(
            host=self._host,
            port=self._port,
            virtualhost=self._virtual_host,
        )
        channel = await self._connection.channel()
        queue = await channel.declare_queue(group, durable=True)
        self._listen_task = asyncio.create_task(queue.consume(partial(self._message_process, callback)))

    def stop_listen(self) -> None:
        if self._listen_task is not None:
            self._listen_task.cancel()

    async def _message_process(self, callback: Callable, message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            parsed_message = self._parse_message(message)
            await callback(parsed_message)

    def _parse_message(self, message: aio_pika.IncomingMessage) -> Message:
        return Message(
            MessageType(message.headers.get('type', 'unknown')),
            message.headers.get('payload_type', ''),
            json.loads(message.body),
        )
