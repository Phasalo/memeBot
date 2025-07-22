from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards import user_keyboards
from DB.db_interface import AbstractMovieDB
from config_data.config import Config, load_config
from DB.db_factory import DBFactory
from lexicon.lexicon import LEXICON_RU

router = Router()
config: Config = load_config()
db_instance: AbstractMovieDB = DBFactory.get_db_instance(config)


@router.message(CommandStart())  # /start
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['/start'])


@router.message(Command(commands=['help']))  # /help
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['/help'])


@router.message(Command(commands=['about']))  # /help
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['/about'])
