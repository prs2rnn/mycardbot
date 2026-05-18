from mycardbot.database.connection import Database, db


class MappingsRepository:
    def __init__(self, db: Database):
        self.db = db

    async def save_reply_mapping(self, group_message_id: int, user_id: int):
        async with self.db._lock:
            await self.db._db.execute(
                """
                INSERT INTO reply_map (group_message_id, user_id)
                VALUES (?, ?);
                """,
                (
                    group_message_id,
                    user_id,
                ),
            )
            await self.db._db.commit()

    async def cleanup_old_mappings(self):
        async with self.db._lock:
            await self.db._db.execute(
                """
                DELETE FROM reply_map
                WHERE created_at < (
                    strftime('%s', 'now') - 2592000
                );
                """
            )
            await self.db._db.commit()

    async def get_user_id(self, group_message_id: int):
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                SELECT user_id
                FROM reply_map
                WHERE group_message_id = ?;
                """,
                (group_message_id,),
            )
            result = await cursor.fetchone()
            return result[0] if result else None


map_repo = MappingsRepository(db)
