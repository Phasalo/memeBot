from dataclasses import dataclass
from DB.phrases import PHRASES_RU
from aiogram.filters.callback_data import CallbackData


@dataclass
class CommandUnit:
    """Контейнер для хранения информации о команде бота"""
    name: str
    description: str
    is_admin: bool

    def __str__(self):
        command = f"/{self.name}"
        if self.description:
            command += f" — {self.description}"
        if self.is_admin:
            command += PHRASES_RU.icon.admin
        return command


class CutMessageCallBack(CallbackData, prefix="cut"):
    action: int
    user_id: int = 0
    page: int = 1