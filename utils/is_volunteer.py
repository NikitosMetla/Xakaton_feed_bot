import traceback
from functools import wraps

from aiogram.fsm.context import FSMContext

from aiogram import types, Bot




def is_volunteer(func):
    @wraps(func)
    async def wrapper(message: types.Message | types.CallbackQuery, state: FSMContext, bot: Bot, **kwargs):
        # print("========================= " + func.__name__ + " ============================")
        try:
            is_volunteer = True
            if is_volunteer:
                # print('Проверка на подписку пройдена')
                return await func(message, state, bot, **kwargs)
            elif type(message) == types.Message:
                await message.delete()
                await message.answer(f"Дорогой друг, ты не являешься волонтером в данном боте, твой telegram_id для"
                                     f" добавления: <b>{message.from_user.id}</b>")
            else:
                await message.message.answer(f"Дорогой друг, ты не являешься волонтером в данном боте, твой telegram_id для"
                                             f" добавления: <b>{message.from_user.id}</b>")
        except Exception:
            print(traceback.format_exc())
        # finally:
        #     # print("========================= " + func.__name__ + " ============================")

    return wrapper
