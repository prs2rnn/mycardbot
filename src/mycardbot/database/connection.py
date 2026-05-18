import asyncio
from pathlib import Path

import aiosqlite


class Database:
    def __init__(self, db_name: str = 'bot.db'):

        Path('data').mkdir(exist_ok=True)

        self._db_path = Path('data') / db_name
        self._db = None
        self._lock = asyncio.Lock()

    async def connect(self):
        self._db = await aiosqlite.connect(self._db_path)
        await self._db.execute('PRAGMA foreign_keys = ON;')

    async def close(self):
        if self._db:
            await self._db.close()
            self._db = None


db = Database()
