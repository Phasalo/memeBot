from dataclasses import dataclass
from typing import Tuple, Optional, Any
from aiogram.filters.callback_data import CallbackData

from config.const import SettingsAction


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


class PageCallBack(CallbackData, prefix='page'):
    type_of_event: int
    user_id: int = 0
    page: int = 1


class SetsCallBack(CallbackData, prefix='sets'):
    action: SettingsAction


class ModeCallBack(CallbackData, prefix='mode'):
    mode: str


class ColorCallBack(CallbackData, prefix='color'):
    color: str
    action: SettingsAction


class GenerateCallBack(CallbackData, prefix='gen'):
    query_id: int
