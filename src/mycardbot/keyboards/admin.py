from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🏠 Главная', callback_data='menu')
    builder.button(text='👥 Список пользователей', callback_data='admin_list')
    builder.button(text='📨 Создать рассылку', callback_data='admin_broadcast')
    builder.adjust(1)
    return builder.as_markup()


def get_return_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙 Вернуться назад', callback_data='admin_menu')
    return builder.as_markup()


def get_cancel_broadcast_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Отменить')
    return builder.as_markup(resize_keyboard=True)


def get_proceed_broadcast_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Подтвердить')
    builder.button(text='Отменить')
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_paginated_keyboard(total_pages: int, page_number: int = 1):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='◀️ Назад' if page_number > 1 else ' ',
        callback_data=f'page_{page_number - 1}' if page_number > 1 else 'none',
    )
    builder.button(text=f'{page_number}/{total_pages}', callback_data='current')
    builder.button(
        text='Вперед ▶️' if page_number < total_pages else ' ',
        callback_data=f'page_{page_number + 1}'
        if page_number < total_pages
        else 'none',
    )
    builder.button(text='🔙 Вернуться в главное меню', callback_data='admin_menu')
    builder.adjust(3, 1)
    return builder.as_markup()
