from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.models import CommandUnit
from phrases import PHRASES_RU
from DB.tables.users import UsersTable

available_commands: List[CommandUnit] = []


def cmd(command: str, rt: Router, description: str = ''):
    """Декоратор для регистрации команд."""

    def decorator(func):
        is_admin = getattr(rt, 'is_admin', False)
        available_commands.append(CommandUnit(command, description, is_admin))

        @rt.message(Command(command))
        async def wrapper(message: Message):
            await func(message)
        return func

    return decorator


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
