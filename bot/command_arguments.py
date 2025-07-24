from aiogram.types import Message

from phrases import PHRASES_RU
from DB.tables.users import UsersTable


def multiple(default=None):
    def decorator(func):
        async def wrapper(message: Message):
            args = message.text.split()[1:]
            if len(args) == 0:
                if default is not None:
                    await func(message, [default])
                    return
                await message.answer(PHRASES_RU.error.empty_argument)
                return
            await func(message, args)
        return wrapper
    return decorator


def digit(default=None):
    def decorator(func):
        @multiple(default=default)
        async def wrapper(message: Message, args):
            digit = args[0]
            if not str(digit).isdigit():
                await message.answer(PHRASES_RU.error.not_digit_argument)
                return
            await func(message, int(digit))
        return wrapper
    return decorator


def user_id(func):
    @digit
    async def wrapper(message: Message, user_id):
        with UsersTable() as users_db:
            if not users_db.is_exists(user_id):
                await message.answer(PHRASES_RU.replace('error.user_not_exist', user_id=user_id))
                return
            await func(message, user_id)
    return wrapper
