from aiogram.types import Message

from aiogram import Router, F

from DB.tables.users import UsersTable
from bot.keyboards import user_keyboards

from config import config
from phrases import PHRASES_RU
from bot.handlers.admin_handlers import command_getcmds


router = Router()


@router.message(F.text == config.tg_bot.password)
async def _(message: Message):
    with UsersTable() as users_db:
        if users_db.set_admin(message.from_user.id, message.from_user.id):
            await message.delete()
            await message.answer(PHRASES_RU.success.promoted)
            await command_getcmds(message)
        else:
            await message.answer(PHRASES_RU.error.db)


@router.message()
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answers.unknown, reply_markup=user_keyboards.keyboard)
