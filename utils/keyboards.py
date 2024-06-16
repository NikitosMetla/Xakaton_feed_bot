from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel

"""OWNER"""
owner_start_keyboard = InlineKeyboardBuilder()
owner_start_keyboard.row(InlineKeyboardButton(text="Сообщить о заполненности точки", callback_data="inform_point"))
# owner_start_keyboard.row(InlineKeyboardButton(text="Связаться с администратором", callback_data="connect_admin"))
""""""


"""ADMIN"""
admin_start_keyboard = InlineKeyboardBuilder()
admin_start_keyboard.row(InlineKeyboardButton(text="Работа с волонтерами", callback_data="edit_volunteer"))
admin_start_keyboard.row(InlineKeyboardButton(text="Работа с точками", callback_data="edit_point"))
admin_start_keyboard.row(InlineKeyboardButton(text="Работа с кормом", callback_data="edit_feed"))
admin_start_keyboard.row(InlineKeyboardButton(text="Работа с получениями", callback_data="work_calls"))
admin_start_keyboard.row(InlineKeyboardButton(text="Работа с передачами", callback_data="work_transfer"))

edit_volunteer_keyboard = InlineKeyboardBuilder()
edit_volunteer_keyboard.row(InlineKeyboardButton(text="Добавить волонтера", callback_data="add_volunteer"))
edit_volunteer_keyboard.row(InlineKeyboardButton(text="Информация о волонтерах", callback_data="info_volunteer"))

edit_point_keyboard = InlineKeyboardBuilder()
edit_point_keyboard.row(InlineKeyboardButton(text="Добавить точку", callback_data="add_point"))
# edit_point_keyboard.row(InlineKeyboardButton(text="Удалить точку", callback_data="delete_point"))

edit_feed_keyboard = InlineKeyboardBuilder()
edit_feed_keyboard.row(InlineKeyboardButton(text="Добавить корм", callback_data="add_feed"))
# edit_feed_keyboard.row(InlineKeyboardButton(text="Удалить корм", callback_data="delete_feed"))


async def confirm_application(message_id, entity:str):
    confirm_application = InlineKeyboardBuilder()
    confirm_application.row(InlineKeyboardButton(text="ДА", callback_data=f"confirm_cancel_{entity}|{message_id}"))
    confirm_application.row(InlineKeyboardButton(text="НЕТ", callback_data=f"not_confirm_cancel_{entity}"))
    return confirm_application
""""""



"""VOLUNTEER"""
volunteer_start_keyboard = InlineKeyboardBuilder()
volunteer_start_keyboard.row(InlineKeyboardButton(text="Принять корм", callback_data="get_animal_food"))
volunteer_start_keyboard.row(InlineKeyboardButton(text="Передать корм", callback_data="transfer_animal_food"))
volunteer_start_keyboard.row(InlineKeyboardButton(text="Четвероногие друзья", callback_data="my_animals"))


photo_call_keyboard = InlineKeyboardBuilder()
photo_call_keyboard.row(InlineKeyboardButton(text="Добавить фотографию для отчета", callback_data="send_photo_call"))
photo_call_keyboard.row(InlineKeyboardButton(text="Закончить отправку фотографий", callback_data="ending_photo_call"))
photo_call_keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_volunteer"))


cancel_volunteer_keyboard = InlineKeyboardBuilder()
cancel_volunteer_keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_volunteer"))
""""""

class InputVolunteers(BaseModel):
    surname: str = None
    firstname: str = None
    patronymic: str = None
    email: str = None
    phone: str = None
    work_experience: str = None