from aiogram.types import Message

from bot.routers import UserRouter
from config import Config, load_config
from DB.phrases.phrases import PHRASES_RU
from bot.decorators import cmd, available_commands

router = UserRouter()
config: Config = load_config()


@cmd('start', router)                               # /start
async def process_start_command(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@cmd('help', router)                                # /help
async def process_help_command(message: Message):
    await message.answer(PHRASES_RU.commands.help)


@cmd('about', router)                               # /about
async def process_about_command(message: Message):
    await message.answer(PHRASES_RU.commands.about)


@cmd('commands', router)                             # /commands
async def process_getcmds_command(message: Message):
    commands_text = "\n".join(
        command.__str__() for command in available_commands if not command.is_admin
    )
    await message.answer(f"<b>📜 Доступные команды:</b>\n\n{commands_text}")