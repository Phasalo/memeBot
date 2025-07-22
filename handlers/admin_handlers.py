from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from DB.users_sqlite import Database
from filters import filters
from utils import format_string, decorators
from keyboards import inline_keyboards as ikb

router = Router()
router.message.filter(filters.AdminUser())


@router.message(Command(commands='get_users'))  # /get_users
async def cmd_get_users(message: Message):
    await ikb.get_users_by_page(message.from_user.id)


@router.message(Command(commands='getcoms'))  # /getcoms
async def cmd_getcoms(message: Message):
    pass


@router.message(Command(commands='query'))  # /query
@decorators.one_argument_command
async def cmd_query(message: Message, amount: Optional[int]):
    if not amount:
        amount = 5

    with Database() as db:
        queries = db.get_last_queries(int(amount))
        if not queries:
            await message.answer('Запросов не было')
            return

        txt = format_string.format_queries_text(
            queries=queries,
            header_template='',
            line_template="{username} <blockquote>{time}</blockquote> <i>{query}</i>\n\n",
            show_username=True
        )

        if txt:
            await message.answer(txt.replace('\t', '\n'), disable_web_page_preview=True)


@router.message(Command(commands='user_query'))  # /user_query
@decorators.one_argument_command
async def cmd_user_query(message: Message, user_id_to_find: int):
    await ikb.user_query_by_page(message.from_user.id, user_id_to_find)
