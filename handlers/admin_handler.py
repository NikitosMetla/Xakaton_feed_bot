import io
import traceback

from aiogram import Router, types, Bot, F
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton, Message, InputFile, InputMediaPhoto, CallbackQuery, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Feeds, CallsBaskets, FeedTransfersBuskets
from db.repository import volunteers_repository, call_points_repository, feeds_repository, users_repository, \
    calls_repository, receiving_albums_repository, calls_baskets_repository, feed_transfers_repository, \
    feed_transfers_buskets_repository, transfers_albums_repository
from settings import volunteer_application, InputMessage, point_application
from utils.input_valunteer_aplication import input_volunteer_application
from utils.is_main_admin import is_main_admin
from utils.keyboards import admin_start_keyboard, edit_volunteer_keyboard, edit_point_keyboard, confirm_application, \
    edit_feed_keyboard
from utils.paginator import PointsPaginator, CallsPaginator, TransfersPaginator, VolunteersPaginator
from utils.pdf_generate import PdfExtractor
from utils.text_application import text_application

admin_router = Router()


@admin_router.message(Command('start'), any_state)
async def admin(message: Message | CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await users_repository.get_user_by_user_id(user_id=message.from_user.id)
    print(user_data)
    if not user_data:
        print("ssdfsdfgsdgfsdfgsd")
        await users_repository.add_user(user_id=message.from_user.id, username=message.from_user.username)

@admin_router.message(Command('admin'), any_state)
@is_main_admin
async def admin(message: Message | CallbackQuery, state: FSMContext, bot: Bot):
    if type(message) == types.CallbackQuery:
        if message.data != "back_to_volunteer_start_without":
            keyboard = await confirm_application(message.message.message_id, entity="admin")
            await message.message.answer("Ты уверен, что хочешь отменить добавление? <b>ВСЕ ДАННЫЕ БУДУТ УДАЛЕНЫ!</b>",
                                         reply_markup=keyboard.as_markup())
            await state.clear()
        else:
            await state.clear()
            await message.message.answer("Вы находитесь на стартовой панели, выберите свои дальнейшие действия",
                                 reply_markup=admin_start_keyboard.as_markup())
            await message.message.delete()

        return
    await state.clear()
    await message.answer("Вы находитесь на стартовой панели, выберите свои дальнейшие действия",
                         reply_markup=admin_start_keyboard.as_markup())


@admin_router.callback_query(Text(text="info_volunteer"), any_state)
async def get_point_for_get_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    volunteer = await volunteers_repository.select_volunteer_by_user_id(int(call.from_user.id))
    points = await volunteers_repository.select_all_volunteers()
    keyboard = VolunteersPaginator(points).generate_now_page()
    await call.message.edit_text(text="Список волонтеров", reply_markup=keyboard.as_markup())


@admin_router.callback_query(Text(startswith="work_calls"), any_state)
async def info_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    points = await calls_repository.select_all_calls()
    keyboard = CallsPaginator(items=points).generate_now_page()
    await call.message.edit_text(text="Выбери получения волонтером", reply_markup=keyboard.as_markup())


@admin_router.callback_query(Text(text="back_to_volunteer_start_without"), any_state)
async def back_from_calls(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await admin(call, state, bot)


@admin_router.callback_query(Text(startswith="work_transfer"), any_state)
async def info_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    points = await feed_transfers_repository.select_all_feed_transfers()
    keyboard = TransfersPaginator(items=points).generate_now_page()
    await call.message.edit_text(text="Выбери получения волонтером", reply_markup=keyboard.as_markup())


@admin_router.callback_query(Text(text="back_to_volunteer_start_without"), any_state)
async def back_from_calls(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await admin(call, state, bot)


@admin_router.callback_query(Text(startswith="transfers_paginator"), any_state)
async def get_calls(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split(":")
    if data[1] == "transfer":
        my_transfer = await feed_transfers_repository.get_feed_transfer_info_by_id(int(data[2]))
        who_get = my_transfer.volunteer.firstname + " " + my_transfer.volunteer.surname
        creation_date = my_transfer.creation_date
        who_give = await volunteers_repository.select_volunteer_by_user_id(my_transfer.user_id)
        fio = [who_give.firstname, who_give.surname, who_give.patronymic]
        feeds = await feed_transfers_buskets_repository.get_feed_transfer_baskets_by_feed_transfer_id(int(data[2]))
        photos = await transfers_albums_repository.get_transfer_albums_by_feed_transfer_id(int(data[2]))
        photos_ids = [photo.photo_id for photo in photos]
        buffers = [io.BytesIO() for i in photos_ids]
        for i in range(len(buffers)):
            await bot.download(photos_ids[i], destination=buffers[i])
        print("\n\n1\n\n")
        pdf_extractor = PdfExtractor(title=" ".join(fio) + " получение " + f"id передачи: {my_transfer.id}")
        pdf_extractor.add_text(f'Получатель: {my_transfer.volunteer.firstname} {my_transfer.volunteer.surname}\n')
        pdf_extractor.add_text(f'Дата создания графы: {creation_date}\n')
        pdf_extractor.add_text('ФИО отправителя: ' + ' '.join(fio))
        for feed in feeds:
            feed: FeedTransfersBuskets
            """
            сюда дописать в каком именно виде будет
            """
            pdf_extractor.add_text(
                feed.feed.category_of_feed + ": " + feed.feed.kind_of_animal + " = " + str(feed.count_feed) + " кг\n")

        for photo in buffers:
            pdf_extractor.add_image(photo)
            pdf_extractor.add_text("/n")

        file_stream = io.BytesIO(pdf_extractor.save_pdf())
        # file_stream.seek(0)
        file_name = f'Передача_{my_transfer.id}.pdf'
        input_file = BufferedInputFile(file_stream.read(), filename=file_name)
        await call.message.answer_document(caption='Вот отчет о выбранно тобой операции',
                                           document=input_file)
        await call.message.delete()




    elif data[1] == "transfer_page_prev_keys":
        points = await feed_transfers_repository.select_all_feed_transfers()
        keyboard = TransfersPaginator(items=points).generate_prev_page()
        try:
            await call.message.edit_text(text="Выбери получения волонтером", reply_markup=keyboard.as_markup())
        except:
            return
    else:
        points = await feed_transfers_repository.select_all_feed_transfers()
        keyboard = TransfersPaginator(items=points).generate_next_page()
        try:
            await call.message.edit_text(text="Выбери получения волонтером", reply_markup=keyboard.as_markup())
        except:
            return

@admin_router.callback_query(Text(startswith="calls_paginator"), any_state)
async def get_calls(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split(":")
    if data[1] == "call":
        my_call = await calls_repository.get_call_info_by_id(call_id=int(data[2]))
        point_name = my_call.call_point.name_of_point
        creation_date = my_call.creation_date
        fio = [my_call.volunteer.firstname, my_call.volunteer.surname, my_call.volunteer.patronymic]
        feeds = await calls_baskets_repository.get_call_baskets_by_call_id(call_id=int(data[2]))
        photos = await receiving_albums_repository.get_receiving_albums_by_call_id(call_id=int(data[2]))
        photos_ids = [photo.photo_id for photo in photos]
        buffers = [io.BytesIO() for i in photos_ids]
        for i in range(len(buffers)):
            await bot.download(photos_ids[i], destination=buffers[i])
        print("\n\n1\n\n")
        pdf_extractor = PdfExtractor(title=" ".join(fio) + " получение " + f"id получения: {my_call.id}")
        pdf_extractor.add_text(f'Название точки: {point_name}\n')
        pdf_extractor.add_text(f'Дата создания графы: {creation_date}\n')
        pdf_extractor.add_text(f'Координаты точки (можно вставить в приложение карт): {my_call.call_point.latitude}, {my_call.call_point.longitude}\n')
        pdf_extractor.add_text('ФИО: ' + ' '.join(fio))
        for feed in feeds:
            feed: CallsBaskets
            """
            сюда дописать в каком именно виде будет
            """
            pdf_extractor.add_text(feed.feed.category_of_feed + ": " + feed.feed.kind_of_animal + " = " + str(feed.count_feed) + " кг\n")

        for photo in buffers:
            pdf_extractor.add_image(photo)
            pdf_extractor.add_text("/n")

        file_stream = io.BytesIO(pdf_extractor.save_pdf())
        # file_stream.seek(0)
        file_name = f'Получение_{my_call.id}.pdf'
        input_file = BufferedInputFile(file_stream.read(), filename=file_name)
        await call.message.answer_document(caption='Вот отчет о выбранно тобой операции',
                                           document=input_file)
        await call.message.delete()

    elif data[1] == "call_page_prev_keys":
        points = await calls_repository.select_all_calls()
        keyboard = TransfersPaginator(items=points).generate_prev_page()
        try:
            await call.message.edit_text(text="Выбери получения волонтером", reply_markup=keyboard.as_markup())
        except:
            return
    else:
        points = await calls_repository.select_all_calls()
        keyboard = TransfersPaginator(items=points).generate_next_page()
        try:
            await call.message.edit_text(text="Выбери получения волонтером", reply_markup=keyboard.as_markup())
        except:
            return


@admin_router.callback_query(Text(startswith="confirm_cancel_admin|"), any_state)
async def edit_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.delete_message(chat_id=call.from_user.id, message_id=int(call.data.split("|")[1]))
    await call.message.answer("Вы находитесь на стартовой панели, выберите свои дальнейшие действия",
                         reply_markup=admin_start_keyboard.as_markup())
    await call.message.delete()


@admin_router.callback_query(Text(text="not_confirm_cancel_admin"), any_state)
async def edit_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()


@admin_router.callback_query(Text(text="cancel_admin"), any_state)
async def cancel_for_admin(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await admin(call, state, bot)


@admin_router.callback_query(Text(text="edit_volunteer"), any_state)
async def edit_volunteer(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text="Выбери свои действия над волонтерами",
                                 reply_markup=edit_volunteer_keyboard.as_markup())


@admin_router.callback_query(Text(text="edit_feed"), any_state)
async def edit_volunteer(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text="Выбери свои действия над волонтерами",
                                 reply_markup=edit_feed_keyboard.as_markup())


@admin_router.callback_query(Text(text="edit_point"), any_state)
async def edit_point_admin(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text="Выбери свои действия над точками",
                                 reply_markup=edit_point_keyboard.as_markup())


@admin_router.callback_query(Text(text="add_feed"), any_state)
async def admin_add_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(InputMessage.AddCategoryFeed)
    await state.update_data(message_id=call.message.message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_admin"))
    await call.message.edit_text("Напиши категорию корма, которого ты хочешь добавить(Собачий, кошачий и т.д.)",
                                 reply_markup=keyboard.as_markup())


@admin_router.message(F.text, InputMessage.AddCategoryFeed)
@is_main_admin
async def admin_enter_feed_category(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    edit_message_id = data.get("message_id")
    await state.set_state(InputMessage.AddKindFeed)
    await state.update_data(category=message.text, message_id=edit_message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_admin"))
    await bot.edit_message_text(text="Отлично, теперь напиши тип корма одним сообщением, например: влажный, сухой,"
                                     " для стерилизованных кошек и т.д.",
                                reply_markup=keyboard.as_markup(),
                                message_id=edit_message_id,
                                chat_id=message.from_user.id)
    await message.delete()


@admin_router.message(F.text, InputMessage.AddKindFeed)
@is_main_admin
async def admin_enter_feed_kind(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    category = data.get("category")
    kind = message.text
    edit_message_id = data.get("message_id")
    await feeds_repository.add_feed(kind_of_animal=kind,
                                    category=category)
    await message.answer("Отлично, новый корм успешно добавлен")
    await bot.delete_message(chat_id=message.from_user.id, message_id=edit_message_id)
    await message.delete()
    await admin(message, state, bot)
    await state.clear()



@admin_router.callback_query(Text(text="add_volunteer"), any_state)
async def admin_add_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(InputMessage.AddVolunteer)
    key = list(volunteer_application.keys())[0]
    keyboard = await input_volunteer_application(0)
    new_message = await call.message.edit_text(text=volunteer_application.get(key),
                                               reply_markup=keyboard.as_markup())
    await state.update_data(number_question=0, message_id=new_message.message_id)


@admin_router.message(F.text, InputMessage.AddVolunteer)
@is_main_admin
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    number_question = data.get("number_question")
    edit_message = data.get("message_id")
    if number_question not in [5, 6]:
        if number_question == 8:
            try:
                data[list(volunteer_application.keys())[-1]] = message.text
                await bot.send_message(text=f"Тебя сделали волонтером\n\nТвои данные:{text_application(data)}",
                                       chat_id=message.text)

            except:
                keyboard = await input_volunteer_application(number_question)
                data.pop(list(volunteer_application.keys())[-1])
                await state.clear()
                await state.set_state(InputMessage.AddVolunteer)
                await state.update_data(data)
                application_text = "<b>Информация о точке:</b>\n" + text_application(data)
                await message.delete()
                try:
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                                text=application_text + "\n\n" + "Введенного тобой телеграм id не существует, либо у данного пользователя нет чата с данным ботом\n" +
                                                     volunteer_application.get(
                                                         list(volunteer_application.keys())[number_question]),
                                                reply_markup=keyboard.as_markup())
                finally:
                    return
            await volunteers_repository.add_volunteer(surname=data.get("Фамилия"),
                                                      firstname=data.get("Имя"),
                                                      patronymic=data.get("Отчество"),
                                                      phone=data.get("Телефон"),
                                                      email=data.get("Почта"),
                                                      work_experience=data.get("Опыт"),
                                                      user_id=int(data.get("Telegram_id")),
                                                      passport_photo_id=data.get("Паспорт").split("|")[1],
                                                      face_photo_id=data.get("Фото").split("|")[1]
                                                      )
            await state.clear()
            await message.answer("Новый волонтер успешно добавлен!")
            await admin(message, state, bot)
            await message.delete()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                        text="<b>Данные волонтера:</b>\n" + text_application(data))
            try:
                await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=edit_message)
            finally:
                return
        key = list(volunteer_application.keys())[number_question]
        next_key = list(volunteer_application.keys())[number_question + 1]
        data[key] = message.text
        data["number_question"] = number_question + 1
        keyboard = await input_volunteer_application(number_question + 1)
        await state.update_data(data)
        application_text = "<b>Данные волонтера:</b>\n" + text_application(data)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                    text=application_text + "\n\n" + volunteer_application.get(next_key),
                                    reply_markup=keyboard.as_markup())
        await message.delete()
    else:
        await message.delete()


@admin_router.message(F.photo, InputMessage.AddVolunteer)
@is_main_admin
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    number_question = data.get("number_question")
    edit_message = data.get("message_id")
    if number_question in [5, 6] and message.photo:
        print(message.photo[-1].file_id)
        key = list(volunteer_application.keys())[number_question]
        next_key = list(volunteer_application.keys())[number_question + 1]
        data[key] = f"Прикреплено📎|{message.photo[-1].file_id}"
        data["number_question"] = number_question + 1
        keyboard = await input_volunteer_application(number_question + 1)
        await state.update_data(data)
        application_text = "<b>Данные волонтера:</b>\n" + text_application(data)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                    text=application_text + "\n\n" + volunteer_application.get(next_key),
                                    reply_markup=keyboard.as_markup())
        # await bot.edit_message_media(media=InputMediaPhoto(media=message.photo[-1].file_id), chat_id=message.from_user.id,
        #                              message_id=edit_message)
        await message.delete()
    else:
        await message.delete()


@admin_router.callback_query(Text(startswith="graph|"), InputMessage.AddVolunteer)
async def admin_filling_graph(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    number_question = data.get("number_question") - 1
    await state.clear()
    await state.set_state(InputMessage.AddVolunteer)
    edit_message = data.get("message_id")
    data["number_question"] = number_question
    data.pop(list(volunteer_application.keys())[number_question])
    await state.update_data(data)
    keyboard = await input_volunteer_application(number_question)
    application_text = "<b>Данные волонтера:</b>" + text_application(data)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=edit_message,
                                text=application_text + "\n\n" + volunteer_application.get(list(volunteer_application.keys())[number_question]),
                                reply_markup=keyboard.as_markup())






@admin_router.callback_query(Text(text="add_point"), any_state)
async def admin_add_point(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(InputMessage.AddPoint)
    key = list(point_application.keys())[0]
    keyboard = await input_volunteer_application(0)
    new_message = await call.message.edit_text(text=point_application.get(key),
                                               reply_markup=keyboard.as_markup())
    await state.update_data(number_question=0, message_id=new_message.message_id)


@admin_router.message(F.text, InputMessage.AddPoint)
@is_main_admin
async def admin_enter_point_application(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    number_question = data.get("number_question")
    edit_message = data.get("message_id")
    if number_question != 3 and number_question != len(list(point_application.keys())) - 2:
        if number_question == len(list(point_application.keys())) - 1:
            try:
                data[list(point_application.keys())[-1]] = message.text
                await bot.send_message(text=f"К тебе прикрепили точку\n\nДанные точки:{text_application(data)}",
                                       chat_id=message.text)
                volunteer = await volunteers_repository.select_volunteer_by_user_id(
                    int(data.get("Telegram id волонтера")))
                if volunteer is not None:
                    volunteer = await volunteers_repository.select_volunteer_by_user_id(int(data.get("Telegram id волонтера")))
                    await call_points_repository.add_call_point(name_of_point=data.get("Название"),
                                                                about=data.get("Описание"),
                                                                phone=data.get("Телефон"),
                                                                latitude=float(data.get("Геолокация").split(": ")[1].split(", ")[0][6:]),
                                                                longitude=float(data.get("Геолокация").split(": ")[1].split(", ")[1][:-7]),
                                                                volunteer_id=volunteer.id,
                                                                owner_user_id=int(data.get("owner_telegram_id")))
                else:
                    keyboard = await input_volunteer_application(number_question)
                    data.pop(list(point_application.keys())[-1])
                    await state.clear()
                    await state.set_state(InputMessage.AddPoint)
                    await state.update_data(data)
                    application_text = "<b>Информация о точке:</b>\n" + text_application(data)
                    await message.delete()
                    try:
                        await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                                    text=application_text + "\n\n" + "Волонтера с введенным тобой telegram id не существует, попробуй еще раз\n" +
                                                         point_application.get(
                                                             list(point_application.keys())[number_question]),
                                                    reply_markup=keyboard.as_markup())
                    finally:
                        return
            except:
                keyboard = await input_volunteer_application(number_question)
                data.pop(list(point_application.keys())[-1])
                await state.clear()
                await state.set_state(InputMessage.AddPoint)
                await state.update_data(data)
                application_text = "<b>Информация о точке:</b>\n" + text_application(data)
                await message.delete()
                try:
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                                text=application_text + "\n\n" + "Введенного тобой телеграм id не существует, либо у данного пользователя нет чата с данным ботом\n" +
                                                     point_application.get(list(point_application.keys())[number_question]),
                                                reply_markup=keyboard.as_markup())
                finally:
                    return
            print(data)
            # await PointRepository.add_point(point_data)
            await state.clear()
            await message.answer("Новая точка успешно добавлена!")
            await admin(message, state, bot)
            await message.delete()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                        text="<b>Информация о точке:</b>\n" + text_application(data))
            try:
                await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=edit_message)
            finally:
                return
        key = list(point_application.keys())[number_question]
        next_key = list(point_application.keys())[number_question + 1]
        data[key] = message.text
        data["number_question"] = number_question + 1
        keyboard = await input_volunteer_application(number_question + 1)
        await state.update_data(data)
        application_text = "<b>Информация о точке:</b>\n" + text_application(data)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                    text=application_text + "\n\n" + point_application.get(next_key),
                                 reply_markup=keyboard.as_markup())
        await message.delete()
        return
    elif number_question == len(list(point_application.keys())) - 2:
        if message.text.isdigit() and await volunteers_repository.select_volunteer_by_user_id(int(message.text)):
            await bot.send_message(text=f"К тебе прикрепили точку\n\nДанные точки:{text_application(data)}",
                                   chat_id=message.text)
            key = list(point_application.keys())[number_question]
            next_key = list(point_application.keys())[number_question + 1]
            data[key] = message.text
            data["number_question"] = number_question + 1
            keyboard = await input_volunteer_application(number_question + 1)
            await state.update_data(data)
            application_text = "<b>Информация о точке:</b>\n" + text_application(data)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                        text=application_text + "\n\n" + point_application.get(next_key),
                                        reply_markup=keyboard.as_markup())
        else:
            keyboard = await input_volunteer_application(number_question)
            await state.clear()
            await state.set_state(InputMessage.AddPoint)
            await state.update_data(data)
            application_text = "<b>Информация о точке:</b>\n" + text_application(data)
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                            text=application_text + "\n\n" + "Введенного тобой телеграм id не существует, либо у данного пользователя нет чата с данным ботом\n" +
                                                 point_application.get(list(point_application.keys())[number_question]),
                                            reply_markup=keyboard.as_markup())
            finally:
                await message.delete()
                return
    await message.delete()


@admin_router.message(F.location, InputMessage.AddPoint)
@is_main_admin
async def admin_enter_point_application(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    number_question = data.get("number_question")
    edit_message = data.get("message_id")
    if number_question == 3:
        longitude = str(message.location.longitude)
        latitude = str(message.location.latitude)
        key = list(point_application.keys())[number_question]
        next_key = list(point_application.keys())[number_question + 1]
        data[key] = f"Координаты: <code>{latitude + ', ' + longitude}</code>"
        data["number_question"] = number_question + 1
        keyboard = await input_volunteer_application(number_question + 1)
        await state.update_data(data)
        application_text = "<b>Данные точки:</b>\n" + text_application(data)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=edit_message,
                                    text=application_text + "\n\n" + point_application.get(next_key),
                                    reply_markup=keyboard.as_markup())
        await message.delete()
    else:
        await message.delete()


@admin_router.callback_query(Text(startswith="graph|"), InputMessage.AddPoint)
async def admin_filling_answer_point(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    number_question = data.get("number_question") - 1
    await state.clear()
    await state.set_state(InputMessage.AddPoint)
    edit_message = data.get("message_id")
    data["number_question"] = number_question
    data.pop(list(point_application.keys())[number_question])
    await state.update_data(data)
    keyboard = await input_volunteer_application(number_question)
    application_text = "<b>Информация о точке:</b>" + text_application(data)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=edit_message,
                                text=application_text + "\n\n" + point_application.get(
                                    list(point_application.keys())[number_question]),
                                reply_markup=keyboard.as_markup())
