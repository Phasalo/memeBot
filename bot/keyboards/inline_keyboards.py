from typing import Union
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from config import bot
from phrases import PHRASES_RU
from utils import format_string
from bot.models import CutMessageCallBack
from config.const import USERS_PER_PAGE, QUERIES_PER_PAGE


async def get_users_by_page(user_id: int, page: int = 1, message_id: Union[int, None] = None):
    with UsersTable() as users_db:
        users, pagination = users_db.get_all_users(page, USERS_PER_PAGE)

        txt = format_string.format_user_list(users)
        reply_markup = page_keyboard(action=1,
                                     page=page,
                                     max_page=pagination.total_pages)
        if message_id:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=txt,
                                        reply_markup=reply_markup)
        else:
            await bot.send_message(chat_id=user_id, text=txt, reply_markup=reply_markup)


async def user_query_by_page(user_id: int, user_id_to_find: Union[int, None], page: int = 1, message_id: Union[int, None] = None):
    with QueriesTable() as queries_db, UsersTable() as users_db:
        queries, pagination = queries_db.get_user_queries(user_id_to_find, page, QUERIES_PER_PAGE)
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

        reply_markup = page_keyboard(
            action=2,
            page=page,
            max_page=pagination.total_pages,
            user_id=user_id_to_find
        )

        text_to_send = txt.replace('\t', '\n')
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


def page_keyboard(action: int, page: int, max_page: int, user_id: int = 0) -> InlineKeyboardMarkup | None:
    if max_page == 1:
        return None

    no_action = CutMessageCallBack(action=-1).pack()

    prev_btn = InlineKeyboardButton(
        text='<',
        callback_data=CutMessageCallBack(action=action, page=page - 1, user_id=user_id).pack()
    ) if page > 1 else InlineKeyboardButton(text=' ', callback_data=no_action)

    next_btn = InlineKeyboardButton(
        text='>',
        callback_data=CutMessageCallBack(action=action, page=page + 1, user_id=user_id).pack()
    ) if page < max_page else InlineKeyboardButton(text=' ', callback_data=no_action)

    return InlineKeyboardMarkup(inline_keyboard=[[
        prev_btn,
        InlineKeyboardButton(text=str(page), callback_data=no_action),
        next_btn
    ]])
