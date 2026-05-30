from contextlib import suppress

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from mycardbot.database.users import users_repo
from mycardbot.keyboards.user import (
    get_broadcast_keyboard,
    get_cancel_feedback_keyboard,
    get_changelog_paginated_keyboard,
    get_cv_keyboard,
    get_main_feedback_keyboard,
    get_main_keyboard,
    get_return_feedback_keyboard,
    get_return_keyboard,
)
from mycardbot.services.broadcast import get_image_on_subscribe
from mycardbot.services.github import get_changelog
from mycardbot.states.user import FeedbackStates
from mycardbot.utils.content import load_html_content

user_callback_router = Router()


@user_callback_router.callback_query(F.data == 'now')
async def now(callback: CallbackQuery):
    text = load_html_content('now')
    await callback.message.edit_text(text, reply_markup=get_return_keyboard())
    await callback.answer()


@user_callback_router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery):
    text = load_html_content('start')
    await callback.message.edit_text(text, reply_markup=get_main_keyboard())
    await callback.answer()


@user_callback_router.callback_query(F.data == 'feedback')
async def feedback(callback: CallbackQuery, state: FSMContext):
    text = load_html_content('feedback')
    await callback.message.edit_text(text, reply_markup=get_main_feedback_keyboard())
    await callback.answer()


@user_callback_router.callback_query(F.data == 'send')
async def proceed_feedback(callback: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await callback.message.delete()
    await callback.message.answer(
        'Напишите ваше сообщение', reply_markup=get_cancel_feedback_keyboard()
    )
    await state.set_state(FeedbackStates.waiting_for_message)
    await callback.answer()


@user_callback_router.callback_query(F.data == 'contact')
async def contact(callback: CallbackQuery):
    text = load_html_content('contact')
    await callback.message.edit_text(text, reply_markup=get_return_feedback_keyboard())
    await callback.answer()


@user_callback_router.callback_query(F.data == 'cv')
async def cv(callback: CallbackQuery):
    text = load_html_content('cv')
    await callback.message.edit_text(text, reply_markup=get_cv_keyboard())
    await callback.answer()


@user_callback_router.callback_query(F.data == 'broadcast')
async def broadcast(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed = await users_repo.check_subscription(user_id)
    text = load_html_content('broadcast')
    await callback.message.edit_text(
        text, reply_markup=get_broadcast_keyboard(is_subscribed)
    )
    await callback.answer()


@user_callback_router.callback_query(F.data == 'unsubscribe')
@user_callback_router.callback_query(F.data == 'subscribe')
async def proceed_subscription(callback: CallbackQuery, bot: Bot):
    user = callback.from_user
    is_subscribed = await users_repo.check_subscription(user.id)

    if is_subscribed is None:
        await users_repo.add_user(user.full_name, user.username, user.id)

    await (
        users_repo.subscribe_user(user.id)
        if not is_subscribed
        else users_repo.unsubscribe_user(user.id)
    )

    if not is_subscribed:
        await callback.answer('Вы подписались на рассылку!')
        await get_image_on_subscribe(bot, user.id)
    else:
        await callback.answer('Вы отписались от рассылки!')

    await callback.message.delete()

    text = load_html_content('broadcast')
    await callback.message.answer(
        text, reply_markup=get_broadcast_keyboard(not is_subscribed)
    )


@user_callback_router.callback_query(F.data == 'changelog')
async def handle_changelog(callback: CallbackQuery):
    releases = await get_changelog()
    total_pages = len(releases)
    if not releases:
        text = 'Не удалось получить информацию от сервера'
    else:
        release = releases[0]
        text = f'{release["text"]}\n\n'

    version = release['version'] if releases else ''

    await callback.message.edit_text(
        text, reply_markup=get_changelog_paginated_keyboard(version, total_pages)
    )


@user_callback_router.callback_query(F.data.startswith('changelog_'))
async def handle_changelog_pagination(callback: CallbackQuery) -> None:
    page_number = int(callback.data.split('_')[-1])
    releases = await get_changelog()
    total_pages = len(releases)

    if not releases:
        text = 'Не удалось получить информацию от сервера'
    else:
        release = releases[page_number]
        text = f'{release["text"]}\n\n'

    version = release['version'] if releases else ''

    await callback.message.edit_text(
        text,
        reply_markup=get_changelog_paginated_keyboard(
            version, total_pages, page_number
        ),
    )
    await callback.answer()


@user_callback_router.callback_query((F.data == 'current') | (F.data == 'none'))
async def handle_changelog_empty_pagination(callback: CallbackQuery) -> None:
    await callback.answer()
