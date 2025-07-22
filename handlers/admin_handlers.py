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
    txt = ''
    if not amount:
        amount = 5
    with Database() as db:
        for query in db.get_last_queries(int(amount)):
            username = query.user.username
            query_time = query.query_date.strftime("%d.%m.%Y %H:%M:%S") if query.query_date else '❓'
            line = f'<i>@{username if username else query.user_id}</i> <blockquote>{query_time}</blockquote> <i>{format_string.format_string(query.query_text)}</i>\n\n'
            if len(line) + len(txt) < 4096:
                txt += line
            else:
                try:
                    await message.answer(text=txt)
                except Exception as e:
                    await message.answer(text=f'Произошла ошибка!\n{e}')
                txt = line
        if len(txt) != 0:
            await message.answer(txt, disable_web_page_preview=True)
        else:
            await message.answer('Запросов не было')


@router.message(Command(commands='user_query'))  # /user_query
@decorators.one_argument_command
async def cmd_user_query(message: Message, user_id_to_find: int):
    await ikb.user_query_by_page(message.from_user.id, user_id_to_find)
