import asyncio
import datetime
import logging
import time
from multiprocessing import Process

from bot.config import bot
from bot.db import publications, channels


class UnfixChatMessage:
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
    async def unfix_chat_message(chat_id: int, message_id: int):
        await bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)

    def work(self):
        current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        for publication in publications:
            if publication.fixing == current_time:
                chat_id = channels.get_id_by_name(publication.name_channel)
                message_id = publication.message_id
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.unfix_chat_message(chat_id=chat_id, message_id=message_id))

    def start_schedule(self):
        while True:
            self.work()
            time.sleep(3600)
