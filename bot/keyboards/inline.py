from typing import Optional
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.const import SettingsAction, UserColors, MemeModes
from phrases import PHRASES_RU
from bot.bot_utils.models import PageCallBack, SetsCallBack, GenerateCallBack, ModeCallBack, ColorCallBack
from DB.models import Pagination


def page_keyboard(type_of_event: int, pagination: Pagination, user_id: int = 0) -> Optional[IMarkup]:
    if pagination.total_pages <= 1:
        return None

    empty_button = IButton(text=' ', callback_data=PageCallBack(type_of_event=-1).pack())

    past_button = IButton(
        text=PHRASES_RU.button.past_page,
        callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page - 1, user_id=user_id).pack()
    ) if pagination.has_prev else empty_button

    next_button = IButton(
        text=PHRASES_RU.button.next_page,
        callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page + 1, user_id=user_id).pack()
    ) if pagination.has_next else empty_button

    return IMarkup(inline_keyboard=[[
        past_button,
        IButton(text=PHRASES_RU.replace('template.page_counter', current=pagination.page, total=pagination.total_pages),
                callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page,
                                           user_id=user_id).pack()),
        next_button
    ]])


def get_keyboard():
    array_buttons: list[list[IButton]] = [[], [], [], []]
    array_buttons[0].append(IButton(text=PHRASES_RU.button.mode, callback_data=SetsCallBack(action=SettingsAction.USER_MODE).pack()))
    array_buttons[1].append(IButton(text=PHRASES_RU.button.upper_text, callback_data=SetsCallBack(action=SettingsAction.UPPER_TEXT).pack()))
    array_buttons[1].append(IButton(text=PHRASES_RU.button.bottom_text, callback_data=SetsCallBack(action=SettingsAction.BOTTOM_TEXT).pack()))
    array_buttons[2].append(IButton(text=PHRASES_RU.button.upper_stroke, callback_data=SetsCallBack(action=SettingsAction.UPPER_STROKE).pack()))
    array_buttons[2].append(IButton(text=PHRASES_RU.button.bottom_stroke, callback_data=SetsCallBack(action=SettingsAction.BOTTOM_STROKE).pack()))
    array_buttons[3].append(IButton(text=PHRASES_RU.button.text_case, callback_data=SetsCallBack(action=SettingsAction.TEXTCASE).pack()))
    markup = IMarkup(inline_keyboard=array_buttons)
    return markup


def get_photo_inline_keyboard(query_id: int):
    array_buttons: list[list[IButton]] = [
        [IButton(text=PHRASES_RU.button.regenerate, callback_data=GenerateCallBack(query_id=query_id).pack())]]
    markup = IMarkup(inline_keyboard=array_buttons)
    return markup


def get_mode_keyboard(current_mode: str):
    builder = InlineKeyboardBuilder()
    for mode_code, mode_name in MemeModes.all_modes().items():
        emoji = ' ✅' if mode_code == current_mode else ''
        builder.button(text=mode_name + emoji, callback_data=ModeCallBack(mode=mode_code).pack())

    builder.adjust(3)
    builder.row(IButton(text=PHRASES_RU.button.back, callback_data=SetsCallBack(action=SettingsAction.SETTINGS).pack()))
    return builder.as_markup()


def get_color_keyboard(current_color, action: SettingsAction):
    builder = InlineKeyboardBuilder()
    for color_name, color_code in UserColors.get_all_colors().items():
        emoji = '✅ ' if color_code == current_color else ''
        builder.button(text=emoji + color_name,
                       callback_data=ColorCallBack(action=action, color=color_code).pack())
    builder.adjust(3)
    builder.row(IButton(text=PHRASES_RU.button.back, callback_data=SetsCallBack(action=SettingsAction.SETTINGS).pack()))
    return builder.as_markup()


def get_case_keyboard(giant: bool):
    array_buttons: list[list[IButton]] = []
    if not giant:
        txt = PHRASES_RU.button.SET_GIANT_CASE
        action = SettingsAction.SET_GIANT_CASE
    else:
        txt = PHRASES_RU.button.set_small_case
        action = SettingsAction.SET_SMALL_CASE
    array_buttons.append([IButton(text=txt,
                                  callback_data=SetsCallBack(action=action).pack())])
    array_buttons.append([IButton(text=PHRASES_RU.button.back,
                                  callback_data=SetsCallBack(action=SettingsAction.SETTINGS).pack())])
    markup = IMarkup(inline_keyboard=array_buttons)
    return markup
