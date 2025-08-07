from typing import Union
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup
from phrases import PHRASES_RU
from bot.bot_utils.models import PageCallBack
from DB.models import Pagination


def page_keyboard(type_of_event: int, pagination: Pagination, user_id: int = 0) -> Union[IMarkup, None]:
    if pagination.total_pages <= 1:
        return None

    no_action = PageCallBack(type_of_event=-1).pack()

    past_button = IButton(
        text=PHRASES_RU.button.past_page,
        callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page - 1, user_id=user_id).pack()
    ) if pagination.has_prev else IButton(text=' ', callback_data=no_action)

    next_button = IButton(
        text=PHRASES_RU.button.next_page,
        callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page + 1, user_id=user_id).pack()
    ) if pagination.has_next else IButton(text=' ', callback_data=no_action)

    return IMarkup(inline_keyboard=[[
        past_button,
        IButton(text=PHRASES_RU.replase('template.page_counter', current=pagination.page, total=pagination.total_pages),
                callback_data=no_action),
        next_button
    ]])
