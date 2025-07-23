from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import Config, load_config
from DB.phrases.phrases import LEXICON_RU

router = Router()
config: Config = load_config()


@router.message(CommandStart())  # /start
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['commands']['start'])


@router.message(Command(commands=['help']))  # /help
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['commands']['help'])


@router.message(Command(commands=['about']))  # /about
async def process_about_command(message: Message):
    await message.answer(LEXICON_RU['commands']['about'])
