from mycardbot.database.connection import Database, db


class UsersRepository:
    def __init__(self, db: Database):
        self.db = db

    async def add_user(
        self, full_name: str, username: str, original_user_id: int
    ) -> bool:
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                INSERT OR IGNORE
                INTO users (full_name, username, original_user_id, is_subscribed, is_ban)
                VALUES (?, ?, ?, ?, ?);
                """,
                (full_name, f'@{username}', original_user_id, False, False),
            )
            await self.db._db.commit()

            return cursor.rowcount > 0

    async def list_users_paginated(self, limit: int = 5, page_number: int = 1) -> dict:
        async with self.db._lock:
            offset = (page_number - 1) * limit

            cursor = await self.db._db.execute(
                """
                SELECT
                full_name Имя, username Username, original_user_id ID,
                is_subscribed Подписка, is_ban Бан,
                strftime('%d.%m.%Y %H:%M', started_at, 'unixepoch', '+3 hours') as 'Дата регистрации'
                FROM users
                ORDER BY started_at
                ASC
                LIMIT ? OFFSET ?;
                """,
                (limit, offset),
            )
            count_cursor = await self.db._db.execute(
                """
                SELECT
                count(*)
                FROM users;
                """
            )

            header = [i[0] for i in cursor.description]
            rows = await cursor.fetchall()
            count = (await count_cursor.fetchone())[0]
            total_pages = (count + limit - 1) // limit
            if not total_pages:
                total_pages = 1
            return {
                'header': header,
                'rows': rows,
                'count': count,
                'total_pages': total_pages,
            }

    async def subscribe_user(self, user_id: int) -> None:
        async with self.db._lock:
            await self.db._db.execute(
                """
                UPDATE users
                SET is_subscribed = True
                WHERE original_user_id = ?
                """,
                (user_id,),
            )
            await self.db._db.commit()

    async def unsubscribe_user(self, user_id: int) -> None:
        async with self.db._lock:
            await self.db._db.execute(
                """
                UPDATE users
                SET is_subscribed = False
                WHERE original_user_id = ?
                """,
                (user_id,),
            )
            await self.db._db.commit()

    async def check_subscription(self, user_id: int) -> bool | int:
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                SELECT is_subscribed
                FROM users
                WHERE original_user_id = ?
                """,
                (user_id,),
            )

            result = await cursor.fetchone()
            return result[0] if result else None

    async def get_subscribed_users(self):
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                SELECT original_user_id
                FROM users
                WHERE is_subscribed = True;
                """
            )
            result = await cursor.fetchall()
            return (i[0] for i in result) if result else None

    async def check_ban(self, user_id: int) -> bool:
        cursor = await self.db._db.execute(
            """
            SELECT is_ban
            FROM users
            WHERE original_user_id = ?;
            """,
            (user_id,),
        )
        result = await cursor.fetchone()

        return result[0] if result else False

    async def ban_user(self, user_id: int) -> bool:
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                UPDATE users
                SET is_ban = True
                WHERE original_user_id = ?;
                """,
                (user_id,),
            )
            await self.db._db.commit()

            return cursor.rowcount > 0

    async def unban_user(self, user_id: int) -> bool:
        async with self.db._lock:
            cursor = await self.db._db.execute(
                """
                UPDATE users
                SET is_ban = False
                WHERE original_user_id = ?;
                """,
                (user_id,),
            )
            await self.db._db.commit()

            return cursor.rowcount > 0


users_repo = UsersRepository(db)
