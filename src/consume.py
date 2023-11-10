import asyncio

from core.container import container


async def main() -> None:
    await container.message_dispatcher().start(container.unit_of_work())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
