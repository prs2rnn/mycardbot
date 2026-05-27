import html
import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from mycardbot.core.config import setting
from mycardbot.database.mappings import map_repo
from mycardbot.database.users import users_repo
from mycardbot.filters.check_admin import IsAdmin
from mycardbot.keyboards.admin import get_main_keyboard, get_proceed_broadcast_keyboard
from mycardbot.services.broadcast import send_broadcast
from mycardbot.states.admin import BroadcastStates
from mycardbot.utils.content import load_html_content

admin_message_router = Router()


@admin_message_router.message(Command('admin'), IsAdmin())
async def list(message: Message) -> None:
    text = load_html_content('admin')
    text = text.replace('{name}', html.escape(message.from_user.first_name))
    await message.answer(text, reply_markup=get_main_keyboard())


@admin_message_router.message(
    StateFilter(BroadcastStates.waiting_for_message), F.text == 'Отменить', IsAdmin()
)
async def cancel_broadcast(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())
    text = load_html_content('admin')
    text = text.replace('{name}', html.escape(message.from_user.first_name))
    await message.answer(text, reply_markup=get_main_keyboard())


@admin_message_router.message(
    StateFilter(BroadcastStates.waiting_for_message), IsAdmin()
)
async def handle_broadcast(message: Message, state: FSMContext):
    await state.update_data(pending_message_id=message.message_id)

    await message.answer(
        'Подтвердите или отмените отправку',
        reply_markup=get_proceed_broadcast_keyboard(),
    )
    await state.set_state(state=None)
    await state.set_state(BroadcastStates.waiting_for_confirmation)


@admin_message_router.message(
    StateFilter(BroadcastStates.waiting_for_confirmation),
    F.text == 'Подтвердить',
    IsAdmin(),
)
async def confirm_broadcast(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get('pending_message_id')
    users = await users_repo.get_subscribed_users()
    admin = message.from_user

    await send_broadcast(bot, admin, users, message_id)

    await state.clear()
    text = load_html_content('admin')
    text = text.replace('{name}', html.escape(admin.first_name))
    await message.answer(text, reply_markup=get_main_keyboard())


@admin_message_router.message(
    StateFilter(BroadcastStates.waiting_for_confirmation),
    F.text == 'Отменить',
    IsAdmin(),
)
async def cancel_confirm_broadcast(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())
    text = load_html_content('admin')
    text = text.replace('{name}', html.escape(message.from_user.first_name))
    await message.answer(text, reply_markup=get_main_keyboard())


@admin_message_router.message(
    StateFilter(BroadcastStates.waiting_for_confirmation), IsAdmin()
)
async def handle_confirm_broadcast(message: Message, state: FSMContext):
    await message.answer(
        'Подтвердите или отмените отправку',
        reply_markup=get_proceed_broadcast_keyboard(),
    )


@admin_message_router.message(
    F.chat.id == setting.group_id, F.reply_to_message, IsAdmin()
)
async def reply(message: Message, bot: Bot):
    group_message_id = message.reply_to_message.message_id
    user_id = await map_repo.get_user_id(group_message_id)
    if not user_id:
        return

    header = f'💬 Ответ на сообщение #{group_message_id}\n\n'

    try:
        await bot.send_message(user_id, header)
        await bot.copy_message(user_id, setting.group_id, message.message_id)

        await message.reply('Сообщение успешно отправлено пользователю!')
    except Exception as e:
        logging.error(e)
        await message.reply('Не удалось отправить сообщение пользователю')


@admin_message_router.message(Command('ban'), IsAdmin())
async def ban_user(message: Message, command: CommandObject):
    user_id = command.args

    if not user_id:
        await message.answer('Укажите ID пользователя, например <code>/ban 123</code>')
        return

    if user_id in map(str, setting.admin_ids):
        await message.answer(
            'Указанный ID пользователя в списке администраторов. Действие отменено.'
        )
        return

    is_ok = await users_repo.ban_user(user_id)

    if is_ok:
        await message.answer(f'Пользователь с ID <i>{user_id}</i> забанен')
    else:
        await message.answer(f'Не удалось забанить пользователя с ID: <i>{user_id}</i>')


@admin_message_router.message(Command('unban'), IsAdmin())
async def unban_user(message: Message, command: CommandObject):
    user_id = command.args

    if not user_id:
        await message.answer(
            'Укажите ID пользователя, например <code>/unban 123</code>'
        )
        return

    is_ok = await users_repo.unban_user(user_id)

    if is_ok:
        await message.answer(f'Пользователь с ID <i>{user_id}</i> разбанен')
    else:
        await message.answer(
            f'Не удалось разбанить пользователя с ID: <i>{user_id}</i>'
        )
