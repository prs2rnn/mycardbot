from mycardbot.database.connection import Database


async def initialize(db: Database):
    async with db._lock:
        await db._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                username TEXT UNIQUE,
                original_user_id TEXT UNIQUE NOT NULL,
                started_at REAL DEFAULT ( strftime('%s', 'now') ),
                is_subscribed BOOLEAN DEFAULT FALSE,
                is_ban BOOLEAN DEFAULT FALSE
            );

            CREATE TABLE IF NOT EXISTS reply_map (
                group_message_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at REAL DEFAULT (
                    strftime('%s', 'now')
                )
            );

            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at REAL
            );
            """
        )
        await db._db.commit()


async def migrate(db: Database):
    cursor = await db._db.execute('PRAGMA table_info(users);')
    columns = await cursor.fetchall()

    column_names = [column[1] for column in columns]

    if 'is_ban' not in column_names:
        await db._db.execute(
            """
            ALTER TABLE users
            ADD COLUMN is_ban BOOLEAN DEFAULT FALSE;
            """
        )
        await db._db.commit()
