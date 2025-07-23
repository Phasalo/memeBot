from aiogram import BaseMiddleware, Dispatcher
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, TelegramObject

from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from config.models import User, Query


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        skip_commands = ['/help', '/get_users', '/query', '/user_query', '/about', '/getcoms']

        if event.text and any(event.text.startswith(cmd) for cmd in skip_commands):
            return await handler(event, data)

        #   <-| ----------------- -<phasalo>- ------------------ |->
        #                                                          |
        #     логгирование или своя логика                         | <=| PHASALO<|||
        #                                                          |
        #   <-| ----------------- -<phasalo>- ------------------ |->

        # например
        user = event.from_user
        db_user = User(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        with UsersTable() as users_db:
            users_db.add_user(db_user)
        if event.text:
            with QueriesTable() as queries_db:
                queries_db.add_query(Query(user.id, event.text))
        #

        return await handler(event, data)


def setup_middlewares(dp: Dispatcher):
    # Создаем экземпляр middleware и передаем в него базу данных
    user_middleware = UserRegistrationMiddleware()

    # Регистрируем middleware для всех сообщений
    dp.message.middleware.register(user_middleware)
