import asyncio

from mycardbot.core.database import bot_db


async def cleanup_task():
    try:
        while True:
            await bot_db.cleanup_old_mappings()
            await asyncio.sleep(86400)
    except asyncio.CancelledError:
        pass
