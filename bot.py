import asyncio

from aiogram import Bot, Dispatcher

from db.engine import DatabaseEngine
from handlers.admin_handler import admin_router
from handlers.owner_point_handler import owner_router
from handlers.volunteer_handler import volunteer_router
from settings import bot_token, storage_bot
from utils.callback_throttling import CallbackSpamMiddleware
from utils.message_throttling import MessageSpamMiddleware

bot = Bot(token=bot_token, parse_mode="HTML")


async def main():
    # db_engine = DatabaseEngine()
    # await db_engine.proceed_schemas()
    print(await bot.get_me())
    dp = Dispatcher(storage=storage_bot)
    dp.message.middleware.register(MessageSpamMiddleware())
    dp.callback_query.middleware.register(CallbackSpamMiddleware())
    dp.include_routers(admin_router, volunteer_router, owner_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())