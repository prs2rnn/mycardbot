import pytest

from mycardbot.database.cache import CacheRepository


class TestCacheRepository:
    @pytest.mark.asyncio
    async def test_set_cache(self, cache_repo: CacheRepository):
        result = await cache_repo.set_cache('test')

        assert result is True

    @pytest.mark.asyncio
    async def test_set_duplicate_cache(self, cache_repo: CacheRepository):
        await cache_repo.set_cache('test')
        result = await cache_repo.set_cache('test')

        assert result is False

    @pytest.mark.asyncio
    async def test_get_empty_cache(self, cache_repo: CacheRepository):
        await cache_repo.set_cache('test')
        result = await cache_repo.get_cache('test')

        assert '{}' in result and 0 in result

    @pytest.mark.asyncio
    async def test_update_cache(self, cache_repo: CacheRepository):
        await cache_repo.set_cache('test')
        result = await cache_repo.update_cache('test', '{key: value}', 10)

        assert result is True

    @pytest.mark.asyncio
    async def test_get_updated_cache(self, cache_repo: CacheRepository):
        await cache_repo.set_cache('test')
        await cache_repo.update_cache('test', '{key: value}', 10)
        result = await cache_repo.get_cache('test')

        assert '{key: value}' in result and 10 in result
