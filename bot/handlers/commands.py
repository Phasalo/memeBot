from aiogram.types import Message

from bot.routers import UserRouter, BaseRouter
from config import Config, load_config
from phrases import PHRASES_RU

router = UserRouter()
config: Config = load_config()


@router.command('start', 'запустить бота')  # /start
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@router.command('help', 'как пользоваться ботом')  # /help
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.help)


@router.command('about', 'о разработчиках')  # /about
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.about, disable_web_page_preview=True)


@router.command(('commands', 'cmd'), 'список всех команд (это сообщение)')  # /commands
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text)
