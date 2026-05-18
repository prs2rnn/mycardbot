import asyncio

from mycardbot.database.mappings import map_repo


async def cleanup_task():
    try:
        while True:
            await map_repo.cleanup_old_mappings()
            await asyncio.sleep(86400)
    except asyncio.CancelledError:
        pass
