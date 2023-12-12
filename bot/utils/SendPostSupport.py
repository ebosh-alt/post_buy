import asyncio

from aiogram.types import FSInputFile

from bot.config import bot
from bot.db import Publication
from bot.config import Config
from bot.utils import ParseDate
from bot.utils.GetMessage import get_mes


async def send(publication: Publication, name_channels: tuple, username: str):
    text = get_mes("mes_support", publication_text=publication.text, username=f"@{username}",
                   channels=", ".join(name_channels), date=ParseDate.parse(publication.publication_time),
                   price=publication.price_publication, fixing=publication.fixing)
    if publication.photo != "":
        photo = FSInputFile(publication.photo)
        await bot.send_photo(chat_id=Config.support_id,
                             caption=text,
                             photo=photo,
                             disable_notification=True)

    elif publication.video != "":
        video = FSInputFile(publication.video)
        await bot.send_video(chat_id=Config.support_id,
                             caption=text,
                             video=video,
                             disable_notification=True)

    else:
        await bot.send_message(chat_id=Config.support_id,
                               text=text)
