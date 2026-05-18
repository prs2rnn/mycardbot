import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from mycardbot.core.config import setting
from mycardbot.core.setup_logging import setup_logger, setup_telegram_logger
from mycardbot.database.connection import db
from mycardbot.database.migrations import initialize, migrate
from mycardbot.middlewares.check_ban import CheckUserIsBanned
from mycardbot.middlewares.logging import LoggingMiddleware
from mycardbot.services.tasks import cleanup_task
from mycardbot.telegram.commands import set_commands
from mycardbot.telegram.routers import setup_router


async def main():
    logger = setup_logger(setting.debug)
    bot = None
    cleanup = None
    try:
        bot = Bot(setting.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
        setup_telegram_logger(logger, bot)
        await set_commands(bot, setting.admin_ids)

        await db.connect()
        await initialize(db)
        await migrate(db)

        cleanup = asyncio.create_task(cleanup_task())

        dp = Dispatcher()

        router = setup_router()
        dp.include_router(router)
        dp.update.outer_middleware(LoggingMiddleware(logger))
        dp.update.outer_middleware(CheckUserIsBanned())

        await dp.start_polling(bot)
    except Exception:
        logger.exception('Critical error')
    finally:
        await db.close()
        if cleanup:
            cleanup.cancel()
        if bot:
            await bot.session.close()
        logger.info('Bot stopped gracefully!')
