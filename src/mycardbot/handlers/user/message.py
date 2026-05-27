from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from mycardbot.database.users import users_repo
from mycardbot.keyboards.user import (
    get_main_feedback_keyboard,
    get_main_keyboard,
    get_proceed_feedback_keyboard,
)
from mycardbot.services.broadcast import send_notification, send_user_message
from mycardbot.states.user import FeedbackStates
from mycardbot.utils.content import load_html_content

user_message_router = Router()


@user_message_router.message(CommandStart())
async def start(message: Message, bot: Bot) -> None:
    text = load_html_content('start')
    await message.answer(text, reply_markup=get_main_keyboard())

    user = message.from_user

    is_added = await users_repo.add_user(user.full_name, user.username, user.id)

    if is_added:
        await send_notification(bot, user.full_name, user.username, user.id)


@user_message_router.message(
    StateFilter(FeedbackStates.waiting_for_message), F.text == 'Отменить'
)
async def cancel_proceed_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())
    text = load_html_content('feedback')
    await message.answer(text, reply_markup=get_main_feedback_keyboard())


@user_message_router.message(
    StateFilter(FeedbackStates.waiting_for_message),
)
async def handle_proceed_feedback(message: Message, state: FSMContext):
    await state.update_data(pending_message_id=message.message_id)

    await message.answer(
        'Подтвердите или отмените отправку',
        reply_markup=get_proceed_feedback_keyboard(),
    )
    await state.set_state(state=None)
    await state.set_state(FeedbackStates.waiting_for_confirmation)


@user_message_router.message(
    StateFilter(FeedbackStates.waiting_for_confirmation), F.text == 'Подтвердить'
)
async def confirm_feedback(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get('pending_message_id')
    user = message.from_user

    await send_user_message(bot, user, message_id)

    await state.clear()
    text = load_html_content('start')
    await message.answer(text, reply_markup=get_main_keyboard())


@user_message_router.message(
    StateFilter(FeedbackStates.waiting_for_confirmation), F.text == 'Отменить'
)
async def cancel_confirm_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())
    text = load_html_content('feedback')
    await message.answer(text, reply_markup=get_main_feedback_keyboard())


@user_message_router.message(StateFilter(FeedbackStates.waiting_for_confirmation))
async def handle_confirm_feedback(message: Message, state: FSMContext):
    await message.answer(
        'Подтвердите или отмените отправку',
        reply_markup=get_proceed_feedback_keyboard(),
    )
