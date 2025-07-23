import os
import logging
import logging.handlers
from dataclasses import dataclass
from pathlib import Path
from aiogram import Bot
from dotenv import load_dotenv, find_dotenv
from config.const import BASE_DIR

load_dotenv(find_dotenv())

Path(BASE_DIR / "logs").mkdir(exist_ok=True)


@dataclass
class LogConfig:
    level: str = "DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/bot.log"
    max_size: int = 10  # MB
    backup_count: int = 3


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
    log: LogConfig


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            password=os.getenv('PASSWORD')
        ),
        database_url=os.getenv('DATABASE_URL'),
        db_type=os.getenv('DB_TYPE', 'sqlite'),
        log=LogConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file_path=os.getenv('LOG_FILE', 'logs/bot.log'),
            max_size=int(os.getenv('LOG_MAX_SIZE', 10)),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', 3))
        )
    )


def setup_logging(config: LogConfig):
    logging.basicConfig(
        level=getattr(logging, config.level),
        format=config.format,
        handlers=[
            logging.handlers.RotatingFileHandler(
                filename=BASE_DIR / config.file_path,
                maxBytes=config.max_size * 1024 * 1024,
                backupCount=config.backup_count,
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('aiogram').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.INFO)


config: Config = load_config()
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

setup_logging(config.log)
