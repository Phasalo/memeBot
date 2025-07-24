from typing import List
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.filters import AdminFilter
from bot.models import CommandUnit


class BaseRouter(Router):
    available_commands: List[CommandUnit] = []
    is_admin: bool = False  # По умолчанию не админский роутер

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_admin:
            self.message.filter(AdminFilter())

    def cmd(self, command: str, description: str = ''):
        def decorator(handler):
            self.available_commands.append(CommandUnit(command, description, self.is_admin))

            @self.message(Command(command))
            async def wrapper(message: Message):
                await handler(message)
            return handler
        return decorator


class AdminRouter(BaseRouter):
    is_admin = True


class UserRouter(BaseRouter):
    is_admin = False
