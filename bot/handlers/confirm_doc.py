from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.config import bot
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(F.data == "continue")
async def con_doc(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = await state.get_data()
    post: Post = data["post"]
    type_state = await state.get_state()
    change: bool = data.get("change")
    if change or type_state == "States:content":
        await bot.delete_message(chat_id=id, message_id=post.message_id)
    post.message_id = call.message.message_id
    await state.set_state(States.content)
    await state.update_data(post=post)
    try:
        await bot.edit_message_text(chat_id=id,
                                    message_id=call.message.message_id,
                                    text=get_mes("inp_content"))
        post.message_id = call.message.message_id

    except:
        mes = await bot.send_message(chat_id=id,
                                     text=get_mes("inp_content"))
        post.message_id = mes.message_id
    await state.update_data(post=post)


confirm_doc_rt = router
