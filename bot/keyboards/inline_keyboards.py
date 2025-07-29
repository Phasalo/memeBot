from typing import Union
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup
from phrases import PHRASES_RU
from bot.models import PageCallBack
from DB.models import Pagination


def page_keyboard(action: int, pagination: Pagination, user_id: int = 0) -> Union[IMarkup, None]:
    if pagination.total_pages <= 1:
        return None

    no_action = PageCallBack(action=-1).pack()

    past_button = IButton(
        text=PHRASES_RU.button.past_page,
        callback_data=PageCallBack(action=action, page=pagination.page - 1, user_id=user_id).pack()
    ) if pagination.page > 1 else IButton(text=' ', callback_data=no_action)

    next_button = IButton(
        text=PHRASES_RU.button.next_page,
        callback_data=PageCallBack(action=action, page=pagination.page + 1, user_id=user_id).pack()
    ) if pagination.page < pagination.total_pages else IButton(text=' ', callback_data=no_action)

    return IMarkup(inline_keyboard=[[
        past_button,
        IButton(text=f'{pagination.page}{PHRASES_RU.icon.page_separator}{pagination.total_pages}', callback_data=no_action),
        next_button
    ]])
