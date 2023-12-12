import asyncio
import logging
import time

from aiogram.types import FSInputFile

from bot.config import bot
from bot.db import channels


async def check() -> list:
    incorrect = []
    logging.log(logging.ERROR, f"start sending")
    for channel in channels:
        if channel.name in ["Парковый", "Заозерный (Менделеева-Комбинатская)"]:
            id = channel.id_telegram
            mes = await bot.send_message(chat_id=id,
                                         text="тестовое сообщение")
            try:
                await bot.pin_chat_message(chat_id=id, message_id=mes.message_id, disable_notification=True)
                logging.log(logging.INFO, f"sending message to: {channel.name}")
            except:
                incorrect.append(channel.name)
                logging.log(logging.ERROR, f"error sending message to: {channel.name}")

            await bot.delete_message(chat_id=id, message_id=mes.message_id)
    return incorrect


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filemode="w",
                        # filename="logging.log",
                        format="%(levelname)s %(asctime)s %(message)s",
                        encoding='utf-8')
    incorrect = asyncio.run(check())
