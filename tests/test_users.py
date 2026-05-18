import pytest

from mycardbot.database.users import UsersRepository


class TestUsersRepository:
    @pytest.mark.asyncio
    async def test_add_user(self, users_repo: UsersRepository):
        result = await users_repo.add_user(
            full_name='John',
            username='john',
            original_user_id=123,
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_add_duplicate_user(self, users_repo: UsersRepository):
        await users_repo.add_user(
            full_name='John',
            username='john',
            original_user_id=123,
        )
        result = await users_repo.add_user(
            full_name='John',
            username='john',
            original_user_id=123,
        )

        assert result is False
