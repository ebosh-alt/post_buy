import datetime
import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.const import tz
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(States.post, F.data.in_(kb.fix_button.values()))
async def choice_fix(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = await state.get_data()
    post: Post = data["post"]
    match call.data:
        case "no_fixing":
            post.fixing = False
        case _:
            fixing = int(call.data.replace("_day", ""))
            post.fixing = fixing

    await state.update_data(post=post)
    logging.log(logging.INFO, f"post fixing {post.fixing}")

    await bot.edit_message_text(chat_id=id,
                                message_id=call.message.message_id,
                                text=get_mes("documents"),
                                reply_markup=kb.document_kb)


choice_fix_rt = router
