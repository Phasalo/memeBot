from aiogram import Router
from bot.filters import AdminFilter


class AdminRouter(Router):
    """Роутер для админ-команд с автоматической проверкой прав"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message.filter(AdminFilter())
        self.is_admin = True


class UserRouter(Router):
    is_admin = False
