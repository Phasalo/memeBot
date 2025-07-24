from aiogram.types import Message

from bot.routers import UserRouter, BaseRouter
from config import Config, load_config
from phrases import PHRASES_RU

router = UserRouter()
config: Config = load_config()


@router.command('start')                               # /start
async def process_start_command(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@router.command('help')                                # /help
async def process_help_command(message: Message):
    await message.answer(PHRASES_RU.commands.help)


@router.command('about')                               # /about
async def process_about_command(message: Message):
    await message.answer(PHRASES_RU.commands.about)


@router.command('commands')                             # /commands
async def process_commands_command(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text)
