from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import Config, bot
from bot.db import channels
from bot.states import States
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb

router = Router()


@router.message(Command("admin"), F.from_user.id == Config.admin_id)
async def start_admin(message: Message):
    id = message.from_user.id
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    await bot.send_message(chat_id=id,
                           text=get_mes("start_admin"),
                           reply_markup=kb.admin_kb)


@router.callback_query(F.data == "mailing")
async def mailing_admin(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=call.message.message_id,
                                text=get_mes("start_mailing_adm"))
    await state.set_state(States.mailing)


@router.message(States.mailing)
async def get_text_by_mailing(message: Message):
    id = message.from_user.id
    for channel in channels:
        await bot.send_message(chat_id=channel.id_telegram, text=message.text)
    await bot.send_message(chat_id=id, text="Рассылка отправлена", reply_markup=kb.del_mes_kb)


@router.callback_query(F.data == "unfix_all")
async def unfix_admin(call: CallbackQuery):
    for channel in channels:
        await bot.unpin_all_chat_messages(chat_id=channel.id_telegram)
    bot.answer_callback_query(callback_query_id=call.id,
                              text="Сообщения откреплены",
                              show_alert=True)


admin_rt = router
