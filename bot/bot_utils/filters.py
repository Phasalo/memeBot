from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message

from DB.tables.users import UsersTable
from DB.models import UserModel


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with UsersTable() as users_db:
            user: Optional[UserModel] = users_db.get_user(message.from_user.id)
            if user:
                return user.is_admin
            return False


class ExplainBlyat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        required = 'поясни за '
        return message.text[0:len(required)].lower() == required
