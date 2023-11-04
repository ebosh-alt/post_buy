import logging

from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.config import Config, bot
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(
    (F.from_user.id == Config.admin_id) & (F.data.contains('paymentYes') | (F.data.contains('paymentNo'))))
async def check_post(call: CallbackQuery):
    data = call.data.split("_")
    match data[0]:
        case "paymentYes":
            await bot.send_message(chat_id=int(data[1]),
                                   text=get_mes("confirm_post"),
                                   reply_markup=kb.success_payment_kb_user)
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=get_mes("successes_del_mess"),
                                            show_alert=False)
        case "paymentNo":
            price = data[2]
            await bot.send_message(chat_id=int(data[1]),
                                   text=get_mes("payment", price=price, requisites=Config.requisites),
                                   reply_markup=kb.check_pay_kb)
    logging.log(logging.INFO, "delete message in checking payment")
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


check_pay_rt = router
