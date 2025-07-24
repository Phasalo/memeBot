from aiogram.types import Message
from aiogram import Router

router = Router()


@router.message(lambda message: message.text.lower() == 'спасибо' or message.text.lower() == 'от души' or message.text.lower() == 'благодарю')
async def _(message: Message):
    await message.answer_sticker(sticker='CAACAgEAAxkBAAEKShplAfTsN4pzL4pB_yuGKGksXz2oywACZQEAAnY3dj9hlcwZRAnaOjAE')
