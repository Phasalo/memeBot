from dataclasses import dataclass
from typing import Tuple, Optional, Any
from aiogram.filters.callback_data import CallbackData


@dataclass
class CommandUnit:
    """Контейнер для хранения информации о команде бота"""
    name: str
    description: str
    is_admin: bool
    placeholders: Optional[Tuple[Any]] = None

    def __str__(self):
        command = f'/{self.name}'
        if self.placeholders:
            for placeholder in self.placeholders:
                command += f' {{{placeholder}}}'
        if self.description:
            command += f' — {self.description}'
        return command


class CutMessageCallBack(CallbackData, prefix='cut'):
    action: int
    user_id: int = 0
    page: int = 1
