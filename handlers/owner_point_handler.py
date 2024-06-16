from aiogram import Router, types, Bot, F
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton, Message

from db.repository import call_points_repository
from utils.keyboards import owner_start_keyboard

owner_router = Router()


@owner_router.message(Command('owner'), any_state)
async def owner(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Здравствуй, выбери свои следующие действия",
                         reply_markup=owner_start_keyboard.as_markup())


@owner_router.callback_query(Text(text="inform_point"), any_state)
async def owner_send(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    point = await call_points_repository.get_call_points_by_owner_user_id(int(message.from_user.id))
    volunteer_telegram_id = point[0].volunteer.user_id
    await bot.send_message(chat_id=int(volunteer_telegram_id),
                           text=f"Администратор точки{point[0].name_of_point} оповещает вас о том,"
                                f" что точка заполнена и требует сбора корма")
    await message.message.answer("Прикрепленный волонтер к вашей точке успешно оповещен о переполнении")
    await message.message.delete()