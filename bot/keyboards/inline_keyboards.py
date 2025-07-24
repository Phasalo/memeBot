from typing import Union
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup
from phrases import PHRASES_RU
from bot.models import CutMessageCallBack


def page_keyboard(action: int, page: int, max_page: int, user_id: int = 0) -> Union[IMarkup, None]:
    if max_page <= 1:
        return None

    no_action = CutMessageCallBack(action=-1).pack()

    past_button = IButton(
        text=PHRASES_RU.button.past_page,
        callback_data=CutMessageCallBack(action=action, page=page - 1, user_id=user_id).pack()
    ) if page > 1 else IButton(text=' ', callback_data=no_action)

    next_button = IButton(
        text=PHRASES_RU.button.next_page,
        callback_data=CutMessageCallBack(action=action, page=page + 1, user_id=user_id).pack()
    ) if page < max_page else IButton(text=' ', callback_data=no_action)

    return IMarkup(inline_keyboard=[[
        past_button,
        IButton(text=str(page), callback_data=no_action),
        next_button
    ]])
