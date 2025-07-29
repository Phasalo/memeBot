from dataclasses import dataclass
from typing import Tuple, Optional, Any, Union
from aiogram.filters.callback_data import CallbackData


@dataclass
class CommandUnit:
    """Контейнер для хранения информации о команде бота"""
    name: str  # Основное имя команды
    aliases: Tuple[str, ...] = ()  # Дополнительные варианты вызова
    description: str = ''
    is_admin: bool = False
    placeholders: Optional[Tuple[Any, ...]] = None

    def __str__(self):
        base = f'/{self.name}'
        if self.aliases:
            base += f", {', '.join(f'/{a}' for a in self.aliases)}"
        if self.placeholders:
            base += ' ' + ' '.join(f'{{{p}}}' for p in self.placeholders)
        if self.description:
            base += f' — {self.description}'
        return base


class PageCallBack(CallbackData, prefix='cut'):
    action: int
    user_id: int = 0
    page: int = 1
