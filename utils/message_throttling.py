import asyncio
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from db.repository import users_repository
from settings import MESSAGE_SPAM_TIMING


class MessageSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.storage = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """
        {'timestamp': 123001, 'spam_block': False}
        """

        user_id = f'{event.from_user.id}'

        user_data = await users_repository.get_user_by_user_id(user_id=event.from_user.id)
        data['user_data'] = user_data
        print(user_data)
        if not user_data:
            print("ssdfsdfgsdgfsdfgsd")
            await users_repository.add_user(user_id=event.from_user.id, username=event.from_user.username)

        check_user = self.storage.get(user_id)
        if check_user:

            if check_user['spam_block']:
                return

            if time.time() - check_user['timestamp'] <= MESSAGE_SPAM_TIMING:
                self.storage[user_id]['timestamp'] = time.time()
                self.storage[user_id]['spam_block'] = True
                await event.answer(f'<b>Обнаружена подозрительная активность.</b>')
                await asyncio.sleep(MESSAGE_SPAM_TIMING)
                self.storage[user_id]['spam_block'] = False
                return

        self.storage[user_id] = {'timestamp': time.time(), 'spam_block': False}
        return await handler(event, data)
