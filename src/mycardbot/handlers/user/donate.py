from contextlib import suppress

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from mycardbot.keyboards.user import (
    get_donate_keyboard,
    get_invoice_keyboard,
)
from mycardbot.utils.content import load_html_content

user_donate_router = Router()


@user_donate_router.callback_query(F.data == 'donate')
async def handle_donate(callback: CallbackQuery):
    text = load_html_content('donate')
    await callback.message.edit_text(text=text, reply_markup=get_donate_keyboard())


@user_donate_router.callback_query(F.data.endswith('_stars'))
async def handle_donate_invoice(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.delete()
    amount = int(callback.data.split('_')[0])
    prices = [
        LabeledPrice(label='XTR', amount=amount),
    ]

    await callback.message.answer_invoice(
        title='Донат',
        description='Спасибо за поддержку автора ❤️',
        payload=f'{amount}_stars',
        provider_token='',
        currency='XTR',
        prices=prices,
        reply_markup=get_invoice_keyboard(amount),
    )


@user_donate_router.callback_query(F.data == 'cancel_donate')
async def handle_cancel_donate(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.delete()
    text = load_html_content('donate')
    await callback.message.answer(text, reply_markup=get_donate_keyboard())


@user_donate_router.pre_checkout_query()
async def handle_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@user_donate_router.message(F.successful_payment)
async def handle_successful_payment(message: Message):

    payment = message.successful_payment

    await message.answer(f'Спасибо за донат ⭐\nПолучено Stars: {payment.total_amount}')
