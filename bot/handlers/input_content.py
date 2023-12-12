import asyncio
import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from bot import keyboards as kb
from bot.config import Config, bot
from bot.db.Post import Post
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


async def download_media(message, type_media: str) -> str:
    if type_media == 'photo':
        file = message.photo[-1]
        destination = f"bot/media/{message.photo[-1].file_id}_{message.message_id}.jpg"
    else:
        file = message.video
        destination = f"bot/media/{message.video.file_id}_{message.message_id}.mp4"
    await bot.download(
        file=file,
        destination=destination
    )
    return destination


@router.message(States.content, F.content_type.in_({'text', 'photo', 'video'}))
async def inp_content(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    post: Post = data["post"]
    change: bool = data.get("change")
    try:
        await bot.delete_message(chat_id=id, message_id=post.message_id)
    except:
        pass
    if message.media_group_id is None:

        photo = message.photo
        video = message.video
        if message.caption:
            post.text = message.caption
        if message.text:
            post.text = message.text
        if change:
            buttons = {"Подтвердить": f"confirmChange_{id}", "Отклонить": f"cancel_{id}"}
        else:
            buttons = {"Подтвердить": f"confirm_{id}", "Отклонить": f"cancel_{id}"}
        keyboard = kb.create_keyboard(buttons, 2)
        if photo is not None:
            path = await download_media(message, "photo")
            post.photo = path
            photo = FSInputFile(post.photo)
            await bot.send_photo(chat_id=id,
                                 photo=photo,
                                 caption=post.text)
            await bot.send_photo(chat_id=Config.admin_id,
                                 photo=photo,
                                 caption=get_mes("mes_info_post_admin", post=post.text, date=post.date, id=id,
                                                 username=message.from_user.username),
                                 reply_markup=keyboard)
        elif video is not None:
            path = await download_media(message, "video")
            post.video = path
            video = FSInputFile(post.video)
            await bot.send_video(chat_id=id,
                                 video=video,
                                 caption=post.text)
            await bot.send_video(chat_id=Config.admin_id,
                                 video=video,
                                 caption=get_mes("mes_info_post_admin", post=post.text, date=post.date, id=id,
                                                 username=message.from_user.username),
                                 reply_markup=keyboard)
        else:
            logging.log(logging.INFO, get_mes("mes_info_post_admin", post=post.text, date=post.date, id=id,
                                              username=message.from_user.username))

            await bot.send_message(chat_id=id,
                                   text=post.text)
            await bot.send_message(chat_id=Config.admin_id,
                                   text=get_mes("mes_info_post_admin", post=post.text, date=post.date, id=id,
                                                username=message.from_user.username),
                                   reply_markup=keyboard)
        await bot.delete_message(chat_id=id, message_id=message.message_id)
        mes = await bot.send_message(chat_id=id,
                                     text="Пост отправлен админу, ожидайте! Никуда не уходите с этого этапа")
        post.message_id = mes.message_id
        if change:
            await state.set_state(States.post)
            await state.update_data(post=post)
        await state.update_data(post=post)


inp_content_rt = router
