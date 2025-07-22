from aiogram import BaseMiddleware, Dispatcher
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, TelegramObject
from DB.db_interface import IDatabase


class UserRegistrationMiddleware(BaseMiddleware):
    def __init__(self, db: IDatabase):
        self.db = db

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

        return await handler(event, data)


def setup_middlewares(dp: Dispatcher, db: IDatabase):
    # Создаем экземпляр middleware и передаем в него базу данных
    user_middleware = UserRegistrationMiddleware(db)

    # Регистрируем middleware для всех сообщений
    dp.message.middleware.register(user_middleware)
