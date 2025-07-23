from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Класс для представления пользователя"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: bool = False
    banned: bool = False
    registration_date: Optional[datetime] = None
    query_count: int = 0

    def full_name(self) -> str:
        """Возвращает полное имя пользователя"""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return ' '.join(parts) if parts else str(self.user_id)


@dataclass
class Query:
    """Класс для представления запроса"""
    user_id: int
    query_text: str
    query_id: Optional[int] = None
    query_date: Optional[datetime] = None
    user: Optional[User] = None


@dataclass
class CommandUnit:
    """
    Контейнер для хранения информации о команде бота.
    """
    name: str
    description: str
    is_admin: bool

    def __str__(self):
        command = f"/{self.name}"
        if self.description:
            command += f" — {self.description}"
        if self.is_admin:
            command += ' [ADMIN]'
        return command
