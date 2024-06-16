import math
from typing import List, Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import CallPoints, Feeds, Calls, FeedTransfers, Animals, Volunteers


class Paginator:
    def __init__(self,
                 items,
                 name_of_paginator: str = None,
                 page_now=0,
                 per_page=10):
        self.items = items
        self.per_page = per_page
        self.page_now = page_now
        self.name_paginator = name_of_paginator

    def _generate_page(self):
        ...

    def __str__(self):
        ...


class PointsPaginator(Paginator):
    def __init__(self, items, page_now=1, per_page=5):
        super().__init__(items=items,
                         page_now=page_now,
                         per_page=per_page,
                         name_of_paginator='points_paginator')

    def _generate_page(self) -> InlineKeyboardMarkup:
        self.items: List[CallPoints]
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            key_text = key_data.name_of_point
            page_kb.row(InlineKeyboardButton(text=key_text,
                                             callback_data=f'{self.name_paginator}:look_key:{key_data.id}'))

        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.name_paginator}:page_prev_keys:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(self.items.__len__() / self.per_page)}',
                                         callback_data=f'{self.name_paginator}:page_now:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.name_paginator}:page_next_keys:{self.page_now}'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в стартовое меню',
                                         callback_data='back_to_volunteer_start'))

        return page_kb.as_markup()

    def generate_next_page(self) -> InlineKeyboardMarkup:
        self.page_now += 1
        return self._generate_page()

    def generate_prev_page(self) -> InlineKeyboardMarkup:
        self.page_now -= 1
        return self._generate_page()

    def generate_now_page(self) -> InlineKeyboardMarkup:
        return self._generate_page()


class FeedsPaginator(Paginator):
    def __init__(self, items, page_now=1, per_page=5):
        super().__init__(items=items,
                         page_now=page_now,
                         per_page=per_page,
                         name_of_paginator='feeds_paginator')

    def _generate_page(self):
        self.items: List[Feeds]
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            key_text = key_data.category_of_feed + ": " + key_data.kind_of_animal
            page_kb.row(InlineKeyboardButton(text=key_text,
                                             callback_data=f'{self.name_paginator}:feed:{key_data.id}'))

        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.name_paginator}:feed_page_prev_keys:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(self.items.__len__() / self.per_page)}',
                                         callback_data=f'{self.name_paginator}:feed_page_now:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.name_paginator}:feed_page_next_keys:{self.page_now}'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в стартовое меню',
                                         callback_data='back_to_volunteer_start'))

        return page_kb

    def generate_next_page(self):
        self.page_now += 1
        return self._generate_page()

    def generate_prev_page(self):
        self.page_now -= 1
        return self._generate_page()

    def generate_now_page(self):
        return self._generate_page()


class CallsPaginator(Paginator):
    def __init__(self, items, page_now=1, per_page=5):
        super().__init__(items=items,
                         page_now=page_now,
                         per_page=per_page,
                         name_of_paginator='calls_paginator')

    def _generate_page(self):
        self.items: List[Calls]
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            key_text = str(key_data.volunteer.user_id) + " -> " + key_data.call_point.name_of_point
            page_kb.row(InlineKeyboardButton(text=key_text,
                                             callback_data=f'{self.name_paginator}:call:{key_data.id}'))

        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.name_paginator}:call_page_prev_keys:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(self.items.__len__() / self.per_page)}',
                                         callback_data=f'{self.name_paginator}:call_page_now:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.name_paginator}:call_page_next_keys:{self.page_now}'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в стартовое меню',
                                         callback_data='back_to_volunteer_start_without'))

        return page_kb

    def generate_next_page(self):
        self.page_now += 1
        return self._generate_page()

    def generate_prev_page(self):
        self.page_now -= 1
        return self._generate_page()

    def generate_now_page(self):
        return self._generate_page()


class TransfersPaginator(Paginator):
    def __init__(self, items, page_now=1, per_page=5):
        super().__init__(items=items,
                         page_now=page_now,
                         per_page=per_page,
                         name_of_paginator='transfers_paginator')

    def _generate_page(self):
        self.items: List[FeedTransfers]
        self.items = self.items[::-1]
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            key_text = str(key_data.volunteer.user_id) + " -> " + str(key_data.volunteer.id)
            page_kb.row(InlineKeyboardButton(text=key_text,
                                             callback_data=f'{self.name_paginator}:transfer:{key_data.id}'))

        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.name_paginator}:transfer_page_prev_keys:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(self.items.__len__() / self.per_page)}',
                                         callback_data=f'{self.name_paginator}:transfer_page_now:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.name_paginator}:transfer_page_next_keys:{self.page_now}'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в стартовое меню',
                                         callback_data='back_to_volunteer_start_without'))

        return page_kb

    def generate_next_page(self):
        self.page_now += 1
        return self._generate_page()

    def generate_prev_page(self):
        self.page_now -= 1
        return self._generate_page()

    def generate_now_page(self):
        return self._generate_page()


class AnimalsPaginator(Paginator):
    def __init__(self, items, page_now=1, per_page=5):
        super().__init__(items=items,
                         page_now=page_now,
                         per_page=per_page,
                         name_of_paginator='animals_paginator')

    def _generate_page(self):
        self.items: List[Animals]
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            key_text = key_data.animal + " по кличке " + key_data.name + " породы " + key_data.breed
            page_kb.row(InlineKeyboardButton(text=key_text,
                                             callback_data=f'{self.name_paginator}:animal:{key_data.id}'))

        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.name_paginator}:animal_page_prev_keys:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(self.items.__len__() / self.per_page)}',
                                         callback_data=f'{self.name_paginator}:animal_page_now:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.name_paginator}:animal_page_next_keys:{self.page_now}'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в стартовое меню',
                                         callback_data='back_to_volunteer_start_without'))

        return page_kb

    def generate_next_page(self):
        self.page_now += 1
        return self._generate_page()

    def generate_prev_page(self):
        self.page_now -= 1
        return self._generate_page()

    def generate_now_page(self):
        return self._generate_page()


class VolunteersPaginator(Paginator):
    def __init__(self, items, page_now=1, per_page=5):
        super().__init__(items=items,
                         page_now=page_now,
                         per_page=per_page,
                         name_of_paginator='animals_paginator')

    def _generate_page(self):
        self.items: List[Volunteers]
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in self.items[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            key_text = key_data.surname + " " + key_data.firstname + " " + key_data.patronymic
            page_kb.row(InlineKeyboardButton(text=key_text,
                                             callback_data=f'{self.name_paginator}:volunteer:{key_data.id}'))

        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.name_paginator}:animal_page_prev_keys:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(self.items.__len__() / self.per_page)}',
                                         callback_data=f'{self.name_paginator}:volunteer_page_now:{self.page_now}'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.name_paginator}:volunteer_page_next_keys:{self.page_now}'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в стартовое меню',
                                         callback_data='back_to_volunteer_start_without'))

        return page_kb

    def generate_next_page(self):
        self.page_now += 1
        return self._generate_page()

    def generate_prev_page(self):
        self.page_now -= 1
        return self._generate_page()

    def generate_now_page(self):
        return self._generate_page()

