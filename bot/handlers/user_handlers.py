from aiogram.types import Message

from aiogram import Router, F

from DB.tables.users import UsersTable
from bot.keyboards import user_keyboards

from config import Config, load_config
from phrases import PHRASES_RU

config: Config = load_config()

router = Router()


@router.message(F.text == config.tg_bot.password)
async def get_verified(message: Message):
    with UsersTable() as users_db:
        if users_db.set_admin(message.from_user.id, message.from_user.id):
            await message.answer(PHRASES_RU.success.promoted)
        else:
            await message.answer(PHRASES_RU.error.db)


@router.message()
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answers.unknown, reply_markup=user_keyboards.keyboard)
