import datetime
import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot import keyboards as kb
from bot.config import Config, bot
from bot.const import tzinfo
from bot.db import Publication, publications
from bot.db.Post import Post
from bot.states import States
from bot.utils import SendPostSupport

router = Router()


@router.callback_query(States.post, F.data == "ready_post")
async def ready_post(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post: Post = data["post"]
    await bot.delete_message(chat_id=call.from_user.id, message_id=post.message_id)
    publication_id = len(publications) + 1
    for name in post.name_channels:
        publication = Publication(len(publications) + 1)
        publication.name_channel = name.strip()
        publication.id_user = call.from_user.id
        publication.price_publication = post.price
        publication.photo = post.photo
        publication.text = post.text
        publication.video = post.video
        publication.publication_time = post.date
        if post.fixing:
            publication.fixing = ((datetime.datetime.now(tz=tzinfo) + datetime.timedelta(days=post.fixing)).
                                  strftime("%Y/%m/%d %H:%M"))
        else:
            publication.fixing = False
        logging.log(logging.INFO, f"add publication {publication.__dict__}")
        publications.add(publication)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id,
                           # message_id=call.message.message_id,
                           text='Все прошло успешно!',
                           reply_markup=kb.greeting_kb)
    publication = publications.get(publication_id)
    await SendPostSupport.send(publication=publication,
                               name_channels=post.name_channels,
                               username=call.from_user.username)
    await state.clear()


ready_post_rt = router
