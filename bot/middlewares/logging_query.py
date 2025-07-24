import logging
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable, Union
from aiogram.types import Message, TelegramObject

from DB.tables.queries import QueriesTable
from DB.models import UserModel as UserModel, QueryModel
from bot.routers import BaseRouter


logger = logging.getLogger(__name__)


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
        skip_commands = [f'/{command.name}' for command in BaseRouter.available_commands if command.is_admin]
        if event.text and any(event.text.startswith(cmd) for cmd in skip_commands):
            return await handler(event, data)

        #   <-| ----------------- -<phasalo>- ------------------ |->
        #                                                          |
        #     логгирование или своя логика                         | <=| PHASALO<|||
        #                                                          |
        #   <-| ----------------- -<phasalo>- ------------------ |->

        # например
        user_row: Union[UserModel, None] = data.get('user_row')
        if user_row is None:
            logger.warning(
                'Cannot add queries. The \'user_row\' '
                'key was not found in the middleware data.'
            )
            return await handler(event, data)
        if event.text:
            with QueriesTable() as queries_db:
                queries_db.add_query(QueryModel(user_row.user_id, event.text))
        #

        return await handler(event, data)
