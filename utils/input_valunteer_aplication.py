from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings import volunteer_application


async def input_volunteer_application(number_answer):
    keyboard = InlineKeyboardBuilder()
    if number_answer != 0:
        keyboard.row(InlineKeyboardButton(text="🔙Предыдущая графа", callback_data=f"graph|{number_answer - 1}"))
    keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_admin"))
    return keyboard