import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from mycardbot.database.users import users_repo
from mycardbot.filters.check_admin import IsAdmin
from mycardbot.keyboards.admin import (
    get_cancel_broadcast_keyboard,
    get_main_keyboard,
    get_paginated_keyboard,
)
from mycardbot.states.admin import BroadcastStates
from mycardbot.utils.content import load_html_content
from mycardbot.utils.format import format_users

admin_callback_router = Router()


@admin_callback_router.callback_query(F.data == 'admin_menu', IsAdmin())
async def menu(callback: CallbackQuery) -> None:
    text = load_html_content('admin')
    text = text.replace('{name}', html.escape(callback.from_user.first_name))
    await callback.message.edit_text(text, reply_markup=get_main_keyboard())
    await callback.answer()


@admin_callback_router.callback_query(F.data == 'admin_broadcast', IsAdmin())
async def proceed_broadcast(callback: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await callback.message.delete()
    text = load_html_content('admin_broadcast')
    await callback.message.answer(text, reply_markup=get_cancel_broadcast_keyboard())
    await state.set_state(BroadcastStates.waiting_for_message)
    await callback.answer()


@admin_callback_router.callback_query(F.data == 'admin_list', IsAdmin())
async def list_users(callback: CallbackQuery) -> None:
    data = await users_repo.list_users_paginated()
    text = format_users(data)

    await callback.message.edit_text(
        text, reply_markup=get_paginated_keyboard(data['total_pages'])
    )
    await callback.answer()


@admin_callback_router.callback_query(F.data.startswith('page_'), IsAdmin())
async def handle_pagination(callback: CallbackQuery) -> None:
    page_number = int(callback.data.split('_')[-1])
    data = await users_repo.list_users_paginated(page_number=page_number)
    text = format_users(data)

    await callback.message.edit_text(
        text, reply_markup=get_paginated_keyboard(data['total_pages'], page_number)
    )
    await callback.answer()


@admin_callback_router.callback_query(
    (F.data == 'current') | (F.data == 'none'), IsAdmin()
)
async def handle_pagination_empty(callback: CallbackQuery) -> None:
    await callback.answer()
