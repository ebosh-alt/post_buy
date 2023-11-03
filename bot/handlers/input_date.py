import datetime

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import publications, channels
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


def check_time_public(name_channels, time) -> bool | str:
    for name in name_channels:
        time_channel = publications.get_time_by_name(name, time)
        if time_channel is not None:
            return name
    return True


@router.callback_query(F.data.in_({"next_step_2"}))
async def choice_data(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    type_state = await state.get_state()
    data = await state.get_data()
    post: Post = data["post"]
    change: bool = data.get("change")
    if change:
        await bot.delete_message(chat_id=id, message_id=post.message_id)
    if type_state == "States:input_name_channel":
        await state.set_state(States.post)
        await state.update_data(post=post)
        try:
            await bot.delete_message(chat_id=id, message_id=post.message_id)
        except:
            pass
    keyboard = kb.create_keyboard(kb.button_date())
    await bot.edit_message_text(chat_id=id,
                                message_id=call.message.message_id,
                                text=get_mes("inp_date"),
                                reply_markup=keyboard)
    # post.message_id = call.message.message_id
    # await state.update_data(post=post)


@router.callback_query(F.data.in_(kb.button_date().values()))
async def start_inp_date(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = await state.get_data()
    post: Post = data["post"]
    post.date = call.data
    post.message_id = call.message.message_id
    await state.update_data(post=post)
    await bot.edit_message_text(chat_id=id,
                                message_id=call.message.message_id,
                                text=get_mes("inp_time"))


@router.message(States.post, F.text.regexp(r'[0-9]{2}:[0-9]{2}'))
async def inp_data(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    post: Post = data["post"]
    change: bool = data.get("change")
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    date = f"{post.date} {message.text}"
    # name_channels = post.name_channels
    # if name_channels is None:
    #     name_channels = channels.get_channel_category(post.category_channel)
    free = check_time_public(post.name_channels, date)
    if type(free) is str:
        post = Post(id_user=id)
        await state.update_data(post=post)
        await bot.edit_message_text(chat_id=id,
                                    message_id=post.message_id,
                                    text=f'В {free} уже запланирован пост на это время, выберите другое время\n'
                                         f'{get_mes("start_buy_ats")}',
                                    reply_markup=kb.keyboard_channel_category())
        return 200
    if post.date == datetime.datetime.now().strftime('%d/%m'):
        if message.text <= (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%H:%M'):
            await bot.edit_message_text(chat_id=id,
                                        message_id=post.message_id,
                                        text=f'В это время нельзя забронировать пост',
                                        reply_markup=kb.kb_by_time)
            return 200
    post.date = date
    await state.update_data(post=post)
    if change:
        await bot.edit_message_text(chat_id=id,
                                    message_id=post.message_id,
                                    text="Дата изменена\n"
                                         "Чтобы посты добавились в ожидание нажмите кнопку 'Готово'",
                                    reply_markup=kb.success_payment_kb_user)
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=post.message_id,
                                    text=get_mes("fixing"),
                                    reply_markup=kb.fixing_kb)


input_date_rt = router
