from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from DB import users_sqlite
from DB.users_sqlite import Database
from filters import filters
from utils import format_string
from keyboards import main_keyboard

router = Router()
router.message.filter(filters.AdminUser())


@router.message(Command(commands='get_users'))  # /get_users
async def cmd_get_users(message: Message):
    await main_keyboard.get_users_by_page(message.from_user.id)


@router.message(Command(commands='getcoms'))  # /getcoms
async def cmd_getcoms(message: Message):
    pass


@router.message(Command(commands='query'))  # /query
async def cmd_query(message: Message):
    txt = ''
    amount = format_string.find_first_number(message.text)
    if not amount:
        amount = 5
    with Database() as db:
        for query in db.get_last_queries(int(amount)):
            print(query.query_date)
            username = db.get_user(query.user_id).username
            query_time = query.query_date if query.query_date else '❓'
            line = f'<i>@{username if username else query.user_id}</i> — [{query_time}]: <blockquote>{format_string.format_string(query.query_text)}</blockquote>\n\n'
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
async def cmd_user_query(message: Message):
    user_id_to_find = format_string.find_first_number(message.text)
    await main_keyboard.user_query_by_page(message.from_user.id, user_id_to_find)
