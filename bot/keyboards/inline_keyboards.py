from typing import Union
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from config import config, bot
from phrases import PHRASES_RU
from utils import format_string
from bot.models import CutMessageCallBack


async def get_users_by_page(user_id: int, page: int = 1, message_id: Union[int, None] = None):
    with UsersTable() as users_db:
        users_info = users_db.get_all_users()

        txt = format_string.format_user_list(users_info)
        pages = format_string.split_text(txt, config.tg_bot.message_max_symbols)

        if message_id:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=pages[page - 1],
                                        reply_markup=page_keyboard(action=1, page=page, max_page=len(pages)))
        else:
            await bot.send_message(chat_id=user_id, text=pages[page - 1], reply_markup=page_keyboard(action=1, page=page, max_page=len(pages)))


async def user_query_by_page(user_id: int, user_id_to_find: Union[int, None], page: int = 1, message_id: Union[int, None] = None):
    with QueriesTable() as queries_db, UsersTable() as users_db:
        queries = queries_db.get_user_queries(user_id_to_find)
        if not user_id_to_find or not queries:
            await bot.send_message(chat_id=user_id, text=PHRASES_RU.error.no_query)
            return

        user = users_db.get_user(user_id_to_find)
        txt = format_string.format_queries_text(
            queries=queries,
            username=user.username if user else None,
            user_id=user_id_to_find,
            header_template=PHRASES_RU.title.user_query,
            line_template=PHRASES_RU.template.user_query
        )

        pages = format_string.split_text(txt, config.tg_bot.message_max_symbols)
        reply_markup = page_keyboard(
            action=2,
            page=page,
            max_page=len(pages),
            user_id=user_id_to_find
        )

        text_to_send = pages[page - 1].replace('\t', '\n')
        if message_id:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=text_to_send,
                reply_markup=reply_markup
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text=text_to_send,
                reply_markup=reply_markup
            )


def page_keyboard(action: int, page: int, max_page: int, user_id: int = 0):
    array_buttons: list[list[InlineKeyboardButton]] = [[]]
    if page > 1:
        array_buttons[0].append(
            InlineKeyboardButton(text='<', callback_data=CutMessageCallBack(action=action, page=page - 1, user_id=user_id).pack())
        )
    array_buttons[0].append(
        InlineKeyboardButton(text=str(page), callback_data=CutMessageCallBack(action=-1).pack())
    )
    if page < max_page:
        array_buttons[0].append(
            InlineKeyboardButton(text='>', callback_data=CutMessageCallBack(action=action, page=page + 1, user_id=user_id).pack())
        )
    if len(array_buttons[0]) == 1:
        return None
    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup
