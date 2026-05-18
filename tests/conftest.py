import pytest_asyncio

from mycardbot.database.cache import CacheRepository
from mycardbot.database.connection import Database
from mycardbot.database.migrations import initialize
from mycardbot.database.users import UsersRepository


@pytest_asyncio.fixture
async def test_db(tmp_path):
    db = Database(tmp_path / 'test.db')

    await db.connect()
    await initialize(db)

    yield db

    await db.close()


@pytest_asyncio.fixture
async def users_repo(test_db):
    return UsersRepository(test_db)


@pytest_asyncio.fixture
async def cache_repo(test_db):
    return CacheRepository(test_db)
