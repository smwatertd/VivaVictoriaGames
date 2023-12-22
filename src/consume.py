import asyncio

from core.container import container
from core.settings import rabbitmq_settings

from main import app  # noqa


async def main() -> None:
    message_handler = container.message_handler()
    await message_handler.start(rabbitmq_settings.games_events_queue)
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
