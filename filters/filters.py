from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message
from DB.users_sqlite import Database
from models.models import User


class AdminUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with Database() as db:
            user: Optional[User] = db.get_user(message.from_user.id)
            if user:
                return user.is_admin
            return False
