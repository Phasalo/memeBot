from aiogram.types import Message
from utils.format_string import find_first_number


def one_argument_command(func):
    async def wrapper(message: Message):
        arg = find_first_number(message.text)
        await func(message, arg)
    return wrapper
