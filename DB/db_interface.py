from abc import ABC, abstractmethod
from typing import Optional, List
from config.models import User, Query


class IDatabase(ABC):
    @abstractmethod
    def __init__(self, db_name: str):
        """Инициализация базы данных"""
        pass

    @abstractmethod
    def _create_tables(self):
        """Создание таблиц users и queries"""
        pass

    @abstractmethod
    def add_user(self, user: User) -> User:
        """Добавление нового пользователя"""
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        pass

    @abstractmethod
    def update_user(self, user: User) -> Optional[User]:
        """Обновление информации о пользователе"""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя и всех его запросов"""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Генератор всех пользователей"""
        pass

    @abstractmethod
    def get_last_queries(self, amount: int = 5) -> List[Query]:
        """Возвращает последние N запросов из базы данных"""
        pass

    @abstractmethod
    def get_admins(self) -> List[User]:
        """Генератор администраторов"""
        pass

    @abstractmethod
    def add_query(self, query: Query) -> Query:
        """Добавление нового запроса"""
        pass

    @abstractmethod
    def get_query(self, query_id: int) -> Optional[Query]:
        """Получение запроса по ID"""
        pass

    @abstractmethod
    def get_user_queries(self, user_id: int, limit: Optional[int] = None) -> List[Query]:
        """Генератор запросов пользователя"""
        pass

    @abstractmethod
    def get_all_queries(self, limit: Optional[int] = None) -> List[Query]:
        """Генератор всех запросов"""
        pass

    @abstractmethod
    def set_admin(self, user_id: int, is_admin: bool = True) -> bool:
        """Устанавливает или снимает права администратора у пользователя"""
        pass

    @abstractmethod
    def delete_query(self, query_id: int) -> bool:
        """Удаление запроса по ID"""
        pass

    @abstractmethod
    def delete_user_queries(self, user_id: int) -> int:
        """Удаление всех запросов пользователя"""
        pass

    @abstractmethod
    def close(self):
        """Закрытие соединения с базой данных"""
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
