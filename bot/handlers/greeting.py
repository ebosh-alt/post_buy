from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import keyboards as kb
from bot.config import bot
from bot.const import Profile
from bot.db import users, User
from bot.utils.GetMessage import get_mes
from bot.states import States

router = Router()


@router.message(Command("start"))
async def greeting_user(message: Message, state: FSMContext):
    id = message.from_user.id
    if id not in users:
        users.add(User(id=id))
        # mes = await bot.send_message(chat_id=id,
        #                              text=get_mes("greeting_new_user"))
        # await state.set_state(States.profile)
        # await state.update_data(profile=Profile())
        # await state.update_data(message_id=mes.message_id)

    await bot.send_message(chat_id=id,
                           text=get_mes("greeting"),
                           reply_markup=kb.greeting_kb)
    await state.clear()


greeting_rt = router
