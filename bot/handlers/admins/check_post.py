import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot import keyboards as kb
from bot.config import Config, bot
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(
    (F.from_user.id == Config.admin_id) & (F.data.contains('confirm') | (F.data.contains('cancel'))))
async def check_post(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = call.data.split("_")
    logging.log(logging.INFO, f"check_post data: {call.data}")
    match data[0]:
        case "confirm":
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=get_mes("successes_del_mess"),
                                            show_alert=True)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=int(data[1]),
                                   text="Ваш пост подтвердили, осталось только оплатить",
                                   reply_markup=kb.create_keyboard({"Оплатить": "payment"}))
        case "cancel":
            await state.set_state(States.admin_comment)
            await bot.edit_message_text(chat_id=id,
                                        message_id=call.message.message_id,
                                        text="Введите комментарий")
            await state.update_data(id=int(data[1]), message_id=call.message.message_id)
        case "confirmChange":
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=get_mes("successes_del_mess"),
                                            show_alert=True)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=int(data[1]),
                                   text="Ваш пост подтвердили\n"
                                        "Чтобы посты добавились в ожидание нажмите кнопку 'Готово'",
                                   reply_markup=kb.success_payment_kb_user)


@router.message(States.admin_comment)
async def comment(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['id']
    message_id = data['message_id']
    comment_post = message.text
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=message_id,
                                text="Сообщение отправлено", reply_markup=kb.del_mes_kb)
    await bot.send_message(chat_id=user_id,
                           text=f"К сожалению Ваш пост отклонен\n\nКомментарий: {comment_post}",
                           reply_markup=kb.cancel_post_kb)
    await state.clear()


check_post_rt = router
