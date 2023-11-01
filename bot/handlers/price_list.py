from aiogram import F
from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import Message

from bot import keyboards as kb
from bot.config import bot
from bot.db import prices
from bot.utils.GetMessage import get_mes

router = Router()


@router.message(F.text == "Прайс-лист")
async def get_price_list(message: Message):
    id = message.from_user.id
    # price_list = prices.get_prices_list()
    await bot.send_message(chat_id=id,
                           text=get_mes("price_list"),
                           reply_markup=kb.buy_advertisement_kb)


price_list_rt = router
