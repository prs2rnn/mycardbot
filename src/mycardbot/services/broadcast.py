import asyncio
import logging
import random

from aiogram import Bot
from aiogram.types import ReplyKeyboardRemove, User

from mycardbot.core.config import setting
from mycardbot.database.mappings import map_repo


async def send_user_message(bot: Bot, user: User, message_id: int):
    header = (
        f'👤 Новое сообщение от пользователя\n\n'
        f'Имя: {user.full_name}\n'
        f'Username: @{user.username}\n'
        f'ID: {user.id}\n\n'
    )

    try:
        await bot.send_message(setting.group_id, header)
        msg = await bot.copy_message(
            setting.group_id,
            user.id,
            message_id,
        )

        await map_repo.save_reply_mapping(msg.message_id, user.id)
        await bot.send_message(
            user.id,
            f'Ваше сообщение #{msg.message_id} успешно отправлено',
            reply_markup=ReplyKeyboardRemove(),
        )
    except Exception as e:
        logging.error(e)
        await bot.send_message(
            user.id,
            'Произошла ошибка при отправке сообщения',
            reply_markup=ReplyKeyboardRemove(),
        )


async def send_broadcast(bot: Bot, admin: User, users: list[User], message_id: int):
    header = '📢 Новая рассылка от бота\n\n'

    success, failure = 0, 0

    await bot.send_message(
        admin.id, 'Начинаю рассылку...', reply_markup=ReplyKeyboardRemove()
    )

    if not users:
        await bot.send_message(
            admin.id,
            'Нет пользователей, подписавшихся на рассылку. Действие отменено',
        )
        return

    try:
        for user_id in users:
            try:
                await bot.send_message(user_id, header)
                await bot.copy_message(user_id, admin.id, message_id)
                success += 1
                pause = random.uniform(0.8, 1.8)
                await asyncio.sleep(pause)
            except Exception as e:
                failure += 1
                logging.error(f'Error: {e}, ID: {user_id}')
        await bot.send_message(
            admin.id,
            f'Ваше сообщение для рассылки отправлено\n\n'
            f'Успешно: {success}\n'
            f'Неудачно: {failure}',
        )
    except Exception as e:
        logging.error(e)
        await bot.send_message(admin.id, 'Произошла ошибка при отправке рассылки')

    # archive to channel
    await bot.send_message(setting.channel_id, header)
    await bot.copy_message(setting.channel_id, admin.id, message_id)


async def send_notification(bot: Bot, full_name: str, username: str, user_id: int):
    text = (
        f'🆕 Новый пользователь в базе:\n\n'
        f'Имя: {full_name}\n'
        f'Username: @{username}\n'
        f'ID: {user_id}'
    )
    try:
        await bot.send_message(chat_id=setting.channel_id, text=text)
        logging.info('Notification sent to private channel')
    except Exception as e:
        logging.error(f'Error: {e}')
