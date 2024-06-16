import traceback

from aiogram import Router, types, Bot, F
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Volunteers, CallPoints
from db.repository import call_points_repository, feeds_repository, volunteers_repository, calls_repository, \
    calls_baskets_repository, feed_transfers_repository, feed_transfers_buskets_repository, transfers_albums_repository, \
    receiving_albums_repository, animals_repository
from settings import InputMessage
from utils.get_feeds_text import get_feeds_text
from utils.is_volunteer import is_volunteer
from utils.keyboards import volunteer_start_keyboard, confirm_application, photo_call_keyboard, \
    cancel_volunteer_keyboard
from utils.paginator import PointsPaginator, FeedsPaginator, AnimalsPaginator

volunteer_router = Router()


@volunteer_router.callback_query(Text(text="back_to_volunteer_start"), any_state)
@volunteer_router.callback_query(Text(text="cancel_volunteer"))
@volunteer_router.message(Command('volunteer'), any_state)
@is_volunteer
async def volunteer(message: Message | CallbackQuery, state: FSMContext, bot: Bot):
    if type(message) == types.CallbackQuery:
        keyboard = await confirm_application(message.message.message_id, entity="volunteer")
        await message.message.answer("Ты уверен, что хочешь отменить добавление? <b>ВСЕ ДАННЫЕ БУДУТ УДАЛЕНЫ!</b>",
                                     reply_markup=keyboard.as_markup())
        return
    await state.clear()
    await message.answer(f"Вы находитесь на стартовой панели, выберите свои дальнейшие действия\n"
                         f"Ваш telegram_id: <b>{message.from_user.id}</b>",
                         reply_markup=volunteer_start_keyboard.as_markup())


@volunteer_router.callback_query(Text(text="get_animal_food"), any_state)
async def get_point_for_get_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(InputMessage.GetAnimalFood)
    points = await call_points_repository.select_all_points()
    keyboard = PointsPaginator(points).generate_now_page()
    await call.message.edit_text(text="Выбери точку получения корма из предложенных", reply_markup=keyboard)


@volunteer_router.callback_query(Text(text="my_animals"), any_state)
async def get_point_for_get_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    volunteer = await volunteers_repository.select_volunteer_by_user_id(int(call.from_user.id))
    points = await animals_repository.get_animals_by_volunteer_id(volunteer.id)
    keyboard = AnimalsPaginator(points).generate_now_page()
    await call.message.edit_text(text="Выбери своего котика", reply_markup=keyboard.as_markup())


@volunteer_router.callback_query(Text(startswith="points_paginator"), InputMessage.GetAnimalFood)
async def get_type_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split(":")
    if data[1] == "look_key":
        point_id = int(data[2])
        point = await call_points_repository.get_call_point_by_id(point_id)
        await state.update_data(point=point)
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Добавить фотографию для отчета", callback_data="start_send_photo_call"))
        keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_volunteer"))
        await call.message.edit_text(f"Ты выбрал точку: <b>{point.name_of_point}</b>\nОтлично,"
                                     f" теперь выбери свои дальнейшие действия",
                                  reply_markup=keyboard.as_markup())
    elif data[1] == "page_prev_keys":
        points = await call_points_repository.select_all_points()
        keyboard = PointsPaginator(points, page_now=int(data[2])).generate_prev_page()
        try:
            await call.message.edit_text(text="Выбери точку получения корма из предложенных", reply_markup=keyboard)
        except:
            return
    else:
        points = await call_points_repository.select_all_points()
        keyboard = PointsPaginator(points, page_now=int(data[2])).generate_next_page()
        try:
            await call.message.edit_text(text="Выбери точку получения корма из предложенных", reply_markup=keyboard)
        except:
            return


@volunteer_router.callback_query(Text(startswith="confirm_cancel_volunteer|"), any_state)
async def confirm_cancel_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.delete_message(chat_id=call.from_user.id, message_id=int(call.data.split("|")[1]))
    await call.message.answer("Вы находитесь на стартовой панели, выберите свои дальнейшие действия",
                         reply_markup=volunteer_start_keyboard.as_markup())
    await call.message.delete()


@volunteer_router.callback_query(Text(text="not_confirm_cancel_volunteer"), any_state)
async def not_confirm_cancel_volunteer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()


@volunteer_router.callback_query(Text(text="start_send_photo_call"), InputMessage.GetAnimalFood)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    data["photos"] = []
    await state.set_state(InputMessage.GivePhotoCall)
    data["start_message_delete_id"] = call.message.message_id
    await state.update_data(data)
    await call.message.answer("Добавь одно фото, далее у тебя будет возможность добавить другие")


@volunteer_router.callback_query(Text(text="send_photo_call"), InputMessage.GivePhotoCall)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    await call.message.answer("Добавь одно фото, далее у тебя будет возможность добавить другие")


@volunteer_router.message(F.photo, InputMessage.GivePhotoCall)
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    start_message_delete_id = data.get("start_message_delete_id")
    if start_message_delete_id is not None:
        await bot.delete_message(chat_id=message.from_user.id, message_id=start_message_delete_id)
        data["start_message_delete_id"] = None
        await state.update_data(start_message_delete_id=None)
    point = data.get("point")
    data["photos"].append(message.photo[-1].file_id)
    await state.clear()
    await state.set_state(InputMessage.GivePhotoCall)
    await state.update_data(data)
    await message.answer(
        f"Ты выбрал точку: <b>{point.name_of_point}</b>\n Теперь выбери свои дальнейшие действия",
        reply_markup=photo_call_keyboard.as_markup())


@volunteer_router.callback_query(Text(text="back_to_feeds"), InputMessage.FeedBasket)
@volunteer_router.callback_query(Text(text="ending_photo_call"), InputMessage.GivePhotoCall)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    await call.message.delete()
    await state.set_state(InputMessage.FeedBasket)
    await state.update_data(state_data)
    keyboard = FeedsPaginator(items=await feeds_repository.select_all_feeds()).generate_now_page()
    try:
        if call.data == "back_to_feeds" and len(list(state_data.get("feeds").keys())) != 0:
            keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
    except:
        print("я гей")
    main_message_edit = await call.message.answer(f"Введенные тобой данные:\n\n<b>Точка сбора</b>"
                                  f" - {state_data.get('point').name_of_point}\n<b>Количество"
                                                  f" прикрепленных фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм:"
                                                  f"\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты получил", reply_markup=keyboard.as_markup())
    await state.update_data(main_message_edit=main_message_edit.message_id)


@volunteer_router.callback_query(Text(startswith="feeds_paginator"), InputMessage.FeedBasket)
async def get_type_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    data = call.data.split(":")
    if data[1] == "feed":
        if state_data.get("feeds") is None:
            await state.update_data(feeds={})
        feed = await feeds_repository.select_feed_by_id(int(data[2]))
        await state.update_data(feed_now=feed)
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Назад к выбору кормов", callback_data="back_to_feeds"))
        error_float_id = await call.message.edit_text(text=f"Введи количество данного корма в кг(например 8 или 0.7)"
                                          f" корма({feed.category_of_feed}: {feed.kind_of_animal}):",
                                     reply_markup=keyboard.as_markup())
        await state.update_data(error_float_id=error_float_id.message_id)

    elif data[1] == "feed_page_prev_keys":
        points = await feeds_repository.select_all_feeds()
        keyboard = FeedsPaginator(points, page_now=int(data[2])).generate_prev_page()
        try:
            if len(list(state_data.get("feeds").keys())) != 0:
                keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
        except:
            print("я гей")
        try:
            await call.message.edit_text(text=f"Введенные тобой данные:\n\n<b>Точка сбора</b>"
                                  f" - {state_data.get('point').name_of_point}\n<b>Количество"
                                              f" прикрепленных фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм"
                                              f":\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты получил", reply_markup=keyboard.as_markup())
        except:
            return
    else:
        points = await feeds_repository.select_all_feeds()
        keyboard = FeedsPaginator(points, page_now=int(data[2])).generate_next_page()
        try:
            if len(list(state_data.get("feeds").keys())) != 0:
                keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
        except:
            print("я гей")
        try:
            await call.message.edit_text(text=f"Введенные тобой данные:\n\n<b>Точка сбора</b>"
                                  f" - {state_data.get('point').name_of_point}\n<b>Количество прикрепленных"
                                              f" фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм:"
                                              f"\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты получил", reply_markup=keyboard.as_markup())
        except:
            return


@volunteer_router.message(F.text, InputMessage.FeedBasket)
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    feed_now = state_data.get("feed_now")
    isfloat = True
    quantity = 0
    try:
        quantity = float(message.text)
    except:
        isfloat = False
    if isfloat:
        state_data["feeds"][feed_now.id] = quantity
        await state.update_data(feed_now=None)
        keyboard = FeedsPaginator(items=await feeds_repository.select_all_feeds()).generate_now_page()
        keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
        await bot.edit_message_text(text=f"Введенные тобой данные:\n\n<b>Точка сбора</b>"
                                  f" - {state_data.get('point').name_of_point}\n<b>Количество прикрепленных"
                                         f" фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм"
                                         f":\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты получил", reply_markup=keyboard.as_markup(),
                                    message_id=state_data.get("main_message_edit"),
                                    chat_id=message.from_user.id
                                    )
        await message.delete()
    else:
        feed = feed_now
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Назад к выбору кормов", callback_data="back_to_feeds"))
        try:
            await bot.edit_message_text(text=f"Введенные тобой данные некорректны\nВведи количество данного корма в"
                                             f" кг(например 8 или 0.7)"
                                             f" корма({feed.category_of_feed}: {feed.kind_of_animal}):",
                                        reply_markup=keyboard.as_markup(),
                                        chat_id=message.from_user.id,
                                        message_id=state_data.get("error_float_id"))
        finally:
            await state.update_data(error_float_id=None)
            await message.delete()
            return


@volunteer_router.callback_query(Text(text="send_call"), InputMessage.FeedBasket)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    print(data)
    text = '\n\n'.join(call.message.text.split("\n\n")[:-1])
    point: CallPoints = data.get("point")
    volunteer: Volunteers = await volunteers_repository.select_volunteer_by_user_id(int(call.from_user.id))
    await calls_repository.add_call(call_point_id=point.id,
                                    volunteer_id=volunteer.id)
    last_call = await calls_repository.get_calls_by_volunteer_id(volunteer_id=volunteer.id)
    last_call = last_call[-1]
    feeds = data.get("feeds")
    print(feeds)
    for key in feeds.keys():
        await calls_baskets_repository.add_call_baskets(call_id=last_call.id,
                                                         feed_id=int(key),
                                                         count_feed=float(feeds.get(key)))
    photos = data.get("photos")
    for photo in photos:
        await receiving_albums_repository.add_call_album(photo_id=photo,
                                                         call_id=last_call.id)
    await call.message.answer(f"<b>Отчет о получении успешно добавлен!</b>\n\n{text}")
    await call.message.answer(f"Вы находитесь на стартовой панели, выберите свои дальнейшие действия\n"
                         f"Ваш telegram_id: <b>{call.from_user.id}</b>",
                         reply_markup=volunteer_start_keyboard.as_markup())
    await call.message.delete()



"""FGSOIDHLJSKDFHGJLSKHDFGJKSHLDFKJGSHLKDFJGLKSDHFGKLSHJFGSLKFJDGHSKLDJFHG"""



@volunteer_router.callback_query(Text(text="transfer_animal_food"), any_state)
async def get_point_for_get_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(InputMessage.GetRecipientId)
    await state.update_data(start_transfer_id=call.message.message_id)
    await call.message.edit_text(text="Введи telegram id волонтера или склада, которому ты передаешь корм!",
                                 reply_markup=cancel_volunteer_keyboard.as_markup())


@volunteer_router.message(F.text, InputMessage.GetRecipientId)
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    try:
        volunteer = await volunteers_repository.select_volunteer_by_user_id(int(message.text))
    except:
        volunteer = False
    if volunteer:
        await state.set_state(InputMessage.GivePhotoTransfer)
        await state.update_data(volunteer=volunteer)
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Добавить фотографию для отчета", callback_data="start_send_photo_call"))
        keyboard.row(InlineKeyboardButton(text="Отменить заполнение🚫", callback_data=f"cancel_volunteer"))
        await bot.edit_message_text(text=f"Ты передаешь корм волонтеру(складу) с telegram id: <b>{message.text}</b>\nОтлично,"
                                     f" теперь выбери свои дальнейшие действия",
                                    reply_markup=keyboard.as_markup(),
                                    chat_id=message.from_user.id,
                                    message_id=state_data.get("start_transfer_id")
                                    )
        await message.delete()
    else:
        await bot.edit_message_text(text="Волонтера(склада) с таким telegram id не существует, попробуй еще раз\n\nВведи telegram id волонтера или склада, которому ты передаешь корм!",
                                     reply_markup=cancel_volunteer_keyboard.as_markup(),
                                    chat_id=message.from_user.id,
                                    message_id=state_data.get("start_transfer_id"))
        await message.delete()


@volunteer_router.callback_query(Text(text="start_send_photo_call"), InputMessage.GivePhotoTransfer)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    data["photos"] = []
    data["start_message_delete_id"] = call.message.message_id
    await state.update_data(data)
    await call.message.answer("Добавь одно фото, далее у тебя будет возможность добавить другие")


@volunteer_router.message(F.photo, InputMessage.GivePhotoTransfer)
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    start_message_delete_id = data.get("start_message_delete_id")
    if start_message_delete_id is not None:
        await bot.delete_message(chat_id=message.from_user.id, message_id=start_message_delete_id)
        data["start_message_delete_id"] = None
        await state.update_data(start_message_delete_id=None)
    point = data.get("point")
    data["photos"].append(message.photo[-1].file_id)
    await state.clear()
    await state.set_state(InputMessage.GivePhotoTransfer)
    await state.update_data(data)
    await message.answer(text=f"Ты передаешь корм волонтеру(складу) с telegram id: <b>{message.text}</b>\nОтлично,"
                            f" теперь выбери свои дальнейшие действия",
                            reply_markup=photo_call_keyboard.as_markup())


@volunteer_router.callback_query(Text(text="send_photo_call"), InputMessage.GivePhotoTransfer)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    await call.message.answer("Добавь одно фото, далее у тебя будет возможность добавить другие")


@volunteer_router.callback_query(Text(text="back_to_feeds"), InputMessage.FeedBasket)
@volunteer_router.callback_query(Text(text="ending_photo_call"), InputMessage.GivePhotoTransfer)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    await call.message.delete()
    await state.set_state(InputMessage.TransferFeedBasket)
    await state.update_data(state_data)
    keyboard = FeedsPaginator(items=await feeds_repository.select_all_feeds()).generate_now_page()
    try:
        if call.data == "back_to_feeds" and len(list(state_data.get("feeds").keys())) != 0:
            keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
    except:
        print("я гей")
    volunteer: Volunteers = state_data.get('volunteer')
    main_message_edit = await call.message.answer(f"Введенные тобой данные:\n\n<b>Получатель</b>"
                                  f" - {volunteer.surname + ' ' + volunteer.firstname + ': ' + str(volunteer.user_id)}"
                                                  f"\n<b>Количество"
                                                  f" прикрепленных фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм:"
                                                  f"\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты передал", reply_markup=keyboard.as_markup())
    await state.update_data(main_message_edit=main_message_edit.message_id)






@volunteer_router.callback_query(Text(startswith="feeds_paginator"), InputMessage.TransferFeedBasket)
async def get_type_food(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    data = call.data.split(":")
    volunteer: Volunteers = state_data.get('volunteer')
    if data[1] == "feed":
        if state_data.get("feeds") is None:
            await state.update_data(feeds={})
        feed = await feeds_repository.select_feed_by_id(int(data[2]))
        await state.update_data(feed_now=feed)
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Назад к выбору кормов", callback_data="back_to_feeds"))
        error_float_id = await call.message.edit_text(text=f"Введи количество данного корма в кг(например 8 или 0.7)"
                                          f" корма({feed.category_of_feed}: {feed.kind_of_animal}):",
                                     reply_markup=keyboard.as_markup())
        await state.update_data(error_float_id=error_float_id.message_id)

    elif data[1] == "feed_page_prev_keys":
        points = await feeds_repository.select_all_feeds()
        keyboard = FeedsPaginator(points, page_now=int(data[2])).generate_prev_page()
        try:
            if len(list(state_data.get("feeds").keys())) != 0:
                keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
        except:
            print("я гей")
        try:
            await call.message.edit_text(text=f"Введенные тобой данные:\n\n<b>Получатель</b>"
                                  f" - {volunteer.surname + ' ' + volunteer.firstname + ': ' + str(volunteer.user_id)}"
                                                  f"\n<b>Количество"
                                                  f" прикрепленных фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм:"
                                                  f"\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты передал", reply_markup=keyboard.as_markup())
        except:
            return
    else:
        points = await feeds_repository.select_all_feeds()
        keyboard = FeedsPaginator(points, page_now=int(data[2])).generate_next_page()
        try:
            if len(list(state_data.get("feeds").keys())) != 0:
                keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
        except:
            print("я гей")
        try:
            await call.message.edit_text(text=f"Введенные тобой данные:\n\n<b>Получатель</b>"
                                  f" - {volunteer.surname + ' ' + volunteer.firstname + ': ' + str(volunteer.user_id)}"
                                                  f"\n<b>Количество"
                                                  f" прикрепленных фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм:"
                                                  f"\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты передал", reply_markup=keyboard.as_markup())
        except:
            print(traceback.format_exc())
            return


@volunteer_router.message(F.text, InputMessage.TransferFeedBasket)
async def admin_enter_application(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    feed_now = state_data.get("feed_now")
    volunteer: Volunteers = state_data.get('volunteer')
    isfloat = True
    quantity = 0
    try:
        quantity = float(message.text)
    except:
        isfloat = False
    if isfloat:
        state_data["feeds"][feed_now.id] = quantity
        await state.update_data(feed_now=None)
        keyboard = FeedsPaginator(items=await feeds_repository.select_all_feeds()).generate_now_page()
        keyboard.row(InlineKeyboardButton(text="Отправить данный отчет", callback_data="send_call"))
        await bot.edit_message_text(text=f"Введенные тобой данные:\n\n<b>Получатель</b>"
                                  f" - {volunteer.surname + ' ' + volunteer.firstname + ': ' + str(volunteer.user_id)}"
                                                  f"\n<b>Количество"
                                                  f" прикрепленных фотографий</b>"
                                  f" - {len(state_data.get('photos'))}\n\nКорм:"
                                                  f"\n{await get_feeds_text(state_data.get('feeds'))}\n\n"
                                  f"Отлично, теперь тебе нужно указать, сколько какого"
                                  f" корма ты передал", reply_markup=keyboard.as_markup(),
                                    message_id=state_data.get("main_message_edit"),
                                    chat_id=message.from_user.id
                                    )
        await message.delete()
    else:
        feed = feed_now
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Назад к выбору кормов", callback_data="back_to_feeds"))
        try:
            await bot.edit_message_text(text=f"Введенные тобой данные некорректны\nВведи количество данного корма в"
                                             f" кг(например 8 или 0.7)"
                                             f" корма({feed.category_of_feed}: {feed.kind_of_animal}):",
                                        reply_markup=keyboard.as_markup(),
                                        chat_id=message.from_user.id,
                                        message_id=state_data.get("error_float_id"))
        finally:
            await state.update_data(error_float_id=None)
            await message.delete()
            return


@volunteer_router.callback_query(Text(text="send_call"), InputMessage.TransferFeedBasket)
async def send_photo_call(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    print(data)
    text = '\n\n'.join(call.message.text.split("\n\n")[:-1])
    volunteer: Volunteers = data.get("volunteer")
    await feed_transfers_repository.add_feed_transfer(volunteer_id=volunteer.id,
                                                      user_id=call.from_user.id)
    last_transfer = await feed_transfers_repository.get_feed_transfers_by_volunteer_id(volunteer_id=volunteer.id)
    last_transfer = last_transfer[-1]
    feeds = data.get("feeds")
    print(feeds)
    photos = data.get("photos")
    for key in feeds.keys():
        await feed_transfers_buskets_repository.add_feed_transfers_basket(feed_transfer_id=last_transfer.id,
                                                        feed_id=int(key),
                                                        count_feed=float(feeds.get(key)))
    for photo in photos:
        await transfers_albums_repository.add_transfer_album(photo_id=photo,
                                                             feed_transfer_id=last_transfer.id)
    await call.message.answer(f"<b>Отчет о получении успешно добавлен!</b>\n\n{text}")
    await call.message.answer(f"Вы находитесь на стартовой панели, выберите свои дальнейшие действия\n"
                         f"Ваш telegram_id: <b>{call.from_user.id}</b>",
                         reply_markup=volunteer_start_keyboard.as_markup())
    await call.message.delete()