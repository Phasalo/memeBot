from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.format_string import find_first_number
from config.models import CommandUnit

available_commands: List[CommandUnit] = []


def cmd(command: str, rt: Router, description: str = ""):
    """Декоратор для регистрации команд."""

    def decorator(func):
        is_admin = getattr(rt, 'is_admin', False)
        available_commands.append(CommandUnit(command, description, is_admin))

        @rt.message(Command(command))
        async def wrapper(message: Message):
            await func(message)
        return func

    return decorator


def one_argument_command(func):
    async def wrapper(message: Message):
        arg = find_first_number(message.text)
        await func(message, arg)
    return wrapper


# def command_with_arguments(func):
#     async def wrapper(message: Message):
#         args = message.text.split()[1:]
#         if len(args) == 0:
#             await message.answer(phrases['error']['empty_argument'], reply_markup=kb.main)
#             return
#         await func(message, args)
#     return wrapper
#
#
# def command_with_digit_argument(func):
#     @command_with_arguments
#     async def wrapper(message: Message, args):
#         digit = args[0]
#         if not digit.isdigit():
#             await message.answer(phrases['error']['not_digit'], reply_markup=kb.main)
#             return
#         await func(message, digit)
#     return wrapper
#
#
# def command_with_user_id_argument(func):
#     @command_with_digit_argument
#     async def wrapper(message: Message, user_id):
#         if not users.is_exists(user_id):
#             await message.answer(phrases['error']['user_not_exist'], reply_markup=kb.main)
#             return
#         await func(message, user_id)
#     return wrapper
