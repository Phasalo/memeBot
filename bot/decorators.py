from aiogram.types import Message

from phrases import PHRASES_RU
from DB.tables.users import UsersTable


def arguments_command(func):
    async def wrapper(message: Message):
        args = message.text.split()[1:]
        if len(args) == 0:
            await message.answer(PHRASES_RU.error.empty_argument)
            return
        await func(message, args)
    return wrapper


def digit_argument_command(func):
    @arguments_command
    async def wrapper(message: Message, args):
        digit = args[0]
        if not digit.isdigit():
            await message.answer(PHRASES_RU.error.not_digit_argument)
            return
        await func(message, digit)

    return wrapper


def user_id_argument_command(func):
    @digit_argument_command
    async def wrapper(message: Message, user_id):
        with UsersTable() as users_db:
            if not users_db.is_exists(user_id):
                await message.answer(PHRASES_RU.replace('error.user_not_exist', user_id=user_id))
                return
            await func(message, user_id)
    return wrapper
