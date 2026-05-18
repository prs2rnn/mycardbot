from mycardbot.database.connection import Database, db


class CacheRepository:
    def __init__(self, db: Database):
        self.db = db
        self.cache_ttl = 60 * 10

    async def get_cache(self, key: str) -> tuple[str, float]:
        cursor = await self.db._db.execute(
            """
            SELECT value, updated_at FROM cache
            WHERE key = ?;
            """,
            (key,),
        )
        result = await cursor.fetchone()

        return result

    async def set_cache(self, key: str) -> bool:
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                INSERT OR IGNORE
                INTO cache (key, value, updated_at)
                VALUES (?, ?, ?);
                """,
                (key, '{}', 0),
            )
            await self.db._db.commit()

            return cursor.rowcount > 0

    async def update_cache(self, key: str, value: str, update_time: float) -> bool:
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                UPDATE cache
                SET value = ?, updated_at = ?
                WHERE key = ?;
                """,
                (value, update_time, key),
            )
            await self.db._db.commit()

            return cursor.rowcount > 0


cache_repo = CacheRepository(db)
