from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserModel:
    """Класс для представления пользователя"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: bool = False
    is_banned: bool = False
    premium: bool = False
    mode: Optional[str] = 'in'
    upper_color: str = '#FFFFFF'
    bottom_color: str = '#FFFFFF'
    upper_stroke_color: str = '#000000'
    bottom_stroke_color: str = '#000000'
    stroke_width: int = 3
    giant_text: bool = False
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
class QueryModel:
    """Класс для представления запроса"""
    user_id: int
    query_text: str
    query_id: Optional[int] = None
    query_date: Optional[datetime] = None
    user: Optional[UserModel] = None


@dataclass
class Pagination:
    page: int
    per_page: int
    total_items: int
    total_pages: int

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page
