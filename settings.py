from os import getenv

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("../.env"))
bot_token = str(getenv("BOT_TOKEN"))
bot_token = ""
print(bot_token)
storage_bot = MemoryStorage()
CALLBACK_SPAM_TIMING = 0
MESSAGE_SPAM_TIMING = 0

volunteer_application = {
    "Фамилия": "Введи фамилию волонтера одним сообщением",
    "Имя": "Введи имя волонтера одним сообщением",
    "Отчество": "Введи отчество волонтера одним сообщением",
    "Почта": "Введи почту волонтера",
    "Телефон": "Введи телефон волонтера",
    "Фото": "Пришли одно фото волонтера одним",
    "Паспорт": "Пришли одно фото паспорта волонтера",
    "Опыт": "Введи опыт волонтера одним сообщением",
    "Telegram_id": "Введи telegram_id волонтера одним сообщением"
}


point_application = {
    "Название": "Введи название точки одним сообщением",
    "Описание": "Введи описание точки одним сообщением",
    "Телефон": "Введи телефон точки",
    "Геолокация": "Пришли геолокацию точки",
    "Telegram id волонтера": "Введи telegram_id волонтера, который будет прикреплен к точке",
    "owner_telegram_id": "Введи telegram_id администратора точки"
}


get_foot_application = {
    "Название": "Введи название точки одним сообщением",
    "Описание": "Введи описание точки одним сообщением",
    "Адрес": "Введи адрес точки одним сообщением",
    "Телефон": "Введи телефон точки",
    "Геолокация": "Пришли геолокацию точки",
    "owner_telegram_id": "Введи telegram_id администратора точки"
}


class InputMessage(StatesGroup):
    AddVolunteer = State()
    AddPoint = State()
    GetAnimalFood = State()
    TransferAnimalFood = State()
    GivePhotoCall = State()
    AddCategoryFeed = State()
    AddKindFeed = State()
    FeedBasket = State()
    GetRecipientId = State()
    GivePhotoTransfer = State()
    TransferFeedBasket = State()
