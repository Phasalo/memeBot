from aiogram.filters import BaseFilter
from aiogram.types import Message
from DB import usersDB


class AdminUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = usersDB.get_user(message.from_user.id)
        if user:
            return user.admin
        return False
