from aiogram import Dispatcher, Bot
from dataclasses import dataclass


@dataclass
class Config:
    # api_key = "6532487125:AAEXJzFXyZKrxDK_dLMLDYoH8GJPBDKJmPA"
    api_key = "6499605545:AAFas4v-PxdjI0VBRS8uj89UY5ygfUVReaM"
    link_to_bot = "https://t.me/Gorodchat_bot"
    parse_mode = "Markdown"
    link_contract = "https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/magic_filters.html"
    link_processing_policy = "https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/magic_filters.html"
    host = "0.0.0.0"
    port = 80
    admin_id = 1321317438
    # admin_id = 686171972
    requisites = 4274320106431458


dp = Dispatcher()
bot = Bot(Config.api_key, parse_mode=Config.parse_mode)
