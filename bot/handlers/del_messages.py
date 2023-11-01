from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery

from bot.config import bot

router = Router()


@router.callback_query(F.data == "del_messages")
async def delete_messages(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


del_messages_rt = router
