import os
from dataclasses import dataclass

from aiogram import Bot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@dataclass
class TgBot:
    token: str
    password: str
    message_max_symbols: int = 400


@dataclass
class Config:
    tg_bot: TgBot
    database_url: str
    db_type: str  # 'sqlite' or 'postgres'


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(token=os.getenv('BOT_TOKEN'), password=os.getenv('PASSWORD')),
        database_url=os.getenv('DATABASE_URL'),
        db_type=os.getenv('DB_TYPE', 'sqlite')  # По умолчанию SQLite, если не указано
    )


config: Config = load_config()

bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
