from typing import Optional
from aiogram.types import Message

from phrases import PHRASES_RU
from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from utils import format_string
from bot import command_arguments, pages
from bot.routers import AdminRouter, BaseRouter

router = AdminRouter()


@router.command('get_users', 'таблица со всем пользователями')      # /get_users
async def _(message: Message):
    await pages.get_users(message.from_user.id)


@router.command('getcmds', 'список всех доступных команд')          # /getcmds
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands)
    await message.answer(PHRASES_RU.title.commands + commands_text)


@router.command('ban', 'заблокировать пользователя по ID')          # /ban
@command_arguments.user_id
async def _(message: Message, user_id):
    if message.from_user.id == int(user_id):
        await message.answer(PHRASES_RU.error.ban_yourself)
        return
    with UsersTable() as user_db:
        if user_db.set_ban_status(user_id, message.from_user.id, True):
            await message.answer(PHRASES_RU.replace('success.banned', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.error.db)


@router.command('unban', 'разблокировать пользователя по ID')       # /unban
@command_arguments.user_id
async def _(message: Message, user_id):
    with UsersTable() as user_db:
        if user_db.set_ban_status(user_id, message.from_user.id, False):
            await message.answer(PHRASES_RU.replace('success.unbanned', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.error.db)


@router.command('promote', 'повышает уровень доступа пользователя') # /promote
@command_arguments.user_id
async def _(message: Message, user_id):
    with UsersTable() as users_db:
        if users_db.set_admin(user_id, message.from_user.id, True):
            await message.answer(PHRASES_RU.replace('success.promoted_by', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.error.db)


@router.command('demote', 'понижает уровень доступа пользователя')  # /demote
@command_arguments.user_id
async def _(message: Message, user_id):
    with UsersTable() as users_db:
        if users_db.set_admin(user_id, message.from_user.id, False):
            await message.answer(PHRASES_RU.replace('success.demoted', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.error.db)


@router.command('query', 'последние N запросов')                    # /query
@command_arguments.digit(default=5)
async def cmd_query(message: Message, amount: int):
    with QueriesTable() as queries_db:
        queries = queries_db.get_last_queries(int(amount))
        if not queries:
            await message.answer(PHRASES_RU.info.no_query)
            return

        txt = format_string.format_queries_text(
            queries=queries,
            header_template=PHRASES_RU.title.all_queries,
            line_template=PHRASES_RU.template.all_queries,
            show_username=True
        )

        if txt:
            await message.answer(txt.replace('\t', '\n'), disable_web_page_preview=True)


@router.command('user_query', 'запросы пользователя по ID')         # /user_query
@command_arguments.user_id
async def cmd_user_query(message: Message, user_id: int):
    await pages.user_query(message.from_user.id, user_id)


@router.command('test', 'отладка и тестирование функций')           # /test
async def _(message: Message):
    await message.answer(PHRASES_RU.template.user_query)
