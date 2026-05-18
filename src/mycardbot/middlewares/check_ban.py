from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from mycardbot.database.users import users_repo


class CheckUserIsBanned(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data.get('event_from_user')
        if not user:
            return await handler(event, data)

        is_banned = await users_repo.check_ban(user.id)

        if is_banned:
            return

        return await handler(event, data)
