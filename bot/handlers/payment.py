from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot import keyboards as kb
from bot.config import Config, bot
from bot.db import prices
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(States.content, F.data == "payment")
async def payment_user(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = await state.get_data()
    post: Post = data["post"]
    await state.set_state(States.post)

    match post.category_channel:
        case "Выбрать по 1 чату":
            count_channel = len(post.name_channels)
            price = prices.get_price_publication(district=post.category_channel) * count_channel
            if post.fixing:
                price += prices.get_price_publication(district=post.category_channel) * count_channel * post.fixing
        case _:
            price = prices.get_price_publication(district=post.category_channel)
            if post.fixing:
                price += prices.get_price_fixing(district=post.category_channel) * post.fixing
    await bot.delete_message(chat_id=id, message_id=post.message_id)
    await bot.edit_message_text(chat_id=id,
                                message_id=call.message.message_id,
                                text=get_mes('payment', price=price, requisites=Config.requisites),
                                reply_markup=kb.check_pay_kb,
                                parse_mode="Markdown")
    post.price = price
    post.message_id = call.message.message_id
    await state.update_data(post=post)


@router.callback_query(States.post, F.data == "check_pay")
async def check_pay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post: Post = data["post"]
    await state.update_data(change=True)
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text=get_mes("check_pay_user"))
    post.message_id = call.message.message_id
    buttons = {"Подтвердить": f"paymentYes_{call.from_user.id}",
               "Отклонить": f"paymentNo_{call.from_user.id}_{post.price}"}
    await state.update_data(post=post)
    await bot.send_message(chat_id=Config.admin_id,
                           text=f"username пользователя: {call.from_user.username}\n"
                                f"id пользователя: {call.from_user.id}\n"
                                f"сумма перевода: {post.price}",
                           reply_markup=kb.create_keyboard(buttons, 2))


payment_rt = router
