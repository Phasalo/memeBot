from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message

from DB.tables.users import UsersTable
from config.models import User


class AdminUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with UsersTable() as users_db:
            user: Optional[User] = users_db.get_user(message.from_user.id)
            if user:
                return user.is_admin
            return False
