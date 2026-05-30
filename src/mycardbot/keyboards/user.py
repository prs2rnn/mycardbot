from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='👤 Now', callback_data='now')
    builder.button(text='📝 CV', callback_data='cv')
    builder.button(text='💬 Связаться c автором', callback_data='feedback')
    builder.button(text='🌐 Сайт', url='https://prs2rnn.github.io/')
    builder.button(text='📨 Рассылка', callback_data='broadcast')
    builder.button(text='📦 Что нового', callback_data='changelog')
    builder.adjust(2)
    return builder.as_markup()


def get_return_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙 Вернуться на главную', callback_data='menu')
    return builder.as_markup()


def get_main_feedback_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить сообщение', callback_data='send')
    builder.button(text='Другие способы связи', callback_data='contact')
    builder.button(text='🔙 Вернуться на главную', callback_data='menu')
    builder.adjust(2, 1)
    return builder.as_markup()


def get_return_feedback_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙 Вернуться назад', callback_data='feedback')
    return builder.as_markup()


def get_cancel_feedback_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Отменить')
    return builder.as_markup(resize_keyboard=True)


def get_proceed_feedback_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Подтвердить')
    builder.button(text='Отменить')
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_cv_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='💬 Связаться c автором', callback_data='feedback')
    builder.button(text='🔙 Вернуться на главную', callback_data='menu')
    builder.adjust(1)
    return builder.as_markup()


def get_broadcast_keyboard(is_subscribed: bool):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=(
            '🔔 Подписаться на рассылку'
            if not is_subscribed
            else '🔕 Отписаться от рассылки'
        ),
        callback_data='subscribe' if not is_subscribed else 'unsubscribe',
    )
    builder.button(text='🔙 Вернуться на главную', callback_data='menu')
    builder.adjust(1)
    return builder.as_markup()


def get_changelog_paginated_keyboard(
    version: str, total_pages: int, page_number: int = 0
):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='◀️ Назад' if page_number > 0 else ' ',
        callback_data=f'changelog_{page_number - 1}' if page_number > 0 else 'none',
    )
    builder.button(text=version, callback_data='current')
    builder.button(
        text='Вперед ▶️' if page_number < total_pages - 1 else ' ',
        callback_data=f'changelog_{page_number + 1}'
        if page_number < total_pages - 1
        else 'none',
    )
    builder.button(text='🔙 Вернуться на главную', callback_data='menu')
    builder.adjust(3, 1)
    return builder.as_markup()
