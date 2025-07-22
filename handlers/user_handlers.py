from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram import Router, F

from DB.users_sqlite import Database
from keyboards import user_keyboards

from config_data.config import Config, load_config
from lexicon.lexicon import LEXICON_RU

config: Config = load_config()

router = Router()


@router.message(lambda message: message.text.lower() == 'спасибо' or message.text.lower() == 'от души' or message.text.lower() == 'благодарю')
async def u_r_wellcome(message: Message):
    await message.answer_sticker(sticker='CAACAgEAAxkBAAEKShplAfTsN4pzL4pB_yuGKGksXz2oywACZQEAAnY3dj9hlcwZRAnaOjAE')


@router.message(F.text == LEXICON_RU['_password'])
async def get_verified(message: Message):
    with Database() as db:
        db.set_admin(message.from_user.id)
        await message.answer('Теперь ты админ')


@router.message()
async def process_name_command(message: Message):
    await message.answer(text='К сожалению, я не понимаю, о чем вы', reply_markup=user_keyboards.keyboard)
