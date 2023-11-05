import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, EditMessageText, DeleteMessage
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import channels
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


def get_list_all_name():
    text = "Список всех чатов:"
    all_district = list(channels.get_category().values())[:-3]
    logging.log(logging.INFO, all_district)
    for district in all_district:
        # if category not in ['Доска объявлений', 'Весь город', 'Выбрать по 1 чату', "Омск без категории"]:
        #     city, district = category.split(" ")
        names = channels.get_name(district)
        text += f"\n\n{district}: \n"
        for name in names:
            text += f"`{name}` | "
        text = text[:-2]
    text += "\n\nНажав на один из чатов он скопируется\n" \
            "Отправьте одним сообщением через запятую все чаты, которые Вам необходимы"
    return text


@router.message(F.text == "Купить рекламу")
@router.callback_query(F.data == "buy_advertisement")
async def buy_advertisement_start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(States.post)
    post = Post(id_user=id)
    await state.update_data(post=post)
    if type(message) is CallbackQuery:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("start_buy_ats"),
                                    reply_markup=kb.keyboard_channel_category())
    else:
        await bot.send_message(chat_id=id, text=get_mes("start_buy_ats"),
                               reply_markup=kb.keyboard_channel_category())


@router.callback_query(States.post, F.data.in_(channels.get_category()))
async def choice_category(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = await state.get_data()
    post: Post = data['post']
    if post.category_channel is None:
        post.category_channel = call.data
    elif post.category_channel != call.data:
        post.category_channel = call.data
    if call.data == "1 любой чат":
        post.category_channel = call.data
        buttons = {}
        text = get_list_all_name()
        buttons.update({"<< Назад": "buy_advertisement"})
        post.message_id = call.message.message_id
        await state.set_state(States.input_name_channel)
        await state.update_data(post=post)
        await bot.edit_message_text(chat_id=id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb.create_keyboard(buttons),
                                    parse_mode="Markdown")

    else:
        all_category = list(channels.get_category().values())
        ind_category = all_category.index(post.category_channel)
        all_category[ind_category] = f"✅{post.category_channel}"
        buttons = dict()
        for category in all_category:
            buttons.update({category: category})
            post.category_channel = call.data
            match call.data:
                case "Доска объявлений":
                    post.name_channels = ["Доска объявлений"]
                case "Весь город":
                    post.name_channels = tuple(channels.get_all_name())
                case _:
                    district = call.data
                    post.name_channels = tuple(channels.get_name(district=district).values())
        buttons.update({"Продолжить >>": "next_step_2"})
        keyboard = kb.create_keyboard(buttons)
        await bot.edit_message_text(chat_id=id,
                                    message_id=call.message.message_id,
                                    text=get_mes("start_buy_ats"),
                                    reply_markup=keyboard)
        await state.update_data(post=post)


@router.message(States.input_name_channel)
async def inp_name_channel(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    post: Post = data['post']
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    await bot.delete_message(chat_id=id, message_id=post.message_id)
    channel_name = message.text.split(",")
    post.name_channels = channel_name
    text = "Вы выбрали: \n"
    for name in channel_name:
        text += f"{name} | "
    text = text[0:-2]
    text += "\n\nЕсли что-то не верно, отправьте повторно список"
    buttons = {}
    buttons.update({"Вернуться в начало": "buy_advertisement"})
    buttons.update({"Продолжить >>": "next_step_2"})
    mes1 = await bot.send_message(chat_id=id,
                                  text=get_list_all_name())
    await bot.send_message(chat_id=id,
                           text=text,
                           reply_markup=kb.create_keyboard(buttons))
    post.message_id = mes1.message_id
    await state.update_data(post=post)


buy_rt = router
