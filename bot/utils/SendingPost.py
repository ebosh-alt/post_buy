import asyncio
import datetime
import logging
import time
from multiprocessing import Process

from aiogram.types import FSInputFile

from bot.config import bot, Config
from bot.const import tzinfo
from bot.db import publications, channels


async def send_mess(chat_id: int, text: str, fixing: bool, reply_to_message_id: int = None) -> int:
    mes = await bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id)
    if fixing != '0':
        await bot.pin_chat_message(message_id=mes.message_id, chat_id=chat_id)
    time.sleep(15)
    await bot.delete_message(chat_id=chat_id, message_id=mes.message_id)
    return mes.message_id


async def send_photo(chat_id: int, text: str, photo, fixing: bool, reply_to_message_id: int = None) -> int:
    mes = await bot.send_photo(chat_id=chat_id, photo=photo, caption=text, reply_to_message_id=reply_to_message_id)
    if fixing != '0':
        await bot.pin_chat_message(message_id=mes.message_id, chat_id=chat_id)
    return mes.message_id


async def send_video(chat_id: int, text: str, video, fixing: bool, reply_to_message_id: int = None) -> int:
    mes = await bot.send_video(chat_id=chat_id, video=video, caption=text, reply_to_message_id=reply_to_message_id)
    if fixing != '0':
        await bot.pin_chat_message(message_id=mes.message_id, chat_id=chat_id)
    return mes.message_id


class SendingPost:
    def __init__(self) -> None:
        self.p0 = Process()

    def start_process(self, func, arg=None):
        if arg is not None:
            self.p0 = Process(target=func, args=(arg,))
        else:
            self.p0 = Process(target=func)
        self.p0.start()

    def stop_process(self):
        self.p0.terminate()

    @staticmethod
    def work():
        current_time = datetime.datetime.now(tz=tzinfo).strftime("%d/%m %H:%M")

        for publication in publications:
            logging.log(logging.INFO, f"Publishing {publication.__dict__}")
            if publication.publication_time == current_time and publication.message_id == 0:
                chat_id = channels.get_id_by_name(publication.name_channel)
                reply_to_message_id = None
                if publication.name_channel == "Доска объявлений":
                    reply_to_message_id = Config.id_theme_board

                if publication.photo != "":
                    photo = FSInputFile(publication.photo)
                    loop = asyncio.get_event_loop()

                    mes_id = loop.run_until_complete(send_photo(chat_id=chat_id,
                                                                text=publication.text,
                                                                photo=photo,
                                                                fixing=publication.fixing,
                                                                reply_to_message_id=reply_to_message_id))

                elif publication.video != "":
                    video = FSInputFile(publication.video)
                    loop = asyncio.get_event_loop()
                    mes_id = loop.run_until_complete(send_video(chat_id=chat_id,
                                                                text=publication.text,
                                                                video=video,
                                                                fixing=publication.fixing,
                                                                reply_to_message_id=reply_to_message_id))

                else:
                    loop = asyncio.get_event_loop()
                    mes_id = loop.run_until_complete(send_mess(chat_id=chat_id,
                                                               text=publication.text,
                                                               fixing=publication.fixing,
                                                               reply_to_message_id=reply_to_message_id))
                publication.message_id = mes_id
                publications.update(publication)

    def start_schedule(self):
        while True:
            self.work()
            time.sleep(40)
