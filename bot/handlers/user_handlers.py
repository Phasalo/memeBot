from aiogram.types import Message

from aiogram import Router, F

from DB.tables.users import UsersTable
from bot.keyboards import user_keyboards

from config import Config, load_config
from DB.phrases.phrases import PHRASES_RU

config: Config = load_config()

router = Router()


@router.message(lambda message: message.text.lower() == 'спасибо' or message.text.lower() == 'от души' or message.text.lower() == 'благодарю')
async def u_r_wellcome(message: Message):
    await message.answer_sticker(sticker='CAACAgEAAxkBAAEKShplAfTsN4pzL4pB_yuGKGksXz2oywACZQEAAnY3dj9hlcwZRAnaOjAE')


@router.message(F.text == config.tg_bot.password)
async def get_verified(message: Message):
    with UsersTable() as users_db:
        ok = users_db.set_admin(message.from_user.id, message.from_user.id)
        if ok:
            await message.answer(PHRASES_RU.success.admin_promoted)
        else:
            await message.answer(PHRASES_RU.errors.db_error)


@router.message()
async def process_name_command(message: Message):
    await message.answer(text=PHRASES_RU.hz_answers, reply_markup=user_keyboards.keyboard)
