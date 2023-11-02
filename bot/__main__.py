import asyncio
import sys


sys.path.append("./post_buy")
from bot.db.Channels import insert
from bot.utils.UnfixChatMessage import UnfixChatMessage

from bot.utils.SendingPost import SendingPost

from contextlib import suppress
import logging
from bot.handlers import routers
from bot.config import bot, dp


async def main() -> None:
    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filemode="w",
                        filename="logging.log",
                        format="%(levelname)s %(asctime)s %(message)s",
                        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        sending_post = SendingPost()
        sending_post.start_process(func=sending_post.start_schedule)
        unfixChatMessage = UnfixChatMessage()
        unfixChatMessage.start_process(func=unfixChatMessage.start_schedule)
        asyncio.run(main())
